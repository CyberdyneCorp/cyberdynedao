"""Learning bounded context.

Owns the modules + paths catalogue (seeded from
``frontend/src/lib/data/learn.ts``) plus the per-user state:
enrollments, module progress, certificates.

Certificates in v1 are signed-JSON blobs (Ed25519). NFT minting is
deferred to Phase 7+.
"""

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
from cyberdyne_backend.domain.learning.gating import (
    LEVEL_ORDER,
    ModuleGate,
    compute_path_gates,
    is_module_unlocked,
    level_rank,
    next_unlocked_module,
)
from cyberdyne_backend.domain.learning.ports import (
    CertificateSigner,
    LearningRepository,
)

__all__ = [
    "LEVEL_ORDER",
    "Certificate",
    "CertificateNotEligibleError",
    "CertificateSigner",
    "Enrollment",
    "EnrollmentNotFoundError",
    "EnrollmentStatus",
    "LearningContentNotFoundError",
    "LearningModule",
    "LearningPath",
    "LearningRepository",
    "ModuleGate",
    "ModuleProgress",
    "ProgressOutOfRangeError",
    "certificate_eligible",
    "compute_path_gates",
    "is_module_unlocked",
    "level_rank",
    "new_certificate",
    "new_enrollment",
    "new_progress",
    "next_unlocked_module",
]
