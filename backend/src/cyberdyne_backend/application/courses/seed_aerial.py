"""Academy seed content — the Aerial Robotics / UAV track (Beginner → Advanced).

* ``aerial-basics``        — aerial robots overview, coordinate frames, attitude (Euler/quaternion), rigid-body kinematics, forces/moments, motor mixing
* ``aerial-intermediate``  — 6-DOF Newton-Euler dynamics, quadrotor equations of motion, numerical simulation (Euler/RK4), cascaded control, PID attitude stabilization
* ``aerial-advanced``      — UAV state estimation (IMU models, complementary filter, EKF, GPS+IMU fusion), trajectory generation (minimum snap), fixed-wing flight dynamics, GNC + sim-to-real

Runnable ``code`` lessons use Python + numpy (validated inline) for rotation
matrices and Euler↔quaternion conversion, motor mixing and its inverse, integrating
the quadrotor equations of motion, PID roll stabilization, a complementary attitude
filter, and a 1-D Kalman filter fusing IMU and GPS. The **equivalent MATLAB**
appears as read-only blocks. Interactive plots include a slider-driven thrust curve
and a tunable step response. Part of the Robotics & Controls curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, θ, φ, ψ, ω, ², ³, ×, ·, ∝, ⁻¹, °) in diagrams.
# ruff: noqa: RUF001, RUF003

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# aerial-basics
# ──────────────────────────────────────────────────────────────────────

_AER_BASICS = SeedCourse(
    slug="aerial-basics",
    title="Aerial Robotics / UAVs — Basics",
    description=(
        "How flying robots represent and move through 3-D space: multirotor vs "
        "fixed-wing vs VTOL, body and inertial (NED) coordinate frames, attitude "
        "representations (Euler angles, gimbal lock, rotation matrices, "
        "quaternions), rigid-body kinematics, the forces and moments on a "
        "multirotor, and how four rotors mix into thrust and torque. With runnable "
        "Python labs, MATLAB equivalents, and an interactive thrust curve."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Aerial robots: multirotor, fixed-wing & VTOL",
            "10 min",
            r"""# Aerial robots: multirotor, fixed-wing & VTOL

An **aerial robot** (UAV — Unmanned Aerial Vehicle, or "drone") is a flying machine
that senses, decides, and acts **without a pilot on board**. What makes it a *robot*
rather than a remote-control toy is **autonomy**: an onboard loop that estimates its
own state, plans a motion, and stabilizes itself faster than any human could. To
build that loop we first need to know *what we are flying*.

Three airframe families dominate, each a different bargain between **hover, speed,
and efficiency**:

- **Multirotor** (quadcopter, hexacopter, …) — lift comes purely from spinning
  rotors. It can **hover** perfectly, take off vertically, and is mechanically
  simple (no swashplate, fixed-pitch props). The cost: it is **inherently unstable**
  and **inefficient** — every gram is held up by brute rotor thrust, so endurance is
  short (tens of minutes). The workhorse of inspection, photography, and research.
- **Fixed-wing** — a wing generates lift from **forward airspeed**, like an airplane.
  Vastly more **efficient** and long-range (hours, hundreds of km), but it **cannot
  hover** and needs a runway or launcher. Used for mapping, surveillance, and
  long-endurance missions.
- **VTOL** (Vertical Take-Off and Landing) — hybrids that **hover like a multirotor**
  yet **cruise like a fixed-wing** (tilt-rotor, tail-sitter, "quadplane"). They buy
  the best of both at the price of **mechanical and control complexity** — the
  transition between hover and forward flight is the hard part.

```
 multirotor      fixed-wing            VTOL (quadplane)
   ✛  ✛            ___/\___              ✛   ___/\___   ✛
    \/            wing + thrust          hover rotors + wing
  hover, simple   efficient, fast        hover AND cruise (complex)
  short range     no hover               transition is the hard bit
```

**Why is hovering so hard?** A hovering multirotor is like **balancing a pencil on
your fingertip in three rotational axes at once** — it is open-loop unstable, so it
*must* run a fast feedback loop (hundreds of Hz) just to stay upright. That necessity
is exactly why aerial robotics leans so heavily on the dynamics, control, and
estimation we build in this track.

This track focuses on the **multirotor** (specifically the **quadrotor**) because it
is the cleanest vehicle for learning the core ideas — frames, attitude, dynamics,
control, estimation — and then closes with a look at **fixed-wing** flight. The same
fundamentals (rigid-body motion, feedback stabilization, state estimation) carry
across all three families; the airframe just changes how forces are produced.

Before we can control a drone we must describe **where it is and which way it is
pointing**, precisely and without ambiguity. That is the job of **coordinate
frames** — next.
""",
        ),
        _t(
            "Coordinate frames: body vs inertial (NED)",
            "11 min",
            r"""# Coordinate frames: body vs inertial (NED)

To talk about position, velocity, and orientation we need **reference frames** — and
in aerial robotics we always juggle (at least) **two**. Confusing them is the single
most common source of sign errors and crashes, so we pin them down carefully.

**The inertial (world) frame** is fixed to the earth — the stage on which the vehicle
moves. The aerospace convention is **NED**:

- **N** — x-axis points **North**,
- **E** — y-axis points **East**,
- **D** — z-axis points **Down** (toward the center of the earth).

NED is **right-handed** (N × E = D), and "down is positive" feels odd at first but is
deliberate: it makes **gravity a positive number** along +z and keeps the
right-handed math clean. Position `p = (p_N, p_E, p_D)` and velocity live here.

**The body frame** is bolted to the vehicle and moves with it. The standard
**FRD** convention:

- **x_b** points **Forward** (out the nose),
- **y_b** points **Right** (out the right side),
- **z_b** points **Down** (out the belly).

The rotors' thrust acts along **−z_b** (up, out the top), and the angular rates a
gyroscope measures — `p` (roll rate about x_b), `q` (pitch rate about y_b),
`r` (yaw rate about z_b) — are **body-frame** quantities.

```
        Inertial (NED)                Body (FRD)
            N (x)                        x_b  (Forward)
            │                             ╱
            │                            ╱
            └──── E (y)        Right ◄──●  (vehicle)
           ╱                            │
          D (z, down)                   z_b (Down)
```

**Why two frames?** Because **different quantities are natural in different frames**:

- **Forces** are easiest in the **body** frame — rotor thrust is always along −z_b no
  matter how the drone is tilted; aerodynamic drag, motor torques, all body-fixed.
- **Position and the goal** ("fly 10 m North") are natural in the **inertial** frame.
- **Gravity** is constant in the **inertial** frame (`[0, 0, g]` in NED) but rotates
  around as the body tilts.

So the central operation of flight dynamics is **transforming vectors between frames**:
thrust is generated in the body frame, but to predict where the drone *goes* we must
express it in the inertial frame and add gravity there. The mathematical object that
performs that transformation — encoding the vehicle's **orientation** — is the
**rotation (attitude)**, and getting it right is the heart of the next several
lessons. A vector `v_b` in the body frame becomes `v_i = R · v_b` in the inertial
frame, where `R` is the rotation matrix we build next.
""",
        ),
        _t(
            "Attitude: Euler angles, gimbal lock & rotation matrices",
            "12 min",
            r"""# Attitude: Euler angles, gimbal lock & rotation matrices

**Attitude** is the vehicle's **orientation** — how the body frame is rotated relative
to the inertial frame. It is the most important and most error-prone quantity in
aerial robotics, and there are several ways to represent it, each with trade-offs.

**Euler angles** are the intuitive one: three successive rotations,

- **roll φ** — rotation about the body **x** (forward) axis (bank left/right),
- **pitch θ** — rotation about the body **y** (right) axis (nose up/down),
- **yaw ψ** — rotation about the body **z** (down) axis (heading).

Aerospace uses the **Z-Y-X (yaw-pitch-roll, "3-2-1")** sequence. Euler angles are
**human-readable** ("nose up 10°, banked 20°") — perfect for displays and intuition.

**The rotation matrix.** Each angle is an elementary rotation, and the full
body→inertial rotation is their product `R = R_z(ψ) R_y(θ) R_x(φ)`:

$$ R = \begin{bmatrix} c\theta c\psi & s\phi s\theta c\psi - c\phi s\psi & c\phi s\theta c\psi + s\phi s\psi \\ c\theta s\psi & s\phi s\theta s\psi + c\phi c\psi & c\phi s\theta s\psi - s\phi c\psi \\ -s\theta & s\phi c\theta & c\phi c\theta \end{bmatrix} $$

(`c` = cos, `s` = sin). `R` is **orthonormal** (`R⁻¹ = Rᵀ`, `det R = +1`) — a member of
the rotation group **SO(3)**. It maps a body vector to inertial: `v_i = R v_b`. Its
columns are the body axes expressed in inertial coordinates; its rows do the inverse.

**Gimbal lock — the fatal flaw of Euler angles.** When **pitch reaches ±90°**
(`θ = ±90°`), the roll and yaw axes **align** — two of the three rotations now do the
*same thing*, and you **lose a degree of freedom**. Mathematically the kinematic
equations blow up (a `1/cos θ` term → ∞); physically the attitude becomes ambiguous.

```
 normal:   roll, pitch, yaw are 3 independent knobs
 θ → 90°:  the roll axis and yaw axis COINCIDE
           ─► only 2 effective DOF, equations sing 1/cos(θ) → ∞
           ─► an acrobatic / vertical-climb drone using Euler angles can BLOW UP
```

This is not academic: a quadrotor doing a flip or a vertical climb passes through
θ = 90° and an Euler-based attitude estimator/controller will glitch or diverge.

**The trade-offs of representations:**

```
 Euler angles (φ,θ,ψ):  intuitive, 3 numbers — but GIMBAL LOCK, wraparound, ugly math
 Rotation matrix R:     no singularity, composes by multiply — but 9 numbers, 6 redundant
 Quaternion q:          no singularity, 4 numbers, cheap & stable — but not human-readable
```

The practical answer used by virtually every real flight controller: **store and
propagate the attitude as a quaternion** (singularity-free, compact, numerically
stable), and **convert to Euler angles only for display**. That is why we meet the
quaternion next — and then build the conversions in code.

The same rotation in **MATLAB** (run it in the MATLAB REPL):

```matlab
phi = 0.1; theta = 0.2; psi = 0.3;          % roll, pitch, yaw (rad)
Rx = [1 0 0; 0 cos(phi) -sin(phi); 0 sin(phi) cos(phi)];
Ry = [cos(theta) 0 sin(theta); 0 1 0; -sin(theta) 0 cos(theta)];
Rz = [cos(psi) -sin(psi) 0; sin(psi) cos(psi) 0; 0 0 1];
R = Rz * Ry * Rx;                            % body -> inertial (ZYX)
disp('R ='); disp(R)
disp('det(R) (should be 1):'); disp(det(R))
```
""",
        ),
        _t(
            "Quaternions for attitude",
            "11 min",
            r"""# Quaternions for attitude

A **quaternion** is a four-number representation of rotation that avoids gimbal lock,
is compact, and is numerically stable to propagate — which is why it lives at the core
of every serious flight controller and attitude estimator.

**The idea.** Euler's rotation theorem says *any* orientation is a single rotation by
some **angle α** about some **unit axis** `n = (n_x, n_y, n_z)`. The quaternion packs
exactly that:

$$ q = \begin{bmatrix} q_w \\ q_x \\ q_y \\ q_z \end{bmatrix} = \begin{bmatrix} \cos(\alpha/2) \\ n_x \sin(\alpha/2) \\ n_y \sin(\alpha/2) \\ n_z \sin(\alpha/2) \end{bmatrix} $$

A valid rotation quaternion is a **unit quaternion**: `q_w² + q_x² + q_y² + q_z² = 1`.
The scalar part `q_w` encodes the half-angle; the vector part `(q_x, q_y, q_z)`
encodes the axis. (The half-angle is why a quaternion needs only 4 numbers yet covers
all of SO(3) without singularities.)

**From quaternion to rotation matrix.** A unit quaternion maps to the body→inertial
rotation matrix:

$$ R(q) = \begin{bmatrix} 1 - 2(q_y^2 + q_z^2) & 2(q_x q_y - q_z q_w) & 2(q_x q_z + q_y q_w) \\ 2(q_x q_y + q_z q_w) & 1 - 2(q_x^2 + q_z^2) & 2(q_y q_z - q_x q_w) \\ 2(q_x q_z - q_y q_w) & 2(q_y q_z + q_x q_w) & 1 - 2(q_x^2 + q_y^2) \end{bmatrix} $$

