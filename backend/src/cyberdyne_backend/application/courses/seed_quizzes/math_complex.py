"""Curated quiz questions for the Mathematics - Complex Analysis course
(math-complex): per-lesson checkpoints keyed by exact content-lesson title plus
a final comprehensive quiz. Every question is answerable from the lesson body."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Complex numbers & the complex plane": (
            q(
                "In the complex number z = a + bi, what does i satisfy?",
                (
                    opt("i squared equals 1"),
                    opt("i squared equals -1", correct=True),
                    opt("i equals the square root of 2"),
                    opt("i equals a divided by b"),
                ),
                "A complex number z = a + bi is defined with i where i squared equals -1.",
            ),
            q(
                "Geometrically, what does multiplying a complex number by i do?",
                (
                    opt("It doubles its modulus"),
                    opt("It rotates it by 90 degrees", correct=True),
                    opt("It reflects it across the real axis"),
                    opt("It shifts it one unit to the right"),
                ),
                "The lesson shows that multiplying by i rotates the number 90 degrees, since i times (a + bi) equals -b + ai.",
            ),
            q(
                "How is the modulus of z = a + bi defined in the lesson?",
                (
                    opt("As the angle arg z that z makes"),
                    opt("As a plus b"),
                    opt("As the square root of a squared plus b squared", correct=True),
                    opt("As a times b"),
                ),
                "The modulus |z| is its length, given by the square root of a squared plus b squared.",
            ),
        ),
        "Polar form & Euler's formula": (
            q(
                "What does Euler's formula state about e to the i theta?",
                (
                    opt("It equals cos theta plus i sin theta", correct=True),
                    opt("It equals sin theta plus i cos theta"),
                    opt("It equals cos theta minus i sin theta"),
                    opt("It equals theta plus i"),
                ),
                "Euler's formula gives e to the i theta as cos theta plus i sin theta.",
            ),
            q(
                "In polar form, how do you multiply two complex numbers r1 e^(i theta1) and r2 e^(i theta2)?",
                (
                    opt("Add the lengths and multiply the angles"),
                    opt("Multiply the lengths and add the angles", correct=True),
                    opt("Multiply both the lengths and the angles"),
                    opt("Subtract the lengths and subtract the angles"),
                ),
                "Polar multiplication multiplies the lengths and adds the angles, giving r1 r2 e^(i(theta1 + theta2)).",
            ),
            q(
                "The lesson says the roots of unity are the backbone of which algorithm?",
                (
                    opt("Gaussian elimination"),
                    opt("The simplex method"),
                    opt("The FFT", correct=True),
                    opt("Gradient descent"),
                ),
                "The roots of unity, equally spaced on the unit circle, are the backbone of the FFT.",
            ),
        ),
        "Functions, analyticity & conformal maps": (
            q(
                "What conditions must an analytic (holomorphic) function satisfy?",
                (
                    opt("The Cauchy-Riemann equations", correct=True),
                    opt("The Pythagorean theorem"),
                    opt("The normal equations"),
                    opt("The KKT conditions"),
                ),
                "Analyticity requires the Cauchy-Riemann equations relating the partials of u and v.",
            ),
            q(
                "What property of the real and imaginary parts follows from analyticity?",
                (
                    opt("They are always linear"),
                    opt("They are harmonic and solve Laplace's equation", correct=True),
                    opt("They are always periodic"),
                    opt("They are discontinuous"),
                ),
                "A consequence is that the real and imaginary parts are harmonic, solving Laplace's equation.",
            ),
            q(
                "Why are analytic maps described as conformal?",
                (
                    opt("They preserve angles", correct=True),
                    opt("They preserve total area"),
                    opt("They reverse orientation"),
                    opt("They eliminate all curvature"),
                ),
                "Analytic maps are conformal, meaning they preserve angles.",
            ),
        ),
        "Contour integrals & residues": (
            q(
                "According to Cauchy's theorem, what is the integral of an analytic function around any closed loop?",
                (
                    opt("Equal to the area enclosed"),
                    opt("Zero", correct=True),
                    opt("Equal to 2 pi i times the radius"),
                    opt("Infinite"),
                ),
                "Cauchy's theorem states the integral of an analytic function around any closed loop is zero.",
            ),
            q(
                "By the residue theorem, what is the integral around a loop containing poles?",
                (
                    opt("Zero regardless of the poles"),
                    opt("2 pi i times the sum of the residues at those poles", correct=True),
                    opt("The product of the pole locations"),
                    opt("Pi times the number of poles"),
                ),
                "The residue theorem gives the integral as 2 pi i times the sum of the residues at the enclosed poles.",
            ),
            q(
                "What is a pole, as described in the lesson?",
                (
                    opt(
                        "A point where a function shoots to infinity, like 1/z at the origin",
                        correct=True,
                    ),
                    opt("A point where the function is zero"),
                    opt("The center of the contour"),
                    opt("Any point on the real axis"),
                ),
                "A pole is where a function shoots to infinity, such as 1/z blowing up at the origin.",
            ),
        ),
        "Poles, transforms & stability": (
            q(
                "How is the Fourier transform related to the Laplace transform?",
                (
                    opt("It is the Laplace transform with s set to zero"),
                    opt("It is the special case s = i omega, the imaginary axis", correct=True),
                    opt("It is the Laplace transform squared"),
                    opt("It is the inverse of the Laplace transform"),
                ),
                "The Fourier transform is the special case of the Laplace transform with s = i omega, the imaginary axis.",
            ),
            q(
                "For a pole at s = sigma + i omega, which part decides stability?",
                (
                    opt("The imaginary part omega"),
                    opt("The real part sigma", correct=True),
                    opt("The modulus of s"),
                    opt("The argument of s"),
                ),
                "Since the time response is e^(sigma t) cos(omega t), the real part sigma sets stability.",
            ),
            q(
                "What does a pole in the left half-plane (sigma less than 0) imply?",
                (
                    opt("The response grows, so the system is unstable"),
                    opt("The response decays, so the system is stable", correct=True),
                    opt("Pure oscillation with no decay"),
                    opt("The transfer function has no denominator"),
                ),
                "With sigma less than 0 the response decays, making the system stable.",
            ),
        ),
        "Lab: complex arithmetic & the Mandelbrot set": (
            q(
                "In the lab, what is the product (1 + 2i) times (3 + i)?",
                (
                    opt("4 + 3i"),
                    opt("1 + 7i", correct=True),
                    opt("3 + 2i"),
                    opt("5 + 5i"),
                ),
                "The lab computes the real part as ar*br - ai*bi and the imaginary part as ar*bi + ai*br, giving 1 + 7i.",
            ),
            q(
                "Which iteration defines the Mandelbrot set in the lab?",
                (
                    opt("z mapped to z squared plus c", correct=True),
                    opt("z mapped to z plus c squared"),
                    opt("z mapped to 2 times z plus c"),
                    opt("z mapped to c divided by z"),
                ),
                "The Mandelbrot set is defined purely by the iteration z mapped to z squared plus c, starting from 0.",
            ),
            q(
                "In the lab, how is a point c judged to be inside the set?",
                (
                    opt("If z reaches exactly zero"),
                    opt("If the magnitude of z stays bounded under iteration", correct=True),
                    opt("If c lies on the real axis"),
                    opt("If the first iteration overflows"),
                ),
                "A point is in the set when the magnitude of z stays bounded as z is iterated; the code caps iterations and checks zr*zr + zi*zi against 4.",
            ),
        ),
    },
    final=(
        q(
            "What is the Argand plane?",
            (
                opt(
                    "The plane where a complex number a + bi is plotted with real part horizontal and imaginary part vertical",
                    correct=True,
                ),
                opt("A 3D surface used only for harmonic functions"),
                opt("The set of all roots of unity"),
                opt("The contour used in Cauchy's theorem"),
            ),
            "The Argand plane plots z = a + bi as a point with real part on the horizontal axis and imaginary part on the vertical.",
        ),
        q(
            "What does Euler's identity e^(i pi) + 1 = 0 follow from?",
            (
                opt("The Cauchy-Riemann equations"),
                opt("Euler's formula e^(i theta) = cos theta + i sin theta", correct=True),
                opt("The residue theorem"),
                opt("The least-squares normal equations"),
            ),
            "Euler's identity falls straight out of Euler's formula evaluated at theta equal to pi.",
        ),
        q(
            "Why can hard real integrals be evaluated by closing a contour and summing residues?",
            (
                opt("Because every real integral equals zero"),
                opt(
                    "Because the residue theorem relates the closed contour integral to 2 pi i times the sum of residues at enclosed poles",
                    correct=True,
                ),
                opt("Because conformal maps preserve area"),
                opt("Because the Fourier transform removes all poles"),
            ),
            "The residue theorem lets a hard real integral be computed by closing a contour in the complex plane and summing the enclosed residues.",
        ),
        q(
            "In control and filter design, where should poles be placed for a stable system?",
            (
                opt("On the imaginary axis"),
                opt("In the right half-plane"),
                opt("In the left half-plane", correct=True),
                opt("At the origin only"),
            ),
            "Poles in the left half-plane give a decaying response, so the system is stable.",
        ),
        q(
            "What does multiplying complex numbers in polar form do to their lengths and angles?",
            (
                opt("Multiplies the lengths and adds the angles", correct=True),
                opt("Adds the lengths and multiplies the angles"),
                opt("Adds both lengths and angles"),
                opt("Multiplies both lengths and angles"),
            ),
            "In polar form, multiplication multiplies the lengths and adds the angles.",
        ),
    ),
)
