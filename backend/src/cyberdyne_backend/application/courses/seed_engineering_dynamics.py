"""Engineering Dynamics track: Basics -> Intermediate -> Advanced.

Particle kinematics, kinetics via Newton's laws, work-energy and impulse-momentum,
then rigid-body planar kinematics/dynamics and an introduction to vibration. Lessons
are `text` with single-backslash LaTeX, interactive ```plot blocks for trajectories,
response curves and frequency response, ```mermaid diagrams for method workflows, and
runnable ```python (NumPy/SciPy) and ```matlab code for integrating the equations of motion.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


_BASICS = SeedCourse(
    slug="engineering-dynamics-basics",
    title="Engineering Dynamics — Basics",
    description=(
        "Build physical intuition for motion: position, velocity and acceleration; "
        "rectilinear and projectile motion; relative motion; and a first reading of "
        "Newton's second law. Plenty of plots and worked numbers, minimal heavy math."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What dynamics studies",
            "10 min",
            r"""
# What dynamics studies

Statics asks when forces balance so nothing accelerates. **Dynamics** asks what happens when they do not: it links forces to *motion*. We split it into **kinematics** (the geometry of motion — position, velocity, acceleration, with no mention of cause) and **kinetics** (the link between forces/moments and the resulting motion through Newton's laws).

A **particle** is a body whose size we ignore: all its mass sits at one point. This is valid when rotation is irrelevant — a thrown ball treated as a point, a car on a long highway. When orientation matters we promote it to a **rigid body** (later courses).

The single most important kinematic fact: velocity is the time derivative of position and acceleration the derivative of velocity,
$$v=\frac{dx}{dt}, \qquad a=\frac{dv}{dt}=\frac{d^2x}{dt^2}.$$
Constant acceleration gives the familiar kinematic equations $v=v_0+at$ and $x=x_0+v_0 t+\tfrac12 a t^2$.

```mermaid
flowchart LR
  A[Mechanics] --> B[Statics: sum F = 0]
  A --> C[Dynamics]
  C --> D[Kinematics: x, v, a]
  C --> E[Kinetics: F = ma]
```

```plot
{"title": "Constant-acceleration position", "xLabel": "t (s)", "yLabel": "x (m)", "xRange": [0,5], "yRange": [0,40], "grid": true, "functions": [{"expr": "2*x + 0.5*3*x^2", "label": "x = v0 t + 1/2 a t^2", "color": "#2563eb"}]}
```

**Next:** describing straight-line motion precisely.
""",
        ),
        _t(
            "Rectilinear motion: position, velocity, acceleration",
            "12 min",
            r"""
# Rectilinear motion: position, velocity, acceleration

For motion along a line, sign carries direction. Position $x(t)$, velocity $v=\dot x$, and acceleration $a=\dot v$ are all signed scalars. A useful chain-rule identity removes time when you know $a$ as a function of $x$:
$$a\,dx = v\,dv \;\Rightarrow\; v^2 = v_0^2 + 2\!\int a\,dx.$$
For constant $a$ this collapses to $v^2=v_0^2+2a(x-x_0)$.

Reading a velocity-time graph: the **slope** is acceleration, the **area** under it is displacement. A particle can have positive position, negative velocity (moving back toward the origin) and positive acceleration (slowing that retreat) all at once — sign of each quantity is independent.

Worked example: a car brakes from $v_0=25\,$m/s at $a=-6\,$m/s$^2$. Stopping distance $d=v_0^2/(2|a|)=625/12\approx 52\,$m, stopping time $t=v_0/|a|\approx 4.2\,$s.

```plot
{"title": "Braking velocity vs time", "xLabel": "t (s)", "yLabel": "v (m/s)", "xRange": [0,5], "yRange": [0,25], "grid": true, "functions": [{"expr": "25 - 6*x", "label": "v = v0 - |a| t", "color": "#dc2626"}]}
```

```python
import numpy as np
v0, a = 25.0, -6.0
t = np.linspace(0, v0/abs(a), 200)
v = v0 + a*t
x = v0*t + 0.5*a*t**2          # displacement
print(f"stop time {t[-1]:.2f}s, distance {x[-1]:.1f}m")
```

**Next:** motion in a plane and curved paths.
""",
        ),
        _t(
            "Curvilinear motion and projectiles",
            "12 min",
            r"""
# Curvilinear motion and projectiles

In two dimensions, position is a vector $\mathbf r(t)=x\,\hat\imath+y\,\hat\jmath$, with $\mathbf v=\dot{\mathbf r}$ and $\mathbf a=\dot{\mathbf v}$. The components decouple when the acceleration is constant — exactly the **projectile** case, where gravity acts only downward:
$$x=v_0\cos\theta\,t,\qquad y=v_0\sin\theta\,t-\tfrac12 g t^2.$$
Eliminating $t$ gives the parabolic trajectory. Range on flat ground is $R=\frac{v_0^2\sin 2\theta}{g}$, maximized at $\theta=45^\circ$; maximum height is $H=\frac{v_0^2\sin^2\theta}{2g}$.

The horizontal velocity is constant (no horizontal force); only the vertical component changes. That single insight solves most projectile problems.

```plot
{"title": "Projectile path (v0=20 m/s, 45 deg)", "xLabel": "x (m)", "yLabel": "y (m)", "xRange": [0,42], "yRange": [0,12], "grid": true, "functions": [{"expr": "x - 9.81/(2*(20*0.7071)^2)*x^2", "label": "y(x)", "color": "#16a34a"}]}
```

```python
import numpy as np
v0, th, g = 20.0, np.deg2rad(45), 9.81
R = v0**2*np.sin(2*th)/g
H = (v0*np.sin(th))**2/(2*g)
print(f"range {R:.1f} m, apex {H:.1f} m")
```

**Next:** the natural axes of a curved path.
""",
        ),
        _t(
            "Normal and tangential acceleration",
            "11 min",
            r"""
# Normal and tangential acceleration

On a curved path it is natural to resolve acceleration along the path (**tangential**) and across it (**normal**). The tangential part changes *speed*; the normal part changes *direction*:
$$a_t=\frac{dv}{dt},\qquad a_n=\frac{v^2}{\rho},$$
where $\rho$ is the radius of curvature and $v$ the speed. The normal component always points toward the center of curvature. Even at constant speed ($a_t=0$) a turning body accelerates, because $a_n\ne 0$ — this is why a car in a steady curve still needs lateral grip.

For a car of mass $m$ rounding a flat curve of radius $\rho$, the friction force must supply $m v^2/\rho$. At $v=20\,$m/s and $\rho=50\,$m the required centripetal acceleration is $8\,$m/s$^2$, near $0.8g$ — at the limit of dry-tire grip.

```mermaid
flowchart LR
  A[Total acceleration a] --> B[a_t = dv/dt : speeds up/slows down]
  A --> C[a_n = v^2/rho : changes direction]
  C --> D[points toward center of curvature]
```

```plot
{"title": "Normal acceleration vs speed (rho=50 m)", "xLabel": "v (m/s)", "yLabel": "a_n (m/s^2)", "xRange": [0,30], "yRange": [0,18], "grid": true, "functions": [{"expr": "x^2/50", "label": "a_n = v^2/rho", "color": "#2563eb"}]}
```

**Next:** motion seen from a moving frame.
""",
        ),
        _t(
            "Relative motion of particles",
            "10 min",
            r"""
# Relative motion of particles

Velocity and acceleration depend on the observer. For two particles A and B viewed from a *non-rotating* translating frame, vectors simply add:
$$\mathbf r_B=\mathbf r_A+\mathbf r_{B/A},\qquad \mathbf v_B=\mathbf v_A+\mathbf v_{B/A},\qquad \mathbf a_B=\mathbf a_A+\mathbf a_{B/A}.$$
Here $\mathbf v_{B/A}$ is the velocity of B *as seen from A*. The classic application is a boat crossing a river: the boat's velocity relative to the ground is its velocity relative to the water plus the current. To go straight across, the heading must be angled upstream so the cross-stream component cancels the drift.

Example: a boat moves at $3\,$m/s relative to water; current is $1.5\,$m/s. To track straight across, $\sin\alpha=1.5/3=0.5$, so aim $30^\circ$ upstream; ground speed across is $3\cos 30^\circ\approx 2.6\,$m/s.

```plot
{"title": "Cross-stream ground speed vs heading", "xLabel": "heading from across (deg)", "yLabel": "v across (m/s)", "xRange": [0,60], "yRange": [0,3], "grid": true, "functions": [{"expr": "3*cos(x*0.01745)", "label": "3 cos(alpha)", "color": "#dc2626"}]}
```

**Next:** the bridge from kinematics to forces.
""",
        ),
        _t(
            "Newton's second law: a first look",
            "11 min",
            r"""
# Newton's second law: a first look

Kinematics describes motion; **kinetics** explains it. Newton's second law states that the net force equals mass times acceleration,
$$\sum \mathbf F = m\,\mathbf a,$$
a vector equation: it holds component by component. Mass is the measure of inertia — resistance to changes in velocity. Weight is a force, $W=mg$; on Earth $g\approx 9.81\,$m/s$^2$.

A free-body diagram (FBD) is the essential first step: isolate the body, draw every external force, choose axes, then write $\sum F_x=ma_x$ and $\sum F_y=ma_y$. For a block of mass $m$ on a frictionless incline of angle $\theta$, the only force along the slope is the weight component $mg\sin\theta$, so $a=g\sin\theta$ — independent of mass.

```mermaid
flowchart LR
  A[Isolate body] --> B[Draw all external forces - FBD]
  B --> C[Choose axes]
  C --> D[Sum F = m a per axis]
  D --> E[Solve for a or unknown force]
```

```plot
{"title": "Acceleration down a frictionless incline", "xLabel": "incline angle (deg)", "yLabel": "a (m/s^2)", "xRange": [0,90], "yRange": [0,10], "grid": true, "functions": [{"expr": "9.81*sin(x*0.01745)", "label": "a = g sin(theta)", "color": "#16a34a"}]}
```

**Next:** turn forces into quantitative kinetics in the Intermediate course.
""",
        ),
        _quiz(),
    ),
)


_INTERMEDIATE = SeedCourse(
    slug="engineering-dynamics-intermediate",
    title="Engineering Dynamics — Intermediate",
    description=(
        "The core quantitative toolkit of particle kinetics: equations of motion with "
        "friction, the work-energy theorem, conservative forces and energy conservation, "
        "linear and angular impulse-momentum, and impact. Numerical integration of the "
        "equations of motion with SciPy."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Equations of motion with friction",
            "12 min",
            r"""
# Equations of motion with friction

Newton's second law becomes a *solvable* problem once you commit to axes and a friction model. Coulomb (dry) friction has two regimes: static, $f\le\mu_s N$, which holds the body until the applied force overcomes it; and kinetic, $f=\mu_k N$ opposing motion once sliding, with $\mu_k<\mu_s$.

For a block pushed by force $P$ at angle $\phi$ on a horizontal surface, the normal force is $N=mg-P\sin\phi$ and, once sliding,
$$m\,a = P\cos\phi-\mu_k(mg-P\sin\phi).$$
Note that pulling up ($\phi>0$) reduces $N$ and so reduces friction — a real design lever.

```python
import numpy as np
m, g, mu_k = 5.0, 9.81, 0.30
P, phi = 40.0, np.deg2rad(20)
N = m*g - P*np.sin(phi)
a = (P*np.cos(phi) - mu_k*N)/m
print(f"N={N:.1f} N, a={a:.2f} m/s^2")   # negative a => stays at rest
```

```plot
{"title": "Acceleration vs applied force (mu_k=0.3)", "xLabel": "P (N)", "yLabel": "a (m/s^2)", "xRange": [0,80], "yRange": [-4,12], "grid": true, "functions": [{"expr": "(x - 0.3*5*9.81)/5", "label": "a = (P - mu_k m g)/m", "color": "#2563eb"}]}
```

**Next:** trading force-over-distance for energy.
""",
        ),
        _t(
            "Work and the work-energy theorem",
            "12 min",
            r"""
# Work and the work-energy theorem

Work is force integrated over displacement, $U=\int \mathbf F\cdot d\mathbf r$. Only the force component along the path does work; a force perpendicular to motion (like the normal force) does none. The **work-energy theorem** states that the net work equals the change in kinetic energy:
$$U_{1\to2}=\Delta T = \tfrac12 m v_2^2 - \tfrac12 m v_1^2.$$
This is a scalar equation — no need to track direction — which makes it the fastest route to a *speed* when forces vary with position.

A spring stores work $\tfrac12 k x^2$; gravity does work $-mg\,\Delta h$; constant friction removes $\mu_k N\,d$. Example: a $2\,$kg block slides $3\,$m down a $30^\circ$ incline ($\mu_k=0.2$) from rest. Net work $=mg\sin30^\circ\cdot3-\mu_k mg\cos30^\circ\cdot3\approx 29.4-10.2=19.2\,$J, so $v=\sqrt{2\cdot19.2/2}\approx 4.4\,$m/s.

```plot
{"title": "Kinetic energy vs distance down incline", "xLabel": "distance (m)", "yLabel": "T (J)", "xRange": [0,3], "yRange": [0,20], "grid": true, "functions": [{"expr": "6.4*x", "label": "T = (net work/length) * d", "color": "#16a34a"}]}
```

```python
import numpy as np
m, g, mu, th, d = 2.0, 9.81, 0.2, np.deg2rad(30), 3.0
U = m*g*np.sin(th)*d - mu*m*g*np.cos(th)*d
v = np.sqrt(2*U/m)
print(f"net work {U:.1f} J, v {v:.2f} m/s")
```

**Next:** when energy is conserved.
""",
        ),
        _t(
            "Conservative forces and energy conservation",
            "12 min",
            r"""
# Conservative forces and energy conservation

A force is **conservative** if the work it does is path-independent and derivable from a potential energy $V$: gravity ($V=mgy$) and ideal springs ($V=\tfrac12 kx^2$) qualify; friction and drag do not. When only conservative forces act, the total mechanical energy is constant:
$$T_1+V_1 = T_2+V_2.$$
This turns many problems into one algebraic line. For a pendulum released from rest at angle $\theta_0$, the speed at the bottom is $v=\sqrt{2gL(1-\cos\theta_0)}$ — no differential equation needed.

When non-conservative forces are present, account for them explicitly: $T_1+V_1+U_{nc}=T_2+V_2$, where $U_{nc}$ is (negative) work done by friction/drag.

```mermaid
flowchart LR
  A[Forces acting] --> B{Conservative only?}
  B -->|Yes| C[T1 + V1 = T2 + V2]
  B -->|No| D[Add U_nc work term]
  C --> E[Solve for v or h]
  D --> E
```

```plot
{"title": "Pendulum speed at bottom vs release angle (L=1 m)", "xLabel": "release angle (deg)", "yLabel": "v (m/s)", "xRange": [0,180], "yRange": [0,7], "grid": true, "functions": [{"expr": "sqrt(2*9.81*1*(1-cos(x*0.01745)))", "label": "v = sqrt(2gL(1-cos))", "color": "#dc2626"}]}
```

**Next:** force-over-time instead of force-over-distance.
""",
        ),
        _t(
            "Linear impulse and momentum",
            "11 min",
            r"""
# Linear impulse and momentum

Integrating Newton's law over *time* gives the **impulse-momentum** principle:
$$\int_{t_1}^{t_2}\sum\mathbf F\,dt = m\mathbf v_2 - m\mathbf v_1.$$
The left side is the linear impulse; the right is the change in linear momentum $\mathbf p=m\mathbf v$. This is the tool of choice for short, hard-to-model forces (impacts, thrust) where you know the impulse but not the instantaneous force.

If the net external impulse is zero, momentum is **conserved** — the cornerstone of collision and recoil analysis. For two particles with no external force, $m_A\mathbf v_A+m_B\mathbf v_B$ is constant before and after interaction.

Example: a $0.15\,$kg ball hits a wall at $20\,$m/s and rebounds at $15\,$m/s. Impulse $=m(v_2-v_1)=0.15(15-(-20))=5.25\,$N·s; over a $5\,$ms contact the average force is $\approx 1050\,$N.

```plot
{"title": "Impulse delivered vs contact time (fixed dp)", "xLabel": "contact time (ms)", "yLabel": "avg force (N)", "xRange": [1,20], "yRange": [0,6000], "grid": true, "functions": [{"expr": "5250/x", "label": "F_avg = dp / dt", "color": "#2563eb"}]}
```

```python
m, v1, v2 = 0.15, -20.0, 15.0     # toward wall negative
J = m*(v2 - v1)                   # impulse, N*s
F_avg = J/0.005                   # 5 ms contact
print(f"impulse {J:.2f} N*s, avg force {F_avg:.0f} N")
```

**Next:** angular momentum and impact.
""",
        ),
        _t(
            "Angular momentum and impact",
            "12 min",
            r"""
# Angular momentum and impact

The **angular momentum** of a particle about a point O is $\mathbf H_O=\mathbf r\times m\mathbf v$, and the moment of the net force changes it: $\sum\mathbf M_O=\dot{\mathbf H}_O$. With no external moment about O, $H_O$ is conserved — why a skater spins faster pulling arms in, and why central-force orbits sweep equal areas in equal times.

**Impact** combines momentum conservation with the **coefficient of restitution** $e$, the ratio of separation to approach speed along the line of impact:
$$e=\frac{v_{B}'-v_{A}'}{v_A-v_B},\qquad 0\le e\le 1.$$
$e=1$ is perfectly elastic (kinetic energy conserved); $e=0$ is perfectly plastic (bodies stick). Together $m_A v_A+m_B v_B = m_A v_A'+m_B v_B'$ and the $e$ relation solve for both post-impact speeds.

```python
import numpy as np
mA, mB, vA, vB, e = 2.0, 3.0, 6.0, -1.0, 0.7
# solve [mA mB; -1 1] [vA'; vB'] = [mA vA + mB vB; e(vA - vB)]
A = np.array([[mA, mB], [-1, 1]])
b = np.array([mA*vA + mB*vB, e*(vA - vB)])
vAp, vBp = np.linalg.solve(A, b)
print(f"vA'={vAp:.2f}, vB'={vBp:.2f} m/s")
```

```plot
{"title": "Energy retained in central impact vs e", "xLabel": "restitution e", "yLabel": "fraction KE kept", "xRange": [0,1], "yRange": [0,1], "grid": true, "functions": [{"expr": "0.4 + 0.6*x^2", "label": "schematic KE fraction", "color": "#16a34a"}]}
```

**Next:** integrating the equations of motion numerically.
""",
        ),
        _t(
            "Numerical integration of the equations of motion",
            "13 min",
            r"""
# Numerical integration of the equations of motion

Most real dynamics — nonlinear drag, varying force, coupled bodies — has no closed-form solution. Recast the second-order law $m\ddot x=F(x,\dot x,t)$ as a **first-order state system** $\dot{\mathbf y}=\mathbf f(t,\mathbf y)$ with $\mathbf y=[x,\;v]$, then hand it to an integrator. SciPy's `solve_ivp` (adaptive Runge-Kutta, `RK45`) is the standard workhorse; choose a stiff method (`Radau`/`BDF`) when time constants differ by orders of magnitude.

Worked case: a projectile with quadratic air drag $F_d=\tfrac12\rho C_d A\,v^2$ opposing velocity. Drag couples the two axes (it depends on speed $|\mathbf v|$), so the closed-form parabola no longer holds and numerics earn their keep.

```python
import numpy as np
from scipy.integrate import solve_ivp
g, k = 9.81, 0.02     # k lumps 0.5*rho*Cd*A/m
def rhs(t, y):
    x, vx, h, vy = y
    sp = np.hypot(vx, vy)
    return [vx, -k*sp*vx, vy, -g - k*sp*vy]
y0 = [0, 30*np.cos(np.deg2rad(40)), 0, 30*np.sin(np.deg2rad(40))]
hit = lambda t, y: y[2]; hit.terminal = True; hit.direction = -1
sol = solve_ivp(rhs, [0, 10], y0, events=hit, max_step=0.01)
print(f"range with drag {sol.y[0,-1]:.1f} m")
```

```plot
{"title": "Trajectory: vacuum vs quadratic drag", "xLabel": "x (m)", "yLabel": "y (m)", "xRange": [0,60], "yRange": [0,16], "grid": true, "functions": [{"expr": "x*0.839 - 9.81/(2*(30*0.766)^2)*x^2", "label": "vacuum parabola", "color": "#2563eb"}]}
```

**Next:** extend particles to spinning rigid bodies in the Advanced course.
""",
        ),
        _quiz(),
    ),
)


_ADVANCED = SeedCourse(
    slug="engineering-dynamics-advanced",
    title="Engineering Dynamics — Advanced",
    description=(
        "Rigid-body planar kinematics and kinetics, the parallel-axis theorem and "
        "rolling, energy and momentum for rigid bodies, then an introduction to "
        "vibration: free/damped response, forced response and resonance, with modern "
        "simulation, frequency-response and optimization workflows."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Rigid-body planar kinematics",
            "13 min",
            r"""
# Rigid-body planar kinematics

A rigid body in a plane has three degrees of freedom: two translation, one rotation. The velocity of any point B on the body relates to a reference point A by the **rigid-body velocity equation**,
$$\mathbf v_B=\mathbf v_A+\boldsymbol\omega\times\mathbf r_{B/A},$$
and accelerations by
$$\mathbf a_B=\mathbf a_A+\boldsymbol\alpha\times\mathbf r_{B/A}-\omega^2\mathbf r_{B/A},$$
where the $-\omega^2 r$ term is the centripetal contribution. Here $\boldsymbol\omega=\omega\hat k$ is the angular velocity, shared by every point of the body.

A powerful shortcut is the **instantaneous center of zero velocity (IC)**: the point about which the body appears to purely rotate at that instant. Every point's speed is $\omega\,d$, where $d$ is its distance to the IC — turning a velocity problem into geometry.

```mermaid
flowchart LR
  A[Pick reference point A] --> B[v_B = v_A + omega x r_BA]
  B --> C[a_B = a_A + alpha x r_BA - omega^2 r_BA]
  A --> D[Or locate IC]
  D --> E[v_P = omega * distance to IC]
```

```plot
{"title": "Point speed vs distance to instantaneous center", "xLabel": "distance to IC (m)", "yLabel": "speed (m/s)", "xRange": [0,2], "yRange": [0,10], "grid": true, "functions": [{"expr": "5*x", "label": "v = omega * d (omega=5 rad/s)", "color": "#2563eb"}]}
```

**Next:** mass distribution and the moment of inertia.
""",
        ),
        _t(
            "Mass moment of inertia and the parallel-axis theorem",
            "12 min",
            r"""
# Mass moment of inertia and the parallel-axis theorem

Rotational inertia depends on *where* mass sits, not just how much. The **mass moment of inertia** about an axis is $I=\int r^2\,dm$. Standard results: solid disk $I=\tfrac12 mR^2$, thin rod about its center $\tfrac{1}{12}mL^2$, solid sphere $\tfrac25 mR^2$.

The **parallel-axis theorem** shifts the axis from the centroid G to a parallel axis a distance $d$ away:
$$I = I_G + m d^2.$$
This is why a rod swung about its end ($\tfrac13 mL^2$) has four times the inertia of one swung about its center. The radius of gyration $k=\sqrt{I/m}$ packages the distribution as an equivalent distance.

```python
import numpy as np
m, L = 2.0, 1.5
I_G = m*L**2/12            # rod about center
I_end = I_G + m*(L/2)**2   # parallel-axis shift to the end
print(f"I_G={I_G:.3f}, I_end={I_end:.3f} kg*m^2, ratio={I_end/I_G:.1f}")
```

```plot
{"title": "Inertia about offset axis: I = I_G + m d^2", "xLabel": "offset d (m)", "yLabel": "I (kg m^2)", "xRange": [0,1], "yRange": [0,2.5], "grid": true, "functions": [{"expr": "0.375 + 2*x^2", "label": "I_G + m d^2", "color": "#16a34a"}]}
```

**Next:** writing the rigid-body equations of motion.
""",
        ),
        _t(
            "Rigid-body kinetics and rolling",
            "13 min",
            r"""
# Rigid-body kinetics and rolling

Planar rigid-body motion obeys three scalar equations: two for translation of the mass center G and one for rotation,
$$\sum F_x=m a_{Gx},\quad \sum F_y=m a_{Gy},\quad \sum M_G=I_G\,\alpha.$$
For **rolling without slipping**, the contact point is the instantaneous center, giving the kinematic constraint $a_G=R\alpha$ and requiring the friction force to satisfy $f\le\mu_s N$ (exceed it and the body slips).

Classic result: a cylinder rolling down a $\theta$ incline has $a_G=\frac{g\sin\theta}{1+I_G/(mR^2)}$. A solid cylinder ($I_G=\tfrac12 mR^2$) gives $a_G=\tfrac23 g\sin\theta$; a hoop ($I_G=mR^2$) only $\tfrac12 g\sin\theta$ — more rotational inertia, slower descent, independent of mass and radius.

```python
import numpy as np
g, th = 9.81, np.deg2rad(20)
for name, c in [("solid cyl", 0.5), ("hoop", 1.0), ("sphere", 0.4)]:
    a = g*np.sin(th)/(1 + c)
    print(f"{name:9s}: a_G = {a:.2f} m/s^2")
```

```plot
{"title": "Roll-down acceleration vs inertia factor I/(mR^2)", "xLabel": "I/(mR^2)", "yLabel": "a_G (m/s^2)", "xRange": [0,1.2], "yRange": [0,4], "grid": true, "functions": [{"expr": "9.81*0.342/(1+x)", "label": "a_G = g sin(theta)/(1+c)", "color": "#dc2626"}]}
```

**Next:** energy and momentum for rigid bodies.
""",
        ),
        _t(
            "Energy and momentum for rigid bodies",
            "12 min",
            r"""
# Energy and momentum for rigid bodies

A rigid body carries both translational and rotational kinetic energy:
$$T=\tfrac12 m v_G^2+\tfrac12 I_G\,\omega^2.$$
The work-energy theorem still applies, now with moments doing work through angle, $U=\int M\,d\theta$. For rolling without slipping the contact friction does *no* work (its point is instantaneously at rest), so energy methods give clean speeds.

Momentum generalizes too: linear momentum $\mathbf p=m\mathbf v_G$ and angular momentum about G, $H_G=I_G\omega$. Angular impulse-momentum, $\int M_G\,dt=I_G\Delta\omega$, handles rotational impacts; about a fixed point or the mass center, with no external angular impulse, $H$ is conserved — the basis of spin-up/spin-down and eccentric-impact analysis.

```mermaid
flowchart LR
  A[Rigid-body methods] --> B[Energy: T = 1/2 m vG^2 + 1/2 IG omega^2]
  A --> C[Linear momentum: p = m vG]
  A --> D[Angular momentum: HG = IG omega]
  B --> E[best for speed vs position]
  C --> F[best for impacts and time]
  D --> F
```

```plot
{"title": "Energy split for a rolling solid cylinder", "xLabel": "speed vG (m/s)", "yLabel": "kinetic energy (J), m=2kg", "xRange": [0,5], "yRange": [0,40], "grid": true, "functions": [{"expr": "0.5*2*x^2", "label": "translational", "color": "#2563eb"}, {"expr": "0.25*2*x^2", "label": "rotational (1/2 of trans)", "color": "#16a34a"}]}
```

**Next:** putting a body on a spring — vibration.
""",
        ),
        _t(
            "Introduction to vibration: free and damped response",
            "13 min",
            r"""
# Introduction to vibration: free and damped response

A mass on a spring with viscous damping obeys $m\ddot x+c\dot x+kx=0$. Define the **natural frequency** $\omega_n=\sqrt{k/m}$ and **damping ratio** $\zeta=\frac{c}{2\sqrt{km}}$. The response type follows $\zeta$:

- $\zeta=0$: undamped, pure sinusoid at $\omega_n$.
- $0<\zeta<1$: **underdamped**, decaying oscillation at $\omega_d=\omega_n\sqrt{1-\zeta^2}$.
- $\zeta=1$: critically damped, fastest non-oscillating return.
- $\zeta>1$: overdamped, slow non-oscillating return.

The **logarithmic decrement** $\delta=\ln(x_n/x_{n+1})=\frac{2\pi\zeta}{\sqrt{1-\zeta^2}}$ lets you measure $\zeta$ from a decaying experimental trace.

```python
import numpy as np
from scipy.integrate import solve_ivp
m, k, zeta = 1.0, 100.0, 0.1
wn = np.sqrt(k/m); c = 2*zeta*np.sqrt(k*m)
rhs = lambda t, y: [y[1], -(c*y[1] + k*y[0])/m]
sol = solve_ivp(rhs, [0, 4], [0.05, 0], max_step=0.005)
print(f"wn={wn:.1f} rad/s, wd={wn*np.sqrt(1-zeta**2):.1f} rad/s")
```

```plot
{"title": "Underdamped free response (zeta=0.1)", "xLabel": "t (s)", "yLabel": "x (normalized)", "xRange": [0,12], "yRange": [-1,1], "grid": true, "functions": [{"expr": "exp(-0.2*x)*cos(3*x)", "label": "x = e^{-zeta wn t} cos(wd t)", "color": "#dc2626"}]}
```

**Next:** driving the system and chasing resonance.
""",
        ),
        _t(
            "Forced vibration, resonance and design optimization",
            "14 min",
            r"""
# Forced vibration, resonance and design optimization

Drive the oscillator harmonically, $m\ddot x+c\dot x+kx=F_0\cos\omega t$. The steady-state amplitude follows the **frequency response** (magnification factor) in terms of the frequency ratio $r=\omega/\omega_n$:
$$M=\frac{X}{F_0/k}=\frac{1}{\sqrt{(1-r^2)^2+(2\zeta r)^2}}.$$
At **resonance** ($r\approx 1$) the response peaks; with light damping it can be many times the static deflection — the failure mode behind the Tacoma Narrows and countless machine mounts. Adding damping flattens and lowers the peak. For **vibration isolation**, mount machinery so $r>\sqrt2$, where transmissibility drops below one.

A modern design loop treats $\zeta$ (or mount stiffness) as a decision variable and *optimizes* a cost — e.g. minimize peak transmissibility subject to a static-deflection limit — with `scipy.optimize`. This is also where surrogate models and Bayesian optimization (e.g. `scikit-optimize`) replace expensive FE/multibody runs in the loop.

```python
import numpy as np
from scipy.optimize import minimize_scalar
def peak_mag(zeta):
    r = np.linspace(0.1, 2.5, 600)
    M = 1/np.sqrt((1-r**2)**2 + (2*zeta*r)**2)
    return M.max()
res = minimize_scalar(peak_mag, bounds=(0.05, 1.0), method="bounded")
print(f"zeta minimizing peak magnification: {res.x:.2f} -> peak {res.fun:.2f}")
```

```plot
{"title": "Frequency response magnification (zeta=0.1)", "xLabel": "frequency ratio r = w/wn", "yLabel": "magnification M", "xRange": [0,2.5], "yRange": [0,6], "grid": true, "functions": [{"expr": "1/sqrt((1-x^2)^2 + (0.2*x)^2)", "label": "M(r)", "color": "#2563eb"}]}
```

**Next:** you have spanned particles to vibrating rigid bodies — pair this with the Control and Robotics tracks.
""",
        ),
        _quiz(),
    ),
)


ENGINEERING_DYNAMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ENGINEERING_DYNAMICS_COURSES"]