**Composing rotations** is **quaternion multiplication** (the Hamilton product),
analogous to multiplying rotation matrices — but cheaper (16 mults vs 27) and it keeps
the result on the unit sphere (just renormalize occasionally). The **inverse** of a
unit quaternion is its **conjugate** `q* = (q_w, −q_x, −q_y, −q_z)` — free to compute.

**Why quaternions win for flight:**

```
 + NO gimbal lock — smooth through any orientation (flips, vertical climbs)
 + compact (4 numbers) and cheap to compose / normalize
 + numerically stable to INTEGRATE (the attitude kinematics qdot = ½ q⊗ω)
 + interpolate smoothly (SLERP) for trajectory/attitude blending
 − not human-readable; the double-cover (q and −q are the SAME rotation) needs care
```

**Attitude kinematics.** Given the body angular rate `ω = (p, q, r)` from the gyro,
the quaternion evolves by the elegant first-order ODE

$$ \dot{q} = \tfrac{1}{2}\, q \otimes \begin{bmatrix} 0 \\ \omega \end{bmatrix} $$

(`⊗` = quaternion product). Integrating *this* — instead of the Euler-angle equations
with their `1/cos θ` — is exactly what lets a drone tumble through any attitude without
the math exploding. That is the propagation step inside attitude estimators (the
complementary filter and EKF of the advanced course).

The takeaway: **Euler angles for humans, quaternions for the computer.** You'll
implement rotation matrices and the Euler↔quaternion round-trip next, and confirm they
agree — the bedrock conversions every flight stack relies on.
""",
        ),
        _code(
            "Rotation matrices & Euler↔quaternion conversion",
            "14 min",
            r"""# Attitude lives in three equivalent forms: Euler angles, a rotation matrix, and a
# quaternion. Here we build R from Euler angles, convert Euler -> quaternion ->
# rotation matrix, and confirm BOTH paths give the SAME matrix (the round-trip check
# every flight stack relies on). All numpy at MODULE level, straight-line. numpy.

import numpy as np

# A test attitude: roll 20 deg, pitch -15 deg, yaw 40 deg (aerospace Z-Y-X).
phi = np.radians(20.0)      # roll  (about body x)
theta = np.radians(-15.0)   # pitch (about body y)
psi = np.radians(40.0)      # yaw   (about body z)

# --- Path A: rotation matrix directly from Euler angles, R = Rz(psi) Ry(theta) Rx(phi).
cphi, sphi = np.cos(phi), np.sin(phi)
cth, sth = np.cos(theta), np.sin(theta)
cpsi, spsi = np.cos(psi), np.sin(psi)

Rx = np.array([[1.0, 0.0, 0.0], [0.0, cphi, -sphi], [0.0, sphi, cphi]])
Ry = np.array([[cth, 0.0, sth], [0.0, 1.0, 0.0], [-sth, 0.0, cth]])
Rz = np.array([[cpsi, -spsi, 0.0], [spsi, cpsi, 0.0], [0.0, 0.0, 1.0]])
R_euler = Rz @ Ry @ Rx

# --- Path B: Euler -> quaternion (half-angle products), then quaternion -> matrix.
cr, sr = np.cos(phi / 2.0), np.sin(phi / 2.0)
cp, sp = np.cos(theta / 2.0), np.sin(theta / 2.0)
cy, sy = np.cos(psi / 2.0), np.sin(psi / 2.0)
qw = cr * cp * cy + sr * sp * sy
qx = sr * cp * cy - cr * sp * sy
qy = cr * sp * cy + sr * cp * sy
qz = cr * cp * sy - sr * sp * cy
qnorm = np.sqrt(qw * qw + qx * qx + qy * qy + qz * qz)
qw, qx, qy, qz = qw / qnorm, qx / qnorm, qy / qnorm, qz / qnorm

