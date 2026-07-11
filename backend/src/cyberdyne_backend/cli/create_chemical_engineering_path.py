"""Create the "Chemical Engineering" learning path + its modules via the
admin API (companion to ``create_computer_engineering_path``).

An operational, run-once helper, NOT app seed data. The courses are seeded
by the academy seed (reused chemistry/thermo/transport/AI/molecular courses
plus the 18 new chemical-process courses); this curates them into 13
modules and a path along the classic chemical-engineering progression,
with an AI + molecular-discovery stage last. Idempotent and extend-safe:
  * each module is POSTed (409 -> already exists, skipped);
  * the path is POSTed, OR - if it already exists - its ``moduleSlugs`` are
    PATCHed to include any new modules;
  * module + path translations (pt-BR/es/fr) are PUT (idempotent).

    python -m cyberdyne_backend.cli.create_chemical_engineering_path

Configuration via environment variables:
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

MODULES: tuple[dict[str, Any], ...] = (
    {
        "slug": "che-foundations",
        "title": "Scientific Foundations",
        "category": "Chemical Engineering",
        "level": "Beginner",
        "duration": "40 hr",
        "icon": "\U0001f4d0",
        "description": "The mathematics, physics and statistics every chemical engineer builds on.",
        "topics": ["Calculus", "Physics", "Differential equations", "Statistics"],
        "courseSlugs": [
            "math-basics",
            "math-intermediate",
            "physics-basics",
            "physics-intermediate",
            "math-probability",
        ],
    },
    {
        "slug": "che-computing",
        "title": "Computing and Data for Engineers",
        "category": "Chemical Engineering",
        "level": "Beginner",
        "duration": "30 hr",
        "icon": "\U0001f4bb",
        "description": "Python, MATLAB, version control and numerical methods for process computation.",
        "topics": ["Python", "MATLAB", "Git", "Numerical methods"],
        "courseSlugs": [
            "python-course",
            "matlab-basics",
            "git-basics",
            "math-numerical",
            "prob-stats-python-basics",
        ],
    },
    {
        "slug": "che-chemistry",
        "title": "Chemistry Core",
        "category": "Chemical Engineering",
        "level": "Intermediate",
        "duration": "40 hr",
        "icon": "\U0001f9ea",
        "description": "General, organic and analytical chemistry - the science behind the processes.",
        "topics": ["General chemistry", "Organic chemistry", "Analytical chemistry"],
        "courseSlugs": [
            "general-chemistry-basics",
            "general-chemistry-intermediate",
            "organic-chemistry-basics",
            "organic-chemistry-intermediate",
            "analytical-chemistry-basics",
        ],
    },
    {
        "slug": "che-intro",
        "title": "Introduction and Graphics",
        "category": "Chemical Engineering",
        "level": "Beginner",
        "duration": "14 hr",
        "icon": "\U0001f3ed",
        "description": "The profession and the language of process drawings.",
        "topics": ["Profession", "Process industries", "CAD", "Flow diagrams"],
        "courseSlugs": ["intro-chemical-engineering", "engineering-graphics-cad-basics"],
    },
    {
        "slug": "che-balances-thermo",
        "title": "Balances and Thermodynamics",
        "category": "Chemical Engineering",
        "level": "Intermediate",
        "duration": "34 hr",
        "icon": "⚖️",
        "description": "Material and energy balances and the thermodynamics that drive process design.",
        "topics": ["Material balances", "Energy balances", "Thermodynamics", "Phase equilibrium"],
        "courseSlugs": [
            "material-energy-balances",
            "chemical-engineering-thermodynamics",
            "engineering-thermodynamics-basics",
            "physical-chemistry-basics",
        ],
    },
    {
        "slug": "che-transport",
        "title": "Transport Phenomena",
        "category": "Chemical Engineering",
        "level": "Intermediate",
        "duration": "40 hr",
        "icon": "\U0001f30a",
        "description": "Momentum, heat and mass transfer - the physics of how processes move fluids, heat and species.",
        "topics": ["Fluid mechanics", "Heat transfer", "Mass transfer", "Separations"],
        "courseSlugs": [
            "fluid-mechanics-basics",
            "fluid-mechanics-intermediate",
            "heat-transfer-basics",
            "heat-transfer-intermediate",
            "mass-transfer-separations",
        ],
    },
    {
        "slug": "che-reactions",
        "title": "Reaction Engineering",
        "category": "Chemical Engineering",
        "level": "Advanced",
        "duration": "22 hr",
        "icon": "\U0001f321",
        "description": "Kinetics, catalysis and reactor design - the heart of the chemical plant.",
        "topics": ["Kinetics", "Reactors", "Catalysis"],
        "courseSlugs": ["chemical-reaction-engineering", "physical-chemistry-intermediate"],
    },
    {
        "slug": "che-unit-ops",
        "title": "Unit Operations and Equipment",
        "category": "Chemical Engineering",
        "level": "Intermediate",
        "duration": "24 hr",
        "icon": "\U0001f527",
        "description": "The standard physical operations and the equipment that carries them out.",
        "topics": ["Distillation", "Drying", "Filtration", "Equipment design"],
        "courseSlugs": ["unit-operations", "process-equipment-design"],
    },
    {
        "slug": "che-control",
        "title": "Process Control and Instrumentation",
        "category": "Chemical Engineering",
        "level": "Intermediate",
        "duration": "28 hr",
        "icon": "\U0001f39b",
        "description": "Measuring and controlling processes - dynamics, PID and advanced control, instrumentation.",
        "topics": ["Process dynamics", "PID control", "MPC", "Instrumentation"],
        "courseSlugs": ["process-dynamics-control", "control-basics", "sensors-intermediate"],
    },
    {
        "slug": "che-design-safety",
        "title": "Process Design, Simulation and Safety",
        "category": "Chemical Engineering",
        "level": "Advanced",
        "duration": "30 hr",
        "icon": "\U0001f4d0",
        "description": "Designing whole plants, simulating them, and keeping them safe.",
        "topics": ["Process design", "Simulation", "CFD", "Process safety"],
        "courseSlugs": [
            "process-design-simulation",
            "process-safety-engineering",
            "computational-fluid-dynamics-basics",
        ],
    },
    {
        "slug": "che-industrial",
        "title": "Industrial Specializations",
        "category": "Chemical Engineering",
        "level": "Advanced",
        "duration": "44 hr",
        "icon": "\U0001f3ed",
        "description": "The major process industries: bioprocess, petrochemical, polymers and pharmaceuticals.",
        "topics": ["Bioprocess", "Petrochemical", "Polymers", "Pharmaceutical"],
        "courseSlugs": [
            "bioprocess-engineering",
            "petrochemical-refining",
            "polymer-engineering",
            "pharmaceutical-engineering",
            "materials-science-basics",
        ],
    },
    {
        "slug": "che-sustainability-econ",
        "title": "Sustainability, Environment and Economics",
        "category": "Chemical Engineering",
        "level": "Advanced",
        "duration": "26 hr",
        "icon": "\U0001f331",
        "description": "Clean processes, the energy transition, and the economics of chemical projects.",
        "topics": ["Environment", "Green hydrogen", "Carbon capture", "Economics"],
        "courseSlugs": [
            "environmental-process-engineering",
            "sustainable-processes",
            "process-economics-management",
        ],
    },
    {
        "slug": "che-ai-molecular",
        "title": "AI, Data Science and Molecular Discovery",
        "category": "Chemical Engineering",
        "level": "Advanced",
        "duration": "40 hr",
        "icon": "\U0001f9ec",
        "description": "AI for processes and for molecules - digital twins, machine learning, generative molecular design, docking and AlphaFold-era drug discovery.",
        "topics": ["Machine learning", "Digital twins", "Drug discovery", "AlphaFold"],
        "courseSlugs": [
            "ai-digital-chemical-engineering",
            "ml-for-engineering-basics",
            "cheminformatics-basics",
            "generative-molecular-design-basics",
            "docking-virtual-screening-basics",
            "protein-science-basics",
        ],
    },
)

PATH: dict[str, Any] = {
    "slug": "chemical-engineering",
    "title": "Chemical Engineering",
    "description": (
        "A full chemical-engineering curriculum, from scientific and chemistry "
        "foundations through balances, thermodynamics, transport, reaction engineering, "
        "unit operations, control, plant design and the major process industries - "
        "closing with a stage on AI, digital twins and AI-driven molecular and drug "
        "discovery (cheminformatics, generative models, AlphaFold-era protein science)."
    ),
    "moduleSlugs": [m["slug"] for m in MODULES],
    "estimatedTime": "52-64 weeks",
    "icon": "\U0001f9ea",
}

MODULE_TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    "che-foundations": {
        "pt-BR": {
            "title": "Fundamentos Cientificos",
            "description": "A matematica, fisica e estatistica que todo engenheiro quimico usa.",
        },
        "es": {
            "title": "Fundamentos Cientificos",
            "description": "Las matematicas, la fisica y la estadistica que todo ingeniero quimico usa.",
        },
        "fr": {
            "title": "Fondements Scientifiques",
            "description": "Les mathematiques, la physique et les statistiques de base de l'ingenieur chimiste.",
        },
    },
    "che-computing": {
        "pt-BR": {
            "title": "Computacao e Dados para Engenheiros",
            "description": "Python, MATLAB, controle de versao e metodos numericos para calculo de processos.",
        },
        "es": {
            "title": "Computacion y Datos para Ingenieros",
            "description": "Python, MATLAB, control de versiones y metodos numericos para el calculo de procesos.",
        },
        "fr": {
            "title": "Informatique et Donnees pour Ingenieurs",
            "description": "Python, MATLAB, gestion de versions et methodes numeriques pour le calcul des procedes.",
        },
    },
    "che-chemistry": {
        "pt-BR": {
            "title": "Nucleo de Quimica",
            "description": "Quimica geral, organica e analitica - a ciencia por tras dos processos.",
        },
        "es": {
            "title": "Nucleo de Quimica",
            "description": "Quimica general, organica y analitica - la ciencia detras de los procesos.",
        },
        "fr": {
            "title": "Noyau de Chimie",
            "description": "Chimie generale, organique et analytique - la science derriere les procedes.",
        },
    },
    "che-intro": {
        "pt-BR": {
            "title": "Introducao e Desenho",
            "description": "A profissao e a linguagem dos desenhos de processo.",
        },
        "es": {
            "title": "Introduccion y Dibujo",
            "description": "La profesion y el lenguaje de los diagramas de proceso.",
        },
        "fr": {
            "title": "Introduction et Dessin",
            "description": "La profession et le langage des schemas de procede.",
        },
    },
    "che-balances-thermo": {
        "pt-BR": {
            "title": "Balancos e Termodinamica",
            "description": "Balancos de massa e energia e a termodinamica que orienta o projeto de processos.",
        },
        "es": {
            "title": "Balances y Termodinamica",
            "description": "Balances de masa y energia y la termodinamica que guia el diseno de procesos.",
        },
        "fr": {
            "title": "Bilans et Thermodynamique",
            "description": "Bilans de matiere et d'energie et la thermodynamique qui guide la conception des procedes.",
        },
    },
    "che-transport": {
        "pt-BR": {
            "title": "Fenomenos de Transporte",
            "description": "Transferencia de momento, calor e massa - a fisica do movimento de fluidos, calor e especies.",
        },
        "es": {
            "title": "Fenomenos de Transporte",
            "description": "Transferencia de momento, calor y masa - la fisica del movimiento de fluidos, calor y especies.",
        },
        "fr": {
            "title": "Phenomenes de Transport",
            "description": "Transfert de quantite de mouvement, de chaleur et de matiere.",
        },
    },
    "che-reactions": {
        "pt-BR": {
            "title": "Engenharia das Reacoes",
            "description": "Cinetica, catalise e projeto de reatores - o coracao da planta quimica.",
        },
        "es": {
            "title": "Ingenieria de las Reacciones",
            "description": "Cinetica, catalisis y diseno de reactores - el corazon de la planta quimica.",
        },
        "fr": {
            "title": "Genie de la Reaction",
            "description": "Cinetique, catalyse et conception des reacteurs - le coeur de l'usine chimique.",
        },
    },
    "che-unit-ops": {
        "pt-BR": {
            "title": "Operacoes Unitarias e Equipamentos",
            "description": "As operacoes fisicas padrao e os equipamentos que as executam.",
        },
        "es": {
            "title": "Operaciones Unitarias y Equipos",
            "description": "Las operaciones fisicas estandar y los equipos que las ejecutan.",
        },
        "fr": {
            "title": "Operations Unitaires et Equipements",
            "description": "Les operations physiques standard et les equipements qui les realisent.",
        },
    },
    "che-control": {
        "pt-BR": {
            "title": "Controle de Processos e Instrumentacao",
            "description": "Medir e controlar processos - dinamica, PID e controle avancado, instrumentacao.",
        },
        "es": {
            "title": "Control de Procesos e Instrumentacion",
            "description": "Medir y controlar procesos - dinamica, PID y control avanzado, instrumentacion.",
        },
        "fr": {
            "title": "Controle des Procedes et Instrumentation",
            "description": "Mesurer et controler les procedes - dynamique, PID et controle avance, instrumentation.",
        },
    },
    "che-design-safety": {
        "pt-BR": {
            "title": "Projeto, Simulacao e Seguranca de Processos",
            "description": "Projetar plantas completas, simula-las e mante-las seguras.",
        },
        "es": {
            "title": "Diseno, Simulacion y Seguridad de Procesos",
            "description": "Disenar plantas completas, simularlas y mantenerlas seguras.",
        },
        "fr": {
            "title": "Conception, Simulation et Securite des Procedes",
            "description": "Concevoir des usines completes, les simuler et les securiser.",
        },
    },
    "che-industrial": {
        "pt-BR": {
            "title": "Especializacoes Industriais",
            "description": "As grandes industrias de processo: bioprocessos, petroquimica, polimeros e farmaceutica.",
        },
        "es": {
            "title": "Especializaciones Industriales",
            "description": "Las grandes industrias de proceso: bioprocesos, petroquimica, polimeros y farmaceutica.",
        },
        "fr": {
            "title": "Specialisations Industrielles",
            "description": "Les grandes industries de procede : bioprocedes, petrochimie, polymeres et pharmacie.",
        },
    },
    "che-sustainability-econ": {
        "pt-BR": {
            "title": "Sustentabilidade, Meio Ambiente e Economia",
            "description": "Processos limpos, a transicao energetica e a economia de projetos quimicos.",
        },
        "es": {
            "title": "Sostenibilidad, Medio Ambiente y Economia",
            "description": "Procesos limpios, la transicion energetica y la economia de los proyectos quimicos.",
        },
        "fr": {
            "title": "Durabilite, Environnement et Economie",
            "description": "Procedes propres, transition energetique et economie des projets chimiques.",
        },
    },
    "che-ai-molecular": {
        "pt-BR": {
            "title": "IA, Ciencia de Dados e Descoberta Molecular",
            "description": "IA para processos e para moleculas - gemeos digitais, aprendizado de maquina, design molecular generativo, docking e descoberta de farmacos na era do AlphaFold.",
        },
        "es": {
            "title": "IA, Ciencia de Datos y Descubrimiento Molecular",
            "description": "IA para procesos y para moleculas - gemelos digitales, aprendizaje automatico, diseno molecular generativo, docking y descubrimiento de farmacos en la era de AlphaFold.",
        },
        "fr": {
            "title": "IA, Science des Donnees et Decouverte Moleculaire",
            "description": "IA pour les procedes et les molecules - jumeaux numeriques, apprentissage automatique, conception moleculaire generative, docking et decouverte de medicaments a l'ere d'AlphaFold.",
        },
    },
}

PATH_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "Engenharia Quimica",
        "description": (
            "Um curriculo completo de engenharia quimica, dos fundamentos cientificos e de quimica aos "
            "balancos, termodinamica, transporte, engenharia das reacoes, operacoes unitarias, controle, "
            "projeto de plantas e as grandes industrias de processo - encerrando com IA, gemeos digitais e "
            "descoberta molecular e de farmacos guiada por IA (quimioinformatica, modelos generativos, "
            "ciencia de proteinas na era do AlphaFold)."
        ),
    },
    "es": {
        "title": "Ingenieria Quimica",
        "description": (
            "Un curriculo completo de ingenieria quimica, desde los fundamentos cientificos y de quimica hasta "
            "los balances, la termodinamica, el transporte, la ingenieria de reacciones, las operaciones "
            "unitarias, el control, el diseno de plantas y las grandes industrias de proceso - cerrando con IA, "
            "gemelos digitales y descubrimiento molecular y de farmacos guiado por IA (quimioinformatica, "
            "modelos generativos, ciencia de proteinas en la era de AlphaFold)."
        ),
    },
    "fr": {
        "title": "Genie Chimique",
        "description": (
            "Un cursus complet de genie chimique, des fondements scientifiques et de la chimie aux bilans, a la "
            "thermodynamique, au transport, au genie de la reaction, aux operations unitaires, au controle, a la "
            "conception d'usines et aux grandes industries de procede - en terminant par l'IA, les jumeaux "
            "numeriques et la decouverte moleculaire et de medicaments guidee par l'IA (chemoinformatique, "
            "modeles generatifs, science des proteines a l'ere d'AlphaFold)."
        ),
    },
}


def build_payloads() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return (module payloads, path payload). Pure - unit-tested."""
    module_slugs = {m["slug"] for m in MODULES}
    missing = [s for s in PATH["moduleSlugs"] if s not in module_slugs]
    if missing:  # pragma: no cover - edit guard
        raise ValueError(f"path references modules not in MODULES: {missing}")
    return list(MODULES), dict(PATH)


