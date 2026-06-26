"""Quiz questions for the Molecular Biology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "DNA structure and the double helix": (
            q(
                "Which base pairs are correct in DNA?",
                (
                    opt("A pairs with T, and G pairs with C", correct=True),
                    opt("A pairs with G, and T pairs with C"),
                    opt("A pairs with C, and G pairs with T"),
                    opt("Every base can pair with any other base"),
                ),
                "Chargaff's rules: A-T (two H-bonds) and G-C (three H-bonds).",
            ),
            q(
                "Why is GC-rich DNA more thermally stable than AT-rich DNA?",
                (
                    opt("G-C pairs have three hydrogen bonds versus two in A-T", correct=True),
                    opt("G-C pairs have only one hydrogen bond"),
                    opt("GC-rich DNA has no phosphate backbone"),
                    opt("AT pairs are covalently bonded"),
                ),
                "The extra hydrogen bond in each G-C pair raises the melting temperature.",
            ),
            q(
                "What does it mean that the two DNA strands are antiparallel?",
                (
                    opt("They run in opposite 5'-to-3' directions", correct=True),
                    opt("They are identical in sequence"),
                    opt("They never base pair"),
                    opt("They are made of different sugars"),
                ),
                "One strand runs 5'->3' while its partner runs 3'->5'.",
            ),
        ),
        "RNA: types and differences from DNA": (
            q(
                "Which base replaces thymine in RNA?",
                (
                    opt("Uracil", correct=True),
                    opt("Cytosine"),
                    opt("Guanine"),
                    opt("Adenine"),
                ),
                "RNA uses uracil (U) in place of thymine (T).",
            ),
            q(
                "Which RNA carries the coding message from gene to ribosome?",
                (
                    opt("mRNA", correct=True),
                    opt("tRNA"),
                    opt("rRNA"),
                    opt("miRNA"),
                ),
                "Messenger RNA carries the protein-coding sequence to the ribosome.",
            ),
            q(
                "What makes RNA chemically less stable than DNA?",
                (
                    opt("The reactive 2'-hydroxyl group on ribose", correct=True),
                    opt("It has no phosphate backbone"),
                    opt("It is always double-stranded"),
                    opt("It contains thymine"),
                ),
                "The 2'-OH of ribose makes RNA more prone to hydrolysis than DNA.",
            ),
        ),
        "The central dogma of molecular biology": (
            q(
                "What is the normal direction of information flow in the central dogma?",
                (
                    opt("DNA -> RNA -> protein", correct=True),
                    opt("Protein -> RNA -> DNA"),
                    opt("RNA -> DNA -> protein"),
                    opt("Protein -> DNA -> RNA"),
                ),
                "DNA is transcribed to RNA, which is translated to protein.",
            ),
            q(
                "Which enzyme performs reverse transcription (RNA -> DNA)?",
                (
                    opt("Reverse transcriptase", correct=True),
                    opt("DNA ligase"),
                    opt("RNA polymerase"),
                    opt("Helicase"),
                ),
                "Retroviruses use reverse transcriptase to copy RNA into DNA.",
            ),
            q(
                "The central dogma forbids information flowing in which direction?",
                (
                    opt("From protein back into nucleic acid sequence", correct=True),
                    opt("From DNA to RNA"),
                    opt("From RNA to protein"),
                    opt("From DNA to DNA"),
                ),
                "Sequence information does not flow from protein to nucleic acid.",
            ),
        ),
        "DNA replication overview": (
            q(
                "What does semiconservative replication mean?",
                (
                    opt(
                        "Each daughter duplex keeps one parental strand and gains one new strand",
                        correct=True,
                    ),
                    opt("Both strands of each daughter are brand new"),
                    opt("The parental duplex stays fully intact"),
                    opt("Only one of the two strands is ever copied"),
                ),
                "Meselson and Stahl showed each new duplex has one old and one new strand.",
            ),
            q(
                "Why is the lagging strand made in Okazaki fragments?",
                (
                    opt(
                        "DNA polymerase only synthesizes 5'->3', so the antiparallel strand is built in pieces",
                        correct=True,
                    ),
                    opt("Helicase chops the strand into pieces"),
                    opt("The lagging strand has no template"),
                    opt("Ligase cuts the DNA into fragments"),
                ),
                "Polymerase works only 5'->3', forcing discontinuous synthesis on the lagging strand.",
            ),
            q(
                "Which enzyme joins Okazaki fragments together?",
                (
                    opt("DNA ligase", correct=True),
                    opt("Primase"),
                    opt("Helicase"),
                    opt("Topoisomerase"),
                ),
                "DNA ligase seals the nicks between adjacent Okazaki fragments.",
            ),
        ),
        "Transcription and translation overview": (
            q(
                "Where does RNA polymerase bind to begin transcription?",
                (
                    opt("The promoter", correct=True),
                    opt("The poly-A tail"),
                    opt("The ribosome"),
                    opt("The stop codon"),
                ),
                "RNA polymerase recognizes and binds the promoter to start transcription.",
            ),
            q(
                "Which codon typically starts translation?",
                (
                    opt("AUG", correct=True),
                    opt("UAA"),
                    opt("UAG"),
                    opt("UGA"),
                ),
                "AUG is the start codon (methionine); UAA/UAG/UGA are stop codons.",
            ),
            q(
                "What molecule matches each codon to its amino acid during translation?",
                (
                    opt("tRNA", correct=True),
                    opt("DNA polymerase"),
                    opt("mRNA cap"),
                    opt("rRNA only"),
                ),
                "tRNA acts as the adaptor, pairing its anticodon to the mRNA codon.",
            ),
        ),
        "The genetic code": (
            q(
                "How many bases make up a codon?",
                (
                    opt("Three", correct=True),
                    opt("One"),
                    opt("Two"),
                    opt("Four"),
                ),
                "Codons are triplets, giving 4^3 = 64 possible codons.",
            ),
            q(
                "What does it mean that the genetic code is degenerate?",
                (
                    opt("Most amino acids are encoded by more than one codon", correct=True),
                    opt("Each codon codes for several amino acids"),
                    opt("Some codons code for nothing at all"),
                    opt("The code differs in every organism"),
                ),
                "Degeneracy means multiple synonymous codons map to the same amino acid.",
            ),
            q(
                "How many stop codons are there in the standard genetic code?",
                (
                    opt("Three (UAA, UAG, UGA)", correct=True),
                    opt("One"),
                    opt("Twenty"),
                    opt("Sixty-four"),
                ),
                "Of the 64 codons, three signal termination.",
            ),
        ),
    },
    final=(
        q(
            "Which sugar distinguishes DNA from RNA?",
            (
                opt("Deoxyribose (DNA) versus ribose (RNA)", correct=True),
                opt("Glucose versus fructose"),
                opt("Ribose (DNA) versus deoxyribose (RNA)"),
                opt("They use the same sugar"),
            ),
            "DNA uses deoxyribose; RNA uses ribose with a 2'-OH.",
        ),
        q(
            "In the double helix, which pairing is correct?",
            (
                opt("Adenine with thymine", correct=True),
                opt("Adenine with guanine"),
                opt("Cytosine with thymine"),
                opt("Guanine with adenine"),
            ),
            "A-T and G-C are the complementary base pairs.",
        ),
        q(
            "Transcription produces which molecule?",
            (
                opt("RNA from a DNA template", correct=True),
                opt("DNA from an RNA template"),
                opt("Protein from RNA"),
                opt("DNA from a protein"),
            ),
            "Transcription copies a gene into RNA.",
        ),
        q(
            "DNA replication is described as semiconservative because:",
            (
                opt("Each new duplex retains one original strand", correct=True),
                opt("Both new strands are entirely new"),
                opt("No new strands are synthesized"),
                opt("The genome is replicated only once per lifetime"),
            ),
            "Each daughter molecule conserves one parental strand.",
        ),
        q(
            "Translation occurs at which cellular machine?",
            (
                opt("The ribosome", correct=True),
                opt("The nucleus"),
                opt("DNA polymerase"),
                opt("The Golgi apparatus"),
            ),
            "Ribosomes read mRNA codons to assemble polypeptides.",
        ),
        q(
            "Because the genetic code is degenerate, many point mutations are:",
            (
                opt("Silent (synonymous), causing no amino-acid change", correct=True),
                opt("Always lethal"),
                opt("Always frameshifts"),
                opt("Impossible to occur"),
            ),
            "Redundant codons mean some base changes do not alter the encoded amino acid.",
        ),
    ),
)
