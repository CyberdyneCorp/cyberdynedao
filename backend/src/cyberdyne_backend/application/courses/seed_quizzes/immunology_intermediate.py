"""Quiz questions for the Immunology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Antibody structure and isotypes": (
            q(
                "Which part of the antibody contains the antigen-binding site?",
                (
                    opt(
                        "The variable (V) regions of the Fab arms, formed by the CDRs", correct=True
                    ),
                    opt("The Fc stem"),
                    opt("The disulfide bonds only"),
                    opt("The light-chain constant region"),
                ),
                "The paratope is built from the CDR loops in the V regions of the Fab arms.",
            ),
            q(
                "Which isotype is the first antibody produced and a strong complement activator?",
                (
                    opt("IgM", correct=True),
                    opt("IgE"),
                    opt("IgD"),
                    opt("IgA"),
                ),
                "IgM is made first, forms a pentamer and activates complement strongly.",
            ),
            q(
                "What distinguishes affinity from avidity?",
                (
                    opt(
                        "Affinity is a single site's strength; avidity is the combined multivalent binding",
                        correct=True,
                    ),
                    opt("They are identical terms"),
                    opt("Affinity requires two arms, avidity one"),
                    opt("Avidity is always weaker than affinity"),
                ),
                "A multivalent antibody achieves high avidity even from modest per-site affinity.",
            ),
        ),
        "Antigen-antibody binding and affinity": (
            q(
                "What does a small dissociation constant Kd indicate?",
                (
                    opt("High affinity binding", correct=True),
                    opt("Low affinity binding"),
                    opt("No binding at all"),
                    opt("That the antigen is multivalent"),
                ),
                "Kd = koff/kon; a small Kd (nanomolar or below) means high affinity.",
            ),
            q(
                "At what free-antigen concentration is binding half-maximal?",
                (
                    opt("When free antigen equals Kd", correct=True),
                    opt("When free antigen is zero"),
                    opt("At infinite antigen"),
                    opt("When kon equals zero"),
                ),
                "Theta = [Ag]/([Ag]+Kd), so half-saturation occurs at [Ag] = Kd.",
            ),
            q(
                "Which method records real-time on- and off-rates of binding?",
                (
                    opt("Surface plasmon resonance (SPR / Biacore)", correct=True),
                    opt("Gram staining"),
                    opt("PCR"),
                    opt("Centrifugation"),
                ),
                "SPR measures kon and koff in real time to derive Kd.",
            ),
        ),
        "MHC and antigen presentation": (
            q(
                "Which T cells recognize peptides presented on MHC class I?",
                (
                    opt("CD8+ cytotoxic T cells", correct=True),
                    opt("CD4+ helper T cells"),
                    opt("B cells"),
                    opt("NK cells via antibody"),
                ),
                "MHC-I presents cytosolic peptides to CD8+ T cells on all nucleated cells.",
            ),
            q(
                "Where do peptides presented on MHC class II originate?",
                (
                    opt(
                        "From extracellular proteins degraded in the endolysosomal pathway",
                        correct=True,
                    ),
                    opt("From cytosolic proteins cut by the proteasome"),
                    opt("From the nucleus directly"),
                    opt("From the mitochondrial matrix only"),
                ),
                "MHC-II presents endocytosed antigen to CD4+ T cells on professional APCs.",
            ),
            q(
                "Why is the MHC locus so important for population-level immunity?",
                (
                    opt(
                        "It is highly polymorphic, broadening the peptides a population can present",
                        correct=True,
                    ),
                    opt("It is identical in everyone"),
                    opt("It encodes antibodies"),
                    opt("It has no allelic variation"),
                ),
                "MHC is the most polymorphic locus, diversifying presented peptides across people.",
            ),
        ),
        "T-cell activation and helper subsets": (
            q(
                "What happens to a T cell that receives signal 1 without signal 2?",
                (
                    opt("It becomes anergic (functionally unresponsive)", correct=True),
                    opt("It becomes fully activated"),
                    opt("It immediately kills the APC"),
                    opt("It switches isotype"),
                ),
                "Costimulation (CD28-B7) is required; signal 1 alone causes anergy.",
            ),
            q(
                "Which CD4+ helper subset secretes IFN-gamma and activates macrophages?",
                (
                    opt("Th1", correct=True),
                    opt("Th2"),
                    opt("Treg"),
                    opt("Th17"),
                ),
                "Th1 cells drive cell-mediated defense against intracellular pathogens.",
            ),
            q(
                "Which cytokine is the key autocrine growth factor for proliferating T cells?",
                (
                    opt("IL-2", correct=True),
                    opt("Hemoglobin"),
                    opt("Insulin"),
                    opt("C3b"),
                ),
                "IL-2 drives clonal expansion of activated T cells.",
            ),
        ),
        "B-cell responses and the germinal center": (
            q(
                "Which enzyme drives both somatic hypermutation and class-switch recombination?",
                (
                    opt("Activation-induced cytidine deaminase (AID)", correct=True),
                    opt("DNA polymerase III"),
                    opt("Lysozyme"),
                    opt("ATP synthase"),
                ),
                "AID initiates both SHM and CSR in germinal-center B cells.",
            ),
            q(
                "What is the outcome of affinity maturation?",
                (
                    opt(
                        "The average affinity rises (mean Kd falls) as better binders are selected",
                        correct=True,
                    ),
                    opt("All antibodies lose their specificity"),
                    opt("The repertoire becomes more diverse and lower affinity"),
                    opt("Antibodies are degraded"),
                ),
                "Selection for higher-affinity mutants lowers the population mean Kd.",
            ),
            q(
                "What does class-switch recombination change while preserving specificity?",
                (
                    opt("The heavy-chain constant region (e.g. IgM to IgG/IgA/IgE)", correct=True),
                    opt("The antigen-binding variable region"),
                    opt("The light chain only"),
                    opt("The MHC allele"),
                ),
                "CSR swaps the heavy-chain constant region to change effector function.",
            ),
        ),
    },
    final=(
        q(
            "Which equation correctly defines the dissociation constant?",
            (
                opt("Kd = koff / kon", correct=True),
                opt("Kd = kon / koff"),
                opt("Kd = kon * koff"),
                opt("Kd = kon + koff"),
            ),
            "Kd is the ratio of the off-rate to the on-rate; small Kd means tight binding.",
        ),
        q(
            "Which pairing of MHC class and T cell is correct?",
            (
                opt("MHC-I with CD8+ T cells; MHC-II with CD4+ T cells", correct=True),
                opt("MHC-I with CD4+ T cells; MHC-II with CD8+ T cells"),
                opt("Both classes only with B cells"),
                opt("Neither class presents to T cells"),
            ),
            "MHC-I -> CD8 cytotoxic; MHC-II -> CD4 helper.",
        ),
        q(
            "What are the three signals required for full T-cell activation?",
            (
                opt("TCR-pMHC, costimulation, and cytokines", correct=True),
                opt("Complement, lysozyme, and mucus"),
                opt("IgG, IgA, and IgM"),
                opt("Skin, pH, and flora"),
            ),
            "Signal 1 (TCR-pMHC), signal 2 (CD28-B7), signal 3 (cytokine milieu).",
        ),
        q(
            "Which isotype dominates the serum, opsonizes, and crosses the placenta?",
            (
                opt("IgG", correct=True),
                opt("IgM"),
                opt("IgE"),
                opt("IgD"),
            ),
            "IgG is the major serum antibody with broad effector and placental transfer.",
        ),
        q(
            "What is the germinal center the engine of?",
            (
                opt("Affinity maturation and class switching of B cells", correct=True),
                opt("Proteasomal degradation"),
                opt("Negative selection of thymocytes"),
                opt("Complement activation"),
            ),
            "GCs drive SHM, selection, affinity maturation and CSR with Tfh help.",
        ),
        q(
            "Fractional occupancy of binding sites follows which functional form in free antigen?",
            (
                opt("A saturating hyperbola, [Ag]/([Ag]+Kd)", correct=True),
                opt("A straight line through the origin with no limit"),
                opt("An exponential that grows without bound"),
                opt("A constant independent of antigen"),
            ),
            "Binding saturates: occupancy = [Ag]/([Ag]+Kd) approaches 1 at high antigen.",
        ),
    ),
)
