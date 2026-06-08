"""Vector Calculus track: Basics -> Intermediate -> Advanced.

Scalar & vector fields, the gradient, divergence and curl, line/surface
integrals, and the great integral theorems (Green, Gauss, Stokes). Lessons are
`text` with LaTeX and interactive ```plot blocks; vector-field plots are
generated on a grid by ``_field_block``. The Advanced track ends with a runnable
Python lab that checks Green's theorem numerically.
"""

# Lesson prose uses typographic characters (×, →, ∇, ∮, ≈, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF002, RUF003
from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


def _field_block(
    title: str,
    comp: Callable[[float, float], tuple[float, float]],
    *,
    n: int = 7,
    lo: float = -2.0,
    hi: float = 2.0,
    scale: float = 0.32,
    color: str = "#2563eb",
    extra: dict[str, Any] | None = None,
) -> str:
    """Build a ```plot block of a 2D vector field: unit-length arrows on an n×n
    grid (direction-only, so the picture stays readable). ``extra`` merges in
    overlays like a parametric path or an animated particle."""
    vectors: list[dict[str, Any]] = []
    for i in range(n):
        for j in range(n):
            x = lo + (hi - lo) * i / (n - 1)
            y = lo + (hi - lo) * j / (n - 1)
            fx, fy = comp(x, y)
            mag = (fx * fx + fy * fy) ** 0.5
            if mag < 1e-9:
                continue
            vectors.append(
                {
                    "from": [round(x, 3), round(y, 3)],
                    "x": round(x + scale * fx / mag, 3),
                    "y": round(y + scale * fy / mag, 3),
                    "color": color,
                }
            )
    spec: dict[str, Any] = {
        "title": title,
        "equal": True,
        "grid": True,
        "xRange": [lo - 0.4, hi + 0.4],
        "yRange": [lo - 0.4, hi + 0.4],
        "vectors": vectors,
    }
    if extra:
        for key, value in extra.items():
            spec[key] = value
    return "```plot\n" + json.dumps(spec, ensure_ascii=False) + "\n```"


# Reusable field pictures ----------------------------------------------------
_SWIRL = _field_block("Vector field F = (−y, x): a swirl (rotation)", lambda x, y: (-y, x))
_SOURCE = _field_block(
    "Source field F = (x, y): arrows point outward (divergence > 0)",
    lambda x, y: (x, y),
    color="#dc2626",
)
_SINK = _field_block(
    "Sink field F = (−x, −y): arrows point inward (divergence < 0)",
    lambda x, y: (-x, -y),
    color="#2563eb",
)
_LEVELS = _field_block(
    "Gradient ∇f (arrows) is perpendicular to the level curves (circles)",
    lambda x, y: (2 * x, 2 * y),
    color="#16a34a",
    extra={
        "parametric": [
            {
                "x": "0.7*cos(s)",
                "y": "0.7*sin(s)",
                "param": "s",
                "range": [0, 6.283],
                "color": "#2563eb",
                "label": "level curves f = const",
            },
            {
                "x": "1.3*cos(s)",
                "y": "1.3*sin(s)",
                "param": "s",
                "range": [0, 6.283],
                "color": "#2563eb",
            },
            {
                "x": "1.9*cos(s)",
                "y": "1.9*sin(s)",
                "param": "s",
                "range": [0, 6.283],
                "color": "#2563eb",
            },
        ]
    },
)
_WORKPATH = _field_block(
    "Work along a path through a field: ∮ F · dr",
    lambda x, y: (-y, x),
    color="#94a3b8",
    extra={
        "animate": {"param": "t", "range": [0, 6.283], "label": "position along the path"},
        "parametric": [
            {
                "x": "1.4*cos(s)",
                "y": "1.4*sin(s)",
                "param": "s",
                "range": [0, 6.283],
                "color": "#2563eb",
                "label": "path C",
            }
        ],
        "points": [
            {
                "xExpr": "1.4*cos(t)",
                "yExpr": "1.4*sin(t)",
                "color": "#dc2626",
                "size": 7,
                "label": "particle",
            }
        ],
    },
)
_GRADFIELD = _field_block(
    "A conservative field F = ∇φ = (2x, 2y): no swirl, curl = 0",
    lambda x, y: (2 * x, 2 * y),
    color="#16a34a",
)
_GREEN = _field_block(
    "Green: circulation around the loop = total curl enclosed",
    lambda x, y: (-y, x),
    color="#94a3b8",
    extra={
        "parametric": [
            {
                "x": "1.4*cos(s)",
                "y": "1.4*sin(s)",
                "param": "s",
                "range": [0, 6.283],
                "color": "#dc2626",
                "label": "loop C",
            }
        ]
    },
)
_GAUSS = _field_block(
    "Divergence theorem: net flux out of the circle = total divergence inside",
    lambda x, y: (x, y),
    color="#94a3b8",
    extra={
        "parametric": [
            {
                "x": "1.4*cos(s)",
                "y": "1.4*sin(s)",
                "param": "s",
                "range": [0, 6.283],
                "color": "#dc2626",
                "label": "closed boundary",
            }
        ]
    },
)


