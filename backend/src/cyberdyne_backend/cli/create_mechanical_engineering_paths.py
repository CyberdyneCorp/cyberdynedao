"""Create the three "Mechanical Engineering" learning paths + their modules via
the admin API.

Companion to ``create_computer_engineering_path`` and
``create_life_sciences_paths`` — an operational, run-once helper, NOT app seed
data. The Mechanical Engineering courses are seeded by the academy seed; this
curates them into three guided, enrollable paths that mirror the degree arc:

  * mechanical-foundations  — classical ME core (13 tracks)
  * mechatronics-robotics   — computational mechanics, mechatronics, robotics (8 tracks)
  * generative-design-ai    — optimization & AI generative design (6 tracks)

Each module bundles one track's three courses ({slug}-basics/-intermediate/
-advanced) via ``courseSlugs``. Idempotent: existing modules/paths (409) are
skipped, so it is safe to re-run.

    python -m cyberdyne_backend.cli.create_mechanical_engineering_paths

Configuration via environment variables (same scheme as the other path
helpers):
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_AUTH_BASE  default https://auth.backend.coolify.cyberdynecorp.ai
  ACADEMY_TOKEN      a bearer token (skips login), OR
  ACADEMY_EMAIL / ACADEMY_PASSWORD   to log in
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_API_BASE = "https://dao.backend.coolify.cyberdynecorp.ai"
DEFAULT_AUTH_BASE = "https://auth.backend.coolify.cyberdynecorp.ai"

# Each tuple is one track -> one module: (slug, title, category, level, icon,
# description). The module bundles the track's three courses.
_Track = tuple[str, str, str, str, str, str]

_FOUNDATIONS: tuple[_Track, ...] = (
    (
        "engineering-statics",
        "Engineering Statics",
        "Engineering Mechanics",
        "Beginner",
        "📐",
        "Forces, moments, equilibrium, trusses, friction and second moments of area.",
    ),
    (
        "engineering-dynamics",
        "Engineering Dynamics",
        "Engineering Mechanics",
        "Beginner",
        "🏃",
        "Kinematics and kinetics of particles and rigid bodies; energy and momentum.",
    ),
    (
        "mechanics-of-materials",
        "Mechanics of Materials",
        "Engineering Mechanics",
        "Intermediate",
        "🔩",
        "Stress, strain, torsion, bending, deflection, buckling and failure.",
    ),
    (
        "engineering-graphics-cad",
        "Engineering Graphics, GD&T & CAD",
        "Design & CAD",
        "Beginner",
        "✏️",
        "Projection, dimensioning, tolerancing and parametric solid modelling.",
    ),
    (
        "engineering-thermodynamics",
        "Engineering Thermodynamics",
        "Thermal & Fluids",
        "Intermediate",
        "🔥",
        "Energy, the laws, entropy and power/refrigeration cycles.",
    ),
    (
        "fluid-mechanics",
        "Fluid Mechanics",
        "Thermal & Fluids",
        "Intermediate",
        "🌊",
        "Hydrostatics, Bernoulli, Navier-Stokes, pipe flow and drag.",
    ),
    (
        "heat-transfer",
        "Heat Transfer",
        "Thermal & Fluids",
        "Intermediate",
        "🌡️",
        "Conduction, convection, radiation, fins and heat exchangers.",
    ),
    (
        "materials-science",
        "Materials Science & Engineering",
        "Materials & Manufacturing",
        "Intermediate",
        "🧱",
        "Structure-property relations, phase diagrams and selection.",
    ),
    (
        "manufacturing-processes",
        "Manufacturing Processes",
        "Materials & Manufacturing",
        "Intermediate",
        "🏭",
        "Casting, forming, machining, joining and design for manufacturing.",
    ),
    (
        "additive-manufacturing",
        "Additive Manufacturing",
        "Materials & Manufacturing",
        "Intermediate",
        "🖨️",
        "FFF/SLA/SLS/DMLS, design for AM, lattices and supports.",
    ),
    (
        "machine-design",
        "Machine Design & Elements",
        "Machines & Mechanisms",
        "Advanced",
        "⚙️",
        "Fatigue, shafts, bearings, gears, fasteners and springs.",
    ),
    (
        "kinematics-of-machinery",
        "Kinematics & Dynamics of Machinery",
        "Machines & Mechanisms",
        "Intermediate",
        "🔗",
        "Linkages, cams, gear trains, balancing and synthesis.",
    ),
    (
        "mechanical-vibrations",
        "Mechanical Vibrations",
        "Machines & Mechanisms",
        "Advanced",
        "📳",
        "Free/forced response, resonance, isolation and modal analysis.",
    ),
)

_MECHATRONICS: tuple[_Track, ...] = (
    (
        "finite-element-analysis",
        "Finite Element Analysis",
        "Computational (CAE)",
        "Advanced",
        "🕸️",
        "Weak form, elements, meshing, solving and validating structural/thermal models.",
    ),
    (
        "computational-fluid-dynamics",
        "Computational Fluid Dynamics",
        "Computational (CAE)",
        "Advanced",
        "💨",
        "Finite-volume discretisation, turbulence models and convergence.",
    ),
    (
        "multibody-dynamics",
        "Multibody Dynamics & Simulation",
        "Computational (CAE)",
        "Advanced",
        "🧩",
        "Joints, constraints and integration for moving assemblies and robots.",
    ),
    (
        "cad-cae-parametric",
        "Parametric & Simulation-Driven Design",
        "Computational (CAE)",
        "Intermediate",
        "🛠️",
        "Parametric models and closing the CAD-CAE loop for automation.",
    ),
    (
        "mechatronics",
        "Mechatronics",
        "Mechatronics",
        "Intermediate",
        "🤖",
        "Integrating sensors, actuators, microcontrollers and control.",
    ),
    (
        "actuators-motion-systems",
        "Actuators & Motion Systems",
        "Mechatronics",
        "Intermediate",
        "🔧",
        "DC/servo/stepper/BLDC motors, drives, gearboxes and motion profiling.",
    ),
    (
        "hydraulics-pneumatics",
        "Hydraulics & Pneumatics",
        "Mechatronics",
        "Intermediate",
        "🛢️",
        "Fluid power: pumps, valves, cylinders, circuits and proportional control.",
    ),
    (
        "robot-manipulators",
        "Robot Manipulators & Industrial Robotics",
        "Robotics",
        "Advanced",
        "🦾",
        "Forward/inverse kinematics, Jacobians, dynamics and trajectory generation.",
    ),
)

_GENERATIVE: tuple[_Track, ...] = (
    (
        "design-optimization",
        "Engineering Design Optimization",
        "Optimization",
        "Advanced",
        "📈",
        "Objectives/constraints, gradient and gradient-free, multi-objective and surrogates.",
    ),
    (
        "topology-optimization",
        "Topology Optimization",
        "Optimization",
        "Advanced",
        "🔲",
        "SIMP, level-set and density methods; letting physics place material.",
    ),
    (
        "ml-for-engineering",
        "Machine Learning for Engineering & Simulation",
        "AI / ML",
        "Intermediate",
        "🧠",
        "Surrogate/ROM models, PINNs and ML-accelerated simulation.",
    ),
    (
        "generative-design",
        "Generative Design & AI for CAD",
        "AI / ML",
        "Advanced",
        "✨",
        "Goal-driven generation, design-space exploration and AI-assisted CAD.",
    ),
    (
        "ai-organic-shapes",
        "AI-Driven Organic & Biomimetic Shapes",
        "AI / ML",
        "Advanced",
        "🌿",
        "Lattices, biomimicry and generative/diffusion models for print-ready geometry.",
    ),
    (
        "capstone-generative-mechanical-design",
        "Capstone: AI-Optimised Organic Part",
        "Capstone",
        "Advanced",
        "🏆",
        "Model -> topology-optimise -> generate -> FEA-validate -> 3D print.",
    ),
)

# (path slug, title, icon, estimated_time, description, tracks)
_PATHS: tuple[tuple[str, str, str, str, str, tuple[_Track, ...]], ...] = (
    (
        "mechanical-foundations",
        "Mechanical Foundations",
        "📐",
        "24-32 weeks",
        "The classical mechanical engineering backbone: statics, dynamics and "
        "mechanics of materials; thermodynamics, fluids and heat transfer; "
        "materials, manufacturing, machine design and mechanisms.",
        _FOUNDATIONS,
    ),
    (
        "mechatronics-robotics",
        "Mechatronics & Robotics",
        "🤖",
        "14-20 weeks",
        "Simulating, sensing, actuating and controlling mechanical systems: "
        "FEA and CFD, multibody and parametric CAE, mechatronics, fluid power "
        "and industrial robot manipulators.",
        _MECHATRONICS,
    ),
    (
        "generative-design-ai",
        "Generative Design & AI",
        "✨",
        "10-16 weeks",
        "Optimisation and AI that generate organic, manufacturable geometry: "
        "design and topology optimisation, ML surrogates, generative design and "
        "an end-to-end AI-optimised organic part capstone.",
        _GENERATIVE,
    ),
)

_LEVELS = ("basics", "intermediate", "advanced")


def build_payloads() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (module payloads, path payloads). Pure — unit-tested. Each module
    bundles a track's three courses; each path references only modules built
    here. Module slugs are namespaced ``me-`` to avoid clashing with existing
    learning modules."""
    modules: list[dict[str, Any]] = []
    paths: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path_slug, title, icon, est, desc, tracks in _PATHS:
        module_slugs: list[str] = []
        for track_slug, m_title, category, level, m_icon, m_desc in tracks:
            mod_slug = f"me-{track_slug}"
            if mod_slug in seen:  # pragma: no cover - guards editing mistakes
                raise ValueError(f"duplicate module slug: {mod_slug}")
            seen.add(mod_slug)
            modules.append(
                {
                    "slug": mod_slug,
                    "title": m_title,
                    "category": category,
                    "level": level,
                    "duration": "4-6 hr",
                    "icon": m_icon,
                    "description": m_desc,
                    "topics": ["Basics", "Intermediate", "Advanced"],
                    "courseSlugs": [f"{track_slug}-{lv}" for lv in _LEVELS],
                }
            )
            module_slugs.append(mod_slug)
        paths.append(
            {
                "slug": path_slug,
                "title": title,
                "description": desc,
                "moduleSlugs": module_slugs,
                "estimatedTime": est,
                "icon": icon,
            }
        )
    return modules, paths


