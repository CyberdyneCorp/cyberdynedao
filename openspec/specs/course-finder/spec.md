# course-finder Specification

## Purpose

Scan-to-Learn: read a photographed question (vision), extract the topic, and
route the learner to the course/lesson that teaches it via embedding-based
semantic match over the catalog. No prompt-stuffing of the catalog — courses +
lessons are embedded and matched by cosine; an in-memory index, no pgvector.
(src: adapters/inbound/api/course_finder/router.py, application/course_finder,
domain/course_finder)

## Requirements

### Requirement: Analyze a photographed question and match the catalog

The system SHALL accept `POST /api/v1/learning/scan` (multipart image) from a
signed-in learner, run a vision step to extract `{question, subject, keywords}`,
embed the query, and rank it (cosine) against an embedded index of published
course + lesson texts. It SHALL return ranked `CourseMatch[]`
(`{courseSlug, lessonId?, score, matchReason}`), with a deep-linkable
`lessonId` for lesson-level hits. The scan SHALL count toward the SCANS quota
(402 when the free cap is hit). A non-image upload SHALL return `415`. Images
are analyzed only and SHALL NOT be retained. Building the catalog index SHALL
batch the embeddings request under the provider's per-request input cap so it
scales as the catalog grows (issue #244).

#### Scenario: Catalog larger than the embeddings cap still builds

- GIVEN a catalog with more entries than the embeddings provider's per-request input cap
- WHEN the index is built
- THEN the embeddings are requested in batches under the cap and the build succeeds

#### Scenario: In-catalog topic routes to its course

- GIVEN a published course covering the photographed topic
- WHEN a learner POSTs the image to `/api/v1/learning/scan`
- THEN the matching course (and lesson when confident) is returned ranked first

### Requirement: Below-threshold no-match

When the top score is below the relevance threshold, the system SHALL return a
no-match (`noMatch: true`) carrying the extracted `{question, subject,
keywords}` so the client can offer "Request this course" (which feeds the
demand registry). The scan endpoint itself SHALL NOT create the request.

#### Scenario: Out-of-catalog topic returns no-match with the extracted query

- GIVEN no course covers the photographed topic
- WHEN a learner scans it
- THEN `noMatch` is true and the response carries the extracted question/subject/keywords
