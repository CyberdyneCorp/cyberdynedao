"""Robotics track (engineering level): Basics -> Intermediate -> Advanced.

Spatial transforms, forward & inverse kinematics, the Jacobian and
singularities, manipulator dynamics, trajectory generation and control. Lessons
are `text` with LaTeX, side-by-side MATLAB and Python (NumPy) code, and
interactive ```plot blocks — including a fully driveable 2-link arm and an
inverse-kinematics animation built by ``_arm_plot``. Runnable NumPy labs (the
interpreter has NumPy) implement FK, analytic + numerical IK, the Jacobian and a
trajectory.
"""

# Lesson prose uses typographic characters (×, →, θ, τ, ≈, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

import json
from typing import Any

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


L1, L2 = 1.2, 1.0  # link lengths used throughout the interactive arm plots


def _arm_plot(
    title: str,
    th1: str,
    th2: str,
    *,
    controls: list[dict[str, Any]] | None = None,
    animate: dict[str, Any] | None = None,
    xr: tuple[float, float] = (-0.6, 2.5),
    yr: tuple[float, float] = (-1.6, 2.0),
    l1: float = L1,
    l2: float = L2,
    end_trail: bool = False,
    parametric_extra: list[dict[str, Any]] | None = None,
    points_extra: list[dict[str, Any]] | None = None,
    vectors_extra: list[dict[str, Any]] | None = None,
) -> str:
    """Build a ```plot of a 2-link planar arm whose joint angles are the
    expression strings ``th1``/``th2`` (in terms of slider controls or the
    animation param). Links are drawn as parametric segments, joints/end-effector
    as points."""
    elbx = f"{l1}*cos({th1})"
    elby = f"{l1}*sin({th1})"
    d2x = f"{l2}*cos(({th1})+({th2}))"
    d2y = f"{l2}*sin(({th1})+({th2}))"
    endx = f"({elbx})+({d2x})"
    endy = f"({elby})+({d2y})"
    parametric: list[dict[str, Any]] = [
        {
            "x": f"u*({elbx})",
            "y": f"u*({elby})",
            "param": "u",
            "range": [0, 1],
            "color": "#334155",
            "label": "link 1",
        },
        {
            "x": f"({elbx})+u*({d2x})",
            "y": f"({elby})+u*({d2y})",
            "param": "u",
            "range": [0, 1],
            "color": "#0891b2",
            "label": "link 2",
        },
    ]
    if parametric_extra:
        parametric += parametric_extra
    end_point: dict[str, Any] = {
        "xExpr": endx,
        "yExpr": endy,
        "color": "#dc2626",
        "size": 8,
        "label": "end-effector",
    }
    if end_trail:
        end_point["trail"] = True
    points: list[dict[str, Any]] = [
        {"x": 0, "y": 0, "color": "#111827", "size": 6, "label": "base"},
        {"xExpr": elbx, "yExpr": elby, "color": "#f59e0b", "size": 7, "label": "joint 2"},
        end_point,
    ]
    if points_extra:
        points += points_extra
    spec: dict[str, Any] = {
        "title": title,
        "equal": True,
        "grid": True,
        "xRange": list(xr),
        "yRange": list(yr),
        "parametric": parametric,
        "points": points,
    }
    if vectors_extra:
        spec["vectors"] = vectors_extra
    if controls:
        spec["controls"] = controls
    if animate:
        spec["animate"] = animate
    return "```plot\n" + json.dumps(spec, ensure_ascii=False) + "\n```"


# Slider-driven arm (joints j1, j2 in degrees) and reusable FK/Jacobian strings.
_J1 = [{"name": "j1", "range": [-180, 180], "value": 35, "label": "joint 1  θ₁ (°)"}]
_J2 = [{"name": "j2", "range": [-180, 180], "value": 45, "label": "joint 2  θ₂ (°)"}]
_JOINTS = _J1 + _J2
_T1, _T2 = "rad(j1)", "rad(j2)"
_ENDX = f"({L1}*cos({_T1}))+{L2}*cos(({_T1})+({_T2}))"
_ENDY = f"({L1}*sin({_T1}))+{L2}*sin(({_T1})+({_T2}))"
_J11 = f"(-{L1}*sin({_T1})-{L2}*sin(({_T1})+({_T2})))"
_J12 = f"(-{L2}*sin(({_T1})+({_T2})))"
_J21 = f"({L1}*cos({_T1})+{L2}*cos(({_T1})+({_T2})))"
_J22 = f"({L2}*cos(({_T1})+({_T2})))"

