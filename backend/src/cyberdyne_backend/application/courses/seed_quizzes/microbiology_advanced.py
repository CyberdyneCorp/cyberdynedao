"""Quiz questions for the Microbiology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Molecular pathogenesis and virulence": (
            q(
                "An AB exotoxin is organized so that:",
                (
                    opt(
                        "the B subunit binds the host receptor and the A subunit is the active enzyme",
                        correct=True,
                    ),
                    opt("both subunits are inert"),
                    opt("the A subunit binds and the B subunit is the toxin"),
                    opt("it is a lipopolysaccharide"),
                ),
                "B = binding, A = active (enzymatic) component, as in cholera and diphtheria toxins.",
            ),
            q(
                "Endotoxin (LPS) of Gram-negative bacteria primarily causes:",
                (
                    opt("inflammation and septic shock when released", correct=True),
                    opt("targeted enzymatic cleavage of host DNA"),
                    opt("immediate cell-wall synthesis"),
                    opt("antibiotic resistance"),
                ),
                "Lipid A of LPS triggers strong innate-immune inflammation.",
            ),
            q(
                "A lower ID50 or LD50 for a pathogen indicates:",
                (
                    opt("greater virulence (fewer organisms cause disease)", correct=True),
                    opt("lower virulence"),
                    opt("no relationship to virulence"),
                    opt("resistance to antibiotics"),
                ),
                "The smaller the dose needed to infect/kill half the hosts, the more virulent.",
            ),
        ),
        "Antimicrobial action and pharmacodynamics": (
            q(
                "Beta-lactam antibiotics are selectively toxic because they target:",
                (
                    opt("bacterial cell-wall synthesis, which human cells lack", correct=True),
                    opt("the human ribosome"),
                    opt("mitochondrial DNA"),
                    opt("host plasma membranes"),
                ),
                "Selective toxicity exploits targets absent in the host, such as peptidoglycan synthesis.",
            ),
            q(
                "The minimum inhibitory concentration (MIC) is:",
                (
                    opt("the lowest drug concentration that prevents visible growth", correct=True),
                    opt("the dose lethal to the patient"),
                    opt("the highest tolerated concentration"),
                    opt("the concentration that kills 50% of hosts"),
                ),
                "MIC quantifies in-vitro potency against a given isolate.",
            ),
            q(
                "Aminoglycosides are described as concentration-dependent killers, meaning:",
                (
                    opt("higher peak concentrations kill faster", correct=True),
                    opt("killing depends only on time above MIC"),
                    opt("they never kill bacteria"),
                    opt("low constant levels are most effective"),
                ),
                "Concentration-dependent agents are dosed for high peaks; time-dependent ones (beta-lactams) for time above MIC.",
            ),
        ),
        "Antibiotic resistance: mechanisms and evolution": (
            q(
                "Beta-lactamases confer resistance by:",
                (
                    opt("enzymatically destroying the antibiotic", correct=True),
                    opt("pumping the drug out via efflux"),
                    opt("altering the ribosome"),
                    opt("thickening the capsule"),
                ),
                "Beta-lactamases hydrolyze the beta-lactam ring before it can act.",
            ),
            q(
                "MRSA resists beta-lactams chiefly through:",
                (
                    opt(
                        "an altered penicillin-binding protein (PBP2a) with low drug affinity",
                        correct=True,
                    ),
                    opt("loss of all peptidoglycan"),
                    opt("producing more LPS"),
                    opt("becoming Gram-positive"),
                ),
                "PBP2a still cross-links the wall but binds beta-lactams poorly.",
            ),
            q(
                "A fitness cost of resistance means that, without the drug, resistant mutants:",
                (
                    opt("may grow more slowly than susceptible cells", correct=True),
                    opt("always outcompete susceptible cells"),
                    opt("immediately die"),
                    opt("cannot transfer the resistance gene"),
                ),
                "Costly mutations can be lost without selection, though compensatory mutations may erase the cost.",
            ),
        ),
        "The human microbiome and metagenomics": (
            q(
                "16S rRNA amplicon sequencing mainly answers which question?",
                (
                    opt("Which taxa are present (who is there)", correct=True),
                    opt("The complete functional gene repertoire"),
                    opt("The host's genome sequence"),
                    opt("Protein 3D structures"),
                ),
                "16S profiling gives taxonomy; shotgun metagenomics adds functional potential.",
            ),
            q(
                "Colonization resistance refers to the microbiome's ability to:",
                (
                    opt("exclude invading pathogens", correct=True),
                    opt("digest all antibiotics"),
                    opt("replace the host immune system"),
                    opt("eliminate all commensals"),
                ),
                "A healthy community competitively excludes pathogens.",
            ),
            q(
                "A rarefaction curve that plateaus indicates that:",
                (
                    opt(
                        "the sample was sequenced deeply enough to capture most species",
                        correct=True,
                    ),
                    opt("the sample has infinite diversity"),
                    opt("sequencing failed"),
                    opt("no species are present"),
                ),
                "When added reads stop revealing new taxa, sampling depth is sufficient.",
            ),
        ),
        "Biofilms, persistence and tolerance": (
            q(
                "Biofilm cells are encased in:",
                (
                    opt(
                        "a self-produced extracellular polymeric substance (EPS) matrix",
                        correct=True,
                    ),
                    opt("host collagen only"),
                    opt("a crystalline salt shell"),
                    opt("pure water"),
                ),
                "EPS of polysaccharide, protein and eDNA holds the community together.",
            ),
            q(
                "Persister cells survive lethal antibiotic doses because they are:",
                (
                    opt("dormant/slow-growing, not because of a resistance mutation", correct=True),
                    opt("genetically resistant via a plasmid"),
                    opt("faster-growing than other cells"),
                    opt("dead before treatment"),
                ),
                "Persistence is phenotypic tolerance from dormancy, distinct from genetic resistance.",
            ),
            q(
                "The biphasic kill curve of a biofilm shows:",
                (
                    opt("rapid initial killing then a tolerant surviving plateau", correct=True),
                    opt("instant complete eradication"),
                    opt("steady exponential decline to zero"),
                    opt("net growth during treatment"),
                ),
                "Bulk cells die fast; persisters survive and regrow after treatment.",
            ),
        ),
        "AI and computational genomics for pathogens": (
            q(
                "Whole-genome sequencing of a clinical isolate can be used to:",
                (
                    opt("identify species, predict resistance and trace outbreaks", correct=True),
                    opt("only measure colony size"),
                    opt("replace the Gram stain's color"),
                    opt("grow the organism faster"),
                ),
                "WGS supports identification, resistance prediction and genomic epidemiology.",
            ),
            q(
                "A key confounder for genotype-to-phenotype resistance models is:",
                (
                    opt("population structure (lineage acts as a hidden variable)", correct=True),
                    opt("the use of agar plates"),
                    opt("the Gram stain"),
                    opt("colony color"),
                ),
                "Clonal lineage correlates with both genotype and phenotype, inflating apparent accuracy.",
            ),
            q(
                "Proper validation of a resistance-prediction model requires holding out:",
                (
                    opt("entire lineages, not just individual isolates", correct=True),
                    opt("nothing; train on all data"),
                    opt("only the labels"),
                    opt("the reference genome"),
                ),
                "Holding out lineages tests generalization beyond memorized population structure.",
            ),
        ),
    },
    final=(
        q(
            "Pathogenicity islands are notable because they are often:",
            (
                opt(
                    "acquired by horizontal gene transfer and encode virulence factors",
                    correct=True,
                ),
                opt("essential housekeeping genes"),
                opt("ribosomal RNA operons"),
                opt("plasmid origins of replication only"),
            ),
            "Clustered virulence genes spread between strains via HGT.",
        ),
        q(
            "Selective toxicity of antibiotics depends on:",
            (
                opt("targeting features unique to (or different in) microbes", correct=True),
                opt("being toxic to all cells equally"),
                opt("high host toxicity"),
                opt("random binding"),
            ),
            "Good antibiotics hit microbial-specific targets like the wall or 70S ribosome.",
        ),
        q(
            "Which is NOT a major mechanism of antibiotic resistance?",
            (
                opt("Increasing the host's body temperature", correct=True),
                opt("Enzymatic drug destruction"),
                opt("Efflux pumps"),
                opt("Target modification"),
            ),
            "Resistance acts at the bacterial level: enzymes, efflux, target change, reduced uptake.",
        ),
        q(
            "Shotgun metagenomics differs from 16S profiling by revealing:",
            (
                opt(
                    "functional gene content and assembled genomes (what they can do)", correct=True
                ),
                opt("only taxonomy"),
                opt("the host genome only"),
                opt("nothing additional"),
            ),
            "Shotgun sequences all DNA, enabling functional and genome-resolved analysis.",
        ),
        q(
            "Antibiotic tolerance and persistence differ from resistance in that they:",
            (
                opt("let cells survive without a change in MIC", correct=True),
                opt("always raise the MIC"),
                opt("are encoded on plasmids only"),
                opt("kill the host immediately"),
            ),
            "Tolerance/persistence are phenotypic survival, not a heritable MIC increase.",
        ),
        q(
            "Machine-learning prediction of resistance from genomes improves with:",
            (
                opt("more labeled genomes, with diminishing returns", correct=True),
                opt("fewer training examples"),
                opt("ignoring population structure"),
                opt("removing all validation"),
            ),
            "Accuracy follows a saturating learning curve; lineage-aware validation is essential.",
        ),
    ),
)