def _ctx() -> ssl.SSLContext | None:
    if os.environ.get("ACADEMY_INSECURE_TLS") == "1":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None


def _call(method: str, url: str, token: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, context=_ctx()) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def _token() -> str:
    token = os.environ.get("ACADEMY_TOKEN")
    if token:
        return token
    auth = os.environ.get("ACADEMY_AUTH_BASE", DEFAULT_AUTH_BASE)
    email = os.environ.get("ACADEMY_EMAIL")
    password = os.environ.get("ACADEMY_PASSWORD")
    if not (email and password):
        raise SystemExit("set ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD")
    req = urllib.request.Request(
        f"{auth}/api/v1/auth/login",
        data=json.dumps({"email": email, "password": password}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=_ctx()) as r:
        access_token: str = json.loads(r.read().decode())["access_token"]
    return access_token


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()
    modules, paths = build_payloads()

    for module in modules:
        st, _ = _call("POST", f"{api}/api/v1/admin/learning/modules", token, module)
        verb = "created" if st in (200, 201) else ("exists" if st == 409 else f"FAILED {st}")
        print(f"  module {module['slug']}: {verb}")

    failed = 0
    for path in paths:
        st, body = _call("POST", f"{api}/api/v1/admin/learning/paths", token, path)
        if st in (200, 201):
            print(f"  path {path['slug']}: created")
        elif st == 409:
            print(f"  path {path['slug']}: exists")
        else:
            print(f"  path {path['slug']}: FAILED {st} {body}")
            failed += 1
    if failed:
        return 1
    print("Done — the three Mechanical Engineering paths are live and enrollable.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
