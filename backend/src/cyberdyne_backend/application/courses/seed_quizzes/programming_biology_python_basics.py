"""Quiz questions for the Python Programming for Biologists - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why Python for biology": (
            q(
                "Which property best describes how Python defines code blocks?",
                (
                    opt("Indentation (whitespace)", correct=True),
                    opt("Curly braces { }"),
                    opt("Semicolons"),
                    opt("BEGIN/END keywords"),
                ),
                "Python uses indentation rather than braces to delimit blocks.",
            ),
            q(
                "Which library is the standard toolkit for biological sequences in Python?",
                (
                    opt("Biopython", correct=True),
                    opt("Matplotlib"),
                    opt("pandas"),
                    opt("requests"),
                ),
                "Biopython provides Seq objects, SeqIO parsers and Entrez access.",
            ),
            q(
                "Python is best described as which kind of language?",
                (
                    opt("Interpreted and dynamically typed", correct=True),
                    opt("Compiled and statically typed"),
                    opt("Assembly-level"),
                    opt("Markup, not a programming language"),
                ),
                "You run Python without a separate compile step and never declare types.",
            ),
        ),
        "Numbers, strings & variables": (
            q(
                "For DNA = 'ATGCGTAA', what does DNA[0:3] return?",
                (
                    opt("'ATG'", correct=True),
                    opt("'TGC'"),
                    opt("'ATGC'"),
                    opt("'A'"),
                ),
                "Slicing 0:3 takes indices 0,1,2 -> the start codon ATG.",
            ),
            q(
                "Why are Python strings well suited to representing DNA?",
                (
                    opt(
                        "They are immutable ordered sequences you can index and slice", correct=True
                    ),
                    opt("They automatically translate to protein"),
                    opt("They can only hold the letters A, C, G, T"),
                    opt("They are mutable so you can edit bases in place"),
                ),
                "Strings are immutable sequences supporting indexing, slicing and counting.",
            ),
            q(
                "Which expression computes GC fraction of a string dna?",
                (
                    opt("(dna.count('G') + dna.count('C')) / len(dna)", correct=True),
                    opt("dna.count('G') + dna.count('C')"),
                    opt("len(dna) / dna.count('GC')"),
                    opt("dna.count('A') / len(dna)"),
                ),
                "GC fraction is the count of G plus C divided by total length.",
            ),
        ),
        "Lists, tuples & dictionaries": (
            q(
                "Which collection is mutable and ordered?",
                (
                    opt("list", correct=True),
                    opt("tuple"),
                    opt("frozenset"),
                    opt("str"),
                ),
                "Lists are ordered and can be changed; tuples and strings are immutable.",
            ),
            q(
                "A codon table mapping codons to amino acids is best stored as a:",
                (
                    opt("dictionary", correct=True),
                    opt("list"),
                    opt("tuple"),
                    opt("integer"),
                ),
                "A dict maps keys (codons) to values (amino acids) with fast lookup.",
            ),
            q(
                "What is the typical average time to look up a key in a dictionary?",
                (
                    opt("O(1) constant time", correct=True),
                    opt("O(n) linear time"),
                    opt("O(n^2)"),
                    opt("O(log n)"),
                ),
                "Dictionaries are hash maps giving average constant-time lookup.",
            ),
        ),
        "Control flow: if, for, while": (
            q(
                "Which loop is most natural for walking DNA codon by codon?",
                (
                    opt("for i in range(0, len(dna)-2, 3)", correct=True),
                    opt("while True with no break"),
                    opt("for base in dna one base at a time"),
                    opt("if/elif chain"),
                ),
                "A for loop with step 3 over range advances one codon per iteration.",
            ),
            q(
                "What does the % operator give for codon position, i % 3?",
                (
                    opt("The remainder, identifying reading-frame position", correct=True),
                    opt("Floor division"),
                    opt("The quotient"),
                    opt("A percentage as a float"),
                ),
                "% is modulo; i % 3 gives 0,1,2 cycling through frame positions.",
            ),
            q(
                "Inside a loop, what does 'continue' do?",
                (
                    opt("Skips the rest of the current iteration", correct=True),
                    opt("Exits the loop entirely"),
                    opt("Restarts the whole program"),
                    opt("Pauses until input"),
                ),
                "continue jumps to the next iteration; break exits the loop.",
            ),
        ),
        "Comprehensions & clean iteration": (
            q(
                "What does [s.upper() for s in seqs] produce?",
                (
                    opt("A new list with each sequence uppercased", correct=True),
                    opt("It modifies seqs in place"),
                    opt("A single concatenated string"),
                    opt("A dictionary"),
                ),
                "A list comprehension builds a new transformed list.",
            ),
            q(
                "How do you keep only reads of length >= 150 in a comprehension?",
                (
                    opt("[r for r in reads if len(r) >= 150]", correct=True),
                    opt("[r for r in reads]"),
                    opt("[len(r) for r in reads]"),
                    opt("[r if r else 0 for r in reads]"),
                ),
                "The trailing if clause filters elements.",
            ),
            q(
                "Pairing two lists into a dict is idiomatically done with:",
                (
                    opt("{g: e for g, e in zip(genes, expr)}", correct=True),
                    opt("genes + expr"),
                    opt("dict(genes)"),
                    opt("[genes, expr]"),
                ),
                "zip walks both lists in lockstep; a dict comprehension builds the map.",
            ),
        ),
    },
    final=(
        q(
            "Which Python type is immutable?",
            (
                opt("tuple", correct=True),
                opt("list"),
                opt("dict"),
                opt("set"),
            ),
            "Tuples cannot be changed after creation; lists, dicts and sets can.",
        ),
        q(
            "What does true division '/' always return in Python 3?",
            (
                opt("A float", correct=True),
                opt("An int"),
                opt("A string"),
                opt("The remainder"),
            ),
            "/ yields a float; // is floor division.",
        ),
        q(
            "For dna = 'ATGCGTAA', dna.count('G') equals:",
            (
                opt("2", correct=True),
                opt("1"),
                opt("3"),
                opt("0"),
            ),
            "There are two G bases in ATGCGTAA.",
        ),
        q(
            "Which collection gives average O(1) key lookup?",
            (
                opt("dictionary", correct=True),
                opt("list"),
                opt("tuple"),
                opt("string"),
            ),
            "Dictionaries are hash maps with constant-time average lookup.",
        ),
        q(
            "Which statement transcribes DNA to RNA by replacing T with U?",
            (
                opt("dna.replace('T', 'U')", correct=True),
                opt("dna.upper()"),
                opt("dna.count('T')"),
                opt("dna[::-1]"),
            ),
            "replace swaps every T for U, mimicking transcription on a string.",
        ),
        q(
            "A list comprehension with an 'if' clause is used to:",
            (
                opt("Filter which elements are kept", correct=True),
                opt("Sort the list"),
                opt("Reverse the list"),
                opt("Convert it to a tuple"),
            ),
            "The if clause selects elements; the expression transforms them.",
        ),
    ),
)