# ── Vector Calculus — Basics ─────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="vectorcalc-basics",
    title="Vector Calculus — Basics",
    description=(
        "Fields and the gradient: scalar vs vector fields, partial derivatives, "
        "the gradient (steepest ascent, perpendicular to level curves), and "
        "directional derivatives. The language of heat, gravity, fluids and "
        "machine-learning loss landscapes, with interactive field and surface plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Scalar & vector fields",
            "11 min",
            "# Scalar & vector fields\n\n"
            "A **field** assigns a value to every point in space.\n\n"
            "- A **scalar field** gives one number per point — temperature in a room, "
            "altitude on a map, pressure, a neural-net's loss. Picture it as a surface "
            "(height = value):\n\n"
            "```plot\n"
            '{"mode": "3d", "title": "A scalar field as a hill: f(x,y) = 3·e^(−(x²+y²)/4)", '
            '"xRange": [-3, 3], "yRange": [-3, 3], "zRange": [0, 3.2], "azimuth": 40, '
            '"elevation": 30, "zLabel": "f", "surfaces": [{"expr": "3*exp(-(x^2+y^2)/4)", '
            '"color": "#2563eb"}]}\n'
            "```\n\n"
            "- A **vector field** gives a whole arrow (magnitude + direction) per point "
            "— wind, water flow, a force, an electric field. Here is the swirl "
            "$\\vec F = (-y,\\,x)$:\n\n"
            + _SWIRL
            + "\n\nVector calculus is the toolkit for measuring how these fields *change* "
            "and *flow*. We start with the gradient.\n\n**Next:** partial derivatives & the gradient.",
        ),
        _t(
            "Partial derivatives & the gradient",
            "12 min",
            "# Partial derivatives & the gradient\n\n"
            "For a function of several variables, a **partial derivative** "
            "$\\partial f/\\partial x$ is the slope if you change *only* $x$ and hold the "
            "rest fixed. Collect all the partials into one vector — the **gradient**:\n\n"
            "$$\\nabla f = \\left(\\frac{\\partial f}{\\partial x}, \\frac{\\partial f}{\\partial y}\\right).$$\n\n"
            "Two facts make the gradient the star of the whole subject:\n\n"
            "1. It **points in the direction of steepest increase** (straight uphill).\n"
            "2. Its **length is the steepness** there.\n\n"
            "On the bowl $f(x,y)=x^2+y^2$, the gradient is $(2x, 2y)$ — pointing outward, "
            "away from the minimum, longer as the wall gets steeper:\n\n"
            "```plot\n"
            '{"mode": "3d", "title": "f(x,y) = x² + y² (gradient points uphill)", '
            '"xRange": [-3, 3], "yRange": [-3, 3], "zRange": [0, 18], "azimuth": 35, '
            '"elevation": 28, "zLabel": "f", "surfaces": [{"expr": "x^2 + y^2", "color": "#2563eb"}]}\n'
            "```\n\n"
            "Seen from above, those gradient arrows look like this:\n\n"
            + _SOURCE
            + "\n\nThe gradient is exactly what optimisation follows (downhill = $-\\nabla f$) "
            "and what heat flows along — the bridge to the [[backpropagation]] you met in the "
            "Optimization course.\n\n**Next:** directional derivatives & level curves.",
        ),
        _t(
            "Directional derivatives & level curves",
            "11 min",
            "# Directional derivatives & level curves\n\n"
            "The **directional derivative** is the slope as you walk in a chosen unit "
            "direction $\\hat u$ — and it's just a dot product with the gradient:\n\n"
            "$$D_{\\hat u} f = \\nabla f \\cdot \\hat u = |\\nabla f|\\cos\\theta.$$\n\n"
            "It's largest when you walk *along* the gradient ($\\theta = 0$) and **zero** "
            "when you walk perpendicular to it. Walking perpendicular keeps $f$ constant — "
            "so you're tracing a **level curve** (a contour line on a map).\n\n"
            "That gives the key geometric picture: **the gradient is always perpendicular "
            "to the level curves.** For $f = x^2+y^2$ the level curves are circles and the "
            "gradient points straight out across them:\n\n"
            + _LEVELS
            + "\n\nContour maps (hiking, weather isobars, magnetic field lines) all use "
            "this: closely-spaced contours mean a steep gradient.\n\n"
            "**Next:** using the gradient to climb or descend.",
        ),
        _t(
            "Steepest ascent & descent",
            "10 min",
            "# Steepest ascent & descent\n\n"
            "Since $\\nabla f$ points uphill, to **maximise** $f$ you step along $+\\nabla f$; "
            "to **minimise** (a loss, an energy, an error) you step along $-\\nabla f$. That "
            "is **gradient descent**, the workhorse of optimisation and machine learning.\n\n"
            "$$\\vec x_{n+1} = \\vec x_n - \\eta\\,\\nabla f(\\vec x_n).$$\n\n"
            "Press **Play**: the point rolls down the slope, always heading in the locally "
            "steepest-downhill direction, and settles at the minimum:\n\n"
            "```plot\n"
            '{"title": "Steepest descent: follow −∇f to the minimum", "xLabel": "x", '
            '"yLabel": "f(x)", "xRange": [-3, 3], "yRange": [0, 9], "animate": {"param": "t", '
            '"range": [0, 3], "label": "steps"}, "functions": [{"expr": "x^2", "label": "f", '
            '"color": "#2563eb"}], "points": [{"xExpr": "2.5*exp(-2*t)", "yExpr": '
            '"(2.5*exp(-2*t))^2", "color": "#dc2626", "size": 7, "trail": true}]}\n'
            "```\n\n"
            "The step size $\\eta$ matters: too small is slow, too large overshoots — the "
            "same trade-off you saw in Numerical Methods.\n\n"
            "**Next:** test what you've learned.",
        ),
        _quiz(),
    ),
)