def merged_module_slugs(existing: list[str], wanted: list[str]) -> list[str]:
    """Existing order preserved; any wanted slug not present is appended."""
    return existing + [s for s in wanted if s not in existing]


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
    email, password = os.environ.get("ACADEMY_EMAIL"), os.environ.get("ACADEMY_PASSWORD")
    if not (email and password):
        raise SystemExit("set ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD")
    req = urllib.request.Request(
        f"{auth}/api/v1/auth/login",
        data=json.dumps({"email": email, "password": password}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=_ctx()) as r:
        return str(json.loads(r.read().decode())["access_token"])


def _upsert_translations(api: str, token: str, kind: str, slug: str, trs: dict[str, Any]) -> None:
    for language, tr in trs.items():
        st, _ = _call(
            "PUT",
            f"{api}/api/v1/admin/learning/{kind}/{slug}/translations/{language}",
            token,
            tr,
        )
        print(f"    {kind[:-1]} {slug} {language}: {'ok' if st == 200 else f'FAILED {st}'}")


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()
    modules, path = build_payloads()

    for module in modules:
        st, _ = _call("POST", f"{api}/api/v1/admin/learning/modules", token, module)
        verb = "created" if st in (200, 201) else ("exists" if st == 409 else f"FAILED {st}")
        print(f"  module {module['slug']}: {verb}")
        if module["slug"] in MODULE_TRANSLATIONS:
            _upsert_translations(
                api, token, "modules", module["slug"], MODULE_TRANSLATIONS[module["slug"]]
            )

    st, body = _call("POST", f"{api}/api/v1/admin/learning/paths", token, path)
    if st in (200, 201):
        print(f"  path {path['slug']}: created")
    elif st == 409:
        _, existing = _call("GET", f"{api}/api/v1/admin/learning/paths", token)
        current: list[str] = next(
            (p["moduleSlugs"] for p in existing if p["slug"] == path["slug"]), []
        )
        merged = merged_module_slugs(list(current), path["moduleSlugs"])
        if merged == current:
            print(f"  path {path['slug']}: exists (all modules already present)")
        else:
            st, body = _call(
                "PATCH",
                f"{api}/api/v1/admin/learning/paths/{path['slug']}",
                token,
                {"moduleSlugs": merged},
            )
            if st != 200:
                print(f"  path {path['slug']}: PATCH FAILED {st} {body}")
                return 1
            print(f"  path {path['slug']}: extended to {len(merged)} modules")
    else:
        print(f"  path {path['slug']}: FAILED {st} {body}")
        return 1
    _upsert_translations(api, token, "paths", path["slug"], PATH_TRANSLATIONS)

    print(f"Done - '{path['title']}' path is live and enrollable.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
