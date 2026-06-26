"""Quiz questions for the Immunology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Immune tolerance and autoimmunity": (
            q(
                "What does AIRE enable in the thymus?",
                (
                    opt(
                        "Expression of peripheral self-antigens for negative selection of self-reactive T cells",
                        correct=True,
                    ),
                    opt("Class switching of B cells"),
                    opt("Complement activation"),
                    opt("Antibody secretion"),
                ),
                "AIRE drives ectopic self-antigen expression so self-reactive thymocytes are deleted.",
            ),
            q(
                "Which cell type enforces peripheral tolerance through suppression?",
                (
                    opt("FoxP3+ regulatory T cells (Tregs)", correct=True),
                    opt("Neutrophils"),
                    opt("Plasma cells"),
                    opt("NK cells"),
                ),
                "FoxP3+ Tregs suppress autoreactive responses via IL-10 and TGF-beta.",
            ),
            q(
                "What is molecular mimicry in autoimmunity?",
                (
                    opt(
                        "A microbial epitope resembling self, triggering cross-reactive attack on self",
                        correct=True,
                    ),
                    opt("Two antibodies with identical sequences"),
                    opt("A vaccine that copies a pathogen exactly"),
                    opt("The deletion of all self-reactive cells"),
                ),
                "Mimicry lets an anti-microbial response cross-react with similar self antigens.",
            ),
        ),
        "Cancer immunotherapy: checkpoints and CAR-T": (
            q(
                "How does PD-1/PD-L1 engagement help tumors evade immunity?",
                (
                    opt("It shuts down the T-cell effector response (exhaustion)", correct=True),
                    opt("It activates T cells more strongly"),
                    opt("It increases MHC-I on tumor cells"),
                    opt("It recruits more neutrophils"),
                ),
                "Tumor PD-L1 engaging PD-1 inhibits the T cell; blocking it reactivates killing.",
            ),
            q(
                "What is the antigen-recognition component of a chimeric antigen receptor?",
                (
                    opt("An antibody-derived scFv (e.g. anti-CD19)", correct=True),
                    opt("A complete MHC molecule"),
                    opt("A native TCR alpha-beta pair"),
                    opt("A complement protein"),
                ),
                "CARs fuse an scFv for tumor antigen to CD3-zeta and costimulatory domains.",
            ),
            q(
                "Which serious toxicity is associated with CAR-T therapy?",
                (
                    opt("Cytokine release syndrome", correct=True),
                    opt("Scurvy"),
                    opt("Iron-deficiency anemia"),
                    opt("Lactose intolerance"),
                ),
                "Massive CAR-T activation can drive dangerous systemic cytokine release.",
            ),
        ),
        "Vaccines and mRNA platforms": (
            q(
                "What does the lipid nanoparticle (LNP) do in an mRNA vaccine?",
                (
                    opt(
                        "Delivers and protects the mRNA so host cells can translate the antigen",
                        correct=True,
                    ),
                    opt("Encodes the antigen sequence"),
                    opt("Acts as the antibody"),
                    opt("Replaces the need for any antigen"),
                ),
                "The LNP encapsulates and delivers nucleoside-modified mRNA into cells.",
            ),
            q(
                "How is vaccine efficacy (VE) defined?",
                (
                    opt(
                        "VE = 1 - RR, where RR is the risk ratio vaccinated vs unvaccinated",
                        correct=True,
                    ),
                    opt("VE = RR - 1"),
                    opt("VE equals the antibody titer"),
                    opt("VE = number of doses given"),
                ),
                "VE is one minus the relative risk of disease in the vaccinated group.",
            ),
            q(
                "Why are adjuvants included in many vaccines?",
                (
                    opt(
                        "They provide the innate danger signal needed for strong adaptive priming",
                        correct=True,
                    ),
                    opt("They are the genetic material of the pathogen"),
                    opt("They suppress the immune response"),
                    opt("They replace memory cells"),
                ),
                "Adjuvants (alum, MF59, the LNP itself) boost innate signals that prime adaptive immunity.",
            ),
        ),
        "Quantitative immunology: flow and sequencing": (
            q(
                "What does flow cytometry measure?",
                (
                    opt(
                        "Fluorophore-tagged markers on individual cells streamed past lasers",
                        correct=True,
                    ),
                    opt("The mass of a whole organ"),
                    opt("DNA replication speed in bulk tissue"),
                    opt("Blood pressure"),
                ),
                "Flow cytometry immunophenotypes single cells by their labeled surface/intracellular markers.",
            ),
            q(
                "What does paired single-cell RNA-seq with TCR/BCR repertoire-seq reveal?",
                (
                    opt(
                        "Each cell's transcriptional state linked to its exact receptor sequence",
                        correct=True,
                    ),
                    opt("Only the average gene expression of a tissue"),
                    opt("The patient's blood type"),
                    opt("Nothing about clonality"),
                ),
                "It connects clonotype to phenotype, mapping clonal expansion and trajectories.",
            ),
            q(
                "What happens to Shannon entropy of a repertoire as one clone dominates?",
                (
                    opt("Diversity falls as the response becomes clonally focused", correct=True),
                    opt("Diversity rises without limit"),
                    opt("It stays exactly constant"),
                    opt("It becomes negative"),
                ),
                "Shannon entropy decreases as expansion concentrates the repertoire on few clones.",
            ),
        ),
        "Computational and AI methods in immunology": (
            q(
                "What do tools like NetMHCpan and MHCflurry predict?",
                (
                    opt(
                        "Which peptides a given HLA allele will present (peptide-MHC binding)",
                        correct=True,
                    ),
                    opt("The patient's heart rate"),
                    opt("Antibody serum half-life only"),
                    opt("The color of a cell culture"),
                ),
                "These neural networks score peptide-HLA pairs to rank candidate epitopes.",
            ),
            q(
                "How is AlphaFold used in immunology?",
                (
                    opt(
                        "To predict antibody/antigen structures and, with docking, their interfaces",
                        correct=True,
                    ),
                    opt("To sequence DNA"),
                    opt("To stain cells for flow cytometry"),
                    opt("To measure body temperature"),
                ),
                "AlphaFold accelerates structure prediction for rational antibody/epitope design.",
            ),
            q(
                "What does the area under the ROC curve (AUC) describe?",
                (
                    opt(
                        "A classifier's ability to rank positives above negatives across thresholds",
                        correct=True,
                    ),
                    opt("The number of training samples"),
                    opt("The molecular weight of the antigen"),
                    opt("The vaccine dose in milligrams"),
                ),
                "AUC summarizes discrimination; 0.5 is random, closer to 1.0 is better.",
            ),
        ),
    },
    final=(
        q(
            "Which mechanism is part of central tolerance?",
            (
                opt(
                    "Thymic negative selection of self-reactive T cells (AIRE-dependent)",
                    correct=True,
                ),
                opt("Peripheral Treg suppression"),
                opt("Anergy from missing costimulation"),
                opt("Complement-mediated lysis"),
            ),
            "Central tolerance deletes self-reactive cells during development in thymus/marrow.",
        ),
        q(
            "Which checkpoint molecule outcompetes CD28 for B7 during T-cell priming?",
            (
                opt("CTLA-4", correct=True),
                opt("PD-L1"),
                opt("CD19"),
                opt("FoxP3"),
            ),
            "CTLA-4 dampens priming by outcompeting CD28; anti-CTLA-4 releases this brake.",
        ),
        q(
            "Why do mRNA vaccines engage both antibody and T-cell arms effectively?",
            (
                opt(
                    "Host cells translate the antigen, enabling MHC presentation and B-cell help",
                    correct=True,
                ),
                opt("They inject preformed antibodies"),
                opt("They contain live replicating virus"),
                opt("They bypass antigen presentation entirely"),
            ),
            "Endogenously translated antigen is presented on MHC and also drives antibody responses.",
        ),
        q(
            "Which assay directly quantifies antigen-specific T cells?",
            (
                opt("MHC tetramer staining", correct=True),
                opt("Gram stain"),
                opt("Spectrophotometry of media"),
                opt("Mass on a balance"),
            ),
            "Tetramers bind T cells of a defined specificity, counting them directly.",
        ),
        q(
            "What is the typical workflow of computational epitope-based vaccine design?",
            (
                opt(
                    "Fragment proteome, predict peptide-HLA binding, rank, then model structure and validate",
                    correct=True,
                ),
                opt("Guess randomly then publish"),
                opt("Measure heart rate then design"),
                opt("Only sequence DNA with no prediction"),
            ),
            "Predicted binders are ranked and structurally modeled, then confirmed in the wet lab.",
        ),
        q(
            "Predicted binders from AI tools still require what before clinical use?",
            (
                opt(
                    "Experimental wet-lab validation (e.g. SPR and functional assays)", correct=True
                ),
                opt("Nothing further; predictions are definitive"),
                opt("Only a higher GPU budget"),
                opt("Removal of all controls"),
            ),
            "Computational predictions accelerate but do not replace experimental confirmation.",
        ),
    ),
)
