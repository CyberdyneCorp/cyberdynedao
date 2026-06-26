"""Tests for the Academy course seed: it provisions the curated MATLAB and
Python courses, is idempotent, and never clobbers hand-authored lessons."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed import (
    ACADEMY_COURSES,
    SeedCourse,
    SeedLesson,
    seed_courses,
)
from cyberdyne_backend.domain.courses import Course, CourseNotFoundError, new_course, new_lesson


class FakeCourseRepo:
    def __init__(self, seed: list[Course] | None = None) -> None:
        self._by_slug: dict[str, Course] = {c.slug: c for c in (seed or [])}

    async def save(self, course: Course) -> None:
        self._by_slug[course.slug] = course

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> Course:
        course = self._by_slug.get(slug)
        if course is None:
            raise CourseNotFoundError(slug)
        if not include_drafts and not course.is_visible_to_anonymous():
            raise CourseNotFoundError(slug)
        return course


class TestSeedCourses:
    async def test_creates_both_courses_published_with_lessons(self) -> None:
        repo = FakeCourseRepo()
        summary = await seed_courses(repo)

        assert len(summary) == 455
        matlab = await repo.get_by_slug("matlab-basics", include_drafts=True)
        python = await repo.get_by_slug("python-course", include_drafts=True)
        assert matlab.status.value == "published"
        assert python.status.value == "published"
        # MATLAB keeps the titles learners already see, with rich bodies now.
        titles = [lesson.title for lesson in matlab.lessons]
        assert "Welcome to MATLAB" in titles
        assert "Run your first script" in titles
        welcome = next(le for le in matlab.lessons if le.title == "Welcome to MATLAB")
        assert welcome.text_body and "Command Window" in welcome.text_body
        code = next(le for le in matlab.lessons if le.lesson_type.value == "code")
        assert code.text_body and "trace" in code.text_body
        # Python course aligns to the live titles + gains a runnable code lesson.
        py_titles = [le.title for le in python.lessons]
        assert "Welcome to Python" in py_titles
        assert "Run your first Python script" in py_titles
        py_code = next(le for le in python.lessons if le.lesson_type.value == "code")
        assert py_code.text_body and "scores" in py_code.text_body
        # Both courses carry a control-flow lesson covering if/for/while/
        # break/continue, with a Mermaid diagram.
        for course in (matlab, python):
            cf = next(le for le in course.lessons if le.title.startswith("Control flow"))
            body = cf.text_body or ""
            for kw in ("if", "for", "while", "break", "continue", "```mermaid"):
                assert kw in body, f"{course.slug} control-flow lesson missing {kw!r}"

    async def test_is_idempotent(self) -> None:
        repo = FakeCourseRepo()
        await seed_courses(repo)
        matlab_first = await repo.get_by_slug("matlab-basics", include_drafts=True)
        ids_first = [le.id for le in matlab_first.lessons]
        counts_first = len(matlab_first.lessons)

        summary = await seed_courses(repo)  # second run
        matlab_second = await repo.get_by_slug("matlab-basics", include_drafts=True)
        # No new lessons, same ids, same count — a pure no-op content-wise.
        assert [le.id for le in matlab_second.lessons] == ids_first
        assert len(matlab_second.lessons) == counts_first
        assert all("+0 lessons" in line for line in summary)

    async def test_updates_in_place_and_preserves_unmentioned_quiz(self) -> None:
        # Simulate the live course: an old Welcome text lesson + a hand-authored
        # quiz the seed never mentions.
        course = new_course(
            title="MATLAB Basics", description="old", level="Beginner", slug="matlab-basics"
        )
        welcome = new_lesson(
            course_id=course.id,
            title="Welcome to MATLAB",
            lesson_type="text",
            text_body="old body",
            sort_order=0,
        )
        quiz = new_lesson(
            course_id=course.id, title="Check your knowledge", lesson_type="quiz", sort_order=99
        )
        course.lessons.extend([welcome, quiz])
        repo = FakeCourseRepo([course])

        await seed_courses(repo)
        updated = await repo.get_by_slug("matlab-basics", include_drafts=True)

        # The existing Welcome lesson is updated in place (same id, new body).
        new_welcome = next(le for le in updated.lessons if le.title == "Welcome to MATLAB")
        assert new_welcome.id == welcome.id
        assert new_welcome.text_body != "old body"
        # The quiz the seed doesn't mention survives untouched.
        kept_quiz = next((le for le in updated.lessons if le.id == quiz.id), None)
        assert kept_quiz is not None
        assert kept_quiz.lesson_type.value == "quiz"
        # Description refreshed from the curated copy.
        assert updated.description != "old"

    async def test_skips_title_match_of_different_type(self) -> None:
        # A quiz titled like a curated text lesson must NOT be overwritten.
        spec = SeedCourse(
            slug="c1",
            title="C1",
            description="d",
            level="Beginner",
            lessons=(SeedLesson(title="Intro", lesson_type="text", text_body="new"),),
        )
        course = new_course(title="C1", description="d", level="Beginner", slug="c1")
        clash = new_lesson(course_id=course.id, title="Intro", lesson_type="quiz", sort_order=0)
        course.lessons.append(clash)
        repo = FakeCourseRepo([course])

        await seed_courses(repo, courses=(spec,))
        updated = await repo.get_by_slug("c1", include_drafts=True)
        intro_quiz = next(le for le in updated.lessons if le.id == clash.id)
        assert intro_quiz.lesson_type.value == "quiz"  # untouched
        assert intro_quiz.text_body is None

    def test_every_registry_quiz_question_has_exactly_one_correct_option(self) -> None:
        # Regression: a quiz question with zero (or >1) correct options passes the
        # in-memory seed path but fails the domain validator (new_quiz) at real-DB
        # seed time, which aborts seed_academy and silently blocks every later
        # course from seeding. Guard the whole registry here.
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        offenders: list[str] = []
        for slug, quiz in QUIZ_REGISTRY.items():
            groups = [*quiz.per_lesson.items(), ("<final>", quiz.final)]
            for lesson, questions in groups:
                for idx, question in enumerate(questions):
                    n_correct = sum(1 for o in question.options if o.is_correct)
                    if n_correct != 1:
                        offenders.append(f"{slug}/{lesson}/q{idx}: {n_correct} correct")
                    if len(question.options) < 2:
                        offenders.append(f"{slug}/{lesson}/q{idx}: <2 options")
        assert not offenders, "invalid quiz questions:\n" + "\n".join(offenders)

    def test_curated_content_covers_all_courses(self) -> None:
        slugs = {c.slug for c in ACADEMY_COURSES}
        assert slugs == {
            "additive-manufacturing-basics",
            "additive-manufacturing-intermediate",
            "additive-manufacturing-advanced",
            "engineering-dynamics-basics",
            "engineering-dynamics-intermediate",
            "engineering-dynamics-advanced",
            "engineering-graphics-cad-basics",
            "engineering-graphics-cad-intermediate",
            "engineering-graphics-cad-advanced",
            "engineering-statics-basics",
            "engineering-statics-intermediate",
            "engineering-statics-advanced",
            "engineering-thermodynamics-basics",
            "engineering-thermodynamics-intermediate",
            "engineering-thermodynamics-advanced",
            "fluid-mechanics-basics",
            "fluid-mechanics-intermediate",
            "fluid-mechanics-advanced",
            "heat-transfer-basics",
            "heat-transfer-intermediate",
            "heat-transfer-advanced",
            "manufacturing-processes-basics",
            "manufacturing-processes-intermediate",
            "manufacturing-processes-advanced",
            "materials-science-basics",
            "materials-science-intermediate",
            "materials-science-advanced",
            "mechanics-of-materials-basics",
            "mechanics-of-materials-intermediate",
            "mechanics-of-materials-advanced",
            "molecular-modeling-basics",
            "molecular-modeling-intermediate",
            "molecular-modeling-advanced",
            "admet-prediction-basics",
            "admet-prediction-intermediate",
            "admet-prediction-advanced",
            "ai-drug-discovery-basics",
            "ai-drug-discovery-intermediate",
            "ai-drug-discovery-advanced",
            "capstone-ai-drug-design-basics",
            "capstone-ai-drug-design-intermediate",
            "capstone-ai-drug-design-advanced",
            "cheminformatics-basics",
            "cheminformatics-intermediate",
            "cheminformatics-advanced",
            "computer-aided-drug-design-basics",
            "computer-aided-drug-design-intermediate",
            "computer-aided-drug-design-advanced",
            "deep-learning-biology-basics",
            "deep-learning-biology-intermediate",
            "deep-learning-biology-advanced",
            "docking-virtual-screening-basics",
            "docking-virtual-screening-intermediate",
            "docking-virtual-screening-advanced",
            "drug-development-regulatory-basics",
            "drug-development-regulatory-intermediate",
            "drug-development-regulatory-advanced",
            "generative-molecular-design-basics",
            "generative-molecular-design-intermediate",
            "generative-molecular-design-advanced",
            "medicinal-chemistry-basics",
            "medicinal-chemistry-intermediate",
            "medicinal-chemistry-advanced",
            "ml-life-sciences-basics",
            "ml-life-sciences-intermediate",
            "ml-life-sciences-advanced",
            "molecular-dynamics-basics",
            "molecular-dynamics-intermediate",
            "molecular-dynamics-advanced",
            "ngs-analysis-basics",
            "ngs-analysis-intermediate",
            "ngs-analysis-advanced",
            "phylogenetics-basics",
            "phylogenetics-intermediate",
            "phylogenetics-advanced",
            "protein-ligand-binding-basics",
            "protein-ligand-binding-intermediate",
            "protein-ligand-binding-advanced",
            "protein-structure-prediction-basics",
            "protein-structure-prediction-intermediate",
            "protein-structure-prediction-advanced",
            "proteomics-metabolomics-basics",
            "proteomics-metabolomics-intermediate",
            "proteomics-metabolomics-advanced",
            "qsar-modeling-basics",
            "qsar-modeling-intermediate",
            "qsar-modeling-advanced",
            "reproducible-research-basics",
            "reproducible-research-intermediate",
            "reproducible-research-advanced",
            "sequence-analysis-basics",
            "sequence-analysis-intermediate",
            "sequence-analysis-advanced",
            "single-cell-omics-basics",
            "single-cell-omics-intermediate",
            "single-cell-omics-advanced",
            "systems-biology-basics",
            "systems-biology-intermediate",
            "systems-biology-advanced",
            "target-identification-basics",
            "target-identification-intermediate",
            "target-identification-advanced",
            "transcriptomics-basics",
            "transcriptomics-intermediate",
            "transcriptomics-advanced",
            "analytical-chemistry-basics",
            "analytical-chemistry-intermediate",
            "analytical-chemistry-advanced",
            "bio-databases-basics",
            "bio-databases-intermediate",
            "bio-databases-advanced",
            "biochemistry-basics",
            "biochemistry-intermediate",
            "biochemistry-advanced",
            "bioinformatics-basics",
            "bioinformatics-intermediate",
            "bioinformatics-advanced",
            "biostatistics-basics",
            "biostatistics-intermediate",
            "biostatistics-advanced",
            "cell-biology-basics",
            "cell-biology-intermediate",
            "cell-biology-advanced",
            "data-visualization-bio-basics",
            "data-visualization-bio-intermediate",
            "data-visualization-bio-advanced",
            "evolution-ecology-basics",
            "evolution-ecology-intermediate",
            "evolution-ecology-advanced",
            "general-chemistry-basics",
            "general-chemistry-intermediate",
            "general-chemistry-advanced",
            "genetics-basics",
            "genetics-intermediate",
            "genetics-advanced",
            "genomics-basics",
            "genomics-intermediate",
            "genomics-advanced",
            "immunology-basics",
            "immunology-intermediate",
            "immunology-advanced",
            "math-life-sciences-basics",
            "math-life-sciences-intermediate",
            "math-life-sciences-advanced",
            "microbiology-basics",
            "microbiology-intermediate",
            "microbiology-advanced",
            "molecular-biology-basics",
            "molecular-biology-intermediate",
            "molecular-biology-advanced",
            "organic-chemistry-basics",
            "organic-chemistry-intermediate",
            "organic-chemistry-advanced",
            "pharmacology-basics",
            "pharmacology-intermediate",
            "pharmacology-advanced",
            "physical-chemistry-basics",
            "physical-chemistry-intermediate",
            "physical-chemistry-advanced",
            "physics-life-sciences-basics",
            "physics-life-sciences-intermediate",
            "physics-life-sciences-advanced",
            "physiology-basics",
            "physiology-intermediate",
            "physiology-advanced",
            "programming-biology-python-basics",
            "programming-biology-python-intermediate",
            "programming-biology-python-advanced",
            "protein-science-basics",
            "protein-science-intermediate",
            "protein-science-advanced",
            "r-data-analysis-basics",
            "r-data-analysis-intermediate",
            "r-data-analysis-advanced",
            "scientific-computing-basics",
            "scientific-computing-intermediate",
            "scientific-computing-advanced",
            "structural-biology-basics",
            "structural-biology-intermediate",
            "structural-biology-advanced",
            "matlab-basics",
            "python-course",
            "blockchain-basics",
            "blockchain-beyond-basics",
            "c-basics",
            "c-intermediate",
            "cpp-basics",
            "cpp-intermediate",
            "swift-basics",
            "swift-intermediate",
            "go-basics",
            "go-intermediate",
            "rust-basics",
            "rust-intermediate",
            "javascript-basics",
            "javascript-intermediate",
            "typescript-basics",
            "typescript-intermediate",
            "sql-basics",
            "sql-intermediate",
            "mongodb",
            "postgresql",
            "docker-basics",
            "docker-intermediate",
            "docker-advanced",
            "kubernetes-basics",
            "kubernetes-intermediate",
            "kubernetes-advanced",
            "terraform-basics",
            "terraform-intermediate",
            "terraform-advanced",
            "ansible-basics",
            "ansible-intermediate",
            "ansible-advanced",
            "linux-basics",
            "linux-intermediate",
            "linux-advanced",
            "csharp-basics",
            "csharp-intermediate",
            "csharp-advanced",
            "physics-basics",
            "physics-intermediate",
            "physics-quadrotor-dynamics",
            "math-basics",
            "math-intermediate",
            "math-advanced",
            "math-optimization",
            "math-probability",
            "math-fourier",
            "math-information",
            "math-numerical",
            "math-discrete",
            "math-complex",
            "math-matrices",
            "vectorcalc-basics",
            "vectorcalc-intermediate",
            "vectorcalc-advanced",
            "statinf-basics",
            "statinf-intermediate",
            "statinf-advanced",
            "robotics-basics",
            "robotics-intermediate",
            "robotics-advanced",
            "algorithms-basics",
            "algorithms-intermediate",
            "algorithms-advanced",
            "signals-basics",
            "signals-intermediate",
            "signals-advanced",
            "control-basics",
            "control-intermediate",
            "control-advanced",
            "digital-logic-basics",
            "digital-logic-intermediate",
            "digital-logic-advanced",
            "electronics-basics",
            "electronics-intermediate",
            "electronics-advanced",
            "power-electronics-basics",
            "power-electronics-intermediate",
            "power-electronics-advanced",
            "embedded-basics",
            "embedded-intermediate",
            "embedded-advanced",
            "electromagnetics-basics",
            "electromagnetics-intermediate",
            "electromagnetics-advanced",
            "rf-comms-basics",
            "rf-comms-intermediate",
            "rf-comms-advanced",
            "sensors-basics",
            "sensors-intermediate",
            "sensors-advanced",
            "pcb-basics",
            "pcb-intermediate",
            "pcb-advanced",
            "semiconductor-basics",
            "semiconductor-intermediate",
            "semiconductor-advanced",
            "vlsi-basics",
            "vlsi-intermediate",
            "vlsi-advanced",
            "dsp-basics",
            "dsp-intermediate",
            "dsp-advanced",
            "machines-basics",
            "machines-intermediate",
            "machines-advanced",
            "comparch-basics",
            "comparch-intermediate",
            "comparch-advanced",
            "sysverilog-basics",
            "sysverilog-intermediate",
            "sysverilog-advanced",
            "analog-ic-basics",
            "analog-ic-intermediate",
            "analog-ic-advanced",
            "photonics-basics",
            "photonics-intermediate",
            "photonics-advanced",
            "battery-basics",
            "battery-intermediate",
            "battery-advanced",
            "digital-comms-basics",
            "digital-comms-intermediate",
            "digital-comms-advanced",
            "microwave-basics",
            "microwave-intermediate",
            "microwave-advanced",
            "fpga-basics",
            "fpga-intermediate",
            "fpga-advanced",
            "power-systems-basics",
            "power-systems-intermediate",
            "power-systems-advanced",
            "ml-basics",
            "ml-intermediate",
            "ml-advanced",
            "transformers",
            "security-basics",
            "security-intermediate",
            "security-advanced",
            "git-basics",
            "git-intermediate",
            "git-advanced",
            "os-basics",
            "os-intermediate",
            "os-advanced",
            "testing-basics",
            "testing-intermediate",
            "testing-advanced",
            "networking-basics",
            "networking-intermediate",
            "networking-advanced",
            "system-design-basics",
            "system-design-intermediate",
            "system-design-advanced",
            "distributed-basics",
            "distributed-intermediate",
            "distributed-advanced",
            "webdev-basics",
            "webdev-intermediate",
            "webdev-advanced",
            "dataeng-basics",
            "dataeng-intermediate",
            "dataeng-advanced",
            "concurrency-basics",
            "concurrency-intermediate",
            "concurrency-advanced",
            "signal-integrity-basics",
            "signal-integrity-intermediate",
            "signal-integrity-advanced",
            "emc-basics",
            "emc-intermediate",
            "emc-advanced",
            "test-measurement-basics",
            "test-measurement-intermediate",
            "test-measurement-advanced",
            "hw-verification-basics",
            "hw-verification-intermediate",
            "hw-verification-advanced",
            "antennas-basics",
            "antennas-intermediate",
            "antennas-advanced",
            "aerial-basics",
            "aerial-intermediate",
            "aerial-advanced",
            "mobile-robotics-basics",
            "mobile-robotics-intermediate",
            "mobile-robotics-advanced",
            "estimation-basics",
            "estimation-intermediate",
            "estimation-advanced",
            "software-quality-basics",
            "software-quality-intermediate",
            "software-quality-advanced",
            "computational-thinking-basics",
            "computational-thinking-intermediate",
            "computational-thinking-advanced",
            "technical-english-basics",
            "technical-english-intermediate",
            "technical-english-advanced",
            "english-br-basics",
            "english-br-intermediate",
            "english-br-advanced",
            "django-basics",
            "django-intermediate",
            "django-advanced",
            "rails-basics",
            "rails-intermediate",
            "rails-advanced",
            "software-architecture-basics",
            "software-architecture-intermediate",
            "software-architecture-advanced",
            "algorithms-logic-computing",
            "prob-stats-python-basics",
            "prob-stats-python-intermediate",
            "prob-stats-python-advanced",
            "circuit-analysis-basics",
            "circuit-analysis-intermediate",
            "circuit-analysis-advanced",
            "filter-design-basics",
            "filter-design-intermediate",
            "filter-design-advanced",
            "data-converters-basics",
            "data-converters-intermediate",
            "data-converters-advanced",
            "rfic-basics",
            "rfic-intermediate",
            "rfic-advanced",
            "stochastic-processes-basics",
            "stochastic-processes-intermediate",
            "stochastic-processes-advanced",
            "coding-theory-basics",
            "coding-theory-intermediate",
            "coding-theory-advanced",
            "analog-comms-basics",
            "analog-comms-intermediate",
            "analog-comms-advanced",
            "wireless-comms-basics",
            "wireless-comms-intermediate",
            "wireless-comms-advanced",
            "fiber-optics-basics",
            "fiber-optics-intermediate",
            "fiber-optics-advanced",
            "radar-basics",
            "radar-intermediate",
            "radar-advanced",
            "image-processing-basics",
            "image-processing-intermediate",
            "image-processing-advanced",
            "audio-processing-basics",
            "audio-processing-intermediate",
            "audio-processing-advanced",
            "adaptive-dsp-basics",
            "adaptive-dsp-intermediate",
            "adaptive-dsp-advanced",
            "advanced-control-basics",
            "advanced-control-intermediate",
            "advanced-control-advanced",
            "electric-drives-basics",
            "electric-drives-intermediate",
            "electric-drives-advanced",
            "high-voltage-basics",
            "high-voltage-intermediate",
            "high-voltage-advanced",
            "power-protection-basics",
            "power-protection-intermediate",
            "power-protection-advanced",
            "smart-grid-basics",
            "smart-grid-intermediate",
            "smart-grid-advanced",
            "renewable-ev-basics",
            "renewable-ev-intermediate",
            "renewable-ev-advanced",
        }
        for course in ACADEMY_COURSES:
            assert course.lessons  # non-empty
            for lesson in course.lessons:
                if lesson.lesson_type in {"text", "code"}:
                    assert lesson.text_body, f"{course.slug}/{lesson.title} missing body"

    def test_language_courses_are_basics_plus_intermediate_with_quiz(self) -> None:
        from cyberdyne_backend.application.courses.seed_languages import LANGUAGE_COURSES

        # Seven languages, each with a basics + intermediate course.
        assert len(LANGUAGE_COURSES) == 14
        for course in LANGUAGE_COURSES:
            # Language lessons are text (no interpreter for these) + a quiz.
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "quiz"}, f"{course.slug} has a non-text lesson"
            assert any(le.lesson_type == "quiz" for le in course.lessons)
            assert course.level in {"Beginner", "Intermediate"}

    def test_database_courses_present_with_text_and_quiz(self) -> None:
        from cyberdyne_backend.application.courses.seed_databases import DATABASE_COURSES

        slugs = {c.slug for c in DATABASE_COURSES}
        assert slugs == {"sql-basics", "sql-intermediate", "mongodb", "postgresql"}
        for course in DATABASE_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "quiz"}
            assert any(le.lesson_type == "quiz" for le in course.lessons)

    def test_devops_courses_cover_docker_and_k8s_three_levels(self) -> None:
        from cyberdyne_backend.application.courses.seed_devops import DEVOPS_COURSES

        slugs = {c.slug for c in DEVOPS_COURSES}
        assert slugs == {
            "docker-basics",
            "docker-intermediate",
            "docker-advanced",
            "kubernetes-basics",
            "kubernetes-intermediate",
            "kubernetes-advanced",
        }
        levels = {c.slug: c.level for c in DEVOPS_COURSES}
        assert levels["docker-advanced"] == "Advanced"
        assert levels["kubernetes-advanced"] == "Advanced"

    def test_iac_courses_cover_terraform_and_ansible_three_levels(self) -> None:
        from cyberdyne_backend.application.courses.seed_iac import IAC_COURSES

        slugs = {c.slug for c in IAC_COURSES}
        assert slugs == {
            "terraform-basics",
            "terraform-intermediate",
            "terraform-advanced",
            "ansible-basics",
            "ansible-intermediate",
            "ansible-advanced",
        }
        levels = {c.slug: c.level for c in IAC_COURSES}
        assert levels["terraform-advanced"] == "Advanced"
        assert levels["ansible-advanced"] == "Advanced"

    def test_linux_track_runs_basics_to_device_drivers(self) -> None:
        from cyberdyne_backend.application.courses.seed_linux import LINUX_COURSES

        slugs = {c.slug for c in LINUX_COURSES}
        assert slugs == {"linux-basics", "linux-intermediate", "linux-advanced"}
        levels = {c.slug: c.level for c in LINUX_COURSES}
        assert levels["linux-basics"] == "Beginner"
        assert levels["linux-intermediate"] == "Intermediate"
        assert levels["linux-advanced"] == "Advanced"
        for course in LINUX_COURSES:
            # Linux lessons are text (no Linux runtime in the Academy) + a quiz.
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "quiz"}, f"{course.slug} has a non-text lesson"
            assert any(le.lesson_type == "quiz" for le in course.lessons)

        # Basics covers day-to-day use; advanced reaches real device drivers.
        basics = next(c for c in LINUX_COURSES if c.slug == "linux-basics")
        basics_titles = " | ".join(le.title for le in basics.lessons)
        for needle in ("shell", "permissions", "Processes", "Pipes", "SSH"):
            assert needle in basics_titles, f"basics missing {needle!r}"

        inter = next(c for c in LINUX_COURSES if c.slug == "linux-intermediate")
        inter_body = "\n".join(le.text_body or "" for le in inter.lessons)
        for kw in ("module_init", "copy_to_user", "file_operations", "kmalloc"):
            assert kw in inter_body, f"intermediate missing {kw!r}"

        adv = next(c for c in LINUX_COURSES if c.slug == "linux-advanced")
        adv_titles = " | ".join(le.title for le in adv.lessons)
        for needle in ("device model", "Platform drivers", "Block", "Network", "PCI & USB"):
            assert needle in adv_titles, f"advanced missing {needle!r}"
        adv_body = "\n".join(le.text_body or "" for le in adv.lessons)
        for kw in ("probe", "of_match_table", "dma_alloc_coherent", "net_device", "pci_driver"):
            assert kw in adv_body, f"advanced missing {kw!r}"

    async def test_seed_interleaves_and_authors_quizzes(self) -> None:
        from cyberdyne_backend.application.courses.seed_linux import LINUX_COURSES

        recorded: list[object] = []

        class _FakeQuizAuthor:
            async def execute(self, lesson_id: object, cmd: object) -> None:
                recorded.append((lesson_id, cmd))

        repo = FakeCourseRepo()
        basics = next(c for c in LINUX_COURSES if c.slug == "linux-basics")
        await seed_courses(repo, courses=(basics,), quiz_author=_FakeQuizAuthor())  # type: ignore[arg-type]
        saved = await repo.get_by_slug("linux-basics", include_drafts=True)

        types = [le.lesson_type.value for le in saved.lessons]
        # Every content (text) lesson is immediately followed by a quiz.
        for i, kind in enumerate(types[:-1]):
            if kind == "text":
                assert types[i + 1] == "quiz", f"no quiz after lesson index {i}"
        quiz_count = sum(1 for k in types if k == "quiz")
        assert quiz_count >= len([k for k in types if k == "text"])
        # One UpsertQuiz call per curated quiz lesson, each with exactly one
        # correct option per question.
        assert len(recorded) == quiz_count
        for _lesson_id, cmd in recorded:  # type: ignore[misc]
            assert cmd.questions  # type: ignore[attr-defined]
            for question in cmd.questions:  # type: ignore[attr-defined]
                assert sum(1 for o in question.options if o.is_correct) == 1

    def test_signals_track_has_three_levels_plots_and_dual_language(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_signals import SIGNALS_COURSES

        slugs = {c.slug for c in SIGNALS_COURSES}
        assert slugs == {"signals-basics", "signals-intermediate", "signals-advanced"}
        levels = {c.slug: c.level for c in SIGNALS_COURSES}
        assert levels["signals-basics"] == "Beginner"
        assert levels["signals-intermediate"] == "Intermediate"
        assert levels["signals-advanced"] == "Advanced"

        plot_blocks = 0
        for course in SIGNALS_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "code"}  # quizzes come from the registry
            assert any(le.lesson_type == "code" for le in course.lessons)  # a runnable lab
            body = "\n".join(le.text_body or "" for le in course.lessons)
            # Dual MATLAB + Python focus and interactive plots in every course.
            assert "```matlab" in body and "```python" in body
            for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                json.loads(raw)  # every plot block is valid JSON
                plot_blocks += 1
            # Every course is covered by the quiz registry (per-lesson + final).
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson).issubset(content_titles)
            assert len(spec.per_lesson) == len(content_titles)
        assert plot_blocks >= 10

    def test_control_track_covers_classic_modern_pid_mpc_adrc(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_control import CONTROL_COURSES
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        slugs = {c.slug for c in CONTROL_COURSES}
        assert slugs == {"control-basics", "control-intermediate", "control-advanced"}
        levels = {c.slug: c.level for c in CONTROL_COURSES}
        assert levels["control-basics"] == "Beginner"
        assert levels["control-intermediate"] == "Intermediate"
        assert levels["control-advanced"] == "Advanced"

        all_body = ""
        plot_blocks = 0
        for course in CONTROL_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "code"}  # quizzes come from the registry
            assert any(le.lesson_type == "code" for le in course.lessons)  # a runnable lab
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            assert "```matlab" in body and "```python" in body  # dual language
            for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                json.loads(raw)  # valid interactive plot JSON
                plot_blocks += 1
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

        # The requested topic coverage: classic + modern, PID/MPC/ADRC, history.
        for needle in (
            "PID",
            "root locus",
            "Bode",
            "state-space",
            "LQR",
            "Kalman",
            "Model Predictive Control",
            "Active Disturbance Rejection",
            "Extended State Observer",
            "Watt",  # the history
        ):
            assert needle in all_body, f"control track missing {needle!r}"
        assert plot_blocks >= 6

    def test_software_quality_track_covers_models_and_maturity(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_software_quality import (
            SOFTWARE_QUALITY_COURSES,
        )

        slugs = {c.slug for c in SOFTWARE_QUALITY_COURSES}
        assert slugs == {
            "software-quality-basics",
            "software-quality-intermediate",
            "software-quality-advanced",
        }
        assert {c.level for c in SOFTWARE_QUALITY_COURSES} == {
            "Beginner",
            "Intermediate",
            "Advanced",
        }

        all_body = ""
        plot_blocks = 0
        mermaid_blocks = 0
        for course in SOFTWARE_QUALITY_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "code"}  # quizzes come from the registry
            assert any(le.lesson_type == "code" for le in course.lessons)  # a runnable lab
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            mermaid_blocks += body.count("```mermaid")
            for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                json.loads(raw)  # valid interactive plot JSON
                plot_blocks += 1
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

        # Coverage of the source-material concepts (case-insensitive).
        haystack = all_body.lower()
        for needle in (
            "quality assurance",
            "maintenance",
            "ISO/IEC 25010",
            "CMMI",
            "MPS.BR",
            "PDCA",
        ):
            assert needle.lower() in haystack, f"software-quality track missing {needle!r}"
        assert mermaid_blocks >= 6  # rich diagrams across the track
        assert plot_blocks >= 3

    def test_computational_thinking_track_covers_logic_and_python(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_computational_thinking import (
            COMPUTATIONAL_THINKING_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        slugs = {c.slug for c in COMPUTATIONAL_THINKING_COURSES}
        assert slugs == {
            "computational-thinking-basics",
            "computational-thinking-intermediate",
            "computational-thinking-advanced",
        }
        assert {c.level for c in COMPUTATIONAL_THINKING_COURSES} == {
            "Beginner",
            "Intermediate",
            "Advanced",
        }

        all_body = ""
        plot_blocks = 0
        mermaid_blocks = 0
        for course in COMPUTATIONAL_THINKING_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "code"}  # quizzes come from the registry
            # A programming track: at least three runnable labs per course.
            assert sum(1 for le in course.lessons if le.lesson_type == "code") >= 3
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            mermaid_blocks += body.count("```mermaid")
            for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                json.loads(raw)  # valid interactive plot JSON
                plot_blocks += 1
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

        haystack = all_body.lower()
        for needle in (
            "decomposition",
            "algorithm",
            "if",
            "for",
            "while",
            "flowchart",
        ):
            assert needle in haystack, f"computational-thinking track missing {needle!r}"
        assert mermaid_blocks >= 6
        assert plot_blocks >= 2

    def test_technical_english_track_is_a_language_course_with_keep_spans(self) -> None:
        import re

        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_technical_english import (
            TECHNICAL_ENGLISH_COURSES,
        )

        slugs = {c.slug for c in TECHNICAL_ENGLISH_COURSES}
        assert slugs == {
            "technical-english-basics",
            "technical-english-intermediate",
            "technical-english-advanced",
        }
        assert {c.level for c in TECHNICAL_ENGLISH_COURSES} == {
            "Beginner",
            "Intermediate",
            "Advanced",
        }

        for course in TECHNICAL_ENGLISH_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds == {"text"}  # a language course — no code labs
            body = "\n".join(le.text_body or "" for le in course.lessons)
            # The taught-English is wrapped in [[keep]]…[[/keep]] do-not-translate
            # spans, and they're balanced.
            opens = body.count("[[keep]]")
            closes = body.count("[[/keep]]")
            assert opens > 0 and opens == closes, f"{course.slug}: unbalanced keep spans"
            assert not re.search(r"\[\[keep\]\][^[]*\[\[keep\]\]", body)  # no nesting
            # Every content lesson has a checkpoint quiz; a final exists.
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

    def test_english_brazil_track_is_a_brazilian_language_course(self) -> None:
        import re

        from cyberdyne_backend.application.courses.seed_english_brazil import (
            ENGLISH_BRAZIL_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        slugs = {c.slug for c in ENGLISH_BRAZIL_COURSES}
        assert slugs == {
            "english-br-basics",
            "english-br-intermediate",
            "english-br-advanced",
        }
        assert {c.level for c in ENGLISH_BRAZIL_COURSES} == {
            "Beginner",
            "Intermediate",
            "Advanced",
        }

        for course in ENGLISH_BRAZIL_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds == {"text"}  # a language course — no code labs
            body = "\n".join(le.text_body or "" for le in course.lessons)
            # The taught-English (and named Portuguese words) are wrapped in
            # [[keep]]…[[/keep]] do-not-translate spans, balanced and not nested.
            opens = body.count("[[keep]]")
            closes = body.count("[[/keep]]")
            assert opens > 0 and opens == closes, f"{course.slug}: unbalanced keep spans"
            assert not re.search(r"\[\[keep\]\][^[]*\[\[keep\]\]", body)  # no nesting
            # Mermaid diagrams are present in every level (explicitly requested).
            assert "```mermaid" in body, f"{course.slug}: no mermaid diagram"
            # Every content lesson has a checkpoint quiz; a final exists.
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {le.title for le in course.lessons if le.lesson_type == "text"}
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

        # It is Brazil-specific: the false-cognate vocabulary names Portuguese
        # words (e.g. the classic push/puxar/empurrar trap).
        basics_body = "\n".join(
            le.text_body or ""
            for c in ENGLISH_BRAZIL_COURSES
            if c.slug == "english-br-basics"
            for le in c.lessons
        )
        for needle in ("empurrar", "puxar", "biblioteca", "falso"):
            assert needle in basics_body, f"english-br-basics missing pt marker {needle!r}"

    def test_prob_stats_python_track_uses_numpy_scipy_pandas_with_plots(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_prob_stats_python import (
            PROB_STATS_PYTHON_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        slugs = {c.slug for c in PROB_STATS_PYTHON_COURSES}
        assert slugs == {
            "prob-stats-python-basics",
            "prob-stats-python-intermediate",
            "prob-stats-python-advanced",
        }
        assert {c.level for c in PROB_STATS_PYTHON_COURSES} == {
            "Beginner",
            "Intermediate",
            "Advanced",
        }
        all_body = ""
        for course in PROB_STATS_PYTHON_COURSES:
            assert {le.lesson_type for le in course.lessons} == {"text"}
            assert len(course.lessons) == 6
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            assert "```python" in body, f"{course.slug}: no python code"
            # Interactive graphs (the ```plot engine) and concept diagrams.
            plots = re.findall(r"```plot\n(.*?)\n```", body, re.S)
            assert len(plots) >= 3, f"{course.slug}: too few interactive plots"
            for raw in plots:
                json.loads(raw)  # valid plot JSON
            assert "```mermaid" in body, f"{course.slug}: no mermaid diagram"
            assert "[[keep]]" not in body  # translatable technical course
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {le.title for le in course.lessons if le.lesson_type == "text"}
            assert set(spec.per_lesson) == content_titles
        # The Python data stack is actually taught.
        for needle in ("numpy", "scipy", "pandas"):
            assert needle in all_body, f"prob-stats-python missing {needle!r}"

    def test_computing_foundations_is_a_single_undecidability_course(self) -> None:
        from cyberdyne_backend.application.courses.seed_computing_foundations import (
            COMPUTING_FOUNDATIONS_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        # A SINGLE course (no Basics/Intermediate/Advanced split).
        assert len(COMPUTING_FOUNDATIONS_COURSES) == 1
        course = COMPUTING_FOUNDATIONS_COURSES[0]
        assert course.slug == "algorithms-logic-computing"
        assert course.level == "Beginner"
        assert {le.lesson_type for le in course.lessons} == {"text"}
        body = "\n".join(le.text_body or "" for le in course.lessons)
        assert body.count("```mermaid") >= 5  # diagram-driven interactivity
        assert "[[keep]]" not in body  # translatable technical course
        # The commissioned themes are covered.
        for needle in (
            "Entscheidungsproblem",
            "Halting Problem",
            "Turing machine",
            "Rice's theorem",
            "Busy Beaver",
            "undecidable",
        ):
            assert needle in body, f"computing-foundations missing {needle!r}"
        # A checkpoint quiz for every lesson + a final.
        assert course.slug in QUIZ_REGISTRY
        spec = QUIZ_REGISTRY[course.slug]
        assert spec.final
        content_titles = {le.title for le in course.lessons if le.lesson_type == "text"}
        assert set(spec.per_lesson) == content_titles

    def test_software_architecture_track_is_uml_and_diagram_driven(self) -> None:
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_software_architecture import (
            SOFTWARE_ARCHITECTURE_COURSES,
        )

        slugs = {c.slug for c in SOFTWARE_ARCHITECTURE_COURSES}
        assert slugs == {
            "software-architecture-basics",
            "software-architecture-intermediate",
            "software-architecture-advanced",
        }
        assert {c.level for c in SOFTWARE_ARCHITECTURE_COURSES} == {
            "Beginner",
            "Intermediate",
            "Advanced",
        }
        all_body = ""
        for course in SOFTWARE_ARCHITECTURE_COURSES:
            assert {le.lesson_type for le in course.lessons} == {"text"}
            assert len(course.lessons) == 6
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            # Diagram-driven subject: many Mermaid diagrams, including UML types.
            assert body.count("```mermaid") >= 5, f"{course.slug}: too few diagrams"
            assert "[[keep]]" not in body  # translatable technical course
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {le.title for le in course.lessons if le.lesson_type == "text"}
            assert set(spec.per_lesson) == content_titles
        # The topics the course was commissioned to cover are present.
        for needle in ("classDiagram", "sequenceDiagram", "MVC", "MVVM", "Hexagonal", "SOLID"):
            assert needle in all_body, f"software-architecture track missing {needle!r}"

    def test_web_framework_tracks_have_code_mermaid_and_quizzes(self) -> None:
        from cyberdyne_backend.application.courses.seed_django import DJANGO_COURSES
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_rails import RAILS_COURSES

        tracks = {
            "django": (DJANGO_COURSES, "```python"),
            "rails": (RAILS_COURSES, "```ruby"),
        }
        for name, (courses, code_fence) in tracks.items():
            slugs = {c.slug for c in courses}
            assert slugs == {f"{name}-basics", f"{name}-intermediate", f"{name}-advanced"}
            assert {c.level for c in courses} == {"Beginner", "Intermediate", "Advanced"}
            for course in courses:
                # Standard technical course: text lessons with illustrative code.
                assert {le.lesson_type for le in course.lessons} == {"text"}
                assert len(course.lessons) == 6
                body = "\n".join(le.text_body or "" for le in course.lessons)
                assert code_fence in body, f"{course.slug}: no {code_fence} block"
                assert "```mermaid" in body, f"{course.slug}: no mermaid diagram"
                # Not a language course — must NOT carry do-not-translate markers.
                assert "[[keep]]" not in body, f"{course.slug}: unexpected keep span"
                # A checkpoint quiz for every lesson + a final.
                assert course.slug in QUIZ_REGISTRY
                spec = QUIZ_REGISTRY[course.slug]
                assert spec.final
                content_titles = {le.title for le in course.lessons if le.lesson_type == "text"}
                assert set(spec.per_lesson) == content_titles

    def test_digital_logic_track_focuses_on_sv_vhdl_cocotb(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_digital_logic import (
            DIGITAL_LOGIC_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        slugs = {c.slug for c in DIGITAL_LOGIC_COURSES}
        assert slugs == {
            "digital-logic-basics",
            "digital-logic-intermediate",
            "digital-logic-advanced",
        }
        levels = {c.slug: c.level for c in DIGITAL_LOGIC_COURSES}
        assert levels["digital-logic-basics"] == "Beginner"
        assert levels["digital-logic-intermediate"] == "Intermediate"
        assert levels["digital-logic-advanced"] == "Advanced"

        all_body = ""
        plot_blocks = 0
        for course in DIGITAL_LOGIC_COURSES:
            # No real simulation: every lesson is text (no runnable code lessons).
            assert {le.lesson_type for le in course.lessons} == {"text"}
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            # Focus: SystemVerilog + VHDL + CocoTB shown in every course.
            assert "```systemverilog" in body
            assert "```vhdl" in body
            assert "cocotb" in body.lower()
            for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                json.loads(raw)  # valid interactive/animated plot JSON
                plot_blocks += 1
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {le.title for le in course.lessons if le.lesson_type == "text"}
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

        for needle in (
            "SystemVerilog",
            "VHDL",
            "CocoTB",
            "always_ff",
            "std_logic",
            "finite state machine",
            "metastab",
            "@cocotb.test",
        ):
            assert needle.lower() in all_body.lower(), f"digital logic missing {needle!r}"
        assert plot_blocks >= 4  # animated/interactive waveforms

    def test_electronics_track_is_complete_dc_ac_analog(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_electronics import ELECTRONICS_COURSES
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        slugs = {c.slug for c in ELECTRONICS_COURSES}
        assert slugs == {
            "electronics-basics",
            "electronics-intermediate",
            "electronics-advanced",
        }
        levels = {c.slug: c.level for c in ELECTRONICS_COURSES}
        assert levels["electronics-basics"] == "Beginner"
        assert levels["electronics-intermediate"] == "Intermediate"
        assert levels["electronics-advanced"] == "Advanced"

        all_body = ""
        plot_blocks = 0
        for course in ELECTRONICS_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "code"}
            assert any(le.lesson_type == "code" for le in course.lessons)  # runnable lab
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            assert "```matlab" in body and "```python" in body  # dual language
            for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                json.loads(raw)  # valid interactive plot JSON
                plot_blocks += 1
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

        # Complete coverage: DC -> AC/reactive -> semiconductors/analog.
        for needle in (
            "Ohm",
            "Kirchhoff",
            "Thevenin",
            "capacitor",
            "impedance",
            "resonance",
            "filter",
            "diode",
            "transistor",
            "JFET",
            "MOSFET",
            "Q-point",
            "load line",
            "operational amplifier",
            "oscillator",
            "Barkhausen",
            "buck",
        ):
            assert needle.lower() in all_body.lower(), f"electronics missing {needle!r}"
        assert plot_blocks >= 8  # lots of interactive plots

    def test_power_electronics_track_covers_converters_inverters_drives(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_power_electronics import (
            POWER_ELECTRONICS_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        slugs = {c.slug for c in POWER_ELECTRONICS_COURSES}
        assert slugs == {
            "power-electronics-basics",
            "power-electronics-intermediate",
            "power-electronics-advanced",
        }
        levels = {c.slug: c.level for c in POWER_ELECTRONICS_COURSES}
        assert levels["power-electronics-basics"] == "Beginner"
        assert levels["power-electronics-intermediate"] == "Intermediate"
        assert levels["power-electronics-advanced"] == "Advanced"

        all_body = ""
        plot_blocks = 0
        for course in POWER_ELECTRONICS_COURSES:
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "code"}
            assert any(le.lesson_type == "code" for le in course.lessons)  # runnable lab
            body = "\n".join(le.text_body or "" for le in course.lessons)
            all_body += body
            assert "```matlab" in body and "```python" in body  # dual language
            for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                json.loads(raw)
                plot_blocks += 1
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson) == content_titles  # a quiz for every lesson

        for needle in (
            "PWM",
            "buck",
            "boost",
            "thyristor",
            "synchronous rectification",
            "flyback",
            "resonant",
            "inverter",
            "field-oriented",
            "SiC",
            "GaN",
        ):
            assert needle.lower() in all_body.lower(), f"power electronics missing {needle!r}"
        assert plot_blocks >= 8

    def test_tier1_ee_tracks_complete(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_electromagnetics import (
            ELECTROMAGNETICS_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_embedded import EMBEDDED_COURSES
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_rf_comms import RF_COMMS_COURSES
        from cyberdyne_backend.application.courses.seed_sensors import SENSORS_COURSES

        tracks = {
            "embedded": (EMBEDDED_COURSES, ("```c", "```python")),
            "electromagnetics": (ELECTROMAGNETICS_COURSES, ("```matlab", "```python")),
            "rf-comms": (RF_COMMS_COURSES, ("```matlab", "```python")),
            "sensors": (SENSORS_COURSES, ("```matlab", "```python")),
        }
        total_plots = 0
        for prefix, (courses, lang_fences) in tracks.items():
            assert len(courses) == 3
            assert {c.level for c in courses} == {"Beginner", "Intermediate", "Advanced"}
            for course in courses:
                assert course.slug.startswith(prefix)
                kinds = {le.lesson_type for le in course.lessons}
                assert kinds <= {"text", "code"}
                assert any(le.lesson_type == "code" for le in course.lessons)  # runnable lab
                body = "\n".join(le.text_body or "" for le in course.lessons)
                for fence in lang_fences:  # dual language
                    assert fence in body, f"{course.slug} missing {fence}"
                course_plots = 0
                for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                    json.loads(raw)  # valid interactive plot JSON
                    course_plots += 1
                assert course_plots >= 3, f"{course.slug} has <3 plots"
                total_plots += course_plots
                # every content lesson has a checkpoint quiz from the registry
                assert course.slug in QUIZ_REGISTRY
                spec = QUIZ_REGISTRY[course.slug]
                assert spec.final
                content_titles = {
                    le.title for le in course.lessons if le.lesson_type in {"text", "code"}
                }
                assert set(spec.per_lesson) == content_titles
        assert total_plots >= 60  # richly interactive across the 4 tracks

    def test_tier2_ee_tracks_complete(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_dsp import DSP_COURSES
        from cyberdyne_backend.application.courses.seed_machines import MACHINES_COURSES
        from cyberdyne_backend.application.courses.seed_pcb import PCB_COURSES
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_semiconductors import (
            SEMICONDUCTOR_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_vlsi import VLSI_COURSES

        tracks = {
            "pcb": (PCB_COURSES, ("```matlab", "```python")),
            "semiconductor": (SEMICONDUCTOR_COURSES, ("```matlab", "```python")),
            "vlsi": (VLSI_COURSES, ("```systemverilog", "```python")),
            "dsp": (DSP_COURSES, ("```matlab", "```python")),
            "machines": (MACHINES_COURSES, ("```matlab", "```python")),
        }
        total_plots = 0
        for prefix, (courses, lang_fences) in tracks.items():
            assert len(courses) == 3
            assert {c.level for c in courses} == {"Beginner", "Intermediate", "Advanced"}
            for course in courses:
                assert course.slug.startswith(prefix)
                kinds = {le.lesson_type for le in course.lessons}
                assert kinds <= {"text", "code"}
                assert any(le.lesson_type == "code" for le in course.lessons)  # runnable lab
                body = "\n".join(le.text_body or "" for le in course.lessons)
                for fence in lang_fences:  # dual language
                    assert fence in body, f"{course.slug} missing {fence}"
                course_plots = 0
                for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                    json.loads(raw)  # valid interactive plot JSON
                    course_plots += 1
                assert course_plots >= 3, f"{course.slug} has <3 plots"
                total_plots += course_plots
                # every content lesson has a checkpoint quiz from the registry
                assert course.slug in QUIZ_REGISTRY
                spec = QUIZ_REGISTRY[course.slug]
                assert spec.final
                content_titles = {
                    le.title for le in course.lessons if le.lesson_type in {"text", "code"}
                }
                assert set(spec.per_lesson) == content_titles
        assert total_plots >= 75  # richly interactive across the 5 tracks

    def test_tier3_ee_tracks_complete(self) -> None:
        import json
        import re

        from cyberdyne_backend.application.courses.seed_analog_ic import ANALOG_IC_COURSES
        from cyberdyne_backend.application.courses.seed_battery import BATTERY_COURSES
        from cyberdyne_backend.application.courses.seed_comparch import COMPARCH_COURSES
        from cyberdyne_backend.application.courses.seed_digital_comms import (
            DIGITAL_COMMS_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_fpga import FPGA_COURSES
        from cyberdyne_backend.application.courses.seed_microwave import MICROWAVE_COURSES
        from cyberdyne_backend.application.courses.seed_photonics import PHOTONICS_COURSES
        from cyberdyne_backend.application.courses.seed_power_systems import (
            POWER_SYSTEMS_COURSES,
        )
        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY

        tracks = {
            "comparch": (COMPARCH_COURSES, ("```c", "```python")),
            "analog-ic": (ANALOG_IC_COURSES, ("```spice", "```python")),
            "photonics": (PHOTONICS_COURSES, ("```matlab", "```python")),
            "battery": (BATTERY_COURSES, ("```matlab", "```python")),
            "digital-comms": (DIGITAL_COMMS_COURSES, ("```matlab", "```python")),
            "microwave": (MICROWAVE_COURSES, ("```matlab", "```python")),
            "fpga": (FPGA_COURSES, ("```systemverilog", "```python")),
            "power-systems": (POWER_SYSTEMS_COURSES, ("```matlab", "```python")),
        }
        total_plots = 0
        for prefix, (courses, lang_fences) in tracks.items():
            assert len(courses) == 3
            assert {c.level for c in courses} == {"Beginner", "Intermediate", "Advanced"}
            for course in courses:
                assert course.slug.startswith(prefix)
                kinds = {le.lesson_type for le in course.lessons}
                assert kinds <= {"text", "code"}
                assert any(le.lesson_type == "code" for le in course.lessons)  # runnable lab
                body = "\n".join(le.text_body or "" for le in course.lessons)
                for fence in lang_fences:  # dual language
                    assert fence in body, f"{course.slug} missing {fence}"
                course_plots = 0
                for raw in re.findall(r"```plot\n(.*?)\n```", body, re.S):
                    json.loads(raw)  # valid interactive plot JSON
                    course_plots += 1
                assert course_plots >= 3, f"{course.slug} has <3 plots"
                total_plots += course_plots
                # every content lesson has a checkpoint quiz from the registry
                assert course.slug in QUIZ_REGISTRY
                spec = QUIZ_REGISTRY[course.slug]
                assert spec.final
                content_titles = {
                    le.title for le in course.lessons if le.lesson_type in {"text", "code"}
                }
                assert set(spec.per_lesson) == content_titles
        assert total_plots >= 120  # richly interactive across the 8 tracks

    def test_sysverilog_track_complete(self) -> None:
        # The SystemVerilog track backs Computer Architecture with RTL: three
        # levels, SystemVerilog throughout, valid interactive plots, diagrams,
        # and full quiz coverage. (It is text/RTL-based, not a MATLAB-runnable
        # lab track, so it is verified here rather than in the Tier-3 EE test.)
        import json
        import re

        from cyberdyne_backend.application.courses.seed_quizzes import QUIZ_REGISTRY
        from cyberdyne_backend.application.courses.seed_sysverilog import SYSVERILOG_COURSES

        assert len(SYSVERILOG_COURSES) == 3
        assert {c.level for c in SYSVERILOG_COURSES} == {"Beginner", "Intermediate", "Advanced"}
        for course in SYSVERILOG_COURSES:
            assert course.slug.startswith("sysverilog-")
            body = "\n".join(le.text_body or "" for le in course.lessons)
            assert "```systemverilog" in body, f"{course.slug} missing SystemVerilog"
            assert "```mermaid" in body, f"{course.slug} missing a diagram"
            for raw in re.findall(r"```(?:plot|vectors)\n(.*?)\n```", body, re.S):
                json.loads(raw)  # every interactive plot block is valid JSON
            assert course.slug in QUIZ_REGISTRY
            spec = QUIZ_REGISTRY[course.slug]
            assert spec.final
            content_titles = {
                le.title for le in course.lessons if le.lesson_type in {"text", "code"}
            }
            assert set(spec.per_lesson) == content_titles

    def test_csharp_track_runs_basics_to_aspnet(self) -> None:
        from cyberdyne_backend.application.courses.seed_csharp import CSHARP_COURSES

        slugs = {c.slug for c in CSHARP_COURSES}
        assert slugs == {"csharp-basics", "csharp-intermediate", "csharp-advanced"}
        levels = {c.slug: c.level for c in CSHARP_COURSES}
        assert levels["csharp-basics"] == "Beginner"
        assert levels["csharp-intermediate"] == "Intermediate"
        assert levels["csharp-advanced"] == "Advanced"
        for course in CSHARP_COURSES:
            # C# lessons are text (no .NET runtime in the Academy) + a quiz.
            kinds = {le.lesson_type for le in course.lessons}
            assert kinds <= {"text", "quiz"}, f"{course.slug} has a non-text lesson"
            assert any(le.lesson_type == "quiz" for le in course.lessons)

        basics = next(c for c in CSHARP_COURSES if c.slug == "csharp-basics")
        basics_body = "\n".join(le.text_body or "" for le in basics.lessons)
        for kw in ("dotnet new", "Console.WriteLine", "var ", "switch"):
            assert kw in basics_body, f"basics missing {kw!r}"

        inter = next(c for c in CSHARP_COURSES if c.slug == "csharp-intermediate")
        inter_body = "\n".join(le.text_body or "" for le in inter.lessons)
        for kw in ("record", "async", "await", ".Where(", "interface"):
            assert kw in inter_body, f"intermediate missing {kw!r}"

        adv = next(c for c in CSHARP_COURSES if c.slug == "csharp-advanced")
        adv_titles = " | ".join(le.title for le in adv.lessons)
        for needle in ("Dependency injection", "REST API", "Entity Framework", "Testing"):
            assert needle in adv_titles, f"advanced missing {needle!r}"
        adv_body = "\n".join(le.text_body or "" for le in adv.lessons)
        for kw in ("AddScoped", "WebApplication.CreateBuilder", "DbContext", "[Fact]"):
            assert kw in adv_body, f"advanced missing {kw!r}"

    def test_physics_track_reaches_quadrotor_via_three_methods(self) -> None:
        from cyberdyne_backend.application.courses.seed_physics import PHYSICS_COURSES

        slugs = {c.slug for c in PHYSICS_COURSES}
        assert slugs == {"physics-basics", "physics-intermediate", "physics-quadrotor-dynamics"}
        # The advanced course covers all three derivation methods + a runnable sim.
        adv = next(c for c in PHYSICS_COURSES if c.slug == "physics-quadrotor-dynamics")
        assert adv.level == "Advanced"
        titles = " | ".join(le.title for le in adv.lessons)
        for needle in ("Newton", "Lagrangian", "Hamiltonian", "Simulate"):
            assert needle in titles, f"advanced physics missing {needle!r}"
        code = next(le for le in adv.lessons if le.lesson_type == "code")
        assert code.text_body and "import" not in code.text_body  # restricted-safe sim

    def test_blockchain_course_covers_idea_pow_and_bitcoin(self) -> None:
        bc = next(c for c in ACADEMY_COURSES if c.slug == "blockchain-basics")
        titles = " | ".join(le.title for le in bc.lessons)
        for needle in ("blockchain", "Hashing", "Proof of Work", "Mine a block", "Bitcoin"):
            assert needle in titles, f"missing lesson about {needle!r}"
        # The runnable miner is a Python code lesson with a working toy PoW.
        code = next(le for le in bc.lessons if le.lesson_type == "code")
        assert code.text_body and "toy_hash" in code.text_body and "nonce" in code.text_body
        # It must avoid hashlib (blocked in the restricted interpreter sandbox).
        assert "hashlib" not in (code.text_body or "")

    def test_advanced_blockchain_course_covers_requested_topics(self) -> None:
        bc = next(c for c in ACADEMY_COURSES if c.slug == "blockchain-beyond-basics")
        titles = " | ".join(le.title for le in bc.lessons)
        for needle in ("Bitcoin Script", "Consensus", "Cold wallets", "Ethereum", "Solidity"):
            assert needle in titles, f"missing lesson about {needle!r}"
        # The runnable Bitcoin Script toy avoids imports (restricted sandbox).
        code = next(le for le in bc.lessons if le.lesson_type == "code")
        assert code.text_body and "stack" in code.text_body and "import" not in code.text_body