_FK_ARM = _arm_plot("Drive a 2-link arm — forward kinematics", _T1, _T2, controls=_JOINTS)

# Workspace sweep: both joints driven by the animation param (press Play).
_WORKSPACE = _arm_plot(
    "The arm sweeps its workspace (press Play)",
    "2*t",
    "3*t",
    animate={"param": "t", "range": [0, 6.283], "label": "sweep"},
    end_trail=True,
    xr=(-2.6, 2.6),
    yr=(-2.6, 2.6),
    parametric_extra=[
        {
            "x": "2.2*cos(s)",
            "y": "2.2*sin(s)",
            "param": "s",
            "range": [0, 6.283],
            "color": "#cbd5e1",
            "label": "outer reach r = l₁+l₂",
        },
        {
            "x": "0.2*cos(s)",
            "y": "0.2*sin(s)",
            "param": "s",
            "range": [0, 6.283],
            "color": "#cbd5e1",
            "label": "inner limit |l₁−l₂|",
        },
    ],
)

# Inverse-kinematics animation: a moving target, joints solved analytically.
_TX, _TY = "(1.3+0.4*cos(t))", "(0.7+0.5*sin(t))"
_C2 = f"((({_TX})^2+({_TY})^2-{L1**2}-{L2 * L2})/(2*{L1}*{L2}))"
_IK_TH2 = f"acos({_C2})"
_IK_TH1 = f"(atan2({_TY},{_TX})-atan2({L2}*sin({_IK_TH2}),{L1}+{L2}*cos({_IK_TH2})))"
_IK_ARM = _arm_plot(
    "Inverse kinematics — the arm tracks a moving target",
    _IK_TH1,
    _IK_TH2,
    animate={"param": "t", "range": [0, 6.283], "label": "target position"},
    end_trail=True,
    xr=(-0.4, 2.4),
    yr=(-0.6, 2.0),
    points_extra=[
        {"xExpr": _TX, "yExpr": _TY, "color": "#16a34a", "size": 6, "label": "target"},
    ],
)

# Velocity: the tip velocity vector when joint 1 turns (first Jacobian column).
_VEL_ARM = _arm_plot(
    "The Jacobian: how joint speed becomes tip velocity",
    _T1,
    _T2,
    controls=_JOINTS,
    vectors_extra=[
        {
            "fromExpr": [_ENDX, _ENDY],
            "xExpr": f"({_ENDX})+0.5*{_J11}",
            "yExpr": f"({_ENDY})+0.5*{_J21}",
            "color": "#9333ea",
            "label": "tip velocity (θ₁̇ = 1)",
        }
    ],
)

# Manipulability ellipse: J applied to a unit circle of joint rates, at the tip.
_MANIP_ARM = _arm_plot(
    "Manipulability ellipse — fat = dexterous, flat = near a singularity",
    _T1,
    _T2,
    controls=_JOINTS,
    parametric_extra=[
        {
            "x": f"({_ENDX})+0.45*({_J11}*cos(s)+{_J12}*sin(s))",
            "y": f"({_ENDY})+0.45*({_J21}*cos(s)+{_J22}*sin(s))",
            "param": "s",
            "range": [0, 6.283],
            "color": "#9333ea",
            "label": "velocity ellipse",
        }
    ],
)


