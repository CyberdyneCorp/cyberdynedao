"""Curated quiz questions for the Information Theory & Coding - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Linear block codes: G and H": (
            q(
                "How is a codeword produced from a message in a linear block code?",
                (
                    opt("c = m + H"),
                    opt("c = m G, the message times the generator matrix", correct=True),
                    opt("c = H mᵀ"),
                    opt("c is chosen at random for each message"),
                ),
                "Encoding multiplies the message vector by the generator matrix G over the field.",
            ),
            q(
                "What does the parity-check matrix H verify?",
                (
                    opt("That the message length equals n"),
                    opt("That c is a valid codeword, i.e. H cᵀ = 0", correct=True),
                    opt("That the code rate is exactly 1/2"),
                    opt("That every codeword is distinct"),
                ),
                "A word c is a valid codeword if and only if H cᵀ = 0.",
            ),
            q(
                "In systematic form G = [I_k | P], what is special about the codeword?",
                (
                    opt("The codeword is fully scrambled"),
                    opt(
                        "The first k bits are the message verbatim, the rest are parity",
                        correct=True,
                    ),
                    opt("Every bit is a parity bit"),
                    opt("The message appears at the end of the codeword"),
                ),
                "Systematic form keeps the k message bits unchanged at the front and appends n − k parity bits.",
            ),
        ),
        "Syndrome decoding": (
            q(
                "Why is the syndrome s = H rᵀ so useful?",
                (
                    opt("It depends on the message, not the error"),
                    opt(
                        "It depends only on the error pattern, not on the transmitted message",
                        correct=True,
                    ),
                    opt("It is always zero regardless of errors"),
                    opt("It equals the original codeword"),
                ),
                "Since H cᵀ = 0, the syndrome H rᵀ reduces to H eᵀ — it depends only on the error.",
            ),
            q(
                "For a single-error-correcting code, what does the syndrome of a single-bit error equal?",
                (
                    opt("The whole received word"),
                    opt("The column of H corresponding to the flipped bit", correct=True),
                    opt("Always the all-ones vector"),
                    opt("The message bits"),
                ),
                "A single-bit error gives a syndrome equal to that bit's column of H — effectively its address.",
            ),
            q(
                "What does a zero syndrome indicate?",
                (
                    opt("The maximum number of errors occurred"),
                    opt("No detectable error; the received word is accepted", correct=True),
                    opt("The decoder must guess randomly"),
                    opt("The message must be retransmitted"),
                ),
                "A zero syndrome means the received word passes the parity checks, so it is accepted.",
            ),
        ),
        "Hamming codes & SECDED": (
            q(
                "How are the columns of H arranged in the (7,4) Hamming code so decoding is trivial?",
                (
                    opt("All columns are identical"),
                    opt(
                        "As the binary numbers 1 through 7, so the syndrome is the error's position",
                        correct=True,
                    ),
                    opt("In random order"),
                    opt("As the all-zero vector"),
                ),
                "With columns equal to binary 1..7, the syndrome read as a number is exactly the position of the flipped bit.",
            ),
            q(
                "What does it mean that the Hamming code is 'perfect'?",
                (
                    opt("It never makes any errors"),
                    opt(
                        "Every word is either a codeword or exactly one flip from a unique codeword",
                        correct=True,
                    ),
                    opt("It has rate 1"),
                    opt("It can correct any number of errors"),
                ),
                "A perfect code wastes nothing: every received word lies within one flip of exactly one codeword.",
            ),
            q(
                "What does SECDED (the (8,4) extended Hamming code) provide?",
                (
                    opt("Single-error correction only"),
                    opt("Single-error correction and double-error detection", correct=True),
                    opt("Double-error correction"),
                    opt("Burst-error correction"),
                ),
                "Adding one overall parity bit gives d_min = 4: it corrects one error and detects two — the basis of ECC memory.",
            ),
        ),
        "Cyclic codes & CRC": (
            q(
                "What algebraic operation underlies encoding and checking in a cyclic code?",
                (
                    opt("Matrix inversion"),
                    opt("Polynomial division by a generator polynomial g(x)", correct=True),
                    opt("Sorting the bits"),
                    opt("Computing a Fourier transform"),
                ),
                "Cyclic codes treat bit strings as polynomials; encoding/checking is polynomial division by g(x), done with an LFSR.",
            ),
            q(
                "Is a CRC primarily used for detection or correction?",
                (
                    opt("Correction of single errors"),
                    opt(
                        "Detection — the receiver checks for a zero remainder and rejects on mismatch",
                        correct=True,
                    ),
                    opt("Correction of bursts"),
                    opt("Compression of the data"),
                ),
                "A CRC detects corruption (nonzero remainder) and triggers a retransmission; it does not correct.",
            ),
            q(
                "Which error types does a well-chosen CRC reliably catch?",
                (
                    opt("Only errors in the first bit"),
                    opt(
                        "All single and double-bit errors, all odd numbers of errors, and short bursts",
                        correct=True,
                    ),
                    opt("Only errors that cancel out"),
                    opt("No errors at all"),
                ),
                "A good generator polynomial catches all single/double errors, any odd number of errors, and bursts shorter than the CRC.",
            ),
        ),
        "Reed–Solomon codes": (
            q(
                "What does a Reed–Solomon code operate on?",
                (
                    opt("Single bits over GF(2)"),
                    opt("Symbols (e.g. bytes) over a Galois field GF(2^m)", correct=True),
                    opt("Floating-point numbers"),
                    opt("Only ASCII characters"),
                ),
                "RS codes work on multi-bit symbols over GF(2^m), which is why they handle bursts well.",
            ),
            q(
                "How many symbol errors can an RS(n, k) code correct?",
                (
                    opt("n − k symbol errors"),
                    opt("(n − k) / 2 symbol errors", correct=True),
                    opt("k symbol errors"),
                    opt("Only one symbol error"),
                ),
                "RS adds n − k parity symbols and corrects up to t = (n − k)/2 symbol errors.",
            ),
            q(
                "Why are RS codes especially good against burst errors?",
                (
                    opt("Bursts never affect symbols"),
                    opt(
                        "A burst of bit errors usually corrupts only a few symbols, within the correction limit",
                        correct=True,
                    ),
                    opt("They convert bursts into more bursts"),
                    opt("They ignore all bursts automatically"),
                ),
                "Since a burst typically hits only a few consecutive symbols, RS can correct it where a bit-level code fails.",
            ),
        ),
        "Interleaving & burst errors": (
            q(
                "What does interleaving do to a burst of channel errors?",
                (
                    opt("It concentrates them into one codeword"),
                    opt("It spreads them across many codewords as scattered errors", correct=True),
                    opt("It deletes them entirely"),
                    opt("It converts them into a single symbol error"),
                ),
                "By shuffling order, interleaving turns a concentrated burst into sparse errors that codes handle well.",
            ),
            q(
                "What is the main cost of interleaving?",
                (
                    opt("It lowers the code's minimum distance"),
                    opt(
                        "Latency and memory, since you must buffer the whole interleaver block",
                        correct=True,
                    ),
                    opt("It increases the bit error rate"),
                    opt("It removes all redundancy"),
                ),
                "Interleaving requires buffering the full block, adding latency and memory cost.",
            ),
            q(
                "What still defeats an interleaver?",
                (
                    opt("Any single-bit error"),
                    opt("A burst longer than the interleaver depth", correct=True),
                    opt("Scattered random errors"),
                    opt("Errors in the parity symbols"),
                ),
                "If a burst exceeds the interleaver depth, it still concentrates errors after de-interleaving — depth is a design knob.",
            ),
        ),
    },
    final=(
        q(
            "Why does the syndrome simplify decoding so dramatically?",
            (
                opt("It reveals the original message bits directly"),
                opt(
                    "It depends only on the error pattern, so it can be mapped to the most likely error",
                    correct=True,
                ),
                opt("It is always zero"),
                opt("It equals the generator matrix"),
            ),
            "The syndrome H eᵀ depends only on the error, so a lookup maps it to the most-likely error to XOR out.",
        ),
        q(
            "What is the relationship between G and H in systematic form?",
            (
                opt("They are the same matrix"),
                opt("If G = [I_k | P], then H = [Pᵀ | I_(n−k)]", correct=True),
                opt("H is the inverse of G"),
                opt("H has more columns than G"),
            ),
            "In systematic form G = [I_k | P] pairs with H = [Pᵀ | I_(n−k)].",
        ),
        q(
            "Which code would you choose to correct byte-level burst errors on a scratched optical disc?",
            (
                opt("A single parity bit"),
                opt("Reed–Solomon, often combined with interleaving", correct=True),
                opt("A (7,4) Hamming code alone"),
                opt("A plain CRC"),
            ),
            "RS works on symbols/bytes and, paired with interleaving (CIRC), recovers long scratches on CDs.",
        ),
        q(
            "What distinguishes a CRC from a Hamming code in typical use?",
            (
                opt("CRC corrects errors; Hamming only detects them"),
                opt(
                    "CRC is used for detection then retransmission; Hamming corrects single errors",
                    correct=True,
                ),
                opt("They are interchangeable in every system"),
                opt("CRC works only on a single bit"),
            ),
            "CRC detects corruption (then you resend); a Hamming code forward-corrects a single-bit error.",
        ),
        q(
            "Reed–Solomon is called maximum-distance-separable (MDS). What does that mean?",
            (
                opt("It has the smallest possible minimum distance"),
                opt(
                    "It achieves the best possible d_min = n − k + 1 for its parameters",
                    correct=True,
                ),
                opt("It separates the message from the noise perfectly"),
                opt("It can only be decoded by maximum likelihood"),
            ),
            "MDS means RS hits the Singleton bound, d_min = n − k + 1 — the best distance any (n,k) code can have.",
        ),
        q(
            "Why is the linear structure of block codes so valuable in practice?",
            (
                opt("It makes codewords longer"),
                opt(
                    "It lets encoding and checking be done with matrix (or polynomial) operations and compact syndromes",
                    correct=True,
                ),
                opt("It removes the need for any redundancy"),
                opt("It guarantees zero errors on every channel"),
            ),
            "Linearity means sums of codewords are codewords, enabling matrix encoding, H-based checks and syndrome decoding.",
        ),
    ),
)
