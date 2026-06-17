# uploads Specification

## Purpose

Accept editor file uploads with MIME-based routing, per-category size caps,
and path-traversal-safe storage; serve stored files read-only over a static
media mount. (src: adapters/inbound/api/uploads/router.py, domain/uploads,
adapters/outbound/storage/local.py)

## Requirements

### Requirement: Validated, traversal-safe upload

The system SHALL accept `POST /api/v1/admin/uploads` (and `…/uploads/batch`)
from an `editor`. It SHALL classify the file by MIME into a category
(image/document/presentation/video), reject unsupported types with `415`,
and enforce a hard global cap (200 MB) plus a per-category cap (exceeding →
`413`). The stored filename SHALL be a server-generated `{uuid}{ext}` (never
client-supplied); the original name SHALL be sanitized for display, and an
empty/unsafe sanitized name SHALL return `422`. A batch SHALL be
all-or-nothing.

#### Scenario: Image upload

- GIVEN an editor and a small PNG
- WHEN they POST it to `/api/v1/admin/uploads`
- THEN it is stored under the `image` category with a `{uuid}.png` filename and a `/media/image/...` URL

#### Scenario: Path-traversal filename is neutralised

- GIVEN a file named `../../../../etc/passwd.png`
- WHEN it is uploaded
- THEN the stored filename is `{uuid}.png` and no path escapes the storage root

#### Scenario: Unsupported type

- GIVEN an executable file
- WHEN it is uploaded
- THEN the system SHALL respond `415`

#### Scenario: Over the size cap

- GIVEN an image larger than the image cap
- WHEN it is uploaded
- THEN the system SHALL respond `413`

### Requirement: Public read-only serving

The system SHALL expose upload metadata at `GET /api/v1/uploads/{id}` (404 if
absent) and serve the stored bytes read-only via the static `/media/*` mount.

#### Scenario: Serve a stored file

- GIVEN a previously uploaded image at `/media/image/abc.png`
- WHEN a client GETs that URL
- THEN the byte-identical file is served
