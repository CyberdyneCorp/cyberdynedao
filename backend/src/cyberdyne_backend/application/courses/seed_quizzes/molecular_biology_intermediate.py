"""Quiz questions for the Molecular Biology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Replication enzymology and fidelity": (
            q(
                "Which enzyme relieves the torsional strain ahead of the replication fork?",
                (
                    opt("Topoisomerase", correct=True),
                    opt("Ligase"),
                    opt("Primase"),
                    opt("SSB protein"),
                ),
                "Topoisomerase relaxes supercoils generated as helicase unwinds the duplex.",
            ),
            q(
                "Proofreading by DNA polymerase relies on which activity?",
                (
                    opt("A 3'->5' exonuclease that removes mismatched bases", correct=True),
                    opt("A 5'->3' exonuclease that degrades primers only"),
                    opt("A helicase that re-melts the duplex"),
                    opt("A kinase that phosphorylates errors"),
                ),
                "The polymerase backs up and excises a wrong base with its 3'->5' exonuclease.",
            ),
            q(
                "Why does overall replication fidelity reach about 1 error in 10^9-10^10 bases?",
                (
                    opt(
                        "Base selection, proofreading and mismatch repair multiply their accuracies",
                        correct=True,
                    ),
                    opt("A single enzyme is simply perfect"),
                    opt("DNA cannot be copied incorrectly"),
                    opt("Mutations are repaired only after cell death"),
                ),
                "Each fidelity layer multiplies the error reduction of the others.",
            ),
        ),
        "Transcription kinetics and RNA processing": (
            q(
                "Which polymerase transcribes protein-coding genes in eukaryotes?",
                (
                    opt("RNA polymerase II", correct=True),
                    opt("DNA polymerase III"),
                    opt("Reverse transcriptase"),
                    opt("Primase"),
                ),
                "Pol II synthesizes mRNA precursors in eukaryotes.",
            ),
            q(
                "What does the spliceosome do to pre-mRNA?",
                (
                    opt("Removes introns and joins exons", correct=True),
                    opt("Adds the 5' cap"),
                    opt("Adds the poly-A tail"),
                    opt("Translates the message"),
                ),
                "The spliceosome excises introns at GU...AG boundaries and ligates exons.",
            ),
            q(
                "If synthesis rate is constant and mRNA degrades first-order, the steady-state level approaches:",
                (
                    opt("The ratio of synthesis rate to degradation rate (k_s/k_d)", correct=True),
                    opt("Zero regardless of synthesis"),
                    opt("Infinity"),
                    opt("The square of the synthesis rate"),
                ),
                "At steady state production balances decay, giving level = k_s/k_d.",
            ),
        ),
        "Translation mechanics and the ribosome": (
            q(
                "The ribosome's peptidyl-transferase center is made of what?",
                (
                    opt("RNA (it is a ribozyme)", correct=True),
                    opt("DNA"),
                    opt("Lipid"),
                    opt("Only protein"),
                ),
                "rRNA catalyzes peptide-bond formation, making the ribosome a ribozyme.",
            ),
            q(
                "Which ribosomal site holds the incoming aminoacyl-tRNA?",
                (
                    opt("The A site", correct=True),
                    opt("The P site"),
                    opt("The E site"),
                    opt("The promoter"),
                ),
                "Aminoacyl-tRNAs enter at the A site; the growing chain sits in the P site.",
            ),
            q(
                "Kinetic proofreading improves translation accuracy by:",
                (
                    opt(
                        "Letting correct pairing proceed while mismatches are rejected before commitment",
                        correct=True,
                    ),
                    opt("Cutting the mRNA at every error"),
                    opt("Adding extra GTP to wrong codons"),
                    opt("Stopping all translation after one error"),
                ),
                "Correct codon-anticodon pairing alters timing so most mismatches dissociate first.",
            ),
        ),
        "Hybridization thermodynamics and Tm": (
            q(
                "The melting temperature Tm of a duplex is the temperature at which:",
                (
                    opt("Half the strands are paired and half are single", correct=True),
                    opt("All strands are permanently denatured"),
                    opt("DNA polymerase is fastest"),
                    opt("The poly-A tail is removed"),
                ),
                "At Tm, 50% of the molecules are duplex (delta-G = 0).",
            ),
            q(
                "Which change raises the Tm of an oligonucleotide?",
                (
                    opt("Higher GC content", correct=True),
                    opt("Lower salt concentration"),
                    opt("Shortening the oligo"),
                    opt("Adding more mismatches"),
                ),
                "More G-C pairs (and higher salt or length) increase Tm.",
            ),
            q(
                "The Wallace rule estimates Tm as approximately:",
                (
                    opt("2(A+T) + 4(G+C) in degrees C", correct=True),
                    opt("4(A+T) + 2(G+C)"),
                    opt("A + T + G + C"),
                    opt("(A+T)/(G+C)"),
                ),
                "Each A/T contributes ~2 C and each G/C ~4 C in the rule of thumb.",
            ),
        ),
        "PCR and exponential amplification": (
            q(
                "Why is a thermostable polymerase like Taq used in PCR?",
                (
                    opt("It survives the repeated ~95 C denaturation steps", correct=True),
                    opt("It works only at room temperature"),
                    opt("It needs no primers"),
                    opt("It copies RNA directly"),
                ),
                "Taq withstands the high denaturation temperature each cycle.",
            ),
            q(
                "With ideal efficiency, the number of target copies after n cycles grows:",
                (
                    opt("Exponentially, roughly doubling each cycle", correct=True),
                    opt("Linearly with cycle number"),
                    opt("Logarithmically"),
                    opt("Not at all"),
                ),
                "N = N0(1+E)^n, with E near 1, gives exponential amplification.",
            ),
            q(
                "In qPCR, a lower cycle-threshold (Ct) value indicates:",
                (
                    opt("More starting template in the sample", correct=True),
                    opt("Less starting template"),
                    opt("No template at all"),
                    opt("A failed reaction"),
                ),
                "More initial template crosses the fluorescence threshold sooner (lower Ct).",
            ),
        ),
        "Mutation and DNA repair": (
            q(
                "A single base change that introduces a premature stop codon is a:",
                (
                    opt("Nonsense mutation", correct=True),
                    opt("Silent mutation"),
                    opt("Frameshift mutation"),
                    opt("Synonymous mutation"),
                ),
                "A nonsense mutation converts a sense codon into a stop codon.",
            ),
            q(
                "Which pathway accurately repairs double-strand breaks using a homologous template?",
                (
                    opt("Homologous recombination", correct=True),
                    opt("Non-homologous end joining"),
                    opt("Base excision repair"),
                    opt("Nucleotide excision repair"),
                ),
                "HR uses a sister chromatid as template; NHEJ is faster but error-prone.",
            ),
            q(
                "UV-induced pyrimidine dimers are removed primarily by which pathway?",
                (
                    opt("Nucleotide excision repair", correct=True),
                    opt("Mismatch repair"),
                    opt("Homologous recombination"),
                    opt("Reverse transcription"),
                ),
                "NER excises bulky helix-distorting lesions such as UV dimers.",
            ),
        ),
    },
    final=(
        q(
            "Which combination of enzymes acts at the replication fork?",
            (
                opt("Helicase, primase, polymerase and ligase", correct=True),
                opt("Only reverse transcriptase"),
                opt("Only the ribosome"),
                opt("Spliceosome and Dicer"),
            ),
            "The replisome includes helicase, primase, polymerase, ligase and more.",
        ),
        q(
            "Co-transcriptional processing of eukaryotic pre-mRNA includes:",
            (
                opt("5' capping, splicing and 3' polyadenylation", correct=True),
                opt("Reverse transcription"),
                opt("Peptide-bond formation"),
                opt("Bridge amplification"),
            ),
            "Cap, splice and poly-A tail mature the transcript before export.",
        ),
        q(
            "The melting temperature of a DNA duplex increases with:",
            (
                opt("Higher GC content and higher salt", correct=True),
                opt("Lower GC content"),
                opt("More mismatches"),
                opt("Shorter length"),
            ),
            "G-C bonds, salt screening and length all stabilize the duplex.",
        ),
        q(
            "After n PCR cycles at full efficiency, copy number scales as:",
            (
                opt("2^n times the starting amount", correct=True),
                opt("n times the starting amount"),
                opt("n^2 times the starting amount"),
                opt("Constant"),
            ),
            "Ideal doubling each cycle gives 2^n amplification.",
        ),
        q(
            "Mismatch repair corrects errors that escape which step?",
            (
                opt("Polymerase base selection and proofreading", correct=True),
                opt("Translation"),
                opt("Capping"),
                opt("Poly-adenylation"),
            ),
            "MMR is the post-replication backstop after selection and proofreading.",
        ),
        q(
            "Why does adding fidelity layers drive the residual error rate down sharply?",
            (
                opt("The layers act in series and their accuracies multiply", correct=True),
                opt("They cancel each other out"),
                opt("Only the last layer matters"),
                opt("They add linearly, not multiplicatively"),
            ),
            "Sequential independent checks multiply, compounding the error reduction.",
        ),
    ),
)