# ── Robotics — Basics ────────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="robotics-basics",
    title="Robotics — Basics",
    description=(
        "Build the foundation of robot manipulators: links, joints and degrees "
        "of freedom; rotations and rigid-body transforms; forward kinematics of "
        "a planar arm; and the reachable workspace. Interactive driveable arm, "
        "with MATLAB and Python (NumPy) code."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Robots, joints & degrees of freedom",
            "11 min",
            "# Robots, joints & degrees of freedom\n\n"
            "A robot manipulator is a chain of rigid **links** connected by **joints**. "
            "Two joint types do almost everything:\n\n"
            "- **Revolute** (R) — rotates, one angle $\\theta$ (an elbow, a shoulder).\n"
            "- **Prismatic** (P) — slides, one length $d$ (a linear actuator).\n\n"
            "Each joint adds one **degree of freedom (DOF)**. The list of all joint values "
            "is the **configuration** $\\mathbf q = (\\theta_1, \\theta_2, \\dots)$ — a point "
            "in *configuration space*. A 6-DOF industrial arm needs 6 numbers to fully fix "
            "its pose (3 to position the hand, 3 to orient it).\n\n"
            "Here is a single revolute joint — press **Play** to sweep the link through its "
            "rotation:\n\n" + "```plot\n"
            '{"title": "A revolute joint: one link sweeping", "equal": true, "grid": true, '
            '"xRange": [-1.8, 1.8], "yRange": [-1.8, 1.8], "animate": {"param": "t", "range": '
            '[0, 6.283], "label": "joint angle θ"}, "parametric": [{"x": "u*1.5*cos(t)", "y": '
            '"u*1.5*sin(t)", "param": "u", "range": [0, 1], "color": "#0891b2", "label": "link"}], '
            '"points": [{"x": 0, "y": 0, "color": "#111827", "size": 6, "label": "joint"}, '
            '{"xExpr": "1.5*cos(t)", "yExpr": "1.5*sin(t)", "color": "#dc2626", "size": 8, '
            '"label": "tip", "trail": true}]}\n'
            "```\n\n"
            "Chain a few of these and you get an arm whose hand can be commanded anywhere in "
            "its reach — the subject of this course.\n\n"
            "**Next:** the math of rotation and rigid transforms.",
        ),
        _t(
            "Rotations & rigid-body transforms",
            "13 min",
            "# Rotations & rigid-body transforms\n\n"
            "Every link carries its own coordinate **frame**. Relating frames needs "
            "**rotation** and **translation**.\n\n"
            "A 2D **rotation matrix** turns one frame's axes into another's:\n\n"
            "$$R(\\theta) = \\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ "
            "\\sin\\theta & \\cos\\theta \\end{bmatrix}.$$\n\n"
            "Press **Play** to watch a frame's axes rotate (the columns of $R$):\n\n" + "```plot\n"
            '{"title": "Rotation matrix R(θ) turns a frame", "equal": true, "xRange": [-1.6, 1.6], '
            '"yRange": [-1.6, 1.6], "animate": {"param": "t", "range": [0, 6.283], "label": "θ"}, '
            '"vectors": [{"xExpr": "1.2*cos(t)", "yExpr": "1.2*sin(t)", "from": [0, 0], "label": '
            '"R·x̂", "color": "#dc2626"}, {"xExpr": "-1.2*sin(t)", "yExpr": "1.2*cos(t)", "from": '
            '[0, 0], "label": "R·ŷ", "color": "#16a34a"}]}\n'
            "```\n\n"
            "To carry **both** rotation and translation in one object we use a **homogeneous "
            "transform** $T \\in SE(2)$ (or $SE(3)$ in 3D):\n\n"
            "$$T = \\begin{bmatrix} R & \\vec p \\\\ 0 & 1 \\end{bmatrix},$$\n\n"
            "so chaining frames is just **matrix multiplication** $T_0^2 = T_0^1 T_1^2$. In 3D "
            "the rotation is $R \\in SO(3)$ (often stored as a **quaternion** to avoid gimbal "
            "lock).\n\n"
            "**MATLAB**\n"
            "```matlab\n"
            "R = [cos(th) -sin(th); sin(th) cos(th)];\n"
            "T = [R, [px; py]; 0 0 1];     % homogeneous transform\n"
            "p_world = T * [p_local; 1];   % transform a point\n"
            "```\n\n"
            "**Python (NumPy)**\n"
            "```python\n"
            "import numpy as np\n"
            "R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])\n"
            "T = np.block([[R, [[px], [py]]], [0, 0, 1]])\n"
            "p_world = T @ np.append(p_local, 1)\n"
            "```\n\n"
            "**Next:** chaining transforms to locate the hand — forward kinematics.",
        ),
        _t(
            "Forward kinematics: where is the hand?",
            "13 min",
            "# Forward kinematics: where is the hand?\n\n"
            "**Forward kinematics (FK)** answers: given the joint angles, where is the "
            "end-effector? You chain the per-link transforms and read off the tip. For a "
            "planar **2-link arm** with lengths $l_1, l_2$ it's pure trigonometry:\n\n"
            "$$x = l_1\\cos\\theta_1 + l_2\\cos(\\theta_1+\\theta_2), \\qquad "
            "y = l_1\\sin\\theta_1 + l_2\\sin(\\theta_1+\\theta_2).$$\n\n"
            "**Drive the joints** and watch the hand move — FK is always a unique, "
            "well-defined answer:\n\n"
            + _FK_ARM
            + "\n\nFor a general arm we compose transforms instead of writing trig by hand:\n\n"
            "**MATLAB**\n"
            "```matlab\n"
            "l1 = 1.2; l2 = 1.0;\n"
            "x = l1*cos(t1) + l2*cos(t1 + t2);\n"
            "y = l1*sin(t1) + l2*sin(t1 + t2);\n"
            "```\n\n"
            "**Python (NumPy)**\n"
            "```python\n"
            "import numpy as np\n"
            "l1, l2 = 1.2, 1.0\n"
            "elbow = np.array([l1*np.cos(t1), l1*np.sin(t1)])\n"
            "end   = elbow + np.array([l2*np.cos(t1+t2), l2*np.sin(t1+t2)])\n"
            "```\n\n"
            "The code lab runs this for several configurations.\n\n"
            "**Next:** the set of all reachable points — the workspace.",
        ),
        _t(
            "The workspace & joint limits",
            "10 min",
            "# The workspace & joint limits\n\n"
            "The **workspace** is every point the end-effector can reach. For the 2-link arm "
            "(no joint limits) it's an **annulus**: an outer radius $l_1+l_2$ (arm stretched "
            "straight) and an inner radius $|l_1-l_2|$ (folded back). Press **Play** to sweep "
            "both joints and trace it:\n\n"
            + _WORKSPACE
            + "\n\nReal joints have **limits** (they can't spin forever), which carve the "
            "workspace down further, and the arm must avoid **self-collision** and obstacles. "
            "Designing a robot cell is largely about making sure every task point lies "
            "comfortably inside this reachable region — away from the boundary, where the arm "
            "loses dexterity (the singularities of a later lesson).\n\n"
            "**Next:** test what you've learned.",
        ),
        _code(
            "Lab: forward kinematics in NumPy",
            "11 min",
            "# Forward kinematics of a 2-link planar arm (the interpreter has NumPy).\n"
            "# MATLAB equivalent is in the lesson; here we run the Python version.\n"
            "import numpy as np\n\n"
            "l1, l2 = 1.2, 1.0                      # link lengths\n"
            "configs = [(0, 0), (30, 45), (90, -45), (45, 90)]   # joint angles in degrees\n\n"
            "for d1, d2 in configs:\n"
            "    t1, t2 = np.deg2rad(d1), np.deg2rad(d2)\n"
            "    elbow = np.array([l1*np.cos(t1), l1*np.sin(t1)])\n"
            "    end = elbow + np.array([l2*np.cos(t1+t2), l2*np.sin(t1+t2)])\n"
            "    reach = np.linalg.norm(end)\n"
            '    print("theta = (%4d, %4d) deg  ->  hand = %s,  reach = %.3f"\n'
            "          % (d1, d2, np.round(end, 3), reach))\n\n"
            "# Try it:\n"
            "#   - Add your own (theta1, theta2) configs and predict the hand position first.\n"
            "#   - Set theta2 = 0 (arm straight): reach should equal l1 + l2 = 2.2.\n",
        ),
        _quiz(),
    ),
)

