"""Academy seed content — <Course Title>.

<One paragraph: what the course teaches, what it is built from (e.g. a
YouTube playlist / talk, with link), and how it is structured. Mention
that every content lesson is followed by a checkpoint quiz and the course
closes with a comprehensive final quiz.>
"""
# TEMPLATE — copy to backend/src/cyberdyne_backend/application/courses/seed_<slug>.py
# and delete these TEMPLATE comments. Rules that MUST hold (see SKILL.md):
#   * every quiz question: EXACTLY ONE opt(..., correct=True), >= 2 options
#   * no en dashes or curly quotes anywhere (ruff RUF001)
#   * mermaid follows the constrained grammar (mindmap: root((Title)) +
#     indentation-only ASCII nodes; graph: quoted labels, no <br/>)
#   * lesson titles are permanent reconciliation keys — choose once
#   * final "Check your knowledge" quiz is the LAST lesson

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
    video_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_COURSE = SeedCourse(
    slug="<kebab-case-slug>",  # stable forever
    title="<Course Title>",
    description=(
        "<2-4 sentence catalogue description: what the learner gets, "
        "in plain direct language.>"
    ),
    level="Beginner",  # Beginner | Intermediate | Advanced
    lessons=(
        # ── Welcome ──────────────────────────────────────────────────
        _t(
            "Welcome — how this course works",
            "5 min",
            """# <Course Title>

<Direct framing: why this topic matters, what the course covers, how to
work through it. Short paragraphs. Bold the key concepts.>

<Optional: numbered list of the course parts.>
""",
        ),
        quiz_lesson(
            "Quiz: Welcome — how this course works",
            (
                q(
                    "<Question answerable from the welcome lesson?>",
                    (
                        opt("<plausible wrong option>"),
                        opt("<the correct option>", correct=True),
                        opt("<plausible wrong option>"),
                        opt("<plausible wrong option>"),
                    ),
                    "<1-2 sentence explanation grounding the answer in the lesson.>",
                ),
            ),
        ),
        # ── Content lesson (text): direct explanation + mermaid ──────
        _t(
            "<Lesson title>",
            "8 min",
            """# <Lesson title>

<Easy, direct explanation. Short paragraphs, one idea each. **Bold** the
key concepts. Concrete examples over abstractions.>

```mermaid
graph TD
    A["Concept"] --> B["Leads to"]
    A --> C["Also enables"]
    B --> D["Result"]
```

<Wrap-up sentence: the one thing to remember.>
""",
        ),
        quiz_lesson(
            "Quiz: <Lesson title>",
            (
                q(
                    "<Question 1 on this lesson?>",
                    (
                        opt("<correct>", correct=True),
                        opt("<wrong>"),
                        opt("<wrong>"),
                        opt("<wrong>"),
                    ),
                    "<why>",
                ),
                q(
                    "<Question 2 — vary the correct option's position?>",
                    (
                        opt("<wrong>"),
                        opt("<wrong>"),
                        opt("<correct>", correct=True),
                        opt("<wrong>"),
                    ),
                    "<why>",
                ),
            ),
        ),
        # ── Content lesson (video): body renders BELOW the player ────
        video_lesson(
            "<Video title>",
            "https://www.youtube.com/watch?v=<id>",
            duration="<NN min>",
            body="""# <Video title>

## Summary
<Complete prose summary of the video, 300-450 words, grounded ONLY in the
video content (fetch the transcript with the youtube-playlist skill) — no
external references, no invented facts.>

## Main ideas
- **<Key concept>** — <one sentence from the video>.
- **<Key concept>** — <one sentence from the video>.

## Mindmap
```mermaid
mindmap
  root((Short Title))
    First theme
      Key point one
      Key point two
    Second theme
      Key point three
```
""",
        ),
        quiz_lesson(
            "Quiz: <Video title>",
            (
                q(
                    "<Question answerable from the video?>",
                    (
                        opt("<wrong>"),
                        opt("<correct>", correct=True),
                        opt("<wrong>"),
                        opt("<wrong>"),
                    ),
                    "<why, citing the video>",
                ),
            ),
        ),
        # ── Final comprehensive quiz — MUST be last ──────────────────
        quiz_lesson(
            "Check your knowledge",
            (
                # 8-12 questions spanning the WHOLE course, different
                # angles from the checkpoint quizzes.
                q(
                    "<Cross-course question?>",
                    (
                        opt("<wrong>"),
                        opt("<wrong>"),
                        opt("<wrong>"),
                        opt("<correct>", correct=True),
                    ),
                    "<why>",
                ),
            ),
            duration="10 min",
        ),
    ),
)

# Registered in seed.py: import alphabetically + append to _RAW_COURSES.
COURSE_TEMPLATE_COURSES: tuple[SeedCourse, ...] = (_COURSE,)
