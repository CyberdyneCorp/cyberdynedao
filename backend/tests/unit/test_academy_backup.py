"""Unit tests for the Academy backup/restore transforms — focused on the
guarantee that no course content is lost on a backup -> restore round-trip."""

from __future__ import annotations

from cyberdyne_backend.cli.academy_backup import (
    course_create_body,
    lesson_content_count,
    lesson_create_body,
    quiz_upsert_body,
    serialize_course,
    serialize_quiz,
)

_DETAIL = {
    "slug": "demo-course",
    "title": "Demo Course",
    "description": "A demo.",
    "level": "Intermediate",
    "status": "published",
    "mandatory": False,
    "sortOrder": 3,
    "lessons": [
        {
            "id": "L1",
            "title": "Intro",
            "lessonType": "text",
            "textBody": "# Hello\n\n$$x=1$$",
            "contentUrl": None,
            "duration": "5 min",
            "sortOrder": 0,
        },
        {
            "id": "L2",
            "title": "Watch",
            "lessonType": "video",
            "textBody": None,
            "contentUrl": "https://youtu.be/abc",
            "duration": None,
            "sortOrder": 1,
        },
        {"id": "Q1", "title": "Check", "lessonType": "quiz", "sortOrder": 2},
    ],
}
_QUIZ = {
    "passingScore": 80,
    "questions": [
        {
            "prompt": "2 + 2 = ?",
            "explanation": "basic",
            "options": [
                {"text": "4", "isCorrect": True},
                {"text": "5", "isCorrect": False},
            ],
        }
    ],
}


def test_serialize_quiz_keeps_prompts_and_correct_flags() -> None:
    out = serialize_quiz(_QUIZ)
    assert out["passingScore"] == 80
    assert out["questions"][0]["prompt"] == "2 + 2 = ?"
    # the correct-answer flag must survive (else a restored quiz is useless)
    assert [o["isCorrect"] for o in out["questions"][0]["options"]] == [True, False]


def test_serialize_course_captures_all_lessons_and_fields() -> None:
    course = serialize_course(_DETAIL, {"Q1": _QUIZ})
    assert course["slug"] == "demo-course"
    assert course["level"] == "Intermediate"
    assert course["sortOrder"] == 3
    assert len(course["lessons"]) == 3
    # text body (incl. its LaTeX) preserved verbatim — no content loss
    assert course["lessons"][0]["textBody"] == "# Hello\n\n$$x=1$$"
    # video keeps its contentUrl, not dropped
    assert course["lessons"][1]["contentUrl"] == "https://youtu.be/abc"
    # the quiz tree is attached to the quiz lesson
    assert course["lessons"][2]["quiz"]["questions"][0]["prompt"] == "2 + 2 = ?"


def test_quiz_lesson_without_authored_quiz_is_tolerated() -> None:
    course = serialize_course(_DETAIL, {"Q1": None})
    assert "quiz" not in course["lessons"][2]


def test_restore_bodies_round_trip_the_backup() -> None:
    course = serialize_course(_DETAIL, {"Q1": _QUIZ})
    # course create body keeps slug/title/level
    cb = course_create_body(course)
    assert cb["slug"] == "demo-course" and cb["level"] == "Intermediate"
    # text lesson keeps its body; video lesson keeps its url; nothing invented
    tb = lesson_create_body(course["lessons"][0], 0)
    assert tb["textBody"] == "# Hello\n\n$$x=1$$" and "contentUrl" not in tb
    vb = lesson_create_body(course["lessons"][1], 1)
    assert vb["contentUrl"] == "https://youtu.be/abc" and "textBody" not in vb
    # quiz upsert body preserves the question with its correct option
    qb = quiz_upsert_body(course["lessons"][2]["quiz"])
    assert qb["passingScore"] == 80
    assert qb["questions"][0]["options"][0]["isCorrect"] is True


def test_content_count_matches_source() -> None:
    course = serialize_course(_DETAIL, {"Q1": _QUIZ})
    assert lesson_content_count(course) == (3, 1)
