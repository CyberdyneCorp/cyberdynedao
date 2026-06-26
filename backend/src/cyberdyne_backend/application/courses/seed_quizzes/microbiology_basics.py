"""Quiz questions for the Microbiology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The microbial world and the three domains": (
            q(
                "Which molecule did Woese compare to define the three domains of life?",
                (
                    opt("Small-subunit ribosomal RNA (16S/18S rRNA)", correct=True),
                    opt("Plasmid DNA"),
                    opt("Cell-wall peptidoglycan"),
                    opt("Flagellar protein"),
                ),
                "Slowly evolving, universal rRNA serves as a molecular clock for deep phylogeny.",
            ),
            q(
                "Bacteria and Archaea are both:",
                (
                    opt("prokaryotic (no membrane-bound nucleus)", correct=True),
                    opt("eukaryotic with a true nucleus"),
                    opt("acellular like viruses"),
                    opt("strictly photosynthetic"),
                ),
                "Both lack a nucleus and organelles, but they are distinct domains.",
            ),
            q(
                "A distinctive feature of archaeal membranes is:",
                (
                    opt("ether-linked isoprenoid lipids", correct=True),
                    opt("ester-linked fatty acids only"),
                    opt("an outer membrane of LPS"),
                    opt("the complete absence of any membrane"),
                ),
                "Archaeal lipids are ether-linked isoprenoids, often stable in extreme conditions.",
            ),
        ),
        "The prokaryotic cell and its envelope": (
            q(
                "The bacterial cell wall is built mainly of:",
                (
                    opt("peptidoglycan", correct=True),
                    opt("cellulose"),
                    opt("chitin"),
                    opt("cholesterol"),
                ),
                "Peptidoglycan (NAG-NAM glycan chains cross-linked by peptides) gives the wall its strength.",
            ),
            q(
                "Compared with Gram-positive cells, Gram-negative cells have:",
                (
                    opt("a thin peptidoglycan layer plus an outer membrane", correct=True),
                    opt("a thick peptidoglycan layer and no outer membrane"),
                    opt("no cell wall at all"),
                    opt("a wall made of teichoic acid only"),
                ),
                "Gram-negative envelopes add an LPS-containing outer membrane over thin peptidoglycan.",
            ),
            q(
                "Penicillin kills growing bacteria by blocking:",
                (
                    opt("the transpeptidase that cross-links peptidoglycan", correct=True),
                    opt("DNA polymerase"),
                    opt("the ribosome"),
                    opt("ATP synthase"),
                ),
                "Beta-lactams inhibit cross-linking, weakening the wall against turgor pressure.",
            ),
        ),
        "Microscopy and the Gram stain": (
            q(
                "In the Gram stain, the critical differentiating step is:",
                (
                    opt("alcohol decolorization", correct=True),
                    opt("adding crystal violet"),
                    opt("adding the iodine mordant"),
                    opt("air-drying the smear"),
                ),
                "Decolorization removes the dye complex from Gram-negative but not Gram-positive cells.",
            ),
            q(
                "Gram-positive cells appear purple after staining because:",
                (
                    opt(
                        "thick peptidoglycan traps the crystal violet-iodine complex", correct=True
                    ),
                    opt("they absorb only the pink safranin"),
                    opt("they have an outer membrane"),
                    opt("they lack any cell wall"),
                ),
                "The thick wall retains the dye complex through decolorization.",
            ),
            q(
                "Resolution of a light microscope improves when you:",
                (
                    opt("increase numerical aperture or use shorter wavelength", correct=True),
                    opt("increase the wavelength of light"),
                    opt("lower the numerical aperture"),
                    opt("reduce the magnification only"),
                ),
                "Abbe's limit d = lambda/(2 NA): higher NA or shorter lambda gives finer detail.",
            ),
        ),
        "Culturing microbes: media and isolation": (
            q(
                "A selective medium is one that:",
                (
                    opt("inhibits unwanted organisms so target microbes grow", correct=True),
                    opt("changes color to reveal a metabolic trait"),
                    opt("has a fully defined chemical composition"),
                    opt("contains no nutrients at all"),
                ),
                "Selective media (e.g. MacConkey) suppress some organisms while allowing others.",
            ),
            q(
                "A single colony on an agar plate ideally represents:",
                (
                    opt("a clone descended from one founding cell", correct=True),
                    opt("a mixture of many different species"),
                    opt("a single virus particle"),
                    opt("dead cells only"),
                ),
                "A colony-forming unit grows from one (or a clump of) viable cell(s).",
            ),
            q(
                "The great plate-count anomaly refers to the fact that:",
                (
                    opt(
                        "most environmental microbes are not cultivable on standard media",
                        correct=True,
                    ),
                    opt("plates always overestimate cell numbers"),
                    opt("agar kills most bacteria"),
                    opt("microscopy undercounts cells"),
                ),
                "Microscopic counts greatly exceed culturable counts because most taxa resist culture.",
            ),
        ),
        "Microbial growth and the growth curve": (
            q(
                "Starting from N0 cells, after n generations the population is:",
                (
                    opt("N0 x 2^n", correct=True),
                    opt("N0 + 2n"),
                    opt("N0 / 2^n"),
                    opt("2 x N0 x n"),
                ),
                "Binary fission doubles the population each generation.",
            ),
            q(
                "During which phase is the specific growth rate maximal?",
                (
                    opt("Log (exponential) phase", correct=True),
                    opt("Lag phase"),
                    opt("Stationary phase"),
                    opt("Death phase"),
                ),
                "Cells divide at their fastest sustained rate during exponential growth.",
            ),
            q(
                "Generation time g relates to specific growth rate mu by:",
                (
                    opt("g = ln(2) / mu", correct=True),
                    opt("g = mu / ln(2)"),
                    opt("g = mu x ln(2)"),
                    opt("g = 2 x mu"),
                ),
                "Doubling corresponds to g = ln(2)/mu.",
            ),
        ),
    },
    final=(
        q(
            "How many domains of life did rRNA analysis reveal?",
            (
                opt("Three (Bacteria, Archaea, Eukarya)", correct=True),
                opt("Two (prokaryotes and eukaryotes)"),
                opt("Five kingdoms"),
                opt("One"),
            ),
            "Woese's three-domain system replaced the older two-empire view.",
        ),
        q(
            "The defining structural difference between prokaryotes and eukaryotes is:",
            (
                opt("prokaryotes lack a membrane-bound nucleus", correct=True),
                opt("prokaryotes have larger cells"),
                opt("prokaryotes never have DNA"),
                opt("prokaryotes always have organelles"),
            ),
            "Prokaryotes keep their DNA in a nucleoid, not a nucleus.",
        ),
        q(
            "Which stain separates bacteria into two broad wall types?",
            (
                opt("The Gram stain", correct=True),
                opt("Hematoxylin and eosin"),
                opt("Coomassie blue"),
                opt("Silver nitrate"),
            ),
            "The Gram stain distinguishes thick-walled (positive) from outer-membrane (negative) cells.",
        ),
        q(
            "A pure culture is best obtained by:",
            (
                opt("the streak-plate method to isolate single colonies", correct=True),
                opt("pooling many species together"),
                opt("growing cells only in liquid forever"),
                opt("heating cells to 121 C"),
            ),
            "Streaking dilutes cells so isolated colonies arise from single cells.",
        ),
        q(
            "Exponential bacterial growth means the population:",
            (
                opt("doubles in a fixed generation time", correct=True),
                opt("increases by a fixed number each minute"),
                opt("stays constant"),
                opt("declines steadily"),
            ),
            "Each cell divides into two, giving geometric (exponential) increase.",
        ),
        q(
            "An obligate aerobe requires which terminal electron acceptor to grow?",
            (
                opt("Oxygen", correct=True),
                opt("Nitrate only"),
                opt("Sulfate only"),
                opt("No acceptor at all"),
            ),
            "Obligate aerobes depend on O2 as the terminal electron acceptor.",
        ),
    ),
)
