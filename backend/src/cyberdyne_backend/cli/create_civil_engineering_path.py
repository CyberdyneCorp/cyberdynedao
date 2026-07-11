"""Create the "Civil Engineering" learning path + its modules via the admin
API (companion to ``create_computer_engineering_path``).

An operational, run-once helper, NOT app seed data. The courses are seeded
by the academy seed (reused foundation/engineering courses plus the 18 new
civil-specific courses); this curates them into 12 modules and a path along
the classic civil-engineering knowledge axes, with the digital/AI stage
last. Idempotent and extend-safe:
  * each module is POSTed (409 -> already exists, skipped);
  * the path is POSTed, OR - if it already exists - its ``moduleSlugs`` are
    PATCHed to include any new modules;
  * module + path translations (pt-BR/es/fr) are PUT (idempotent).

    python -m cyberdyne_backend.cli.create_civil_engineering_path

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

# Each module is a track stage bundling seeded courses via ``courseSlugs``.
# Ordered as the intended learning progression (foundations -> digital/AI).
MODULES: tuple[dict[str, Any], ...] = (
    {
        "slug": "civ-foundations",
        "title": "Scientific Foundations",
        "category": "Civil Engineering",
        "level": "Beginner",
        "duration": "40 hr",
        "icon": "\U0001f4d0",
        "description": "The math, physics, chemistry and statistics every civil engineer builds on.",
        "topics": ["Calculus", "Linear algebra", "Physics", "Chemistry", "Statistics"],
        "courseSlugs": [
            "math-basics",
            "math-intermediate",
            "physics-basics",
            "general-chemistry-basics",
            "math-probability",
        ],
    },
    {
        "slug": "civ-computing",
        "title": "Computing and Data for Engineers",
        "category": "Civil Engineering",
        "level": "Beginner",
        "duration": "28 hr",
        "icon": "\U0001f4bb",
        "description": "Programming, version control and numerical methods for engineering computation.",
        "topics": ["Python", "Computational thinking", "Git", "Numerical methods"],
        "courseSlugs": [
            "python-course",
            "computational-thinking-basics",
            "git-basics",
            "math-numerical",
        ],
    },
    {
        "slug": "civ-intro",
        "title": "Introduction to Civil Engineering",
        "category": "Civil Engineering",
        "level": "Beginner",
        "duration": "8 hr",
        "icon": "\U0001f3d7",
        "description": "The profession, the lifecycle of a built asset, regulation, ethics and digital practice.",
        "topics": ["Profession", "Asset lifecycle", "Ethics", "Digital transformation"],
        "courseSlugs": ["intro-civil-engineering"],
    },
    {
        "slug": "civ-graphics-bim",
        "title": "Graphics, CAD and BIM",
        "category": "Civil Engineering",
        "level": "Intermediate",
        "duration": "20 hr",
        "icon": "\U0001f4d0",
        "description": "Technical drawing, CAD and Building Information Modeling for civil projects.",
        "topics": ["Technical drawing", "CAD", "BIM", "IFC"],
        "courseSlugs": ["engineering-graphics-cad-basics", "bim-for-civil"],
    },
    {
        "slug": "civ-mechanics",
        "title": "Engineering Mechanics",
        "category": "Civil Engineering",
        "level": "Intermediate",
        "duration": "36 hr",
        "icon": "⚙️",
        "description": "Statics and mechanics of materials: forces, stresses, strains and deformations.",
        "topics": ["Statics", "Mechanics of materials", "Stress and strain"],
        "courseSlugs": [
            "engineering-statics-basics",
            "engineering-statics-intermediate",
            "mechanics-of-materials-basics",
            "mechanics-of-materials-intermediate",
        ],
    },
    {
        "slug": "civ-materials",
        "title": "Materials and Concrete Technology",
        "category": "Civil Engineering",
        "level": "Intermediate",
        "duration": "28 hr",
        "icon": "\U0001f9f1",
        "description": "Construction materials and the science and practice of concrete.",
        "topics": ["Materials science", "Construction materials", "Concrete technology"],
        "courseSlugs": [
            "materials-science-basics",
            "construction-materials",
            "concrete-technology",
        ],
    },
    {
        "slug": "civ-geotechnics",
        "title": "Geotechnics",
        "category": "Civil Engineering",
        "level": "Intermediate",
        "duration": "30 hr",
        "icon": "\U0001faa8",
        "description": "Engineering geology, soil mechanics and the design of foundations and retaining works.",
        "topics": ["Engineering geology", "Soil mechanics", "Foundations", "Retaining structures"],
        "courseSlugs": ["engineering-geology", "soil-mechanics", "foundations-retaining"],
    },
    {
        "slug": "civ-structures",
        "title": "Structural Engineering",
        "category": "Civil Engineering",
        "level": "Advanced",
        "duration": "44 hr",
        "icon": "\U0001f309",
        "description": "Structural analysis and the design of reinforced-concrete, steel and timber structures.",
        "topics": ["Structural analysis", "Reinforced concrete", "Steel and timber", "FEA"],
        "courseSlugs": [
            "structural-analysis",
            "reinforced-concrete-design",
            "steel-timber-structures",
            "finite-element-analysis-basics",
        ],
    },
    {
        "slug": "civ-hydraulics",
        "title": "Hydraulics, Water and Sanitation",
        "category": "Civil Engineering",
        "level": "Intermediate",
        "duration": "40 hr",
        "icon": "\U0001f6b0",
        "description": "Fluid mechanics, hydrology, water supply, sanitation, drainage and building systems.",
        "topics": ["Fluid mechanics", "Hydrology", "Sanitation", "Drainage"],
        "courseSlugs": [
            "fluid-mechanics-basics",
            "fluid-mechanics-intermediate",
            "hydrology-water-resources",
            "sanitation-drainage",
            "building-hydraulic-systems",
        ],
    },
    {
        "slug": "civ-transportation",
        "title": "Surveying, Transportation and Infrastructure",
        "category": "Civil Engineering",
        "level": "Intermediate",
        "duration": "24 hr",
        "icon": "\U0001f6e3",
        "description": "Surveying and geoprocessing, highway and pavement design, traffic and mobility.",
        "topics": ["Surveying", "Geoprocessing", "Highways", "Pavement", "Mobility"],
        "courseSlugs": ["surveying-geoprocessing", "highways-pavement-mobility"],
    },
    {
        "slug": "civ-construction",
        "title": "Construction Management and Sustainability",
        "category": "Civil Engineering",
        "level": "Advanced",
        "duration": "24 hr",
        "icon": "\U0001f477",
        "description": "Planning, cost engineering, quality and safety, and sustainable, low-carbon construction.",
        "topics": ["Planning", "Cost engineering", "Safety", "Sustainability"],
        "courseSlugs": ["construction-management-cost", "sustainable-construction"],
    },
    {
        "slug": "civ-digital",
        "title": "Digital and AI in Civil Engineering",
        "category": "Civil Engineering",
        "level": "Advanced",
        "duration": "30 hr",
        "icon": "\U0001f9e0",
        "description": "Digital twins, machine learning, computer vision and generative design for infrastructure.",
        "topics": ["Digital twins", "Machine learning", "Computer vision", "Generative design"],
        "courseSlugs": [
            "digital-twins-ai-construction",
            "ml-for-engineering-basics",
            "generative-design-basics",
            "dataeng-basics",
        ],
    },
)

PATH: dict[str, Any] = {
    "slug": "civil-engineering",
    "title": "Civil Engineering",
    "description": (
        "A full civil-engineering curriculum, from scientific foundations to the "
        "design of structures, geotechnics, water and transportation systems, and "
        "construction management - closing with the digital and AI technologies "
        "(BIM, digital twins, machine learning, computer vision) reshaping the field."
    ),
    "moduleSlugs": [m["slug"] for m in MODULES],
    "estimatedTime": "48-60 weeks",
    "icon": "\U0001f309",
}

MODULE_TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    "civ-foundations": {
        "pt-BR": {
            "title": "Fundamentos Cientificos",
            "description": "A matematica, fisica, quimica e estatistica que todo engenheiro civil usa.",
        },
        "es": {
            "title": "Fundamentos Cientificos",
            "description": "Las matematicas, la fisica, la quimica y la estadistica que todo ingeniero civil usa.",
        },
        "fr": {
            "title": "Fondements Scientifiques",
            "description": "Les mathematiques, la physique, la chimie et les statistiques de base de l'ingenieur civil.",
        },
    },
    "civ-computing": {
        "pt-BR": {
            "title": "Computacao e Dados para Engenheiros",
            "description": "Programacao, controle de versao e metodos numericos para calculo em engenharia.",
        },
        "es": {
            "title": "Computacion y Datos para Ingenieros",
            "description": "Programacion, control de versiones y metodos numericos para el calculo en ingenieria.",
        },
        "fr": {
            "title": "Informatique et Donnees pour Ingenieurs",
            "description": "Programmation, gestion de versions et methodes numeriques pour le calcul en ingenierie.",
        },
    },
    "civ-intro": {
        "pt-BR": {
            "title": "Introducao a Engenharia Civil",
            "description": "A profissao, o ciclo de vida da obra, regulamentacao, etica e pratica digital.",
        },
        "es": {
            "title": "Introduccion a la Ingenieria Civil",
            "description": "La profesion, el ciclo de vida de la obra, la regulacion, la etica y la practica digital.",
        },
        "fr": {
            "title": "Introduction au Genie Civil",
            "description": "La profession, le cycle de vie de l'ouvrage, la reglementation, l'ethique et la pratique numerique.",
        },
    },
    "civ-graphics-bim": {
        "pt-BR": {
            "title": "Desenho, CAD e BIM",
            "description": "Desenho tecnico, CAD e Modelagem da Informacao da Construcao em projetos civis.",
        },
        "es": {
            "title": "Dibujo, CAD y BIM",
            "description": "Dibujo tecnico, CAD y Modelado de Informacion de la Construccion en proyectos civiles.",
        },
        "fr": {
            "title": "Dessin, CAO et BIM",
            "description": "Dessin technique, CAO et modelisation des donnees du batiment pour les projets civils.",
        },
    },
    "civ-mechanics": {
        "pt-BR": {
            "title": "Mecanica das Estruturas",
            "description": "Estatica e resistencia dos materiais: forcas, tensoes, deformacoes.",
        },
        "es": {
            "title": "Mecanica Estructural",
            "description": "Estatica y resistencia de materiales: fuerzas, tensiones y deformaciones.",
        },
        "fr": {
            "title": "Mecanique des Structures",
            "description": "Statique et resistance des materiaux : forces, contraintes et deformations.",
        },
    },
    "civ-materials": {
        "pt-BR": {
            "title": "Materiais e Tecnologia do Concreto",
            "description": "Materiais de construcao e a ciencia e pratica do concreto.",
        },
        "es": {
            "title": "Materiales y Tecnologia del Hormigon",
            "description": "Materiales de construccion y la ciencia y practica del hormigon.",
        },
        "fr": {
            "title": "Materiaux et Technologie du Beton",
            "description": "Materiaux de construction et science et pratique du beton.",
        },
    },
    "civ-geotechnics": {
        "pt-BR": {
            "title": "Geotecnia",
            "description": "Geologia de engenharia, mecanica dos solos e projeto de fundacoes e contencoes.",
        },
        "es": {
            "title": "Geotecnia",
            "description": "Geologia de ingenieria, mecanica de suelos y diseno de cimentaciones y contenciones.",
        },
        "fr": {
            "title": "Geotechnique",
            "description": "Geologie de l'ingenieur, mecanique des sols et conception des fondations et soutenements.",
        },
    },
    "civ-structures": {
        "pt-BR": {
            "title": "Engenharia de Estruturas",
            "description": "Analise estrutural e projeto de estruturas de concreto armado, aco e madeira.",
        },
        "es": {
            "title": "Ingenieria Estructural",
            "description": "Analisis estructural y diseno de estructuras de hormigon armado, acero y madera.",
        },
        "fr": {
            "title": "Ingenierie des Structures",
            "description": "Analyse structurale et conception de structures en beton arme, acier et bois.",
        },
    },
    "civ-hydraulics": {
        "pt-BR": {
            "title": "Hidraulica, Agua e Saneamento",
            "description": "Mecanica dos fluidos, hidrologia, abastecimento, saneamento, drenagem e instalacoes prediais.",
        },
        "es": {
            "title": "Hidraulica, Agua y Saneamiento",
            "description": "Mecanica de fluidos, hidrologia, abastecimiento, saneamiento, drenaje e instalaciones.",
        },
        "fr": {
            "title": "Hydraulique, Eau et Assainissement",
            "description": "Mecanique des fluides, hydrologie, alimentation, assainissement, drainage et installations.",
        },
    },
    "civ-transportation": {
        "pt-BR": {
            "title": "Topografia, Transportes e Infraestrutura",
            "description": "Topografia e geoprocessamento, projeto de estradas e pavimentos, trafego e mobilidade.",
        },
        "es": {
            "title": "Topografia, Transporte e Infraestructura",
            "description": "Topografia y geoprocesamiento, diseno de carreteras y pavimentos, trafico y movilidad.",
        },
        "fr": {
            "title": "Topographie, Transports et Infrastructure",
            "description": "Topographie et geotraitement, conception routiere et de chaussees, trafic et mobilite.",
        },
    },
    "civ-construction": {
        "pt-BR": {
            "title": "Gestao de Obras e Sustentabilidade",
            "description": "Planejamento, engenharia de custos, qualidade e seguranca, e construcao sustentavel de baixo carbono.",
        },
        "es": {
            "title": "Gestion de Obras y Sostenibilidad",
            "description": "Planificacion, ingenieria de costos, calidad y seguridad, y construccion sostenible de bajo carbono.",
        },
        "fr": {
            "title": "Gestion de Chantier et Durabilite",
            "description": "Planification, ingenierie des couts, qualite et securite, et construction durable bas carbone.",
        },
    },
    "civ-digital": {
        "pt-BR": {
            "title": "Digital e IA na Engenharia Civil",
            "description": "Gemeos digitais, aprendizado de maquina, visao computacional e projeto generativo para infraestrutura.",
        },
        "es": {
            "title": "Digital e IA en Ingenieria Civil",
            "description": "Gemelos digitales, aprendizaje automatico, vision por computador y diseno generativo para infraestructura.",
        },
        "fr": {
            "title": "Numerique et IA en Genie Civil",
            "description": "Jumeaux numeriques, apprentissage automatique, vision par ordinateur et conception generative pour l'infrastructure.",
        },
    },
}

PATH_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "Engenharia Civil",
        "description": (
            "Um curriculo completo de engenharia civil, dos fundamentos cientificos ao projeto de "
            "estruturas, geotecnia, sistemas de agua e transportes e gestao de obras - encerrando com "
            "as tecnologias digitais e de IA (BIM, gemeos digitais, aprendizado de maquina, visao "
            "computacional) que estao transformando a area."
        ),
    },
    "es": {
        "title": "Ingenieria Civil",
        "description": (
            "Un curriculo completo de ingenieria civil, desde los fundamentos cientificos hasta el diseno "
            "de estructuras, geotecnia, sistemas de agua y transporte y gestion de obras - cerrando con las "
            "tecnologias digitales y de IA (BIM, gemelos digitales, aprendizaje automatico, vision por "
            "computador) que estan transformando el campo."
        ),
    },
    "fr": {
        "title": "Genie Civil",
        "description": (
            "Un cursus complet de genie civil, des fondements scientifiques a la conception des structures, "
            "la geotechnique, les systemes d'eau et de transport et la gestion de chantier - en terminant par "
            "les technologies numeriques et d'IA (BIM, jumeaux numeriques, apprentissage automatique, vision "
            "par ordinateur) qui transforment le domaine."
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