# ── Robotics — Intermediate ──────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="robotics-intermediate",
    title="Robotics — Inverse Kinematics & the Jacobian",
    description=(
        "Make the arm go where you want: analytic inverse kinematics (and its "
        "multiple solutions), the velocity Jacobian, and singularities & "
        "manipulability. Interactive IK animation and manipulability ellipse, "
        "with MATLAB and Python (NumPy) code including a Jacobian IK solver."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Inverse kinematics: find the joint angles",
            "14 min",
            "# Inverse kinematics: find the joint angles\n\n"
            "**Inverse kinematics (IK)** is the hard, useful direction: given a desired hand "
            "position $(x, y)$, what joint angles get there? For the 2-link arm there's a "
            "clean closed form (law of cosines):\n\n"
            "$$\\cos\\theta_2 = \\frac{x^2 + y^2 - l_1^2 - l_2^2}{2\\,l_1 l_2}, \\qquad "
            "\\theta_1 = \\operatorname{atan2}(y, x) - \\operatorname{atan2}\\big(l_2\\sin\\theta_2,\\; l_1 + l_2\\cos\\theta_2\\big).$$\n\n"
            "Watch IK in action — the arm continuously solves for the joint angles that keep "
            "its hand on a **moving target** (the green dot); the red end-effector stays "
            "locked onto it:\n\n" + _IK_ARM + "\n\n**MATLAB**\n"
            "```matlab\n"
            "c2 = (x^2 + y^2 - l1^2 - l2^2) / (2*l1*l2);\n"
            "t2 = acos(c2);                                   % elbow-down\n"
            "t1 = atan2(y, x) - atan2(l2*sin(t2), l1 + l2*cos(t2));\n"
            "```\n\n"
            "**Python (NumPy)**\n"
            "```python\n"
            "c2 = (x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2)\n"
            "t2 = np.arccos(c2)                               # elbow-down\n"
            "t1 = np.arctan2(y, x) - np.arctan2(l2*np.sin(t2), l1 + l2*np.cos(t2))\n"
            "```\n\n"
            "**Next:** why IK can have several answers — or none.",
        ),
        _t(
            "Multiple solutions, reach & singularities",
            "11 min",
            "# Multiple solutions, reach & singularities\n\n"
            "Unlike FK, IK is rarely unique:\n\n"
            "- **Multiple solutions.** $\\theta_2$ from $\\arccos$ can be $\\pm$ — the famous "
            "**elbow-up vs elbow-down** poses reach the *same* point. A 6-DOF arm typically "
            "has up to **8** IK solutions; the controller picks one (joint limits, obstacle "
            "avoidance, staying away from singularities).\n"
            "- **No solution.** If the target is outside the workspace annulus, "
            "$|\\cos\\theta_2| > 1$ and $\\arccos$ is undefined — the point is simply "
            "unreachable.\n"
            "- **Singularities.** At the workspace boundary (arm fully stretched, "
            "$\\theta_2 = 0$) the two solutions merge and the arm **loses a degree of "
            "freedom** — it can't move radially. Near there, small Cartesian moves demand "
            "huge joint speeds.\n\n"
            "These are exactly why path planning keeps the arm *inside* its dexterous region. "
            "The Jacobian (next) makes the singularity idea precise.\n\n"
            "**Next:** velocities and the Jacobian.",
        ),
        _t(
            "Velocity kinematics & the Jacobian",
            "13 min",
            "# Velocity kinematics & the Jacobian\n\n"
            "The **Jacobian** $J(\\mathbf q)$ is the matrix that maps **joint velocities** to "
            "**end-effector velocity**:\n\n"
            "$$\\dot{\\vec x} = J(\\mathbf q)\\,\\dot{\\mathbf q}.$$\n\n"
            "Each column is how the tip moves when one joint turns. For the 2-link arm,\n\n"
            "$$J = \\begin{bmatrix} -l_1 s_1 - l_2 s_{12} & -l_2 s_{12} \\\\ "
            "\\;\\;l_1 c_1 + l_2 c_{12} & \\;\\;l_2 c_{12} \\end{bmatrix},$$\n\n"
            "with $s_1=\\sin\\theta_1$, $s_{12}=\\sin(\\theta_1+\\theta_2)$, etc. Drive the "
            "joints and watch the **tip-velocity arrow** produced by turning joint 1 alone "
            "(the first column of $J$):\n\n"
            + _VEL_ARM
            + "\n\nThe Jacobian is the workhorse of robot control: invert it to turn a desired "
            "Cartesian velocity into joint commands ($\\dot{\\mathbf q} = J^{-1}\\dot{\\vec x}$), "
            "and its **transpose** maps end-effector forces to joint torques "
            "($\\vec\\tau = J^{T}\\vec F$). It also drives **numerical IK** (the code lab).\n\n"
            "**Next:** where the Jacobian breaks down — singularities & manipulability.",
        ),
        _t(
            "Singularities & manipulability",
            "12 min",
            "# Singularities & manipulability\n\n"
            "A **singularity** is a configuration where the Jacobian loses rank — "
            "$\\det J = 0$. There the arm can't instantaneously move in some Cartesian "
            "direction, and $J^{-1}$ blows up (commanded joint speeds explode). For the "
            "2-link arm this happens when $\\theta_2 = 0$ or $\\pi$ (arm straight or fully "
            "folded).\n\n"
            "The **manipulability ellipse** visualises this: feed a unit circle of joint "
            "rates through $J$ and you get the set of possible tip velocities. A fat, round "
            "ellipse means the arm is **dexterous** (moves easily every way); a flat, "
            "collapsed ellipse means it's **near a singularity**. Drive the joints — fold the "
            "elbow toward $0°$ and watch the ellipse flatten:\n\n"
            + _MANIP_ARM
            + "\n\nManipulability $w = \\sqrt{\\det(JJ^T)}$ is the ellipse's area; control "
            "schemes maximise it to keep the arm responsive and away from the speed blow-ups "
            "at singularities.\n\n"
            "**Next:** test what you've learned.",
        ),
        _code(
            "Lab: analytic & numerical inverse kinematics",
            "13 min",
            "# Inverse kinematics two ways for the 2-link arm (NumPy).\n"
            "import numpy as np\n\n"
            "l1, l2 = 1.2, 1.0\n"
            "target = np.array([1.5, 0.8])\n"
            "x, y = target\n\n"
            "# 1) ANALYTIC IK (law of cosines) -- both elbow solutions.\n"
            "c2 = (x*x + y*y - l1*l1 - l2*l2) / (2*l1*l2)\n"
            "for sign, name in [(+1, 'elbow-down'), (-1, 'elbow-up')]:\n"
            "    t2 = sign * np.arccos(c2)\n"
            "    t1 = np.arctan2(y, x) - np.arctan2(l2*np.sin(t2), l1 + l2*np.cos(t2))\n"
            '    print("%-10s theta = %s deg" % (name, np.round(np.rad2deg([t1, t2]), 2)))\n\n'
            "# 2) NUMERICAL IK via the Jacobian pseudo-inverse (works for any arm).\n"
            "q = np.array([0.2, 0.2])               # initial guess\n"
            "for it in range(100):\n"
            "    a, b = q[0], q[1]\n"
            "    p = np.array([l1*np.cos(a) + l2*np.cos(a+b), l1*np.sin(a) + l2*np.sin(a+b)])\n"
            "    J = np.array([[-l1*np.sin(a) - l2*np.sin(a+b), -l2*np.sin(a+b)],\n"
            "                  [ l1*np.cos(a) + l2*np.cos(a+b),  l2*np.cos(a+b)]])\n"
            "    q = q + np.linalg.pinv(J) @ (target - p)\n"
            'print("numerical IK theta =", np.round(np.rad2deg(q), 2), "deg")\n\n'
            "# Verify: forward kinematics of the numerical solution lands on the target.\n"
            "a, b = q[0], q[1]\n"
            "end = np.array([l1*np.cos(a) + l2*np.cos(a+b), l1*np.sin(a) + l2*np.sin(a+b)])\n"
            'print("FK check =", np.round(end, 3), " target =", target)\n\n'
            "# Try it:\n"
            "#   - Move the target outside the reach (e.g. [3, 0]): arccos fails -> unreachable.\n"
            "#   - Change the initial guess: numerical IK may converge to the other elbow.\n",
        ),
        _quiz(),
    ),
)