# ── Vector Calculus — Intermediate ───────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="vectorcalc-intermediate",
    title="Vector Calculus — Intermediate",
    description=(
        "How fields spread and spin: divergence (sources & sinks), curl "
        "(rotation), line integrals and work, and conservative fields with a "
        "potential. The vocabulary of fluid dynamics, electromagnetism and "
        "thermodynamics, with interactive field plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Divergence: sources & sinks",
            "12 min",
            "# Divergence: sources & sinks\n\n"
            "**Divergence** measures how much a field *spreads out* from a point — the net "
            "outflow per unit area:\n\n"
            "$$\\nabla \\cdot \\vec F = \\frac{\\partial F_x}{\\partial x} + \\frac{\\partial F_y}{\\partial y}.$$\n\n"
            "- **Positive** divergence = a **source** (field flows outward, like water from "
            "a sprinkler). The field $\\vec F=(x,y)$ has $\\nabla\\cdot\\vec F = 2$:\n\n"
            + _SOURCE
            + "\n\n- **Negative** divergence = a **sink** (field flows inward, like a drain). "
            "$\\vec F=(-x,-y)$ has divergence $-2$:\n\n"
            + _SINK
            + "\n\n- **Zero** divergence = **incompressible** (whatever flows in flows out) — "
            "the swirl $(-y,x)$ from the last course has $\\nabla\\cdot\\vec F = 0$.\n\n"
            "Divergence is the heart of the **continuity equation** (conservation of mass/"
            "charge), **Gauss's law** in electromagnetism, and incompressible fluid flow.\n\n"
            "**Next:** the rotational counterpart — curl.",
        ),
        _t(
            "Curl: rotation & circulation",
            "12 min",
            "# Curl: rotation & circulation\n\n"
            "**Curl** measures how much a field *rotates* around a point — drop a tiny "
            "paddlewheel in the flow; curl is how fast it spins. In 2D it's a single number:\n\n"
            "$$\\nabla \\times \\vec F = \\frac{\\partial F_y}{\\partial x} - \\frac{\\partial F_x}{\\partial y}.$$\n\n"
            "The swirl $\\vec F=(-y,x)$ rotates everywhere — its curl is $2$ (a paddlewheel "
            "anywhere spins counter-clockwise):\n\n"
            + _SWIRL
            + "\n\nA purely radial field like $(x,y)$ has **zero curl** — it spreads but never "
            "spins. A field can have divergence, curl, both, or neither.\n\n"
            "Curl is **vorticity** in fluids (whirlpools, tornadoes, aerofoil lift), and it "
            "is exactly what a changing magnetic field induces (Faraday's law).\n\n"
            "**Next:** adding a field up along a path — line integrals.",
        ),
        _t(
            "Line integrals & work",
            "12 min",
            "# Line integrals & work\n\n"
            "A **line integral** adds up a field *along a path* $C$:\n\n"
            "$$\\int_C \\vec F \\cdot d\\vec r.$$\n\n"
            "When $\\vec F$ is a force, this is the **work** done moving along the path; when "
            "you go around a closed loop it's the **circulation** $\\oint_C \\vec F\\cdot d\\vec r$. "
            "Only the part of $\\vec F$ *along* the motion counts (the dot product).\n\n"
            "Press **Play** to carry a particle around a loop through the swirl field and "
            "accumulate work — because the field pushes along the direction of travel the "
            "whole way, the circulation is positive:\n\n"
            + _WORKPATH
            + "\n\nLine integrals compute work in mechanics, voltage along a wire (EMF), and "
            "circulation in aerodynamics.\n\n"
            "**Next:** the special fields where the path doesn't matter.",
        ),
        _t(
            "Conservative fields & potential",
            "12 min",
            "# Conservative fields & potential\n\n"
            "A field is **conservative** if the work between two points is **independent of "
            "the path** — equivalently, the circulation around *every* closed loop is zero. "
            "Three statements that all mean the same thing:\n\n"
            "$$\\vec F = \\nabla\\varphi \\;\\;\\Longleftrightarrow\\;\\; \\nabla\\times\\vec F = 0 "
            "\\;\\;\\Longleftrightarrow\\;\\; \\oint_C \\vec F\\cdot d\\vec r = 0.$$\n\n"
            "Such a field is the gradient of a **potential** $\\varphi$. Gravity and "
            "electrostatics are conservative: the potential is potential energy / voltage, "
            "and 'energy is conserved' is exactly path-independence. The gradient field "
            "$\\vec F = (2x, 2y) = \\nabla(x^2+y^2)$ has no swirl at all:\n\n"
            + _GRADFIELD
            + "\n\nThis is why you can define **potential energy** at all (Physics track), why "
            "voltage is well-defined, and it connects straight back to the gradient lessons: "
            "a conservative field *is* a gradient.\n\n"
            "**Next:** test what you've learned.",
        ),
        _quiz(),
    ),
)

