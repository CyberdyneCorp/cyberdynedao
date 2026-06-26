"""Quiz questions for the Python Programming for Biologists - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Functions, modules & docstrings": (
            q(
                "What is the purpose of a docstring?",
                (
                    opt("To document what a function does", correct=True),
                    opt("To speed up the function"),
                    opt("To define the return type at runtime"),
                    opt("To import a module"),
                ),
                "A triple-quoted docstring documents the function for humans and tools.",
            ),
            q(
                "A 'pure' function is one that:",
                (
                    opt(
                        "Returns output depending only on its inputs, with no hidden state",
                        correct=True,
                    ),
                    opt("Always prints to the screen"),
                    opt("Modifies global variables"),
                    opt("Reads from a file each call"),
                ),
                "Pure functions are deterministic and easy to test in isolation.",
            ),
            q(
                "How do you bring gc_content from seqtools.py into another script?",
                (
                    opt("from seqtools import gc_content", correct=True),
                    opt("include seqtools.gc_content"),
                    opt("load gc_content"),
                    opt("require('seqtools')"),
                ),
                "The from-import statement pulls a name out of a module.",
            ),
        ),
        "Files & biological formats": (
            q(
                "Why open files with a 'with' (context manager) block?",
                (
                    opt("It closes the file automatically, even on error", correct=True),
                    opt("It makes reading faster"),
                    opt("It compresses the file"),
                    opt("It converts text to binary"),
                ),
                "The context manager guarantees the file is closed when the block exits.",
            ),
            q(
                "How many lines does each read occupy in a FASTQ file?",
                (
                    opt("Four: id, sequence, '+', quality", correct=True),
                    opt("One"),
                    opt("Two: header and sequence"),
                    opt("Three"),
                ),
                "FASTQ stores four lines per read; FASTA uses header plus sequence.",
            ),
            q(
                "Phred quality is defined as Q = -10 log10(P). As Q rises, the error probability:",
                (
                    opt("Falls steeply", correct=True),
                    opt("Rises"),
                    opt("Stays constant"),
                    opt("Becomes negative"),
                ),
                "Higher Phred Q means exponentially lower probability of a base-call error.",
            ),
        ),
        "NumPy arrays & vectorisation": (
            q(
                "Compared with a Python list, a NumPy ndarray is:",
                (
                    opt("Fixed-type, contiguous and faster for numbers", correct=True),
                    opt("Slower but uses less code"),
                    opt("Able to mix any types freely with no speed cost"),
                    opt("Only one-dimensional"),
                ),
                "ndarrays are homogeneous, contiguous and enable fast vectorised math.",
            ),
            q(
                "What does 'vectorisation' mean in NumPy?",
                (
                    opt(
                        "Applying an operation to a whole array at once in compiled C", correct=True
                    ),
                    opt("Converting arrays to Python lists"),
                    opt("Looping in pure Python over each element"),
                    opt("Drawing arrows on a plot"),
                ),
                "Vectorised operations run in C with no per-element Python loop.",
            ),
            q(
                "log_fc > 1 on a NumPy array produces:",
                (
                    opt("A boolean mask for selecting elements", correct=True),
                    opt("A single number"),
                    opt("A syntax error"),
                    opt("A new sorted array"),
                ),
                "Comparisons give a boolean array usable for masking/fancy indexing.",
            ),
        ),
        "pandas DataFrames": (
            q(
                "A pandas DataFrame is best described as:",
                (
                    opt("A labelled 2-D table backed by NumPy", correct=True),
                    opt("A single column of numbers"),
                    opt("A plain Python dictionary"),
                    opt("An image format"),
                ),
                "A DataFrame is a labelled, columnar table, like a spreadsheet.",
            ),
            q(
                "Which accessor selects rows/columns by label?",
                (
                    opt(".loc", correct=True),
                    opt(".iloc"),
                    opt(".index"),
                    opt(".values"),
                ),
                ".loc selects by label; .iloc selects by integer position.",
            ),
            q(
                "The split-apply-combine pattern in pandas is implemented by:",
                (
                    opt("groupby followed by an aggregation", correct=True),
                    opt("read_csv"),
                    opt("sort_values"),
                    opt("to_csv"),
                ),
                "groupby splits by a key, applies a function, and combines results.",
            ),
        ),
        "From data to a tidy analysis": (
            q(
                "Why normalise raw counts to CPM before comparing samples?",
                (
                    opt("To remove differences in library (sequencing depth) size", correct=True),
                    opt("To increase the number of genes"),
                    opt("To convert counts to integers"),
                    opt("To sort the genes alphabetically"),
                ),
                "CPM scales by total counts so samples sequenced to different depths compare fairly.",
            ),
            q(
                "Selecting highly variable genes before clustering helps because it:",
                (
                    opt("Focuses on real biological signal rather than noise", correct=True),
                    opt("Removes all the data"),
                    opt("Guarantees no false positives"),
                    opt("Converts genes to samples"),
                ),
                "High-variance genes carry the structure; low-variance ones add mostly noise.",
            ),
            q(
                "Building the pipeline from small named functions mainly improves:",
                (
                    opt("Testability and reproducibility", correct=True),
                    opt("File size on disk"),
                    opt("The colour of plots"),
                    opt("Internet speed"),
                ),
                "Small functions can each be tested and rerun, aiding reproducibility.",
            ),
        ),
    },
    final=(
        q(
            "Type hints such as 'seq: str -> float' primarily:",
            (
                opt("Document intent and let tools catch type errors", correct=True),
                opt("Make code run faster at runtime"),
                opt("Are required by Python"),
                opt("Encrypt the function"),
            ),
            "Hints aid readability and static checkers like mypy; they are optional.",
        ),
        q(
            "Which format stores genomic feature coordinates?",
            (
                opt("BED / GFF", correct=True),
                opt("FASTQ"),
                opt("FASTA"),
                opt("PNG"),
            ),
            "BED and GFF describe feature intervals on a genome.",
        ),
        q(
            "What does broadcasting let NumPy do?",
            (
                opt("Combine arrays of different but compatible shapes", correct=True),
                opt("Send arrays over the network"),
                opt("Convert arrays to strings"),
                opt("Always require identical shapes"),
            ),
            "Broadcasting stretches a smaller array across a larger one without copying.",
        ),
        q(
            "df.loc[df['sample1'] > 100] returns:",
            (
                opt("Rows where sample1 exceeds 100", correct=True),
                opt("The number 100"),
                opt("Only the column names"),
                opt("A transposed table"),
            ),
            "A boolean mask inside .loc filters rows.",
        ),
        q(
            "A 'tidy' table has:",
            (
                opt("One observation per row and one variable per column", correct=True),
                opt("All data in a single cell"),
                opt("One column only"),
                opt("No headers"),
            ),
            "Tidy data makes plotting, modelling and statistics straightforward.",
        ),
        q(
            "Why prefer vectorised NumPy/pandas operations over Python loops on large arrays?",
            (
                opt("They run in compiled C and are far faster", correct=True),
                opt("They use more memory deliberately"),
                opt("They are required to read files"),
                opt("They change the data type to string"),
            ),
            "Vectorised operations avoid per-element Python overhead.",
        ),
    ),
)