# ── Robotics — Advanced ──────────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="robotics-advanced",
    title="Robotics — Dynamics, Trajectories & Control",
    description=(
        "From geometry to motion: Denavit-Hartenberg parameters for 3D arms, "
        "manipulator dynamics (M, C, g), trajectory generation, and feedback "
        "control (PID and computed torque). Interactive trajectory and control "
        "plots, with MATLAB and Python (NumPy) code."
    ),
    level="Advanced",
    lessons=(
        _t(
            "DH parameters & 3D forward kinematics",
            "13 min",
            "# DH parameters & 3D forward kinematics\n\n"
            "Real arms are 3D with 6+ joints. The **Denavit-Hartenberg (DH)** convention is "
            "the standard recipe: attach a frame to each link and describe the step from one "
            "to the next with just **four numbers** $(\\theta_i, d_i, a_i, \\alpha_i)$ — joint "
            "angle, link offset, link length, link twist. Each becomes a homogeneous "
            "transform $T_i$, and the full forward kinematics is their product:\n\n"
            "$$T_0^n = T_1(\\theta_1)\\,T_2(\\theta_2)\\cdots T_n(\\theta_n).$$\n\n"
            "A DH table fully specifies an arm (here, a classic elbow manipulator):\n\n"
            "| link | $\\theta$ | $d$ | $a$ | $\\alpha$ |\n"
            "|------|-----------|-----|-----|-----------|\n"
            "| 1 | $\\theta_1$ | $d_1$ | 0 | $90°$ |\n"
            "| 2 | $\\theta_2$ | 0 | $a_2$ | $0°$ |\n"
            "| 3 | $\\theta_3$ | 0 | $a_3$ | $0°$ |\n\n"
            "Each joint carries its own frame; FK rotates and translates one into the next. "
            "Here is one such body frame (the red/green/blue triad) — **rotate and tilt** to "
            "see it in 3D:\n\n" + "```plot\n"
            '{"mode": "3d", "title": "A link frame in 3D (DH attaches one per joint)", '
            '"xRange": [-1.5, 1.5], "yRange": [-1.5, 1.5], "zRange": [-1.5, 1.5], "azimuth": 40, '
            '"elevation": 25, "vectors": [{"x": 1.2, "y": 0, "z": 0, "label": "x", "color": '
            '"#dc2626"}, {"x": 0, "y": 1.2, "z": 0, "label": "y", "color": "#16a34a"}, '
            '{"x": 0, "y": 0, "z": 1.2, "label": "z (joint axis)", "color": "#2563eb"}]}\n'
            "```\n\n"
            "**Python (NumPy)** — one DH transform:\n"
            "```python\n"
            "import numpy as np\n"
            "def dh(theta, d, a, alpha):\n"
            "    ct, st, ca, sa = np.cos(theta), np.sin(theta), np.cos(alpha), np.sin(alpha)\n"
            "    return np.array([[ct, -st*ca,  st*sa, a*ct],\n"
            "                     [st,  ct*ca, -ct*sa, a*st],\n"
            "                     [ 0,     sa,     ca,    d],\n"
            "                     [ 0,      0,      0,    1]])\n"
            "T = dh(t1, d1, 0, np.pi/2) @ dh(t2, 0, a2, 0) @ dh(t3, 0, a3, 0)\n"
            "```\n\n"
            "**Next:** the forces and torques behind the motion — dynamics.",
        ),
        _t(
            "Manipulator dynamics",
            "13 min",
            "# Manipulator dynamics\n\n"
            "Kinematics ignores mass; **dynamics** asks what **torques** move the arm. Every "
            "manipulator obeys the same matrix equation of motion:\n\n"
            "$$\\mathbf M(\\mathbf q)\\,\\ddot{\\mathbf q} + \\mathbf C(\\mathbf q,\\dot{\\mathbf q})\\,\\dot{\\mathbf q} + \\mathbf g(\\mathbf q) = \\boldsymbol\\tau,$$\n\n"
            "where $\\mathbf M$ is the (configuration-dependent) **inertia matrix**, "
            "$\\mathbf C$ captures **Coriolis & centrifugal** effects, $\\mathbf g$ is "
            "**gravity**, and $\\boldsymbol\\tau$ are the joint torques. It's derived exactly "
            "like the quadrotor EOM in the Physics track — Newton-Euler or Lagrange.\n\n"
            "Gravity alone is already nonlinear: a single link held out horizontally needs "
            "torque $\\tau = m g \\ell \\cos\\theta$, swinging like a pendulum if you let go. "
            "Press **Play** to watch an undriven link fall and swing under gravity:\n\n"
            + "```plot\n"
            '{"title": "An undriven link swinging under gravity", "equal": true, "grid": true, '
            '"xRange": [-1.8, 1.8], "yRange": [-1.8, 0.6], "animate": {"param": "t", "range": '
            '[0, 6.283], "label": "time"}, "parametric": [{"x": "u*1.5*sin(1.1*cos(t))", "y": '
            '"-u*1.5*cos(1.1*cos(t))", "param": "u", "range": [0, 1], "color": "#0891b2", '
            '"label": "link"}], "points": [{"x": 0, "y": 0, "color": "#111827", "size": 6, '
            '"label": "joint"}, {"xExpr": "1.5*sin(1.1*cos(t))", "yExpr": "-1.5*cos(1.1*cos(t))", '
            '"color": "#dc2626", "size": 8, "label": "mass", "trail": true}]}\n'
            "```\n\n"
            "Dynamics is what you need to **size motors**, **simulate** the robot, and build "
            "**model-based controllers** that feed-forward the exact torques a motion needs.\n\n"
            "**Next:** planning smooth motions — trajectory generation.",
        ),
        _t(
            "Trajectory generation",
            "12 min",
            "# Trajectory generation\n\n"
            "You can't just command a target angle — that demands infinite acceleration. A "
            "**trajectory** is a smooth time profile $q(t)$ with matched velocity and "
            "acceleration at the ends. A **cubic polynomial** meets zero-velocity boundary "
            "conditions; normalised over $0\\le s\\le 1$ it is the smoothstep "
            "$q(s) = q_0 + (q_f-q_0)(3s^2 - 2s^3)$.\n\n"
            "Its **position** eases in and out, **velocity** is a smooth bump (zero at both "
            "ends), and **acceleration** is finite — exactly what keeps a robot from "
            "jerking:\n\n" + "```plot\n"
            '{"title": "Cubic joint trajectory: position, velocity, acceleration", "xLabel": '
            '"time s", "yLabel": "value", "xRange": [0, 1], "yRange": [-7, 7], "functions": '
            '[{"expr": "3*x^2 - 2*x^3", "label": "position q(s)", "color": "#2563eb"}, '
            '{"expr": "6*x - 6*x^2", "label": "velocity", "color": "#16a34a"}, {"expr": '
            '"6 - 12*x", "label": "acceleration", "color": "#dc2626"}]}\n'
            "```\n\n"
            "For long moves at a speed limit, a **trapezoidal velocity profile** (accelerate, "
            "cruise, decelerate) is common; **quintic** polynomials also match accelerations "
            "for extra smoothness. Multi-segment paths through waypoints are stitched with "
            "**splines** (see Numerical Methods). The code lab samples a cubic.\n\n"
            "**Next:** closing the loop — feedback control.",
        ),
        _t(
            "Control: PID & computed torque",
            "13 min",
            "# Control: PID & computed torque\n\n"
            "A trajectory says where the joint *should* be; **control** drives the real joint "
            "there despite friction, payload and modelling error. The workhorse is **PID**:\n\n"
            "$$\\tau = K_p\\,e + K_i\\!\\int e\\,dt + K_d\\,\\dot e, \\qquad e = q_{\\text{des}} - q.$$\n\n"
            "- $K_p$ (proportional) pulls toward the target,\n"
            "- $K_d$ (derivative) damps oscillation,\n"
            "- $K_i$ (integral) erases steady-state error.\n\n"
            "Tuning is a balance: too little damping overshoots and rings; too much is "
            "sluggish. Slide the damping and watch a joint's step response settle:\n\n"
            + "```plot\n"
            '{"title": "Joint step response — tune the damping", "xLabel": "time", "yLabel": '
            '"angle", "xRange": [0, 10], "yRange": [0, 1.8], "animate": {"param": "t", "range": '
            '[0, 10], "label": "time"}, "controls": [{"name": "z", "range": [0.05, 1.2], '
            '"value": 0.25, "label": "damping (∝ K_d)"}], "functions": [{"expr": '
            '"1 - exp(-z*x)*cos(3*x)", "label": "q(t) toward setpoint = 1", "color": "#2563eb"}, '
            '{"expr": "1", "label": "setpoint", "color": "#94a3b8"}], "points": [{"xExpr": "t", '
            '"yExpr": "1 - exp(-z*t)*cos(3*t)", "color": "#dc2626", "size": 6, "trail": true}]}\n'
            "```\n\n"
            "For high performance we go **model-based**: **computed-torque control** uses the "
            "dynamics $\\mathbf M, \\mathbf C, \\mathbf g$ to cancel the nonlinearities and "
            "feed-forward the torque the trajectory needs, leaving PID only the small error "
            "to clean up. This is how modern arms move fast *and* accurately.\n\n"
            "**Next:** put trajectories and the Jacobian together in code.",
        ),
        _code(
            "Lab: trajectory + Jacobian velocity",
            "12 min",
            "# Trajectory sampling and Jacobian velocity for the 2-link arm (NumPy).\n"
            "import numpy as np\n\n"
            "l1, l2 = 1.2, 1.0\n\n"
            "# CUBIC trajectory for joint 1 from 0 to 90 deg (smoothstep in s in [0,1]).\n"
            "q0, qf = 0.0, np.deg2rad(90)\n"
            'print("  s   q(deg)  qdot")\n'
            "for s in np.linspace(0, 1, 6):\n"
            "    q = q0 + (qf - q0) * (3*s**2 - 2*s**3)\n"
            "    qd = (qf - q0) * (6*s - 6*s**2)          # d q / d s\n"
            '    print(" %.1f  %6.1f  %5.2f" % (s, np.rad2deg(q), qd))\n\n'
            "# JACOBIAN: map joint rates to end-effector velocity at a configuration.\n"
            "t1, t2 = np.deg2rad(30), np.deg2rad(60)\n"
            "J = np.array([[-l1*np.sin(t1) - l2*np.sin(t1+t2), -l2*np.sin(t1+t2)],\n"
            "              [ l1*np.cos(t1) + l2*np.cos(t1+t2),  l2*np.cos(t1+t2)]])\n"
            "qdot = np.array([1.0, -0.5])                 # joint rates (rad/s)\n"
            'print("\\nend-effector velocity =", np.round(J @ qdot, 3), "m/s")\n'
            'print("det(J) =", round(float(np.linalg.det(J)), 4), "(-> 0 means singular)")\n\n'
            "# manipulability w = sqrt(det(J J^T)): bigger = more dexterous\n"
            'print("manipulability w =", round(float(np.sqrt(np.linalg.det(J @ J.T))), 4))\n\n'
            "# Try it:\n"
            "#   - Set t2 = 0 (arm straight): det(J) -> 0, a singularity (lost a DOF).\n"
            "#   - Change qdot and watch which Cartesian direction the tip moves.\n",
        ),
        _quiz(),
    ),
)


ROBOTICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)

__all__ = ["ROBOTICS_COURSES"]
