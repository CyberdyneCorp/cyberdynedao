"""Learning bounded context.

Owns the modules + paths catalogue (seeded from
``frontend/src/lib/data/learn.ts``) plus the per-user state:
enrollments, module progress, certificates.

Certificates in v1 are signed-JSON blobs (Ed25519). NFT minting is
deferred to Phase 7+.
"""

from cyberdyne_backend.domain.learning.deadlines import (
    DeadlineStatus,
    EnrollmentDeadline,
    days_remaining,
    deadline_status,
)
from cyberdyne_backend.domain.learning.entities import (
    Certificate,
    Enrollment,
    EnrollmentStatus,
    LearningModule,
    LearningPath,
    ModuleProgress,
    certificate_eligible,
    new_certificate,
    new_enrollment,
    new_progress,
)
from cyberdyne_backend.domain.learning.errors import (
    CertificateNotEligibleError,
    EnrollmentNotFoundError,
    LearningContentNotFoundError,
    ProgressOutOfRangeError,
)
from cyberdyne_backend.domain.learning.ports import (
    CertificateSigner,
    LearningRepository,
)

__all__ = [
    "Certificate",
    "CertificateNotEligibleError",
    "CertificateSigner",
    "DeadlineStatus",
    "Enrollment",
    "EnrollmentDeadline",
    "EnrollmentNotFoundError",
    "EnrollmentStatus",
    "LearningContentNotFoundError",
    "LearningModule",
    "LearningPath",
    "LearningRepository",
    "ModuleProgress",
    "ProgressOutOfRangeError",
    "certificate_eligible",
    "days_remaining",
    "deadline_status",
    "new_certificate",
    "new_enrollment",
    "new_progress",
]
