"""Back up and restore Academy course material through the public + admin API.

The Learning System has no single backup endpoint, so this tool composes the
existing endpoints into a faithful, content-safe backup/restore:

    # save every course (lessons + quizzes, with answers) to a JSON file
    python -m cyberdyne_backend.cli.academy_backup backup [--out FILE]

    # recreate courses from a backup file (non-destructive by default)
    python -m cyberdyne_backend.cli.academy_backup restore FILE
    python -m cyberdyne_backend.cli.academy_backup restore FILE --replace --yes

Content-safety guarantees:
  * ``backup`` only issues GETs and **aborts on any fetch error** — it never
    writes a partial (lossy) file.
  * ``restore`` defaults to ``create`` mode: it **skips any course that already
    exists**, so it can never overwrite or delete existing material. Replacing
    an existing course requires the explicit ``--replace --yes`` flags.
  * After a restore it re-reads each course and verifies the lesson count,
    exiting non-zero on any mismatch.

Configuration (no secrets in code) via environment variables:
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_AUTH_BASE  default https://auth.backend.coolify.cyberdynecorp.ai
  ACADEMY_TOKEN      a bearer token (skips login), OR
  ACADEMY_EMAIL / ACADEMY_PASSWORD   to log in
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any

DEFAULT_API_BASE = "https://dao.backend.coolify.cyberdynecorp.ai"
DEFAULT_AUTH_BASE = "https://auth.backend.coolify.cyberdynecorp.ai"
BACKUP_VERSION = 1

# ── Pure transforms (no I/O — unit-tested) ───────────────────────────────────


def serialize_quiz(quiz: dict[str, Any]) -> dict[str, Any]:
    """Reduce an editor-quiz response to the fields needed to recreate it
    (prompts, explanations and which option is correct)."""
    return {
        "passingScore": quiz.get("passingScore", 70),
        "questions": [
            {
                "prompt": q["prompt"],
                "explanation": q.get("explanation", ""),
                "options": [
                    {"text": o["text"], "isCorrect": bool(o["isCorrect"])} for o in q["options"]
                ],
            }
            for q in quiz.get("questions", [])
        ],
    }


def serialize_course(
    detail: dict[str, Any], quiz_by_lesson_id: dict[str, dict[str, Any] | None]
) -> dict[str, Any]:
    """Build a self-contained backup record for one course (all lessons, plus
    quiz trees for quiz lessons)."""
    lessons: list[dict[str, Any]] = []
    for lesson in detail.get("lessons", []):
        record: dict[str, Any] = {
            "title": lesson["title"],
            "lessonType": lesson["lessonType"],
            "textBody": lesson.get("textBody"),
            "contentUrl": lesson.get("contentUrl"),
            "duration": lesson.get("duration"),
            "sortOrder": lesson.get("sortOrder"),
        }
        quiz = quiz_by_lesson_id.get(lesson["id"])
        if quiz is not None:
            record["quiz"] = serialize_quiz(quiz)
        lessons.append(record)
    return {
        "slug": detail["slug"],
        "title": detail["title"],
        "description": detail.get("description", ""),
        "level": detail["level"],
        "status": detail.get("status", "published"),
        "mandatory": detail.get("mandatory", False),
        "sortOrder": detail.get("sortOrder", 0),
        "lessons": lessons,
    }


def course_create_body(course: dict[str, Any]) -> dict[str, Any]:
    return {
        "slug": course["slug"],
        "title": course["title"],
        "description": course.get("description", ""),
        "level": course["level"],
        "mandatory": course.get("mandatory", False),
        "sortOrder": course.get("sortOrder", 0),
    }


def lesson_create_body(lesson: dict[str, Any], index: int) -> dict[str, Any]:
    body: dict[str, Any] = {
        "title": lesson["title"],
        "lessonType": lesson["lessonType"],
        "sortOrder": lesson.get("sortOrder") if lesson.get("sortOrder") is not None else index,
    }
    for key in ("textBody", "contentUrl", "duration"):
        if lesson.get(key) is not None:
            body[key] = lesson[key]
    return body


def quiz_upsert_body(quiz: dict[str, Any]) -> dict[str, Any]:
    return {"passingScore": quiz.get("passingScore", 70), "questions": quiz["questions"]}


def lesson_content_count(course: dict[str, Any]) -> tuple[int, int]:
    """(#lessons, #quiz-questions) — used to verify nothing was dropped."""
    lessons = course.get("lessons", [])
    questions = sum(len(le.get("quiz", {}).get("questions", [])) for le in lessons)
    return len(lessons), questions


# ── HTTP client ──────────────────────────────────────────────────────────────


class ApiClient:
    def __init__(self, api_base: str, auth_base: str, *, insecure: bool) -> None:
        self.api = api_base.rstrip("/")
        self.auth = auth_base.rstrip("/")
        self.token: str | None = None
        self.ctx: ssl.SSLContext | None = None
        if insecure:
            self.ctx = ssl.create_default_context()
            self.ctx.check_hostname = False
            self.ctx.verify_mode = ssl.CERT_NONE

    def _send(self, method: str, url: str, body: dict[str, Any] | None) -> Any:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("content-type", "application/json")
        if self.token:
            req.add_header("authorization", f"Bearer {self.token}")
        with urllib.request.urlopen(req, context=self.ctx) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else None

    def login(self, email: str, password: str) -> None:
        result = self._send(
            "POST", f"{self.auth}/api/v1/auth/login", {"email": email, "password": password}
        )
        self.token = result["access_token"]

    def get(self, path: str) -> Any:
        return self._send("GET", f"{self.api}{path}", None)

    def post(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return self._send("POST", f"{self.api}{path}", body)

    def put(self, path: str, body: dict[str, Any]) -> Any:
        return self._send("PUT", f"{self.api}{path}", body)

    def delete(self, path: str) -> Any:
        return self._send("DELETE", f"{self.api}{path}", None)


# ── Backup ───────────────────────────────────────────────────────────────────


def run_backup(client: ApiClient) -> dict[str, Any]:
    """Fetch every course, lesson and quiz. Aborts (raises) on any error so a
    partial backup is never produced."""
    listing = client.get("/api/v1/courses")
    items = (
        listing if isinstance(listing, list) else listing.get("items", listing.get("courses", []))
    )
    courses: list[dict[str, Any]] = []
    for summary in items:
        slug = summary["slug"]
        detail = client.get(f"/api/v1/courses/{slug}")
        quiz_by_id: dict[str, dict[str, Any] | None] = {}
        for lesson in detail.get("lessons", []):
            if lesson["lessonType"] == "quiz":
                # a quiz lesson without an authored quiz yet returns 404 — that's
                # legitimately empty (not data loss); any other error aborts.
                try:
                    quiz = client.get(f"/api/v1/admin/lessons/{lesson['id']}/quiz")
                except urllib.error.HTTPError as exc:
                    if exc.code != 404:
                        raise
                    quiz = None
                quiz_by_id[lesson["id"]] = (
                    quiz if isinstance(quiz, dict) and "questions" in quiz else None
                )
        courses.append(serialize_course(detail, quiz_by_id))
        print(f"  backed up {slug} ({len(detail.get('lessons', []))} lessons)")
    stamp = datetime.now().astimezone().isoformat()
    return {"version": BACKUP_VERSION, "createdAt": stamp, "courses": courses}


# ── Restore ──────────────────────────────────────────────────────────────────


def _course_exists(client: ApiClient, slug: str) -> bool:
    try:
        client.get(f"/api/v1/courses/{slug}")
        return True
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        raise


def _create_course(client: ApiClient, course: dict[str, Any]) -> None:
    client.post("/api/v1/admin/courses", course_create_body(course))
    for index, lesson in enumerate(course["lessons"]):
        client.post(
            f"/api/v1/admin/courses/{course['slug']}/lessons", lesson_create_body(lesson, index)
        )
    if course.get("status", "published") == "published":
        client.post(f"/api/v1/admin/courses/{course['slug']}/publish")
    # quizzes must be authored AFTER publish (publish re-issues lesson ids)
    detail = client.get(f"/api/v1/courses/{course['slug']}")
    quiz_lessons = [le for le in detail.get("lessons", []) if le["lessonType"] == "quiz"]
    backup_quizzes = [
        le for le in course["lessons"] if le["lessonType"] == "quiz" and le.get("quiz")
    ]
    for live, src in zip(quiz_lessons, backup_quizzes, strict=False):
        client.put(f"/api/v1/admin/lessons/{live['id']}/quiz", quiz_upsert_body(src["quiz"]))


def run_restore(client: ApiClient, data: dict[str, Any], *, replace: bool) -> int:
    """Recreate courses from a backup. Returns the process exit code.

    create mode (default): skip any course that already exists (never clobbers).
    replace mode: delete the existing course first, then recreate it.
    """
    courses = data["courses"]
    created = skipped = replaced = 0
    failures: list[str] = []
    for course in courses:
        slug = course["slug"]
        exists = _course_exists(client, slug)
        if exists and not replace:
            skipped += 1
            print(f"  skip {slug} (already exists)")
            continue
        if exists and replace:
            client.delete(f"/api/v1/admin/courses/{slug}")
            replaced += 1
        _create_course(client, course)
        created += 1 if not exists else 0
        print(f"  {'replaced' if exists else 'created'} {slug}")
        # verify nothing was dropped
        want_lessons = lesson_content_count(course)[0]
        back = client.get(f"/api/v1/courses/{slug}")
        got_lessons = len(back.get("lessons", []))
        if got_lessons != want_lessons:
            failures.append(f"{slug}: expected {want_lessons} lessons, found {got_lessons}")
    print(
        f"\nrestore: {created} created, {replaced} replaced, {skipped} skipped, "
        f"{len(failures)} verification failures"
    )
    for line in failures:
        print(f"  ! {line}")
    return 1 if failures else 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def _client_from_env(insecure_flag: bool) -> ApiClient:
    insecure = insecure_flag or os.environ.get("ACADEMY_INSECURE_TLS") == "1"
    client = ApiClient(
        os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE),
        os.environ.get("ACADEMY_AUTH_BASE", DEFAULT_AUTH_BASE),
        insecure=insecure,
    )
    token = os.environ.get("ACADEMY_TOKEN")
    if token:
        client.token = token
    else:
        email = os.environ.get("ACADEMY_EMAIL")
        password = os.environ.get("ACADEMY_PASSWORD")
        if not email or not password:
            print(
                "error: set ACADEMY_TOKEN, or ACADEMY_EMAIL and ACADEMY_PASSWORD.",
                file=sys.stderr,
            )
            raise SystemExit(2)
        client.login(email, password)
    return client


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="academy_backup", description=__doc__)
    parser.add_argument("--insecure", action="store_true", help="disable TLS verification")
    sub = parser.add_subparsers(dest="command", required=True)

    backup_cmd = sub.add_parser("backup", help="save all courses to a JSON file")
    backup_cmd.add_argument("--out", help="output file (default: academy_backup_<timestamp>.json)")

    restore_cmd = sub.add_parser("restore", help="recreate courses from a backup file")
    restore_cmd.add_argument("file", help="backup JSON file to restore from")
    restore_cmd.add_argument(
        "--replace", action="store_true", help="DELETE and recreate courses that already exist"
    )
    restore_cmd.add_argument(
        "--yes", action="store_true", help="confirm a --replace (destructive) run"
    )

    args = parser.parse_args(argv)

    if args.command == "backup":
        client = _client_from_env(args.insecure)
        print("backing up Academy courses…")
        data = run_backup(client)
        out = args.out or f"academy_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(out, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=1)
        total_q = sum(lesson_content_count(c)[1] for c in data["courses"])
        total_l = sum(lesson_content_count(c)[0] for c in data["courses"])
        print(
            f"\nwrote {out}: {len(data['courses'])} courses, {total_l} lessons, {total_q} quiz questions"
        )
        return 0

    # restore
    with open(args.file, encoding="utf-8") as handle:
        data = json.load(handle)
    if args.replace and not args.yes:
        print(
            "refusing to run --replace without --yes: this DELETES existing courses "
            "before recreating them.",
            file=sys.stderr,
        )
        return 2
    client = _client_from_env(args.insecure)
    print(
        f"restoring from {args.file} ({len(data['courses'])} courses, mode="
        f"{'replace' if args.replace else 'create/skip-existing'})…"
    )
    return run_restore(client, data, replace=args.replace)


if __name__ == "__main__":
    raise SystemExit(main())