R_quat = np.array([
    [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
    [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
    [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
])

print("quaternion (w,x,y,z) = (%.4f, %.4f, %.4f, %.4f), |q| = %.6f"
      % (qw, qx, qy, qz, qnorm / qnorm))
print("R is orthonormal: det(R_euler) = %.6f (should be +1)" % float(np.linalg.det(R_euler)))
print("max |R_euler - R_quat| = %.2e  (the two paths AGREE)"
      % float(np.max(np.abs(R_euler - R_quat))))
print("R R^T = I check: max off-identity = %.2e"
      % float(np.max(np.abs(R_euler @ R_euler.T - np.eye(3)))))
print("Euler angles and quaternions describe the SAME rotation; quaternions avoid gimbal lock.")
""",
        ),
        _t(
            "Rigid-body kinematics",
            "10 min",
            r"""# Rigid-body kinematics

**Kinematics** describes motion **without worrying about the forces that cause it** —
how position and orientation evolve given velocities. (Dynamics, next course, adds the
forces.) A flying robot is a **rigid body** with **six degrees of freedom (6-DOF)**:
three for **position** and three for **orientation**.

**The 6-DOF state.** A complete description of where the vehicle is and how it moves:

- **Position** `p = (p_N, p_E, p_D)` in the inertial frame — 3 DOF (translation).
- **Attitude** `q` (or φ, θ, ψ) — 3 DOF (rotation).
- **Linear velocity** — often expressed in the **body** frame as `v_b = (u, v, w)`.
- **Angular velocity** `ω = (p, q, r)` in the body frame (what the **gyro** reads).

**Translational kinematics.** The inertial position changes at the inertial velocity.
Since the rotors push in the *body* frame, we rotate the body velocity into inertial:

$$ \dot{p} = R(q)\, v_b $$

— the rotation matrix `R` from before turns body-frame velocity into the ground-frame
rate of change of position. This is why attitude couples into translation: **tilt the
drone, and its thrust pushes it sideways**, because the body z-axis (thrust direction)
is no longer vertical.

**Rotational kinematics.** Attitude changes at a rate set by the body angular velocity.
In quaternion form (singularity-free):

$$ \dot{q} = \tfrac{1}{2}\, q \otimes \begin{bmatrix} 0 \\ \omega \end{bmatrix} $$

In Euler form the mapping from body rates `(p, q, r)` to Euler-angle rates is **not the
identity** — it involves a matrix that contains the dreaded `1/cos θ`:

$$ \begin{bmatrix} \dot{\phi} \\ \dot{\theta} \\ \dot{\psi} \end{bmatrix} = \begin{bmatrix} 1 & s\phi\,t\theta & c\phi\,t\theta \\ 0 & c\phi & -s\phi \\ 0 & s\phi/c\theta & c\phi/c\theta \end{bmatrix} \begin{bmatrix} p \\ q \\ r \end{bmatrix} $$

(`t` = tan). The `1/cos θ` is gimbal lock again — another reason to propagate the
quaternion instead.

```
   body rates ω = (p,q,r)   ──►   attitude rate  (qdot = ½ q⊗ω)
   body velocity v_b        ──► (rotate by R) ──►  position rate  pdot = R v_b
```

**The key coupling to remember:** in a multirotor, **you steer by tilting**. There is
no sideways thruster — the only way to move horizontally is to *rotate* the body so the
(always body-fixed) thrust vector points partly sideways. Translation is therefore
**driven by attitude**, which is precisely why multirotor control is **cascaded**: an
outer loop commands a desired *tilt* to achieve a desired *position*, and an inner loop
realizes that tilt (intermediate course).

Kinematics tells us *how* the state moves given velocities; to know how the velocities
themselves change we need the **forces and moments** — next.
""",
        ),
        _t(
            "Forces & moments on a multirotor",
            "11 min",
            r"""# Forces & moments on a multirotor

To predict and control flight we account for every **force** (causing linear
acceleration) and every **moment / torque** (causing angular acceleration) acting on
the vehicle. A multirotor has a refreshingly small, clean set.

**The forces:**

- **Thrust `T`** — each rotor produces lift roughly **proportional to the square of
  its speed**: `T_i = k_T ω_i²` (a rotor pushes air down, gets pushed up). The total
  thrust acts along the body **−z_b** axis (out the top). This is the *only* control
  force a multirotor has for translation.
- **Gravity `mg`** — acts straight down in the **inertial** frame (`[0, 0, mg]` in
  NED). Constant in the world frame, so as the body tilts, gravity "leaks" sideways in
  body coordinates — the restoring/disturbing force the controller fights.
- **Drag** — aerodynamic resistance opposing motion, roughly `∝ v²` at speed; usually
  a secondary effect for slow flight but important at high speed and for energy.

Newton's second law in the **inertial** frame ties them together:

$$ m\ddot{p} = \begin{bmatrix} 0 \\ 0 \\ mg \end{bmatrix} + R(q) \begin{bmatrix} 0 \\ 0 \\ -T \end{bmatrix} + F_{\text{drag}} $$

Read it: gravity pulls down; the rotors push along the (rotated) body −z axis; tilt the
body and the thrust acquires a horizontal component → the drone accelerates sideways.
**Hover** is the balance `T = mg` with the body level.

**The moments (torques)** — what spins the body about its three axes:

- **Roll torque (about x_b)** — from a **left-right thrust difference**.
- **Pitch torque (about y_b)** — from a **front-back thrust difference**.
- **Yaw torque (about z_b)** — subtler: each spinning rotor exerts a **reaction
  torque** on the body (Newton's third law); spinning two clockwise and two
  counter-clockwise lets their reaction torques **cancel in hover** and be
  **unbalanced on command** to yaw. `Q_i = k_Q ω_i²` is each rotor's drag torque.

```
        front
          ▲
     M1   |   M2            M1,M3 spin CW   M2,M4 spin CCW
      ●───┼───●             roll  = right rotors  vs left rotors
      │   +   │  → right    pitch = front rotors  vs back rotors
      ●───┼───●             yaw   = CW pair       vs CCW pair (reaction torque)
     M4   |   M3            thrust= all four together
        (top view, X-config)
```

So **four rotors → four independent commands**: total **thrust** (all four together)
plus **roll, pitch, yaw torques** (differences between rotors). A multirotor is
**underactuated** — 4 controls for 6 DOF — which is the deep reason you cannot move
sideways without tilting (no direct lateral force). Mapping the four desired
quantities `(T, τ_φ, τ_θ, τ_ψ)` onto the four individual motor speeds is **motor
mixing / control allocation** — the final, very practical, piece of the basics, and
the topic of the next lesson and lab.
""",
        ),
        _t(
            "The quadrotor: motor mixing & allocation",
            "11 min",
            r"""# The quadrotor: motor mixing & allocation

A **quadrotor** has four fixed-pitch rotors, and the controller's job is to turn four
*desired* effects — **total thrust** and **three torques** — into four *motor*
commands. That mapping is **motor mixing** (a.k.a. **control allocation**), and it is
where the abstract dynamics meet the hardware.

**The four control quantities** the controller wants to produce:

- **`T`** — total upward thrust (altitude / vertical motion),
- **`τ_φ`** — roll torque (tilt left/right),
- **`τ_θ`** — pitch torque (tilt forward/back),
- **`τ_ψ`** — yaw torque (rotate heading).

**The four actuators:** rotor thrusts `f_1, f_2, f_3, f_4` (each `f_i = k_T ω_i²`, set
by motor speed). For the common **X-configuration** with arm length and CW/CCW
spin pattern, the four effects are **linear combinations** of the four rotor thrusts.
The **mixing matrix `M`** maps rotor thrusts → effects:

$$ \begin{bmatrix} T \\ \tau_\phi \\ \tau_\theta \\ \tau_\psi \end{bmatrix} = \underbrace{\begin{bmatrix} 1 & 1 & 1 & 1 \\ -\ell & -\ell & \ell & \ell \\ \ell & -\ell & -\ell & \ell \\ c & -c & c & -c \end{bmatrix}}_{M} \begin{bmatrix} f_1 \\ f_2 \\ f_3 \\ f_4 \end{bmatrix} $$

- Row 1: **all four** add to total thrust.
- Rows 2–3: **differences** of rotor thrusts (scaled by the moment arm `ℓ`) make roll
  and pitch torque.
- Row 4: the **CW/CCW reaction-torque** pattern (`c = k_Q/k_T`) makes yaw — the
  `+,−,+,−` signs are the alternating spin directions.

**The controller actually needs the inverse.** It computes desired `(T, τ_φ, τ_θ,
τ_ψ)`, then **allocates** them to the rotors by inverting the mixing:

$$ \begin{bmatrix} f_1 \\ f_2 \\ f_3 \\ f_4 \end{bmatrix} = M^{-1} \begin{bmatrix} T \\ \tau_\phi \\ \tau_\theta \\ \tau_\psi \end{bmatrix} $$

For a symmetric quad `M` is invertible, so the allocation is a single matrix multiply
— cheap enough to run every control cycle. Finally each rotor thrust is converted to a
motor command via `ω_i = √(f_i / k_T)`.

**Practical realities that matter:**

```
 saturation:  f_i must stay in [0, f_max] — you cannot pull DOWN (props one-way).
              If a command would go negative or exceed max, it must be CLIPPED,
              and naive clipping breaks the torque balance -> smart allocation
              PRIORITIZES attitude (keep it flying) over thrust.
 redundancy:  hexa/octocopters have MORE rotors than controls -> M is non-square,
              use the pseudo-inverse; the spare rotors give FAULT TOLERANCE
              (lose a motor and still fly).
```

Motor mixing is the clean bridge from "what torque do I want" to "how fast does each
motor spin," and the **forward (effects from thrusts) / inverse (thrusts from effects)**
pair you'll build in the lab is run, in both directions, by every flight controller.
Next, the lab implements mixing and its inverse — and you'll confirm the round-trip is
exact.

The mixing in **MATLAB** (run it in the MATLAB REPL):

```matlab
l = 0.25; c = 0.02;                          % arm length, torque/thrust ratio
M = [ 1  1  1  1;                            % total thrust
     -l  l  l -l;                            % roll
     -l -l  l  l;                            % pitch
     -c  c -c  c ];                          % yaw
u = [10; 0.5; 0; 0];                         % desired [thrust; roll; pitch; yaw]
f = M \ u;                                  % solve for the four rotor thrusts
disp('rotor thrusts:'); disp(f')
disp('recovered M*f:'); disp((M*f)')
```
""",
        ),
        _code(
            "Motor mixing: thrust/torque ↔ four rotor commands",
            "14 min",
            r"""# A quadrotor controller produces desired (thrust, roll/pitch/yaw torque); motor
# mixing maps those FOUR effects onto FOUR rotor thrusts via the mixing matrix M, and
# the controller inverts M to allocate. We build M, go effects -> rotors -> effects,
# and confirm the round-trip is exact. All numpy at MODULE level. numpy.

import numpy as np

ell = 0.25         # moment arm (m): rotor distance from center
c = 0.02           # yaw coefficient = k_Q / k_T (drag-torque / thrust ratio)
mass = 1.2         # kg
g = 9.81

# Mixing matrix M: [T, tau_phi, tau_theta, tau_psi]^T = M @ [f1, f2, f3, f4]^T  (X-config).
M = np.array([
    [1.0, 1.0, 1.0, 1.0],         # total thrust = sum of rotor thrusts
    [-ell, -ell, ell, ell],       # roll torque  (left vs right rotors)
    [ell, -ell, -ell, ell],       # pitch torque (front vs back rotors)
    [c, -c, c, -c],               # yaw torque   (CW vs CCW reaction torque)
])
Minv = np.linalg.inv(M)

# Desired effects: hover thrust (mg) plus a small roll command, no pitch/yaw.
T_des = mass * g
tau_des = np.array([T_des, 0.3, 0.0, 0.0])     # [thrust, roll, pitch, yaw]

# ALLOCATE: invert the mixing to get the four rotor thrusts the motors must produce.
f = Minv @ tau_des

# FORWARD: feed those rotor thrusts back through M -> should recover the desired effects.
tau_check = M @ f

print("desired effects [T, tau_phi, tau_theta, tau_psi] =", np.round(tau_des, 4))
print("allocated rotor thrusts  [f1, f2, f3, f4] (N)     =", np.round(f, 4))
print("forward-mixed effects (recovered)                 =", np.round(tau_check, 4))
print("round-trip error = %.2e (M^-1 then M is exact)" % float(np.max(np.abs(tau_check - tau_des))))
print()
# A positive roll command makes the RIGHT rotors push more than the LEFT (signs of M row 2).
print("roll command -> right rotors (f3,f4) > left rotors (f1,f2)? %s"
      % str(bool(f[2] > f[0] and f[3] > f[1])))
print("all four rotor thrusts non-negative (feasible)? %s" % str(bool(np.all(f >= 0.0))))
print("motor mixing is just M (effects<-thrusts) and its inverse (thrusts<-effects).")
""",
        ),
        _t(
            "Thrust, throttle & the hover point",
            "9 min",
            r"""# Thrust, throttle & the hover point

Before flying we need the link between the **command** a controller sends (throttle /
motor speed) and the **thrust** that actually lifts the drone — because that
relationship is **nonlinear**, and ignoring it makes a controller sluggish at one end
and twitchy at the other.

**Thrust grows with the square of rotor speed.** A propeller's lift is, to good
approximation,

$$ T = k_T\, \omega^2 $$

where `ω` is the rotor angular speed and `k_T` lumps together air density, blade
geometry, and diameter. **Doubling the rotor speed quadruples the thrust** — so the
control "feel" changes across the throttle range: near idle a small throttle change
barely moves thrust; near full throttle the same change moves a lot.

```plot
{"title": "Rotor thrust vs throttle — T = k·(throttle)² (drag the constant)", "xLabel": "throttle (0–1)", "yLabel": "thrust (N)", "xRange": [0, 1], "yRange": [0, 40], "controls": [{"name": "k", "label": "thrust const k", "range": [10, 40], "step": 1, "value": 25}], "functions": [{"expr": "k * x * x", "label": "T = k·throttle²", "color": "#2563eb"}]}
```

**The hover throttle.** To hover, total thrust must equal weight, `T = mg`. With four
rotors each carrying a quarter of the weight, the per-rotor hover thrust is `mg/4`, and
the hover throttle sits **wherever the curve crosses mg** — typically around the middle
of the stick (a well-sized drone hovers near **50% throttle**, leaving headroom to
accelerate up *and* the ability to descend by reducing thrust).

**Thrust-to-weight ratio (TWR).** The single most telling agility number:

$$ \text{TWR} = \frac{T_{\max}}{mg} $$

- **TWR ≈ 1** — can barely hold itself up; no climb authority, dangerous.
- **TWR ≈ 2** — typical for stable photography platforms (hover at ~50% throttle).
- **TWR ≈ 4–8+** — racing/acrobatic drones, explosive vertical acceleration.

**Why the nonlinearity matters for control.** A controller that outputs "thrust"
must **invert the curve** — `throttle = √(T/k)` — to send the right command, or
**linearize around the hover point** so its gains behave consistently. Flight stacks
also **battery-compensate**: as the battery sags, the same throttle yields *less*
rotor speed and thrust, so `k_T` effectively drops and the controller must push harder.

The mental model to keep: **command (throttle) and effect (thrust) are related by a
square law, and hover is just the operating point where thrust equals weight.**
Everything the controller does — holding altitude, accelerating, fighting gusts — is a
push *around* that hover point on a curved thrust map. With frames, attitude, dynamics,
mixing, and the thrust map in hand, you have the full kinematic and force picture of a
multirotor; the next course makes it *move* by integrating the equations of motion.
""",
        ),
        quiz_lesson(
            "Quiz: Aerial Robotics Fundamentals",
            (
                q(
                    "What is the defining trade-off between multirotor, fixed-wing, and VTOL UAVs?",
                    (
                        opt(
                            "Multirotors hover but are inefficient/short-range; fixed-wing is efficient/long-range but can't hover; VTOL does both at the cost of complexity",
                            correct=True,
                        ),
                        opt("They are identical except in color"),
                        opt("Fixed-wing aircraft can hover better than multirotors"),
                        opt("Multirotors are the most efficient and longest-range"),
                    ),
                    "Lift source sets the bargain: rotors (hover, inefficient) vs a wing (efficient, no hover); VTOL hybrids hover AND cruise but add mechanical/control complexity.",
                ),
                q(
                    "Why do aerial robots use both a body frame and an inertial (NED) frame?",
                    (
                        opt(
                            "Forces (thrust, drag) are natural in the body frame, while position/goals and gravity are natural in the inertial frame — so we transform vectors via the rotation matrix",
                            correct=True,
                        ),
                        opt("Two frames are used only for redundancy"),
                        opt(
                            "The body frame measures gravity and the inertial frame measures thrust"
                        ),
                        opt("There is no real difference between the frames"),
                    ),
                    "Thrust is along body −z_b regardless of tilt; position/gravity live in NED. v_i = R v_b converts between them; mixing the frames causes sign errors.",
                ),
                q(
                    "What is gimbal lock, and how do flight controllers avoid it?",
                    (
                        opt(
                            "At pitch = ±90° two Euler rotation axes align and a DOF is lost (equations blow up via 1/cos θ); controllers store attitude as a quaternion instead",
                            correct=True,
                        ),
                        opt("It is when the motors physically lock; you add more motors"),
                        opt("It happens only at zero pitch; ignore it"),
                        opt("Quaternions cause gimbal lock and Euler angles cure it"),
                    ),
                    "Euler angles are singular at θ = ±90°. Quaternions (4 numbers, unit norm) represent any orientation without singularity and are stable to integrate (q̇ = ½ q⊗ω).",
                ),
                q(
                    "On a multirotor, how is horizontal motion produced?",
                    (
                        opt(
                            "By tilting the body so the body-fixed thrust vector points partly sideways — there is no direct lateral thruster (it is underactuated)",
                            correct=True,
                        ),
                        opt("By a dedicated sideways propeller"),
                        opt("By spinning all rotors faster"),
                        opt("By changing the wing angle"),
                    ),
                    "Thrust is always along −z_b; the only way sideways is to rotate the body (attitude drives translation), which is why control is cascaded: tilt to move.",
                ),
                q(
                    "What does motor mixing (control allocation) do on a quadrotor?",
                    (
                        opt(
                            "Maps desired (total thrust, roll/pitch/yaw torque) onto four rotor thrusts via the mixing matrix M, and the controller inverts M to allocate per-motor commands",
                            correct=True,
                        ),
                        opt("It charges the battery between flights"),
                        opt("It converts GPS to altitude"),
                        opt("It is only needed for fixed-wing aircraft"),
                    ),
                    "M maps four rotor thrusts to four effects (sum = thrust; differences = roll/pitch; CW/CCW pattern = yaw). The controller uses M⁻¹ to get rotor thrusts from desired effects.",
                ),
                q(
                    "How does rotor thrust depend on rotor speed, and what is the hover condition?",
                    (
                        opt(
                            "T = k_T·ω² (thrust ∝ speed squared); hover is when total thrust equals weight (T = mg), typically near mid-throttle",
                            correct=True,
                        ),
                        opt("Thrust is linear in speed; hover needs full throttle"),
                        opt("Thrust is independent of rotor speed"),
                        opt("Hover requires zero thrust"),
                    ),
                    "The square law means doubling speed quadruples thrust; a controller inverts/linearizes it around the hover point (T = mg). TWR = T_max/(mg) sets agility.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# aerial-intermediate
# ──────────────────────────────────────────────────────────────────────

_AER_INTERMEDIATE = SeedCourse(
    slug="aerial-intermediate",
    title="Aerial Robotics / UAVs — Intermediate",
    description=(
        "Making the quadrotor move and stay upright: 6-DOF rigid-body dynamics "
        "(Newton–Euler), the full quadrotor equations of motion, numerical "
        "integration (explicit Euler and RK4), attitude dynamics, cascaded inner/"
        "outer control, and PID attitude stabilization. With runnable Python labs "
        "that integrate the equations of motion and stabilize a roll axis, plus an "
        "interactive step-response plot."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "6-DOF rigid-body dynamics (Newton–Euler)",
            "12 min",
            r"""# 6-DOF rigid-body dynamics (Newton–Euler)

Kinematics told us how the state moves *given* velocities; **dynamics** tells us how
the velocities themselves change under **forces and torques**. For a rigid body the
governing laws are **Newton's** (translation) and **Euler's** (rotation) equations —
together the **Newton–Euler** formulation.

**Translation — Newton's second law.** In the **inertial** frame, mass times
acceleration equals the net force:

$$ m\,\ddot{p} = \sum F = m g\,\hat{z}_i + R(q)\,F_{\text{body}} $$

The forces are gravity (inertial, downward) plus the body forces (thrust, drag)
rotated into inertial coordinates by `R`. Simple and linear — translation is the easy
half.

**Rotation — Euler's equation.** This is where rigid-body motion gets subtle. In the
**body** frame, the angular momentum is `J ω` (with `J` the **inertia matrix**), and
the net torque drives its change:

$$ J\,\dot{\omega} = \sum \tau - \omega \times (J\,\omega) $$

The first term is the applied torque (from motor-thrust differences). The second,
`ω × (J ω)`, is the **gyroscopic / Coriolis coupling** — a torque-free term that
arises purely because we express things in the *rotating* body frame. It is what makes
a spinning body **precess** and couples the rotational axes together; for a fast or
asymmetric vehicle it is not negligible.

**The inertia matrix `J`** is the rotational analog of mass — it says how hard each
axis is to angularly accelerate:

$$ J = \begin{bmatrix} J_{xx} & 0 & 0 \\ 0 & J_{yy} & 0 \\ 0 & 0 & J_{zz} \end{bmatrix} $$

For a symmetric quadrotor the off-diagonal **products of inertia** are ~0 (the body is
nearly symmetric), so `J` is diagonal — a big simplification. Typically
`J_xx ≈ J_yy` (roll and pitch feel alike) and `J_zz` is larger (yaw has the most
inertia), which is why **yaw is the sluggish axis** on most quads.

```
   FORCES  (inertial frame)         TORQUES (body frame)
   m p̈ = mg ẑ + R F_body            J ω̇ = τ − ω×(Jω)
        translation                      rotation
   (gravity + rotated thrust)       (motor torques − gyroscopic coupling)
```

**Why split inertial vs body?** Forces and gravity are cleanest in the inertial frame;
the inertia matrix `J` is **constant only in the body frame** (it rotates with the
vehicle), so Euler's equation is written in the body frame to keep `J` fixed. The two
equations are coupled through `R(q)` and the kinematics from the last course.

Put the **dynamics** (how `v_b`, `ω` change) together with the **kinematics** (how `p`,
`q` change) and you have the **complete equations of motion** — a set of coupled ODEs
that fully predict the flight given the motor commands. Assembling them specifically
for a quadrotor is the next lesson.
""",
        ),
        _t(
            "The full quadrotor equations of motion",
            "12 min",
            r"""# The full quadrotor equations of motion

Now we assemble the complete **equations of motion (EOM)** of a quadrotor — the set of
coupled ODEs that, given the four motor commands, predict every aspect of the flight.
This model is the heart of any simulator, and the plant every controller is designed
against.

**The state** (12 numbers, the classic 6-DOF set):

- position `p = (x, y, z)` (inertial),
- velocity `v = (ẋ, ẏ, ż)` (inertial) — or body `v_b`,
- attitude `(φ, θ, ψ)` (or quaternion `q`),
- body angular rate `ω = (p, q, r)`.

**The inputs** (from motor mixing): total thrust `T` and the three torques
`τ = (τ_φ, τ_θ, τ_ψ)`.

**Translational dynamics** — Newton's law with gravity plus rotated thrust (thrust acts
along body −z, i.e. the third column of `R` gives the world thrust direction):

$$ \ddot{x} = -\tfrac{T}{m}(c\phi\, s\theta\, c\psi + s\phi\, s\psi) $$
$$ \ddot{y} = -\tfrac{T}{m}(c\phi\, s\theta\, s\psi - s\phi\, c\psi) $$
$$ \ddot{z} = g - \tfrac{T}{m}\, c\phi\, c\theta $$

(in NED, `g` positive down; the trig is exactly `R`'s third column, which is where the
thrust points). When level (`φ = θ = 0`) the first two vanish and `z̈ = g − T/m` — pure
vertical motion, hover at `T = mg`.

**Rotational dynamics** — Euler's equation for a diagonal inertia `J`, written out per
axis (the cross-coupling terms come from `ω × Jω`):

$$ \dot{p} = \frac{\tau_\phi + (J_{yy} - J_{zz})\, q\, r}{J_{xx}} $$
$$ \dot{q} = \frac{\tau_\theta + (J_{zz} - J_{xx})\, p\, r}{J_{yy}} $$
$$ \dot{r} = \frac{\tau_\psi + (J_{xx} - J_{yy})\, p\, q}{J_{zz}} $$

The bracketed products are the gyroscopic coupling; near hover (small rates) they're
tiny, which is why a **linearized hover model** decouples the axes so nicely.

**Attitude kinematics** — body rates to Euler-angle rates (the `1/cos θ` map from the
basics), or `q̇ = ½ q⊗ω` for the quaternion.

```
  motors → mixing → (T, τ)
            │
            ├─ translational:  p̈ = g ẑ − (T/m)·(thrust direction from R)
            └─ rotational:     J ω̇ = τ − ω×Jω ,   then attitude kinematics
            ↓
         full 12-state evolution (a simulator)
```

**The structure to internalize — underactuation and cascade.** Notice `T` and `τ`
appear in **different** equations: torques set the **attitude**, and the attitude
*direction* of `T` then sets the **horizontal** acceleration. You cannot command `ẍ`
directly — you command it *through* attitude. This is the mathematical root of the
**cascaded control** architecture (an attitude inner loop inside a position outer loop)
that we build later in this course.

These EOM are **nonlinear and coupled**, so we rarely solve them on paper — we
**integrate them numerically** to simulate flight. How to do that accurately (Euler vs
RK4) is the next lesson, and then you'll integrate this very model in a lab.
""",
        ),
        _t(
            "Numerical integration: Euler & RK4",
            "11 min",
            r"""# Numerical integration: Euler & RK4

The quadrotor equations of motion are nonlinear ODEs of the form `ẋ = f(x, u)` — no
closed-form solution. To **simulate** flight (and to run model-based estimators) we
**integrate numerically**: step the state forward in small time increments `dt`. The
choice of integrator trades **accuracy against cost**, and it matters.

**Explicit (forward) Euler** — the simplest method. Assume the derivative is constant
over the step:

$$ x_{k+1} = x_k + dt \cdot f(x_k, u_k) $$

One function evaluation per step, trivial to code. But it is only **first-order
accurate** (local error `∝ dt²`, global `∝ dt`), so it needs a **small `dt`** to be
accurate, and it tends to **inject energy** into oscillatory/rotational systems — a
simulated drone can slowly *gain* energy and drift unphysically if `dt` is too big.
Fine for a quick sketch or a very small step; risky for serious simulation.

**Runge–Kutta 4 (RK4)** — the workhorse. It samples the derivative at **four** points
within the step and takes a weighted average, canceling error terms:

$$ k_1 = f(x_k),\quad k_2 = f(x_k + \tfrac{dt}{2}k_1),\quad k_3 = f(x_k + \tfrac{dt}{2}k_2),\quad k_4 = f(x_k + dt\, k_3) $$
$$ x_{k+1} = x_k + \frac{dt}{6}\,(k_1 + 2k_2 + 2k_3 + k_4) $$

Four evaluations per step, but **fourth-order accurate** (global error `∝ dt⁴`) — so
for the *same* accuracy RK4 can take **far larger steps** than Euler, usually winning
overall despite the 4× per-step cost. It is the default for trajectory simulation,
physics, and flight dynamics.

```
 Euler:  ●────────►          1 sample, slope held flat -> drifts, needs tiny dt
            (one slope)

 RK4:    ●─·─·─·──►           4 samples averaged -> tracks curvature, big dt OK
          k1 k2 k3 k4
```

**Choosing `dt` and a method:**

- **Stability** — too large a `dt` makes *any* explicit method blow up; stiff or fast
  dynamics (high rotor/attitude bandwidth) force a smaller step.
- **Accuracy** — RK4 lets you relax `dt` for the same fidelity; Euler is acceptable
  only when `dt` is very small relative to the fastest dynamics.
- **Real-time** — onboard, the control loop *is* a fixed-step integrator (often
  semi-implicit Euler, which conserves energy better than plain Euler at the same
  cost), running at 400 Hz–1 kHz.

A subtle but important variant for physics: **semi-implicit (symplectic) Euler**
updates velocity first, then uses the **new** velocity to update position. It is the
same cost as plain Euler but does **not** artificially pump energy — which is why game
engines and many flight sims prefer it over naive forward Euler.

The practical rule: **forward Euler to understand, RK4 to simulate accurately,
semi-implicit Euler for cheap energy-stable real-time steps.** In the next lab you'll
integrate the quadrotor's vertical/hover dynamics with explicit Euler and watch the
state evolve step by step — and see how `dt` and thrust set the response.
""",
        ),
        _code(
            "Integrating the quadrotor vertical (hover) dynamics",
            "14 min",
            r"""# We integrate the quadrotor's VERTICAL equation of motion step by step. With the
# body level, z-dynamics reduce to:  zddot = g - T/m  (NED, g positive down). We
# apply a thrust profile and use explicit Euler in a straight-line MODULE-LEVEL loop
# to evolve height and vertical speed. Deterministic, no helper functions. numpy.

import numpy as np

mass = 1.2          # kg
g = 9.81            # m/s^2 (NED: +z is down)
dt = 0.02           # 50 Hz integration step
steps = 400         # 8 seconds

hover_thrust = mass * g                      # thrust to exactly cancel gravity

# Thrust profile (N): hover, then a climb burst (T > mg), then back to hover.
# Build it with numpy at module level (no random, fully deterministic).
k = np.arange(steps)
thrust = np.full(steps, hover_thrust)
thrust[k >= 50] = hover_thrust + 4.0         # climb (extra upward thrust)
thrust[k >= 150] = hover_thrust              # back to hover -> coast
thrust[k >= 250] = hover_thrust - 3.0        # descend (less than weight)
thrust[k >= 350] = hover_thrust              # hover again

# State: altitude (m, UP positive for readability) and vertical velocity (m/s, up+).
# In NED zddot = g - T/m points DOWN; we track UP = -down, so up_acc = T/m - g.
altitude = np.zeros(steps)
vz_up = np.zeros(steps)
alt = 0.0
vup = 0.0
for i in range(steps):
    acc_up = thrust[i] / mass - g            # net upward acceleration
    vup = vup + acc_up * dt                   # explicit Euler: velocity
    alt = alt + vup * dt                      # explicit Euler: position
    altitude[i] = alt
    vz_up[i] = vup

print("hover thrust = %.2f N (= m*g); climb adds +4 N, descend uses -3 N" % hover_thrust)
print(" t(s)   thrust(N)   alt(m)   vz_up(m/s)")
for i in [0, 50, 100, 150, 200, 250, 300, 399]:
    print("  %4.1f   %7.2f   %6.2f   %8.3f" % (i * dt, thrust[i], altitude[i], vz_up[i]))
print()
print("peak altitude = %.2f m, final altitude = %.2f m" % (float(altitude.max()), altitude[-1]))
print("T > mg climbs, T = mg coasts at constant speed, T < mg descends:")
print("the integrated EOM turns a thrust profile into a flight trajectory.")
""",
        ),
        _t(
            "Attitude dynamics & the linearized hover model",
            "11 min",
            r"""# Attitude dynamics & the linearized hover model

Stabilizing a multirotor is overwhelmingly about **attitude** — keeping it upright. So
we zoom in on the **rotational** equations and, crucially, **linearize** them around
hover, because the simple linear model that results is what makes controller design
tractable.

**The full attitude dynamics** (from Euler's equation, diagonal inertia):

$$ J_{xx}\dot{p} = \tau_\phi + (J_{yy}-J_{zz})\,q r, \quad J_{yy}\dot{q} = \tau_\theta + (J_{zz}-J_{xx})\,p r, \quad J_{zz}\dot{r} = \tau_\psi + (J_{xx}-J_{yy})\,p q $$

plus the kinematics linking body rates `(p, q, r)` to Euler-rate `(φ̇, θ̇, ψ̇)`.

**Linearizing around hover.** At hover the vehicle is level (`φ ≈ θ ≈ 0`) with small
angular rates. Under those assumptions two big simplifications happen:

- The **gyroscopic products** `qr, pr, pq` are products of *small* quantities → ≈ 0, so
  the **three axes decouple**.
- The body-rate→Euler-rate map becomes the **identity** (`cos θ ≈ 1`, `sin φ ≈ 0`), so
  `φ̇ ≈ p`, `θ̇ ≈ q`, `ψ̇ ≈ r`.

The attitude per axis collapses to a beautifully simple **double integrator**. For
roll:

$$ \ddot{\phi} \approx \frac{\tau_\phi}{J_{xx}} $$

That is: **torque in → angular acceleration → (integrate) rate → (integrate) angle.**
Each axis is an independent "torque drives angle through two integrators," exactly like
a mass on a frictionless track but rotational.

```
   τ_φ ──[ 1/J_xx ]──► φ̈ ──[ ∫ ]──► φ̇ (=p) ──[ ∫ ]──► φ
        torque        ang. accel    roll rate         roll angle
   (a DOUBLE INTEGRATOR per axis — and it is OPEN-LOOP UNSTABLE)
```

**Why this matters:** a double integrator is **marginally/open-loop unstable** — with
no control, any disturbance makes the angle drift away and never returns (two poles at
the origin). There is **no natural restoring force** keeping a quad level (unlike a
pendulum or a plane's static stability). Therefore the attitude **must be actively
stabilized by feedback** — which is precisely why every multirotor runs a fast inner
attitude loop, and why we reach for **PID** next.

**The payoff of linearization:** three **decoupled double integrators** are the
friendliest possible plant. Classic linear control (PID, pole placement, LQR) applies
directly, gains are easy to reason about, and a controller tuned on this model works
beautifully near hover (where drones spend most of their time). Far from hover —
aggressive flips, high-rate maneuvers — the coupling returns and you need the full
nonlinear model or gain scheduling, but the linear hover model is the foundation.

So attitude stabilization reduces to: **close a feedback loop around a double
integrator, per axis.** The tool that does it — proportional, integral, derivative
action — and how it stabilizes and shapes the response is the next lesson, with a roll
stabilization lab to follow.
""",
        ),
        _t(
            "Cascaded control: inner attitude, outer position",
            "11 min",
            r"""# Cascaded control: inner attitude, outer position

A multirotor is **underactuated** — 4 inputs (thrust + 3 torques) for 6 DOF — and, as
we saw, **you steer by tilting**: horizontal motion comes only from attitude. The
elegant architecture that exploits this is **cascaded (nested) control**: loops within
loops, each handling one layer of the dynamics at its own timescale.

**The cascade, from inside out:**

```
 position cmd ─►[ POSITION ]─►accel ─►[ ATTITUDE ]─►rate ─►[ RATE ]─►torque─►[ MIXER ]─► motors
   (slow,        (outer)         cmd    (mid)       cmd    (inner,            allocation
    ~50 Hz)                  desired tilt        desired ω   400-1000 Hz)
                                 │                              ▲
                                 └──────── attitude drives translation ───────┘
```

- **Inner loop — body-rate (and attitude) control.** The fastest loop (often
  400 Hz–1 kHz). It takes a desired attitude / angular rate and produces the **torques**
  to achieve it, by controlling the (open-loop-unstable) double-integrator attitude
  dynamics. This loop *keeps the drone flying* — it must be fast and robust.
- **Middle loop — attitude.** Converts a desired tilt into desired body rates fed to
  the rate loop. (Often the rate and attitude loops are described together as "the
  attitude controller.")
- **Outer loop — position / velocity.** The slowest loop. It takes a desired **position**
  and computes the **acceleration** needed to get there; since horizontal acceleration
  *is* tilt (`ẍ ≈ −g·θ` near hover), it outputs a **desired attitude** (and total
  thrust) for the inner loops to realize. "Go North" becomes "pitch nose-down a few
  degrees."

**Why nest the loops?** Three reasons that make cascade the universal multirotor
architecture:

- **It matches the physics.** The dynamics are naturally layered — torque sets
  attitude, attitude sets translation — so the controller mirrors that chain, each loop
  inverting one link.
- **Timescale separation.** The inner loop is **much faster** than the outer, so from
  the outer loop's view the inner loop is "instant" — you can design each loop almost
  **independently**, a huge simplification (design the fast attitude loop first, then
  the slow position loop assuming attitude is already achieved).
- **Robustness & saturation handling.** The fast inner loop rejects disturbances
  (gusts) before they corrupt position; limits (max tilt, max thrust) are naturally
  imposed between layers, and you can prioritize the inner (keep-it-flying) loop when
  actuators saturate.

**The rule of thumb:** each loop should be **~5–10× faster** than the loop outside it,
so timescale separation holds. Violate it (outer loop too fast, or inner too slow) and
the loops **fight each other** and oscillate.

This cascade is not unique to drones — it's the standard pattern for underactuated and
multi-rate systems (robot arms, cars, rockets). For a quadrotor it cleanly turns the
hard 6-DOF underactuated problem into a stack of simple **single-loop** problems, each
solvable with the **PID** controller of the next lesson — starting with the most
critical: stabilizing attitude.
""",
        ),
        _t(
            "PID attitude stabilization",
            "12 min",
            r"""# PID attitude stabilization

The inner attitude loop must hold a (open-loop-unstable) double-integrator axis at a
commanded angle, fast and without oscillation. The tool that does this on virtually
every drone is the **PID controller** — proportional, integral, derivative feedback —
simple, tunable, and remarkably effective on the linearized hover model.

**The PID law.** Given the error `e = φ_desired − φ` (commanded minus measured angle),
the control torque is

$$ \tau = K_p\, e + K_i \int e\, dt + K_d\, \frac{de}{dt} $$

Each term has a clear job on the double-integrator attitude plant:

- **P (proportional), `K_p e`** — a restoring torque proportional to error. It supplies
  the **missing "spring"** the double integrator lacks, pulling the angle back toward
  the target. Higher `K_p` → stiffer, faster — but P alone on a double integrator
  **oscillates** (it's an undamped spring).
- **D (derivative), `K_d ė`** — torque opposing the *rate* of error change: **damping**.
  It supplies the missing "friction," killing the oscillation P creates. P+D turns the
  axis into a well-behaved damped second-order system — the **core** of attitude
  control. (Conveniently, `ė ≈ −φ̇ = −p`, the gyro rate — so D is essentially **rate
  feedback**, which is why the inner loop is often literally a *rate* controller.)
- **I (integral), `K_i ∫e`** — accumulates persistent error to cancel **steady-state
  bias** (a slightly off CG, a constant wind, motor mismatch) that P+D would otherwise
  leave as a small standing offset. Powerful but prone to **integral windup**
  (the integrator over-charges during saturation) — real controllers add **anti-windup**.

```
   e ─┬─► Kp·e ───────────┐
      ├─► Ki·∫e dt ────────┼──(+)──► τ ──► [ 1/(J s²) ] ──► φ  (double integrator)
      └─► Kd·de/dt ───────┘                        │
                ▲──────────────── measured φ ──────┘   (feedback)
   P = stiffness (spring) | D = damping (friction) | I = removes steady bias
```

**Tuning the response — the P/D balance is everything** on attitude:

```
 too little D (under-damped):  fast but OVERSHOOTS and rings — wobbly, can go unstable
 too much   D (over-damped):   smooth but SLUGGISH, slow to reach the target
 right P/D:                    crisp rise, little overshoot, quick settle (critically-ish damped)
 add I:                        removes any residual offset (trim, wind) — but watch windup
```

Drag the damping slider on a model second-order step response to feel it:

```plot
{"title": "Attitude step response — drag damping (P fixed): more D ⇒ less overshoot", "xLabel": "time (s)", "yLabel": "roll angle (normalised)", "xRange": [0, 6], "yRange": [0, 1.8], "controls": [{"name": "z", "label": "damping ratio ζ", "range": [0.1, 1.5], "step": 0.05, "value": 0.3}], "functions": [{"expr": "1 - exp(-z*3*x) * cos(3*x*sqrt(abs(1-z*z)))", "label": "step response (ζ sets overshoot)", "color": "#2563eb"}]}
```

(Low ζ rings and overshoots; ζ ≈ 0.7 is the classic crisp-with-little-overshoot
sweet spot; ζ ≥ 1 is over-damped and sluggish — exactly the P/D trade-off above.)

**Practical notes for real drones:** the **D term amplifies noise** (differentiating a
gyro signal), so it's filtered and/or replaced by direct rate feedback; **gains scale
with inertia** (a bigger drone needs bigger `K_p`); and the same PID structure repeats
for **all three axes** (roll, pitch, yaw) and the altitude/position loops, with
different gains.

The big picture: PID on the **decoupled double-integrator** attitude model gives a
fast, stable inner loop — P for stiffness, D for damping, I for bias — and nesting it
inside the cascade stabilizes the whole vehicle. You'll implement a PID roll
stabilizer next and watch a disturbed roll angle converge to the commanded attitude.
""",
        ),
        _code(
            "PID stabilization of a 1-axis (roll) attitude model",
            "14 min",
            r"""# We stabilize ONE axis (roll) of the linearized hover model. The plant is a double
# integrator phidot_dot = tau / J_xx (open-loop unstable). A PID controller drives the
# roll angle from an initial disturbance to a commanded setpoint. Integrated with
# explicit Euler in a straight-line MODULE-LEVEL loop. Deterministic. numpy.

import numpy as np

Jxx = 0.02          # roll moment of inertia (kg m^2)
dt = 0.004          # 250 Hz inner loop
steps = 1000        # 4 seconds

# PID gains (tuned for a crisp, lightly-damped response on this plant).
Kp = 0.9
Ki = 0.6
Kd = 0.18

setpoint = np.radians(0.0)        # command: level (0 deg roll)
phi = np.radians(25.0)            # initial disturbance: rolled 25 deg
phidot = 0.0                      # initial roll rate
integral = 0.0
prev_err = setpoint - phi

phi_hist = np.zeros(steps)
tau_hist = np.zeros(steps)
for i in range(steps):
    err = setpoint - phi
    integral = integral + err * dt
    deriv = (err - prev_err) / dt           # ~ -phidot (rate feedback)
    prev_err = err
    tau = Kp * err + Ki * integral + Kd * deriv      # PID torque

    # Plant: double integrator, phi_dot_dot = tau / J. Semi-implicit Euler (velocity first).
    ang_acc = tau / Jxx
    phidot = phidot + ang_acc * dt
    phi = phi + phidot * dt
    phi_hist[i] = np.degrees(phi)
    tau_hist[i] = tau

# Settling: first time |phi| stays within 1 deg of the setpoint for the rest of the run.
within = np.abs(phi_hist - np.degrees(setpoint)) <= 1.0
settle_idx = steps - 1
for i in range(steps):
    if bool(np.all(within[i:])):
        settle_idx = i
        break

print("plant: double integrator phi'' = tau/Jxx (open-loop UNSTABLE)")
print("PID gains: Kp=%.2f Ki=%.2f Kd=%.2f" % (Kp, Ki, Kd))
print(" t(s)    roll(deg)    torque(N m)")
for i in [0, 25, 50, 100, 200, 400, 999]:
    print("  %4.2f   %8.2f    %9.4f" % (i * dt, phi_hist[i], tau_hist[i]))
print()
print("start 25.0 deg -> final %.3f deg (commanded 0)" % phi_hist[-1])
print("settled within 1 deg after %.2f s" % (settle_idx * dt))
print("P supplies the restoring 'spring', D the damping, I removes residual offset:")
print("feedback stabilizes an inherently unstable axis and drives it to the setpoint.")
""",
        ),
        quiz_lesson(
            "Quiz: Quadrotor Dynamics & Control",
            (
                q(
                    "In the Newton–Euler equations, what is the ω × (Jω) term in J ω̇ = τ − ω × (Jω)?",
                    (
                        opt(
                            "The gyroscopic / Coriolis coupling that arises from writing the rotation in the rotating body frame; it couples the axes and causes precession",
                            correct=True,
                        ),
                        opt("The gravitational torque"),
                        opt("The thrust force"),
                        opt("A numerical integration error"),
                    ),
                    "Euler's equation is written in the body frame (so J is constant); the ω×Jω term is the torque-free coupling. Near hover (small rates) it ≈ 0 and the axes decouple.",
                ),
                q(
                    "Why are the quadrotor equations of motion underactuated, leading to cascaded control?",
                    (
                        opt(
                            "Thrust T and torques τ enter different equations — torques set attitude, and attitude sets the direction of T, so horizontal acceleration is commanded only through attitude",
                            correct=True,
                        ),
                        opt("Because there are more motors than states"),
                        opt("Because gravity is ignored"),
                        opt("Because the equations are linear and decoupled"),
                    ),
                    "4 inputs for 6 DOF: you can't command ẍ directly, only via tilt (ẍ ≈ −g·θ near hover). Hence an attitude inner loop nested inside a position outer loop.",
                ),
                q(
                    "Why is RK4 usually preferred over explicit Euler for simulating flight dynamics?",
                    (
                        opt(
                            "RK4 samples the derivative at four points and is 4th-order accurate, so it allows much larger time steps for the same accuracy (Euler is 1st-order and can inject energy)",
                            correct=True,
                        ),
                        opt("RK4 needs no time step"),
                        opt("Euler is always more accurate than RK4"),
                        opt("RK4 only works for linear systems"),
                    ),
                    "Euler holds the slope flat (global error ∝ dt, can pump energy); RK4 averages four slopes (global error ∝ dt⁴), winning despite 4× per-step cost. Semi-implicit Euler is energy-stable and cheap.",
                ),
                q(
                    "Near hover, the linearized single-axis attitude dynamics reduce to what, and why must it be actively controlled?",
                    (
                        opt(
                            "A double integrator (φ̈ ≈ τ/J) — open-loop unstable with no natural restoring force, so feedback is required to keep it level",
                            correct=True,
                        ),
                        opt("A stable first-order lag that self-corrects"),
                        opt("A constant, needing no control"),
                        opt("A nonlinear chaotic system that cannot be controlled"),
                    ),
                    "Linearizing about hover decouples the axes into double integrators (two poles at the origin). With no restoring force, any disturbance drifts away — it must be stabilized by feedback.",
                ),
                q(
                    "Why must each loop in a cascaded controller be much faster than the loop outside it?",
                    (
                        opt(
                            "Timescale separation (~5–10×) lets the outer loop treat the inner as instantaneous, so the loops can be designed independently and don't fight/oscillate",
                            correct=True,
                        ),
                        opt("To save battery power"),
                        opt("So all loops run at exactly the same rate"),
                        opt("Faster inner loops are only for cosmetic reasons"),
                    ),
                    "The fast inner (rate/attitude) loop rejects disturbances and appears instant to the slow outer (position) loop; violating the separation makes the loops interact and oscillate.",
                ),
                q(
                    "In PID attitude control of the double-integrator plant, what do the P and D terms each provide?",
                    (
                        opt(
                            "P provides the restoring 'spring' (stiffness) the plant lacks; D provides 'friction' (damping) that kills the oscillation P alone would cause — D ≈ rate feedback",
                            correct=True,
                        ),
                        opt("P provides damping and D provides stiffness"),
                        opt("Both P and D remove steady-state error"),
                        opt("Neither affects stability"),
                    ),
                    "On a double integrator, P alone is an undamped spring (rings); adding D (≈ −φ̇, gyro rate feedback) damps it. I removes steady-state bias but risks windup.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# aerial-advanced
# ──────────────────────────────────────────────────────────────────────

_AER_ADVANCED = SeedCourse(
    slug="aerial-advanced",
    title="Aerial Robotics / UAVs — Advanced",
    description=(
        "Knowing where you are and how to get there: UAV state estimation (IMU "
        "gyro/accel models, the complementary filter, the EKF for attitude/position, "
        "GPS+IMU fusion and drift), trajectory generation (waypoints and the "
        "minimum-snap idea), a brief on fixed-wing flight dynamics, and the GNC "
        "stack and sim-to-real gap. With runnable Python labs — a complementary "
        "attitude filter and a 1-D Kalman filter fusing IMU and GPS — and an "
        "estimate-vs-truth plot."
    ),
    level="Advanced",
    lessons=(
        _t(
            "UAV state estimation & IMU models",
            "12 min",
            r"""# UAV state estimation & IMU models

A flight controller can only stabilize and navigate what it can **measure** — but no
sensor reports attitude, velocity, or position directly and cleanly. **State
estimation** fuses the noisy, partial, drifting sensors into the best estimate of the
full state. It starts with the sensor at the heart of every drone: the **IMU**.

**The IMU (Inertial Measurement Unit)** combines two (often three) sensors:

- A **3-axis gyroscope** measures **angular rate** `ω = (p, q, r)` in the body frame.
- A **3-axis accelerometer** measures **specific force** — the sum of true
  acceleration and the reaction to gravity (`a_meas = a_true − g` in the body frame).
- Often a **3-axis magnetometer** (compass) for absolute heading (yaw).

**The gyroscope model — great short-term, drifts long-term.** A real gyro reports

$$ \omega_{\text{meas}} = \omega_{\text{true}} + b_g + n_g $$

a **bias `b_g`** (a slowly-varying offset) plus white **noise `n_g`**. To get *angle*
you **integrate** the rate — but integration also **integrates the bias**, so the
angle estimate **drifts linearly with time** (a tiny 0.5°/s bias becomes 30° of error
in a minute). Gyros are trustworthy over **short** intervals (high frequency), useless
alone over **long** ones.

**The accelerometer model — great long-term, noisy short-term.** When the drone is
**not accelerating**, the accelerometer reads pure **gravity**, so its direction gives
the **tilt angle** absolutely (no drift — gravity is always "down"):

$$ \phi_{\text{accel}} = \operatorname{atan2}(a_y, a_z), \qquad \theta_{\text{accel}} = \operatorname{atan2}(-a_x, \sqrt{a_y^2 + a_z^2}) $$

But the moment the vehicle **maneuvers**, its own acceleration contaminates the
gravity reading, and the sensor is **noisy and vibration-sensitive**. So the accel is
trustworthy over the **long** term (drift-free) but bad over the **short** term.

```
   gyro:   ω + bias + noise → INTEGRATE → angle    (smooth short-term, DRIFTS)
   accel:  gravity direction → angle               (drift-free long-term, NOISY)
                       └──── complementary errors ────┘
                    fuse them → an estimate good at ALL timescales
```

**The fusion imperative.** The gyro and accelerometer have **exactly complementary**
error characteristics — one good where the other is bad. **Neither alone gives a usable
attitude**, but **fused** they do: trust the gyro at high frequency, the accel at low
frequency. That is the whole game of attitude estimation, and the **complementary
filter** (next) and the **EKF** are two ways to do the fusion.

For **position** the story repeats with GPS: GPS is **absolute but noisy and slow**
(1–10 Hz, metre-level), while accelerometers integrated **twice** give smooth,
high-rate position that **drifts badly** (double integration of bias → error grows as
`t²`). Fusing GPS + IMU gives smooth, drift-free position — the core of every
navigation system, and the subject of the GPS+IMU lab.

The mindset: **every UAV sensor is flawed, but their flaws are complementary**, and
estimation is the art of fusing them into a state estimate good enough to fly on. We
start with the lightest fusion — the complementary filter.
""",
        ),
        _t(
            "The complementary filter for attitude",
            "11 min",
            r"""# The complementary filter for attitude

The cheapest, most widely-deployed attitude estimator on small drones is the
**complementary filter**. With one constant and almost no computation it fuses the
gyro and accelerometer into a drift-free, smooth tilt estimate — no matrices, no
covariances. It is the perfect first fusion algorithm because it makes the
"complementary errors" idea literal.

**The recipe.** Recall the two sensors' opposite flaws:

- **Gyro-integrated angle** — smooth and responsive, but **drifts** (integrated bias).
- **Accelerometer angle** — **drift-free** (always sees gravity), but **noisy**.

The complementary filter blends them so each is trusted in its **good frequency band**:
**high-pass** the gyro estimate (keep its fast, accurate part; reject its slow drift)
and **low-pass** the accel estimate (keep its slow, accurate part; reject its fast
noise), then add:

$$ \theta_k = \alpha\,\bigl(\theta_{k-1} + \omega_{\text{gyro}}\,\Delta t\bigr) + (1-\alpha)\,\theta_{\text{accel}} $$

Read the structure: take the previous estimate, **propagate it with the gyro rate**
(the `θ + ω·dt` term — pure integration), then **nudge it toward the accelerometer
angle** by a small fraction `(1−α)`. The gyro provides the smooth backbone; the accel
provides a slow, persistent correction that **cancels the drift**.

```
   gyro rate ─►[ integrate ]─►[ HIGH-PASS  (α) ]─┐
                                                 ├─(+)─► fused tilt θ
   accel ─────►[ angle ]──────►[ LOW-PASS (1−α) ]─┘
   α near 1 → lean on the gyro (smooth, but drift creeps if too high)
   α lower  → lean on the accel (drift-free, but noisier)
```

**The one knob, α.** Typically **0.95–0.99**. It sets the **crossover frequency**
between trusting the gyro and trusting the accel. The two weights `α` and `(1−α)`
**always sum to one** — that is the "complementary" in the name: it is a frequency-
weighted average that hands each band to its best sensor. A useful relation:
`α = τ / (τ + Δt)`, where `τ` is the filter time constant — bigger `τ` (α closer to 1)
trusts the gyro longer before the accel pulls it back.

**Relationship to the Kalman filter.** The complementary filter is essentially a
**steady-state, hand-tuned Kalman filter** for this 1-D attitude problem — `(1−α)`
plays the role of a fixed Kalman gain, set by hand instead of computed online from
covariances. You give up the KF's adaptivity (a true KF would **estimate and remove**
the gyro bias and adapt its gain) and its uncertainty output, in exchange for **trivial
cost** — which is why it runs on the tiniest flight controllers.

```
 complementary filter:  one α, no matrices, fixed trust   → tiny MCUs, attitude
 EKF:                    estimates bias, adapts gain, gives covariance, fuses GPS
                         → full navigation (next lesson)
```

The takeaway: the complementary filter captures the **entire essence of sensor fusion**
— combine a smooth-but-drifting source with a noisy-but-absolute one, weighting each
where it's reliable — in a single line of code. You'll implement it in the lab and
watch it beat *both* raw sensors. When you need bias estimation, position, and honest
uncertainty, you graduate to the EKF — next.

The complementary filter in **MATLAB** (run it in the MATLAB REPL):

```matlab
dt = 0.01; alpha = 0.98; n = 400;
k = 1:n;
gyro = 0.5 * ones(1, n);                      % near-constant rate (rad/s)
acc_angle = 0.5*dt*k + 0.03*sin(0.3*k);       % noisy absolute tilt
angle = 0; est = zeros(1, n);
for i = 1:n
  angle = alpha*(angle + gyro(i)*dt) + (1-alpha)*acc_angle(i);
  est(i) = angle;
end
disp('final fused tilt:'); disp(est(end))
```
""",
        ),
        _t(
            "The EKF for attitude & position",
            "12 min",
            r"""# The EKF for attitude & position

When a UAV needs more than a tilt angle — full attitude, **velocity**, **position**,
estimated sensor **biases**, and an honest **uncertainty** — the workhorse is the
**Extended Kalman Filter (EKF)**. It is the standard navigation estimator in PX4,
ArduPilot, and essentially every serious autopilot, because flight is **nonlinear** and
the EKF is the Kalman filter adapted to nonlinear models.

**Why nonlinear?** A UAV's models are full of trig and cross products: the attitude
kinematics `q̇ = ½ q⊗ω`, rotating body acceleration into the world frame `R(q)·a`,
GPS measuring position as a nonlinear function of state. The ordinary (linear) Kalman
filter doesn't apply directly, so the EKF **linearizes** the models at each step.

**The recap of the Kalman idea.** The filter maintains a state estimate `x̂` and a
**covariance `P`** (its uncertainty), and runs two steps forever:

- **Predict** — propagate the state through the (nonlinear) motion model and **grow**
  the covariance by the process noise `Q`. (Belief spreads.)
- **Update** — when a measurement arrives, fold it in, weighting it against the
  prediction by the **Kalman gain**, and **shrink** the covariance. (Belief sharpens.)

**The nonlinear models and their Jacobians.** With motion `f` and measurement `h`
nonlinear,

$$ x_t = f(x_{t-1}, u_t) + w, \qquad z_t = h(x_t) + v $$

the EKF replaces the linear `F, H` with **Jacobians** — matrices of partial
derivatives evaluated at the current estimate, recomputed every step:

$$ F = \left.\frac{\partial f}{\partial x}\right|_{\hat{x}}, \qquad H = \left.\frac{\partial h}{\partial x}\right|_{\hat{x}} $$

**The EKF loop** — Kalman equations with `f`/`h` for the means, Jacobians for the
covariances:

$$ \hat{x}^- = f(\hat{x}, u), \qquad P^- = F P F^\top + Q $$
$$ y = z - h(\hat{x}^-), \quad S = H P^- H^\top + R, \quad K = P^- H^\top S^{-1} $$
$$ \hat{x} = \hat{x}^- + K y, \qquad P = (I - K H)\,P^- $$

```
 PREDICT (fast, IMU-driven):  push state by gyro/accel, grow P by Q
 UPDATE  (slow, GPS/mag/baro): correct state, shrink P, weighted by Kalman gain
   high-rate prediction + low-rate corrections = smooth, drift-free, high-rate estimate
```

**What a UAV EKF estimates** (a typical 15–24 state navigation filter): attitude
(quaternion), velocity, position, **and the gyro and accel biases** — estimating the
biases is the EKF's big win over the complementary filter, because it actively removes
the very drift source the complementary filter only suppresses. It also **outputs `P`**,
so the autopilot knows *how much to trust its own estimate* (e.g. to refuse a mission
if uncertainty is too high).

**The architecture in practice:** the **IMU drives the fast predict step** (hundreds of
Hz), propagating attitude/velocity/position by integrating gyro and accel; the slower,
absolute sensors (**GPS, magnetometer, barometer**) drive **update steps** that pin
down the drift. This "IMU predicts, aiding sensors correct" pattern is the spine of all
inertial navigation.

**Caveats** (inherited from the EKF's linearization): the Jacobians must be **correct**
(a common bug source), and strong nonlinearity over a large uncertainty can make the
filter **inconsistent or diverge** — which is why autopilots monitor innovation
consistency and why some have moved to the **UKF** or **error-state KF** (which
linearizes the small *error*, behaving better for attitude). Still, the EKF remains the
default. You'll build a 1-D version — fusing IMU-driven prediction with GPS position —
in the lab.
""",
        ),
        _t(
            "GPS + IMU fusion & drift",
            "11 min",
            r"""# GPS + IMU fusion & drift

Position estimation is where the EKF earns its keep, because the two sensors that give
it — the **IMU** and **GPS** — fail in exactly opposite ways, and only their fusion
yields position good enough to fly autonomous missions on.

**The IMU path — dead reckoning, and why it drifts catastrophically.** You can get
position from the IMU by **integrating acceleration twice**: accel → velocity →
position. It is **smooth and high-rate** (hundreds of Hz, no dropouts). But any
constant accelerometer bias `b_a` becomes, after **double integration**, a position
error that grows as

$$ \Delta x(t) \approx \tfrac{1}{2}\, b_a\, t^2 $$

— **quadratically in time**. A tiny 0.01 m/s² bias is ~18 m of error after 60 s, and
it only accelerates. Pure inertial navigation drifts away **fast**; it is great for
**short** intervals, hopeless for **long** ones.

**The GPS path — absolute, but noisy and slow.** GPS gives **absolute** position
(fixed to the earth, no drift) — but it is **noisy** (metre-level), **slow**
(1–10 Hz), and can **drop out** (tunnels, indoors, urban canyons, under bridges). Great
**long-term** (bounds the error), bad **short-term** (jittery, low-rate, intermittent).

```
   IMU (double integrate):  smooth, fast, but DRIFTS as ~½·b·t²   (good short-term)
   GPS:                     absolute, drift-free, but NOISY/SLOW   (good long-term)
                              └──── complementary errors again ────┘
              EKF fusion → smooth, high-rate, drift-free position
```

**The fusion — the same predict/update rhythm.** This maps perfectly onto the EKF:

- **Predict with the IMU** at high rate — integrate accel/gyro to propagate position,
  velocity, attitude. Between GPS fixes, the IMU **coasts** the estimate smoothly and
  at full bandwidth.
- **Update with GPS** whenever a fix arrives — correct the accumulated drift, pulling
  the position back to absolute truth and (crucially) **re-estimating the
  accelerometer bias** so the next prediction drifts less.

The result is **better than either sensor alone**: GPS's absolute accuracy **bounds**
the IMU's drift, while the IMU's high rate and smoothness **fill the gaps** between (and
through brief dropouts of) GPS — the classic **GPS-aided inertial navigation system
(GPS/INS)** at the core of every outdoor drone, aircraft, and missile.

**Handling GPS dropout.** When GPS is lost, the filter **predicts only** (IMU
dead-reckoning); the estimate stays smooth but its **covariance `P` grows** — the filter
*honestly reports rising uncertainty*. When GPS returns, the update **snaps** the
estimate back and `P` collapses. (Aggressive snapping can jolt the controller, so
filters limit correction rate.) This is why the **covariance output matters**: it tells
the mission planner when dead-reckoning has drifted too far to trust.

**Beyond GPS.** Indoors or in GPS-denied settings, the *same fusion structure* swaps
GPS for other absolute/aiding sensors — **visual odometry / VIO** (camera + IMU),
**LIDAR**, **optical flow**, **UWB beacons**, **barometer** (altitude) — each acting as
the drift-correcting "GPS-like" update on top of IMU prediction. The pattern is
universal: **a fast-but-drifting inertial predictor corrected by a slow-but-absolute
aiding sensor.**

The lab builds exactly this in 1-D: an IMU-driven prediction (which would drift) fused
with noisy GPS position updates by a Kalman filter — and you'll see the fused estimate
beat both the drifting dead-reckoning and the noisy GPS.
""",
        ),
        _code(
            "Complementary filter for tilt (gyro + accel)",
            "14 min",
            r"""# A complementary filter fuses a DRIFTING integrated-gyro angle with a NOISY but
# drift-free accelerometer angle:  theta = a*(theta + gyro*dt) + (1-a)*accel_angle.
# We synthesize deterministic sensor signals (gyro with a bias, accel with noise),
# run the filter in a straight-line MODULE-LEVEL loop, and compare RMS errors. numpy.

import numpy as np

dt = 0.01           # 100 Hz IMU
steps = 1500        # 15 seconds
t = np.arange(steps) * dt

# Ground-truth tilt: a smooth maneuver (deg) and its exact derivative (deg/s).
truth = 20.0 * np.sin(0.4 * t) + 5.0 * np.sin(1.1 * t)
true_rate = 20.0 * 0.4 * np.cos(0.4 * t) + 5.0 * 1.1 * np.cos(1.1 * t)

# Gyro: true rate + constant BIAS + small noise -> integrating it DRIFTS.
gyro_bias = 1.5                                   # deg/s bias (the drift source)
raw_g = np.sin(11.0 * t) + np.sin(23.0 * t + 0.5)
gyro = true_rate + gyro_bias + 0.3 * (raw_g - raw_g.mean()) / raw_g.std()

# Accelerometer-derived angle: drift-free but NOISY (deterministic noise).
raw_a = np.sin(7.0 * t) + np.sin(17.0 * t + 1.0) + np.sin(29.0 * t + 2.0)
accel_angle = truth + 4.0 * (raw_a - raw_a.mean()) / raw_a.std()

alpha = 0.98        # crossover: lean on gyro short-term, accel long-term
gyro_only = np.zeros(steps)
fused = np.zeros(steps)
g_int = 0.0
f_est = accel_angle[0]
for i in range(steps):
    g_int = g_int + gyro[i] * dt                                  # pure integration -> drifts
    f_est = alpha * (f_est + gyro[i] * dt) + (1.0 - alpha) * accel_angle[i]
    gyro_only[i] = g_int
    fused[i] = f_est

err_gyro = float(np.sqrt(np.mean((gyro_only - truth) ** 2)))
err_accel = float(np.sqrt(np.mean((accel_angle - truth) ** 2)))
err_fused = float(np.sqrt(np.mean((fused - truth) ** 2)))
print("complementary attitude filter (alpha = %.2f), %d Hz, %.0f s" % (alpha, int(1.0 / dt), steps * dt))
print("RMS tilt error (deg):")
print("  gyro-only (integrated, drifts): %6.2f" % err_gyro)
print("  accel-only (noisy):             %6.2f" % err_accel)
print("  complementary (fused):          %6.2f" % err_fused)
print("final drift of gyro-only = %.1f deg (bias %.1f deg/s integrated over %.0f s)"
      % (gyro_only[-1] - truth[-1], gyro_bias, steps * dt))
print("fusion beats BOTH: high-pass the gyro (kill drift), low-pass the accel (kill noise).")
""",
        ),
        _code(
            "GPS + IMU fusion: a 1-D Kalman filter",
            "15 min",
            r"""# A 1-D navigation Kalman filter fuses an IMU-driven PREDICTION (acceleration
# integrated to position+velocity, which DRIFTS due to bias) with noisy, slow GPS
# position UPDATES. State x = [position, velocity]. All matrix algebra (F P F',
# K = P H' inv(S)) runs at MODULE LEVEL in a straight-line loop. Deterministic. numpy.

import numpy as np

dt = 0.02           # 50 Hz IMU prediction
steps = 1000        # 20 seconds
gps_every = 25      # GPS update every 25 steps -> 2 Hz

# Model: constant-velocity, position-only GPS measurement.
F = np.array([[1.0, dt], [0.0, 1.0]])            # state transition
B = np.array([[0.5 * dt * dt], [dt]])            # control (acceleration) input
H = np.array([[1.0, 0.0]])                       # GPS sees position only
Q = np.array([[1e-4, 0.0], [0.0, 1e-3]])         # process-noise covariance
R = np.array([[4.0]])                            # GPS variance (sigma = 2 m)
I2 = np.eye(2)

# Ground truth: a smooth trajectory. True acceleration drives it.
k = np.arange(steps)
true_acc = 0.5 * np.sin(0.05 * k)
true_pos = np.zeros(steps)
true_vel = np.zeros(steps)
pos = 0.0
vel = 0.0
for i in range(steps):
    vel = vel + true_acc[i] * dt
    pos = pos + vel * dt
    true_pos[i] = pos
    true_vel[i] = vel

# IMU accelerometer = true accel + constant BIAS + noise -> dead-reckoning DRIFTS.
accel_bias = 0.05
raw = np.sin(3.1 * k) + np.sin(7.7 * k + 1.0) + np.sin(15.3 * k + 2.0)
imu_acc = true_acc + accel_bias + 0.02 * (raw - raw.mean()) / raw.std()

# Deterministic GPS measurement noise.
raw2 = np.sin(2.3 * k) + np.sin(5.9 * k + 0.7) + np.sin(12.1 * k + 1.7)
gps_noise = 2.0 * (raw2 - raw2.mean()) / raw2.std()
gps_meas = true_pos + gps_noise

# Pure IMU dead-reckoning (no GPS) for comparison -> shows the drift.
dr_pos = np.zeros(steps)
dr_p = 0.0
dr_v = 0.0
for i in range(steps):
    dr_v = dr_v + imu_acc[i] * dt
    dr_p = dr_p + dr_v * dt
    dr_pos[i] = dr_p

# The fused Kalman filter: IMU drives PREDICT, GPS drives UPDATE.
x = np.array([[0.0], [0.0]])
P = np.array([[1.0, 0.0], [0.0, 1.0]])
est_pos = np.zeros(steps)
for i in range(steps):
    # PREDICT with the (biased) IMU acceleration as the control input.
    u = np.array([[imu_acc[i]]])
    x = F @ x + B @ u
    P = F @ P @ F.T + Q
    # UPDATE with GPS when a fix is available.
    if i % gps_every == 0:
        z = np.array([[gps_meas[i]]])
        y = z - H @ x                             # innovation
        S = H @ P @ H.T + R
        Kgain = P @ H.T @ np.linalg.inv(S)
        x = x + Kgain @ y
        P = (I2 - Kgain @ H) @ P
    est_pos[i] = float(x[0, 0])

err_dr = float(np.sqrt(np.mean((dr_pos - true_pos) ** 2)))
err_gps = float(np.sqrt(np.mean((gps_meas - true_pos) ** 2)))
err_fused = float(np.sqrt(np.mean((est_pos - true_pos) ** 2)))
print("GPS/INS fusion: 50 Hz IMU predict, 2 Hz GPS update, %.0f s" % (steps * dt))
print("RMS position error (m):")
print("  IMU dead-reckoning (drifts): %7.2f" % err_dr)
print("  GPS-only (noisy):            %7.2f" % err_gps)
print("  fused Kalman estimate:       %7.2f" % err_fused)
print("IMU coasts smoothly between fixes; GPS bounds the drift; fusion beats both.")
""",
        ),
        _t(
            "Trajectory generation: waypoints & minimum snap",
            "11 min",
            r"""# Trajectory generation: waypoints & minimum snap

Knowing the state (estimation) and being able to track a reference (control) is not
enough — the autopilot also needs a **reference to track**: a smooth, dynamically
feasible **trajectory** through space and time. **Trajectory generation** turns a few
**waypoints** ("go here, then here") into a continuous `x(t)` the controller can
follow.

**Why not just fly straight lines between waypoints?** A piecewise-linear path has
**corners** — points of infinite curvature. Following one would demand an **instant**
change of velocity (infinite acceleration), which the rotors cannot produce; the drone
would overshoot the corner, slow to a stop, or shudder. We need a path that is **smooth
in its higher derivatives**, not just continuous in position.

**How smooth? The differential-flatness insight.** A quadrotor is **differentially
flat**: its entire state and all four inputs can be written as functions of the
**position** (`x, y, z`) and **yaw** (`ψ`) and their derivatives. This is a powerful
gift — it means we can **plan purely in position/yaw space** and recover the required
attitude and thrust algebraically, *provided the position trajectory is smooth enough*.
How smooth? Because **thrust** depends on acceleration and **body torque** (hence motor
commands) depends on the **snap** (the 4th derivative of position), a trajectory with
**continuous snap** maps to **smooth, feasible motor commands**.

**Minimum-snap trajectories.** The celebrated result (Mellinger & Kumar, 2011): generate
the trajectory that **minimizes the integral of snap squared** subject to passing
through the waypoints:

$$ \min \int_0^T \left\lVert \frac{d^4 \mathbf{r}(t)}{dt^4} \right\rVert^2 dt $$

The minimizer is a set of **piecewise polynomials** (typically degree 7+) joining the
waypoints, with continuity of position, velocity, acceleration, jerk, and snap enforced
at the junctions. Minimizing snap directly **minimizes the aggressiveness of the motor
commands**, giving trajectories that are both **smooth** and **aggressive yet
feasible** — exactly the fast, graceful flips and slaloms quadrotors are famous for.

```
 waypoints:      ●        ●          ●         ●
                  \      / \        /  ...
 straight lines:   \    /   \      /   → CORNERS = infinite curvature = infeasible
 min-snap poly:    ╭──────────────────╮  → smooth through velocity..SNAP,
                  ●                     ●    feasible & efficient motor commands
```

**The full pipeline** that produces a flyable trajectory:

```
 path planner (A*, RRT*) → waypoints → time allocation (how long per segment)
   → min-snap polynomial fit → reference x(t), and (via flatness) attitude + thrust
   → fed to the cascaded controller as the setpoint
```

**Practical pieces:** **time allocation** (how long to spend on each segment) strongly
affects feasibility and is often optimized jointly; **corridor / collision constraints**
keep the smooth path inside free space; and **replanning** handles dynamic obstacles. The
broader family (minimum-jerk, polynomial splines, and modern **MPC**, which optimizes the
trajectory online over a receding horizon) all share the goal: a **smooth, feasible,
optimal** reference.

The takeaway: trajectory generation bridges *discrete* planning (waypoints) and
*continuous* control (a reference `x(t)`), and **minimum-snap** is the canonical method
— it exploits the quad's differential flatness to make the smoothest path *also* the
most feasible one. With estimation, control, and now reference generation, only one
piece remains: assembling them into the full **GNC** stack and crossing the
**sim-to-real** gap.
""",
        ),
        _t(
            "Fixed-wing dynamics, GNC & sim-to-real",
            "12 min",
            r"""# Fixed-wing dynamics, GNC & sim-to-real

We close the track by widening the lens: a brief look at **fixed-wing** flight (a
different way to make lift), the **GNC** stack that ties everything together, and the
**sim-to-real** gap that separates a working simulation from a flying robot.

**Fixed-wing flight dynamics — the four forces.** A fixed-wing UAV gets lift from a
**wing** moving through the air, balancing **four forces**:

- **Lift `L`** — perpendicular to airflow, `L = ½ ρ V² S C_L(α)`. It grows with the
  **square of airspeed** `V` and with the **angle of attack `α`** (wing-to-airflow
  angle) — up to a point.
- **Weight `mg`** — down; in steady level flight **`L = mg`**.
- **Thrust `T`** — forward, from a propeller/jet; in steady cruise **`T = D`**.
- **Drag `D`** — opposing motion, `D = ½ ρ V² S C_D`.

```
            L (lift)
            ▲
            │
   D ◄──────●──────► T        steady level flight:  L = mg,  T = D
            │
            ▼
           mg (weight)
```

**The critical difference from a multirotor: the stall.** Lift rises with angle of
attack only until `α` reaches a **critical angle** (~15°); beyond it the airflow
**separates** from the wing, lift **collapses**, and the aircraft **stalls** and falls.
There is also a **minimum airspeed** below which the wing cannot make enough lift. So a
fixed-wing **must keep flying forward** — it cannot hover or slow below stall speed,
the fundamental constraint multirotors don't have. **Static stability** (a well-designed
plane naturally returns to level after a disturbance, thanks to tail surfaces and CG
placement) is a key advantage — unlike the inherently-unstable multirotor, a good
fixed-wing partly stabilizes *itself*. Control is via **aerodynamic surfaces**
(ailerons = roll, elevator = pitch, rudder = yaw) whose effectiveness **scales with
airspeed** (no airspeed → no control authority).

**GNC — Guidance, Navigation & Control** — the standard decomposition that organizes the
whole autonomy stack (and names what we've built):

```
   NAVIGATION ──► "Where am I?"      (state estimation: IMU/GPS fusion, EKF)
   GUIDANCE   ──► "Where should I go?" (trajectory generation, path planning)
   CONTROL    ──► "How do I get there?" (cascaded PID / the control loops)
        └── Navigation feeds Control the state; Guidance feeds it the reference ──┘
```

Every autonomous vehicle — drone, plane, rocket, spacecraft, self-driving car — runs
this loop: **estimate (N) → plan (G) → actuate (C)**, closed at high rate. This track
built all three for a quadrotor.

**The sim-to-real gap.** A controller that flies perfectly in simulation often fails on
hardware, because the real world adds what the model omitted:

- **Unmodeled dynamics** — motor lag, prop aerodynamics, airframe flex, the
  **ground effect** near surfaces, aerodynamic interactions between rotors.
- **Sensor reality** — noise, **bias drift**, vibration, latency, time
  synchronization, and limited sample rates (the very reasons we needed estimation).
- **Actuator limits** — saturation, deadbands, **battery sag** changing the thrust map
  mid-flight, ESC delays.
- **Disturbances** — wind, gusts, turbulence, payload changes.

**Crossing the gap:** higher-fidelity simulation and **domain randomization** (train/tune
across randomized parameters so the controller is **robust** to the unknown true
values), careful **system identification** (measure the real inertia, thrust constants,
delays), **robust/adaptive control** (margins and online adaptation), and **incremental
flight testing** (tethered → low/slow → full envelope). The discipline: **trust
simulation for design, but validate relentlessly on hardware** — the model is a map, not
the territory.

**The throughline of the whole track:** an aerial robot is **rigid-body dynamics**
(frames, attitude, EOM) made to fly by **feedback control** (cascaded PID stabilizing
an unstable, underactuated plant), pointed where you want by **trajectory generation**,
and told where it is by **state estimation** that fuses flawed but complementary sensors
— all wrapped in the **GNC** loop and hardened against the **sim-to-real** gap. From a
hovering quad to a long-range fixed-wing, it is the same physics and the same loop,
applied with ever more autonomy.
""",
        ),
        quiz_lesson(
            "Quiz: UAV Estimation, Trajectories & Flight",
            (
                q(
                    "Why must a UAV fuse its gyroscope and accelerometer for attitude?",
                    (
                        opt(
                            "Their errors are complementary: the integrated gyro is smooth but drifts (integrated bias), while the accel is drift-free (sees gravity) but noisy — fused, they're good at all timescales",
                            correct=True,
                        ),
                        opt("Both sensors are perfect, so fusion is for redundancy only"),
                        opt("The gyro measures position and the accelerometer measures heading"),
                        opt("Fusion is only needed when GPS fails"),
                    ),
                    "Gyro: ω+bias+noise → integrate → drifts (good short-term). Accel: gravity direction → angle, drift-free but noisy (good long-term). Complementary filter / EKF fuses them.",
                ),
                q(
                    "In the complementary filter θ = α(θ + ω·dt) + (1−α)·θ_accel, what does α do?",
                    (
                        opt(
                            "It sets the crossover: high-passes the drift-prone gyro and low-passes the noisy accel; α and (1−α) sum to one (≈ a fixed-gain Kalman filter)",
                            correct=True,
                        ),
                        opt("It is the gyroscope bias"),
                        opt("It converts radians to degrees"),
                        opt("It must equal exactly 0.5 to work"),
                    ),
                    "α (≈0.95–0.99) trusts the gyro short-term and the accel long-term; (1−α) acts as a fixed Kalman gain. A true KF would also estimate and remove the gyro bias.",
                ),
                q(
                    "What is the EKF's key advantage over a complementary filter for UAV navigation?",
                    (
                        opt(
                            "It linearizes nonlinear models via Jacobians, fuses many sensors (IMU/GPS/mag), estimates sensor biases, and outputs an honest covariance P",
                            correct=True,
                        ),
                        opt("It needs no sensors at all"),
                        opt("It is simpler and uses no matrices"),
                        opt("It only works for linear systems"),
                    ),
                    "The EKF (predict via IMU, update via GPS/mag/baro) estimates biases — actively removing drift — and reports uncertainty P, at the cost of Jacobians and possible divergence if strongly nonlinear.",
                ),
                q(
                    "Why does pure IMU dead-reckoning for position drift so quickly, and how does GPS fusion fix it?",
                    (
                        opt(
                            "Double-integrating accelerometer bias gives position error ~ ½·b·t² (grows quadratically); GPS provides absolute fixes that bound the drift and re-estimate the bias",
                            correct=True,
                        ),
                        opt("The IMU is perfectly accurate; GPS adds the only error"),
                        opt("Drift is linear and GPS makes it worse"),
                        opt("IMU position never drifts"),
                    ),
                    "Bias double-integrated → error ∝ t². GPS is absolute but noisy/slow; the EKF predicts with the IMU (smooth, high-rate) and updates with GPS (bounds drift) — better than either alone.",
                ),
                q(
                    "Why are minimum-snap trajectories used for quadrotors instead of straight lines between waypoints?",
                    (
                        opt(
                            "Straight lines have corners (infinite curvature, infeasible); the quad is differentially flat, and minimizing snap (4th derivative of position) yields smooth, feasible motor commands",
                            correct=True,
                        ),
                        opt("Straight lines are illegal in airspace"),
                        opt("Minimum-snap trajectories are slower and that is the goal"),
                        opt("Quadrotors cannot follow polynomials"),
                    ),
                    "Body torque depends on snap, so continuous-snap polynomial trajectories (exploiting differential flatness) give smooth, feasible commands — the smoothest path is also the most flyable.",
                ),
                q(
                    "What fundamentally distinguishes fixed-wing flight from a multirotor?",
                    (
                        opt(
                            "Lift comes from forward airspeed over a wing (L = ½ρV²S·C_L), so it must keep flying above stall speed and cannot hover — but it is efficient and often statically stable",
                            correct=True,
                        ),
                        opt("Fixed-wing aircraft hover better than multirotors"),
                        opt("Fixed-wing aircraft have no need for thrust"),
                        opt("There is no difference in how they generate lift"),
                    ),
                    "A wing needs airspeed and stalls past a critical angle of attack, so a fixed-wing can't hover and must stay above stall speed; in return it's efficient, long-range, and often self-stabilizing.",
                ),
            ),
        ),
    ),
)


AERIAL_COURSES = (_AER_BASICS, _AER_INTERMEDIATE, _AER_ADVANCED)