# ── Vector Calculus — Advanced ───────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="vectorcalc-advanced",
    title="Vector Calculus — Advanced",
    description=(
        "The great integral theorems that unify the subject: multiple & surface "
        "integrals and flux, Green's theorem, the Divergence (Gauss) theorem, and "
        "Stokes' theorem — the mathematics behind Maxwell's equations. Includes a "
        "runnable lab that checks a theorem numerically."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Multiple integrals, surfaces & flux",
            "12 min",
            "# Multiple integrals, surfaces & flux\n\n"
            "A **double integral** $\\iint_R f\\,dA$ adds a scalar field over a 2D region "
            "(volume under a surface, total mass, total charge); a **triple integral** does "
            "the same over a 3D solid.\n\n"
            "**Flux** measures how much of a vector field passes *through* a surface — the "
            "flow rate across it:\n\n"
            "$$\\Phi = \\iint_S \\vec F \\cdot \\hat n\\, dA,$$\n\n"
            "where $\\hat n$ is the surface's unit normal. Only the component of $\\vec F$ "
            "*through* the surface counts. Think of water through a net, heat through a wall, "
            "or electric field through a closed shell. Here is a surface over a region — the "
            "volume beneath it is a double integral:\n\n"
            "```plot\n"
            '{"mode": "3d", "title": "Volume under a surface = ∬ f dA", "xRange": [-2, 2], '
            '"yRange": [-2, 2], "zRange": [0, 4], "azimuth": 40, "elevation": 30, "zLabel": "f", '
            '"surfaces": [{"expr": "1 + cos(x)*cos(y)", "color": "#2563eb"}]}\n'
            "```\n\n"
            "The next three theorems each say: an integral over a region equals an integral "
            "over its **boundary**.\n\n**Next:** Green's theorem.",
        ),
        _t(
            "Green's theorem",
            "12 min",
            "# Green's theorem\n\n"
            "**Green's theorem** links a loop integral to what's happening *inside* the "
            "loop. The circulation of $\\vec F$ around a closed curve $C$ equals the total "
            "curl over the region $R$ it encloses:\n\n"
            "$$\\oint_C \\vec F \\cdot d\\vec r = \\iint_R (\\nabla \\times \\vec F)\\, dA.$$\n\n"
            "Spin around the boundary once; that equals all the little swirls inside added "
            "up. For the swirl field (curl $=2$), the circulation around a loop is just "
            "$2\\times$ the enclosed area:\n\n"
            + _GREEN
            + "\n\nA neat consequence: you can compute an **area** purely from a boundary "
            "walk — exactly how a *planimeter* measures land area by tracing its outline. "
            "The code lab checks this theorem numerically.\n\n"
            "**Next:** its 3D cousin for flux — the Divergence theorem.",
        ),
        _t(
            "The Divergence (Gauss) theorem",
            "12 min",
            "# The Divergence (Gauss) theorem\n\n"
            "The **Divergence theorem** is the 3D flux version: the net flux of $\\vec F$ "
            "out through a closed surface $S$ equals the total divergence inside the volume "
            "$V$ it encloses:\n\n"
            "$$\\oiint_S \\vec F \\cdot \\hat n\\, dA = \\iiint_V (\\nabla \\cdot \\vec F)\\, dV.$$\n\n"
            "Sources inside push flux out; sinks pull it in. In 2D the analogue is flux "
            "across a closed boundary equals the divergence inside — for the source field "
            "$(x,y)$ every arrow crosses outward:\n\n"
            + _GAUSS
            + "\n\nThis **is** Gauss's law in electromagnetism (flux of $\\vec E$ out of a "
            "surface = enclosed charge / $\\varepsilon_0$) and the conservation/continuity "
            "laws of fluid and heat flow.\n\n"
            "**Next:** Stokes' theorem and Maxwell.",
        ),
        _t(
            "Stokes' theorem & Maxwell",
            "12 min",
            "# Stokes' theorem & Maxwell\n\n"
            "**Stokes' theorem** is Green's theorem lifted into 3D: the circulation of "
            "$\\vec F$ around the boundary curve of a surface equals the flux of its curl "
            "through that surface:\n\n"
            "$$\\oint_{\\partial S} \\vec F \\cdot d\\vec r = \\iint_S (\\nabla \\times \\vec F) \\cdot \\hat n\\, dA.$$\n\n"
            "All three theorems are one idea — *what happens on the boundary is the sum of "
            "what happens inside*:\n\n"
            "```mermaid\n"
            "flowchart TB\n"
            '  G["Green (2D circulation)"] --> S["Stokes (3D circulation = flux of curl)"]\n'
            '  D["Divergence / Gauss (flux = enclosed divergence)"]\n'
            '  S --> M["Maxwell equations"]\n'
            "  D --> M\n"
            "```\n\n"
            "Their payoff is **electromagnetism**: Gauss's law (divergence theorem), "
            "Faraday's law and Ampère's law (Stokes' theorem) are Maxwell's four equations — "
            "the same equations that predict light. Vector calculus is literally the language "
            "Maxwell wrote physics in.\n\n"
            "**Next:** verify a theorem in code.",
        ),
        _code(
            "Lab: check Green's theorem numerically",
            "12 min",
            "# Vector calculus, numerically — divergence and a check of Green's theorem.\n"
            "# No libraries.\n\n"
            "# Green's theorem on the unit square for the swirl field F = (-y, x).\n"
            "# curl F = dFy/dx - dFx/dy = 1 - (-1) = 2, and the area is 1, so the loop\n"
            "# integral around the boundary should equal curl * area = 2.\n"
            "N = 2000\n"
            "step = 1.0 / N\n"
            "circ = 0.0\n"
            "# bottom edge y=0, x:0->1, dr=(dx,0), F=(-0,x) -> F.dr = 0\n"
            "# right edge  x=1, y:0->1, dr=(0,dy), F=(-y,1) -> F.dr = 1*dy\n"
            "for i in range(N):\n"
            "    circ = circ + 1.0 * step\n"
            "# top edge    y=1, x:1->0, dr=(-dx,0), F=(-1,x) -> F.dr = (-1)*(-dx) = dx\n"
            "for i in range(N):\n"
            "    circ = circ + 1.0 * step\n"
            "# left edge   x=0, y:1->0, F=(-y,0) -> F.dr = 0\n"
            'print("loop integral  of F.dr =", round(circ, 4), " (Green: curl*area = 2)")\n\n'
            "# Divergence of the source field G = (x, y) at (1,1) by central differences.\n"
            "# Gx = x so dGx/dx = 1;  Gy = y so dGy/dy = 1;  divergence = 2.\n"
            "h = 0.0001\n"
            "x = 1.0\n"
            "y = 1.0\n"
            "dGxdx = ((x + h) - (x - h)) / (2 * h)\n"
            "dGydy = ((y + h) - (y - h)) / (2 * h)\n"
            'print("divergence of (x,y) =", round(dGxdx + dGydy, 4), " (expect 2)")\n\n'
            "# Try it:\n"
            "#   - Raise N for a finer loop integral (it converges to exactly 2).\n"
            "#   - Change the field components above and re-derive curl/divergence by hand.\n",
        ),
        _quiz(),
    ),
)


VECTORCALC_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)

__all__ = ["VECTORCALC_COURSES"]
