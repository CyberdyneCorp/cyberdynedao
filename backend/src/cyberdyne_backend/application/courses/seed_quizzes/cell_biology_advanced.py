"""Quiz questions for the Cell Biology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Cell-cycle control and checkpoints": (
            q(
                "What complexes drive transitions through the cell cycle?",
                (
                    opt("Cyclin-CDK complexes", correct=True),
                    opt("Histone-DNA complexes"),
                    opt("Ribosome-tRNA complexes"),
                    opt("Bcl-2-Bax complexes"),
                ),
                "Oscillating cyclins activate constitutive CDKs to time each transition.",
            ),
            q(
                "The spindle assembly checkpoint prevents what until chromosomes are attached?",
                (
                    opt("Activation of the APC/C and the onset of anaphase", correct=True),
                    opt("DNA replication in S phase"),
                    opt("Translation of mRNA"),
                    opt("Entry into G1"),
                ),
                "The SAC holds the APC/C inactive until all kinetochores are properly bioriented.",
            ),
            q(
                "Why is M-CDK activation described as switch-like (bistable)?",
                (
                    opt(
                        "Feedback makes activation steep and all-or-none, committing to mitosis",
                        correct=True,
                    ),
                    opt("It rises linearly with cyclin"),
                    opt("It never changes"),
                    opt("It is purely random"),
                ),
                "Positive feedback (Cdc25/Wee1) creates an ultrasensitive switch for irreversible commitment.",
            ),
        ),
        "Apoptosis and programmed cell death": (
            q(
                "Which enzymes execute apoptosis?",
                (
                    opt("Caspases", correct=True),
                    opt("DNA polymerases"),
                    opt("ATP synthases"),
                    opt("Kinesins"),
                ),
                "Caspases are cysteine proteases that drive the apoptotic cascade.",
            ),
            q(
                "The intrinsic apoptotic pathway is gated at which organelle?",
                (
                    opt("The mitochondrion (MOMP, cytochrome c release)", correct=True),
                    opt("The nucleus"),
                    opt("The Golgi apparatus"),
                    opt("The lysosome"),
                ),
                "Bax/Bak permeabilize the mitochondrial outer membrane, releasing cytochrome c.",
            ),
            q(
                "How do anti-apoptotic Bcl-2 family members act?",
                (
                    opt("They restrain Bax/Bak to prevent membrane permeabilization", correct=True),
                    opt("They directly cut DNA"),
                    opt("They synthesize ATP"),
                    opt("They activate executioner caspases directly"),
                ),
                "Bcl-2 and Bcl-xL inhibit the pore-forming Bax/Bak, raising the death threshold.",
            ),
        ),
        "Cancer: hallmarks and growth kinetics": (
            q(
                "Which is a hallmark of cancer?",
                (
                    opt("Resisting apoptosis (cell death)", correct=True),
                    opt("Reduced proliferation"),
                    opt("Increased dependence on growth signals"),
                    opt("Loss of genome instability"),
                ),
                "Evading apoptosis is a classic Hanahan-Weinberg hallmark.",
            ),
            q(
                "Why does real tumor growth deviate from pure exponential growth?",
                (
                    opt(
                        "Nutrient and oxygen limits slow growth as the tumor enlarges (Gompertzian)",
                        correct=True,
                    ),
                    opt("Tumors stop dividing immediately"),
                    opt("Cells shrink over time"),
                    opt("Mutations stop accumulating"),
                ),
                "Resource limitation decelerates growth, giving a saturating Gompertzian curve.",
            ),
            q(
                "What is a 'driver' mutation?",
                (
                    opt("A mutation that confers a selective growth advantage", correct=True),
                    opt("A mutation with no effect on fitness"),
                    opt("A mutation that always reverts"),
                    opt("A mutation only found in normal cells"),
                ),
                "Drivers promote cancer; passengers ride along without conferring advantage.",
            ),
        ),
        "Super-resolution and live-cell imaging": (
            q(
                "Roughly what is the diffraction limit of conventional light microscopy?",
                (
                    opt("About 200 nm", correct=True),
                    opt("About 2 nm"),
                    opt("About 2 micrometers"),
                    opt("About 200 micrometers"),
                ),
                "d is about lambda/(2 NA), roughly 200 nm for visible light.",
            ),
            q(
                "Which technique localizes single blinking molecules to beat the diffraction limit?",
                (
                    opt("PALM/STORM", correct=True),
                    opt("Brightfield microscopy"),
                    opt("Conventional confocal microscopy"),
                    opt("X-ray crystallography"),
                ),
                "PALM/STORM precisely localize sparse, blinking emitters to reach ~10-30 nm.",
            ),
            q(
                "How does localization precision scale with detected photons N?",
                (
                    opt("It improves roughly as 1/sqrt(N)", correct=True),
                    opt("It worsens as N increases"),
                    opt("It is independent of N"),
                    opt("It improves linearly with N"),
                ),
                "More photons sharpen localization, with sigma about s/sqrt(N).",
            ),
        ),
        "Single-cell omics and CRISPR": (
            q(
                "What is the purpose of UMIs in single-cell RNA sequencing?",
                (
                    opt("To count individual molecules rather than amplified reads", correct=True),
                    opt("To cut the genome"),
                    opt("To stain the cell membrane"),
                    opt("To measure pH"),
                ),
                "Unique molecular identifiers tag each original transcript so PCR duplicates are collapsed.",
            ),
            q(
                "Which method is commonly used to visualize scRNA-seq clusters in 2D?",
                (
                    opt("UMAP (or t-SNE) after PCA", correct=True),
                    opt("Gel electrophoresis"),
                    opt("Mass spectrometry"),
                    opt("Northern blotting"),
                ),
                "Nonlinear embeddings like UMAP/t-SNE project high-dimensional cell profiles to 2D.",
            ),
            q(
                "How does catalytically dead Cas9 (dCas9) modulate genes without cutting?",
                (
                    opt(
                        "Fused to repressor or activator domains, it tunes transcription (CRISPRi/a)",
                        correct=True,
                    ),
                    opt("It still makes double-strand breaks"),
                    opt("It deletes whole chromosomes"),
                    opt("It only edits RNA"),
                ),
                "dCas9 binds the target and, via fused effectors, represses or activates expression.",
            ),
        ),
        "Deep learning for cellular image analysis": (
            q(
                "Which architecture is widely used for cell and nucleus segmentation?",
                (
                    opt("U-Net (encoder-decoder with skip connections)", correct=True),
                    opt("A linear regression model"),
                    opt("A single decision tree"),
                    opt("A Fourier transform"),
                ),
                "U-Net and tools like Cellpose/StarDist excel at biomedical instance segmentation.",
            ),
            q(
                "What is 'virtual staining' in microscopy deep learning?",
                (
                    opt(
                        "Predicting fluorescence labels from label-free (e.g. brightfield) images",
                        correct=True,
                    ),
                    opt("Physically swelling the sample"),
                    opt("Adding more antibodies"),
                    opt("Increasing laser power"),
                ),
                "Networks learn to infer fluorescence signals from unstained inputs, reducing labeling.",
            ),
            q(
                "Why is held-out-plate validation important for these models?",
                (
                    opt(
                        "To detect batch effects and domain shift, avoiding overstated performance",
                        correct=True,
                    ),
                    opt("Because it speeds up training"),
                    opt("Because it removes the need for labels"),
                    opt("Because it increases image resolution"),
                ),
                "Validating across separate plates/instruments exposes batch effects that per-cell splits hide.",
            ),
        ),
    },
    final=(
        q(
            "Which checkpoint guards against entering mitosis with damaged DNA?",
            (
                opt("The G2/M DNA-damage checkpoint (ATM/ATR -> Chk -> p53)", correct=True),
                opt("The G1 restriction point only"),
                opt("The spindle assembly checkpoint"),
                opt("There is no such checkpoint"),
            ),
            "The G2/M checkpoint halts cells with DNA damage before mitosis.",
        ),
        q(
            "After MOMP, caspase activation is best described as what?",
            (
                opt("An irreversible, self-amplifying switch (point of no return)", correct=True),
                opt("Easily reversible"),
                opt("Linear and slow"),
                opt("Completely random"),
            ),
            "Once the mitochondrion is permeabilized, the caspase cascade commits the cell to death.",
        ),
        q(
            "Synthetic lethality is exploited therapeutically by which drug class in BRCA-mutant tumors?",
            (
                opt("PARP inhibitors", correct=True),
                opt("Antihistamines"),
                opt("Statins"),
                opt("Beta-blockers"),
            ),
            "PARP inhibition is synthetically lethal with BRCA deficiency in homologous recombination.",
        ),
        q(
            "Which microscopy approach minimizes phototoxicity for long volumetric live imaging?",
            (
                opt("Light-sheet microscopy", correct=True),
                opt("Electron microscopy"),
                opt("X-ray diffraction"),
                opt("Standard widefield with continuous illumination"),
            ),
            "Light-sheet illuminates only the focal plane, greatly reducing phototoxicity.",
        ),
        q(
            "A pooled CRISPR screen read out by single-cell sequencing is called what?",
            (
                opt("Perturb-seq", correct=True),
                opt("Sanger sequencing"),
                opt("Western blotting"),
                opt("FRAP"),
            ),
            "Perturb-seq couples pooled CRISPR perturbations with single-cell transcriptomic readout.",
        ),
        q(
            "Why does self-supervised pretraining help cellular image models?",
            (
                opt(
                    "Labeled-data learning curves saturate, so pretraining reduces labeling needs",
                    correct=True,
                ),
                opt("Because labels are never useful"),
                opt("Because it removes the need for any images"),
                opt("Because it eliminates batch effects automatically"),
            ),
            "Diminishing returns on labeled data motivate pretraining on large unlabeled corpora.",
        ),
    ),
)
