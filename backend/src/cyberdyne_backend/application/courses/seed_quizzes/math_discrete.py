from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Logic & proofs": (
            q(
                "When is the implication P implies Q false?",
                (
                    opt("When both P and Q are true"),
                    opt("When P is true but Q is false", correct=True),
                    opt("When P is false but Q is true"),
                    opt("When both P and Q are false"),
                ),
                "An implication is only false when the hypothesis P is true and the conclusion Q is false.",
            ),
            q(
                "Which statement is logically equivalent to P implies Q?",
                (
                    opt("Its converse Q implies P"),
                    opt("Its inverse not P implies not Q"),
                    opt("Its contrapositive not Q implies not P", correct=True),
                    opt("Its negation P and not Q"),
                ),
                "The contrapositive not Q implies not P is logically equivalent and is the basis of proof by contrapositive.",
            ),
            q(
                "Why can a single perceptron not learn the XOR function?",
                (
                    opt("XOR has too many inputs to enumerate"),
                    opt(
                        "XOR is not linearly separable, so no single straight line splits the 1s from the 0s",
                        correct=True,
                    ),
                    opt("XOR requires real-valued inputs"),
                    opt("XOR is undefined when both inputs are equal"),
                ),
                "Plotting XOR's four inputs shows no single line separates the 1s from the 0s, which is why hidden layers are needed.",
            ),
        ),
        "Sets, relations & functions": (
            q(
                "Which three properties define an equivalence relation?",
                (
                    opt("Reflexive, symmetric, transitive", correct=True),
                    opt("Reflexive, antisymmetric, transitive"),
                    opt("Symmetric, antisymmetric, transitive"),
                    opt("Injective, surjective, bijective"),
                ),
                "An equivalence relation is reflexive, symmetric, and transitive, partitioning a set into classes.",
            ),
            q(
                "A function that maps distinct inputs to distinct outputs is called what?",
                (
                    opt("Surjective"),
                    opt("Injective", correct=True),
                    opt("Bijective"),
                    opt("Reflexive"),
                ),
                "Injective (one-to-one) means distinct inputs give distinct outputs.",
            ),
            q(
                "Why is f(x) = x squared over the reals not injective?",
                (
                    opt("It never reaches negative outputs"),
                    opt("It is not defined at x equals 0"),
                    opt("Both -2 and 2 map to the output 4", correct=True),
                    opt("It hits every output exactly once"),
                ),
                "Since -2 and 2 both map to 4, distinct inputs share an output, so it is not injective and has no inverse without restricting the domain.",
            ),
        ),
        "Combinatorics: counting": (
            q(
                "Which counting tool is used when order matters?",
                (
                    opt("Combinations"),
                    opt("Permutations", correct=True),
                    opt("Inclusion-exclusion"),
                    opt("The product rule alone"),
                ),
                "Permutations P(n,k) count arrangements where order matters.",
            ),
            q(
                "What does the inclusion-exclusion formula for the size of A union B equal?",
                (
                    opt("Size of A plus size of B"),
                    opt("Size of A plus size of B minus size of A intersect B", correct=True),
                    opt("Size of A times size of B"),
                    opt("Size of A intersect B"),
                ),
                "Inclusion-exclusion corrects for overlap: the size of A union B is the size of A plus the size of B minus the size of A intersect B.",
            ),
            q(
                "What shape do the binomial coefficients C(10, k) trace when plotted?",
                (
                    opt("A straight line"),
                    opt("A bell shape, the discrete root of the Normal distribution", correct=True),
                    opt("A sawtooth wave"),
                    opt("An exponential curve"),
                ),
                "The rows of Pascal's triangle plotted for n=10 trace a bell shape, the discrete root of the Normal distribution.",
            ),
        ),
        "Recurrences & induction": (
            q(
                "In a proof by induction, after establishing the base case, what must you show?",
                (
                    opt("That the statement holds for n minus 1"),
                    opt("That n implies n+1", correct=True),
                    opt("That the statement is false for some n"),
                    opt("That every case is independent"),
                ),
                "Induction proves a base case and then that n implies n+1, like falling dominoes.",
            ),
            q(
                "Approximately how fast does the Fibonacci sequence grow according to Binet's formula?",
                (
                    opt("Linearly with n"),
                    opt(
                        "Like the golden ratio to the power n divided by the square root of 5",
                        correct=True,
                    ),
                    opt("Like n times log n"),
                    opt("Like n squared"),
                ),
                "Binet's formula shows Fibonacci grows like phi to the n over the square root of 5, with phi the golden ratio about 1.618.",
            ),
            q(
                "Using the Master theorem, what is the runtime of T(n) = 2 T(n/2) + n?",
                (
                    opt("Theta of n"),
                    opt("Theta of n squared"),
                    opt("Theta of n log n", correct=True),
                    opt("Theta of 2 to the n"),
                ),
                "The Master theorem gives Theta of n log n for this recurrence, which is merge sort.",
            ),
        ),
        "Number theory & modular arithmetic": (
            q(
                "What does a mod m compute?",
                (
                    opt("The quotient after dividing a by m"),
                    opt(
                        "The remainder after dividing a by m, which wraps around like a clock",
                        correct=True,
                    ),
                    opt("The product of a and m"),
                    opt("The greatest common divisor of a and m"),
                ),
                "a mod m is the remainder after dividing by m, wrapping around like a clock.",
            ),
            q(
                "Which algorithm finds the greatest common divisor of two numbers very fast?",
                (
                    opt("Euclid's algorithm", correct=True),
                    opt("The sieve of Eratosthenes"),
                    opt("Modular exponentiation"),
                    opt("The Master theorem"),
                ),
                "Euclid's algorithm finds gcd(a, b) astonishingly fast.",
            ),
            q(
                "What asymmetry makes RSA secure?",
                (
                    opt("Adding two numbers is easy but subtracting is hard"),
                    opt(
                        "Multiplying two big primes is easy but factoring the product back is brutally hard",
                        correct=True,
                    ),
                    opt("Finding remainders is easy but finding quotients is hard"),
                    opt("Listing primes is easy but counting them is hard"),
                ),
                "RSA relies on the asymmetry that multiplying two big primes is easy while factoring the product back is brutally hard.",
            ),
        ),
        "Lab: Euclid, modular power, primes & Fibonacci": (
            q(
                "In Euclid's algorithm as coded, what is the loop's stopping condition?",
                (
                    opt("When a equals b"),
                    opt("When b becomes 0", correct=True),
                    opt("When the remainder exceeds b"),
                    opt("When a becomes 1"),
                ),
                "The while loop runs until b is 0, at which point a holds the gcd.",
            ),
            q(
                "Why does the fast modular exponentiation in the lab never build the giant value 7 to the 128?",
                (
                    opt("It uses floating point to approximate the result"),
                    opt("It reduces modulo 13 at every step, keeping numbers small", correct=True),
                    opt("It skips even exponents entirely"),
                    opt("It precomputes the answer from a table"),
                ),
                "The code keeps results and the base reduced mod 13 throughout, so it never builds the giant power.",
            ),
            q(
                "How does the lab decide whether a number is prime?",
                (
                    opt(
                        "By checking divisors d while d times d is at most the number", correct=True
                    ),
                    opt("By using Euclid's algorithm on each candidate"),
                    opt("By computing its Fibonacci index"),
                    opt("By taking the number mod 2 only"),
                ),
                "Trial division tests divisors d while d times d is at most num, marking the number not prime if any divides it.",
            ),
        ),
    },
    final=(
        q(
            "Which proof technique relies on showing a base case and then that n implies n+1?",
            (
                opt("Proof by contradiction"),
                opt("Proof by contrapositive"),
                opt("Proof by induction", correct=True),
                opt("Direct proof"),
            ),
            "Induction establishes a base case and the step that n implies n+1.",
        ),
        q(
            "A function that is both injective and surjective is called what?",
            (
                opt("Reflexive"),
                opt("Bijective", correct=True),
                opt("Transitive"),
                opt("Symmetric"),
            ),
            "A bijective function is both injective and surjective, a perfect pairing.",
        ),
        q(
            "Which formula gives the number of combinations of k items chosen from n?",
            (
                opt("n factorial over (n minus k) factorial"),
                opt("n factorial over k factorial times (n minus k) factorial", correct=True),
                opt("n times m"),
                opt("n factorial times k factorial"),
            ),
            "Combinations, where order does not matter, equal n factorial over k factorial times (n minus k) factorial.",
        ),
        q(
            "What underlies the security of RSA?",
            (
                opt("That gcd is slow to compute"),
                opt(
                    "That multiplying primes is easy but factoring the product is hard",
                    correct=True,
                ),
                opt("That XOR is not linearly separable"),
                opt("That Fibonacci grows exponentially"),
            ),
            "RSA's security comes from the asymmetry between easy multiplication of primes and hard factoring of the product.",
        ),
        q(
            "What does a mod m do as you increase x along a number line?",
            (
                opt("Grows linearly without bound"),
                opt("Wraps around like a clock, producing a sawtooth pattern", correct=True),
                opt("Traces a bell shape"),
                opt("Stays constant"),
            ),
            "a mod m wraps around like clock arithmetic, producing a repeating sawtooth.",
        ),
    ),
)
