"""Quiz questions for the Protein Structure Prediction - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "AlphaFold2: end-to-end structure prediction": (
            q(
                "AlphaFold2 won which competition in 2020?",
                (
                    opt("CASP14", correct=True),
                    opt("The Nobel lottery"),
                    opt("CASP1"),
                    opt("ImageNet"),
                ),
                "AF2 achieved near-experimental accuracy at CASP14.",
            ),
            q(
                "Which two modules define AlphaFold2's architecture?",
                (
                    opt("The Evoformer and the structure module", correct=True),
                    opt("BLAST and Clustal"),
                    opt("A decision tree and SVM"),
                    opt("PCR and gel"),
                ),
                "Evoformer reasons over MSA/pair; the structure module builds 3D.",
            ),
            q(
                "What does AF2's 'recycling' do?",
                (
                    opt(
                        "Feeds outputs back into the network for iterative refinement", correct=True
                    ),
                    opt("Deletes the prediction"),
                    opt("Reuses old crystals"),
                    opt("Recomputes the MSA from scratch only"),
                ),
                "Recycling iteratively improves the prediction.",
            ),
        ),
        "RoseTTAFold and the three-track idea": (
            q(
                "RoseTTAFold's three tracks operate at which levels?",
                (
                    opt("1D sequence/MSA, 2D pairwise, 3D coordinates", correct=True),
                    opt("DNA, RNA, protein"),
                    opt("Past, present, future"),
                    opt("Helix, sheet, coil only"),
                ),
                "Information flows among 1D, 2D and 3D representations.",
            ),
            q(
                "Which lab released RoseTTAFold?",
                (
                    opt("The Baker lab", correct=True),
                    opt("DeepMind only"),
                    opt("The Sanger Centre"),
                    opt("NASA"),
                ),
                "RoseTTAFold came from the Baker lab.",
            ),
            q(
                "Which RoseTTAFold descendant is used for de novo protein design?",
                (
                    opt("RFdiffusion", correct=True),
                    opt("PSI-BLAST"),
                    opt("DSSP"),
                    opt("Clustal Omega"),
                ),
                "RFdiffusion generates novel backbones by denoising.",
            ),
        ),
        "Confidence metrics: pLDDT and PAE": (
            q(
                "What does pLDDT estimate?",
                (
                    opt("Per-residue local prediction accuracy (0-100)", correct=True),
                    opt("The melting temperature"),
                    opt("The molecular weight"),
                    opt("The number of chains"),
                ),
                "pLDDT scores local confidence per residue.",
            ),
            q(
                "A very low pLDDT region often indicates what?",
                (
                    opt("Intrinsic disorder rather than a simple error", correct=True),
                    opt("A perfect crystal"),
                    opt("High resolution"),
                    opt("A disulfide bond"),
                ),
                "Low pLDDT correlates with disordered regions.",
            ),
            q(
                "PAE (Predicted Aligned Error) is especially useful for judging:",
                (
                    opt("Relative domain positions and orientations", correct=True),
                    opt("The exact sequence"),
                    opt("The codon usage"),
                    opt("The crystallisation buffer"),
                ),
                "PAE reveals confident domains and uncertain orientations.",
            ),
        ),
        "Model quality assessment (MQA)": (
            q(
                "Which metric is length-normalised and >0.5 means the same fold?",
                (
                    opt("TM-score", correct=True),
                    opt("RMSD"),
                    opt("pH"),
                    opt("R-free"),
                ),
                "TM-score is robust to length and fold-discriminative.",
            ),
            q(
                "Consensus MQA estimates model quality by:",
                (
                    opt("Comparing across many decoys; good models cluster together", correct=True),
                    opt("Reading the answer key"),
                    opt("Measuring the gel band"),
                    opt("Counting atoms only"),
                ),
                "Consensus exploits agreement among decoys.",
            ),
            q(
                "Which is the CASP-standard superposition-based accuracy metric?",
                (
                    opt("GDT_TS", correct=True),
                    opt("Codon adaptation index"),
                    opt("Isoelectric point"),
                    opt("Tm"),
                ),
                "GDT_TS is the long-standing CASP backbone metric.",
            ),
        ),
        "Complexes, design and the frontier": (
            q(
                "Which metric scores protein-protein interface quality?",
                (
                    opt("DockQ / ipTM", correct=True),
                    opt("Q3"),
                    opt("Neff/L"),
                    opt("R-factor"),
                ),
                "ipTM and DockQ assess complex interfaces.",
            ),
            q(
                "ProteinMPNN is used for what?",
                (
                    opt("Designing sequences that fold to a target backbone", correct=True),
                    opt("Aligning DNA"),
                    opt("Solving crystals"),
                    opt("Measuring entropy of water"),
                ),
                "ProteinMPNN designs sequences for a given backbone.",
            ),
            q(
                "Why are protein language models (e.g. ESMFold) attractive for orphan proteins?",
                (
                    opt(
                        "They predict structure from a single sequence without a deep MSA",
                        correct=True,
                    ),
                    opt("They require the deepest possible MSA"),
                    opt("They need a crystal first"),
                    opt("They only work on DNA"),
                ),
                "Language models help when MSAs are shallow or absent.",
            ),
        ),
    },
    final=(
        q(
            "The AlphaFold2 module that jointly processes MSA and pair features is the:",
            (
                opt("Evoformer", correct=True),
                opt("Structure module"),
                opt("Distogram only"),
                opt("BLAST core"),
            ),
            "The Evoformer is the deep attention trunk.",
        ),
        q(
            "RoseTTAFold's defining design is its:",
            (
                opt("Three-track (1D/2D/3D) architecture", correct=True),
                opt("Single fragment library"),
                opt("Pure homology pipeline"),
                opt("Use of NMR restraints only"),
            ),
            "Three coupled tracks refine one another.",
        ),
        q(
            "pLDDT below ~50 most often signals:",
            (
                opt("Intrinsic disorder", correct=True),
                opt("A perfect model"),
                opt("A salt bridge"),
                opt("High resolution"),
            ),
            "Very low pLDDT flags disordered regions.",
        ),
        q(
            "A length-normalised fold-similarity score (>0.5 = same fold) is:",
            (
                opt("TM-score", correct=True),
                opt("RMSD"),
                opt("Q3"),
                opt("Tm"),
            ),
            "TM-score normalises for length.",
        ),
        q(
            "Which pairing designs novel proteins end to end?",
            (
                opt("RFdiffusion (backbone) + ProteinMPNN (sequence)", correct=True),
                opt("BLAST + Clustal"),
                opt("DSSP + STRIDE"),
                opt("PCR + gel"),
            ),
            "RFdiffusion generates backbones; ProteinMPNN designs sequences.",
        ),
        q(
            "An advantage of protein language model predictors (ESMFold) is:",
            (
                opt("Fast, MSA-independent prediction from a single sequence", correct=True),
                opt("They need an experimental structure first"),
                opt("They only work with quaternary structure"),
                opt("They ignore the amino-acid sequence"),
            ),
            "They trade some accuracy for speed and MSA independence.",
        ),
    ),
)
