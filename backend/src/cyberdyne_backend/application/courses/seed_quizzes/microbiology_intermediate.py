"""Quiz questions for the Microbiology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Growth kinetics: Monod and the chemostat": (
            q(
                "At steady state in a chemostat, the specific growth rate equals:",
                (
                    opt("the dilution rate D", correct=True),
                    opt("zero"),
                    opt("the substrate concentration"),
                    opt("the yield coefficient"),
                ),
                "Steady state requires mu = D so biomass neither accumulates nor washes out.",
            ),
            q(
                "The Monod equation describes growth rate as a function of:",
                (
                    opt(
                        "limiting-substrate concentration, saturating hyperbolically", correct=True
                    ),
                    opt("temperature only"),
                    opt("a linear function of substrate"),
                    opt("oxygen exclusively"),
                ),
                "mu = mu_max S/(Ks+S) is the microbial analogue of Michaelis-Menten.",
            ),
            q(
                "Raising the dilution rate above mu_max causes:",
                (
                    opt("washout of the culture", correct=True),
                    opt("faster steady-state growth"),
                    opt("higher biomass yield"),
                    opt("spore formation"),
                ),
                "Cells leave faster than they divide, so the population is washed out.",
            ),
        ),
        "Microbial metabolism and respiration": (
            q(
                "Fermentation differs from respiration in that fermentation:",
                (
                    opt(
                        "uses an organic molecule, not an electron-transport chain, to regenerate NAD+",
                        correct=True,
                    ),
                    opt("requires oxygen as the terminal acceptor"),
                    opt("yields more ATP than aerobic respiration"),
                    opt("uses nitrate as the acceptor"),
                ),
                "Fermentation regenerates NAD+ by reducing an organic intermediate; yield is low.",
            ),
            q(
                "A chemolithoautotroph obtains energy, electrons and carbon from:",
                (
                    opt("inorganic chemicals (energy/electrons) and CO2 (carbon)", correct=True),
                    opt("light, organics and CO2"),
                    opt("organic compounds for all three"),
                    opt("only sunlight"),
                ),
                "Chemo = chemical energy, litho = inorganic electron donor, auto = CO2 carbon.",
            ),
            q(
                "In anaerobic respiration the terminal electron acceptor is:",
                (
                    opt(
                        "an inorganic molecule other than O2 (e.g. nitrate, sulfate)", correct=True
                    ),
                    opt("always molecular oxygen"),
                    opt("an organic fermentation product"),
                    opt("never present"),
                ),
                "Acceptors such as nitrate, sulfate or Fe(III) replace O2, giving lower yields.",
            ),
        ),
        "Regulation of gene expression": (
            q(
                "In the lac operon, the LacI repressor is released from the operator by:",
                (
                    opt("allolactose, the inducer", correct=True),
                    opt("glucose"),
                    opt("cAMP"),
                    opt("oxygen"),
                ),
                "Allolactose binds LacI, lifting repression so the operon can be transcribed.",
            ),
            q(
                "Catabolite repression ensures that bacteria preferentially use:",
                (
                    opt("glucose before alternative sugars like lactose", correct=True),
                    opt("lactose before glucose"),
                    opt("all sugars simultaneously"),
                    opt("no sugars at all"),
                ),
                "Low glucose raises cAMP, activating CAP; high glucose suppresses alternative-sugar operons.",
            ),
            q(
                "A two-component regulatory system consists of:",
                (
                    opt("a sensor kinase and a response regulator", correct=True),
                    opt("two identical repressors"),
                    opt("two ribosomes"),
                    opt("a promoter and a terminator only"),
                ),
                "The sensor kinase autophosphorylates and transfers phosphate to the response regulator.",
            ),
        ),
        "Mutation and horizontal gene transfer": (
            q(
                "Transfer of DNA from a donor to a recipient through a pilus-mediated bridge is:",
                (
                    opt("conjugation", correct=True),
                    opt("transformation"),
                    opt("transduction"),
                    opt("transcription"),
                ),
                "Conjugation moves plasmids (e.g. the F plasmid) cell-to-cell via a mating bridge.",
            ),
            q(
                "Bacteriophage-mediated transfer of host DNA is called:",
                (
                    opt("transduction", correct=True),
                    opt("transformation"),
                    opt("conjugation"),
                    opt("translation"),
                ),
                "A phage accidentally packages host DNA and delivers it to a new cell.",
            ),
            q(
                "The Luria-Delbruck fluctuation test demonstrated that resistance mutations:",
                (
                    opt(
                        "arise spontaneously before selection, not in response to it", correct=True
                    ),
                    opt("are induced only by the antibiotic"),
                    opt("never occur in bacteria"),
                    opt("always revert immediately"),
                ),
                "Fluctuation in mutant numbers showed pre-existing, random mutation (Darwinian).",
            ),
        ),
        "Sterilisation and disinfection kinetics": (
            q(
                "Microbial killing by heat or chemicals typically follows:",
                (
                    opt("first-order (exponential) kinetics", correct=True),
                    opt("zero-order kinetics with constant numbers killed"),
                    opt("instantaneous total kill"),
                    opt("no predictable pattern"),
                ),
                "A constant fraction of survivors dies per unit time: N = N0 e^(-kt).",
            ),
            q(
                "The decimal reduction time D is the time required to:",
                (
                    opt("kill 90% (one log) of the population", correct=True),
                    opt("kill 50% of the population"),
                    opt("kill 100% instantly"),
                    opt("double the population"),
                ),
                "D is the one-log (90%) reduction time at a given temperature.",
            ),
            q(
                "Standard autoclave sterilization conditions are:",
                (
                    opt("saturated steam at 121 C, ~15 psi, ~15 min", correct=True),
                    opt("dry air at 37 C for 24 h"),
                    opt("freezing at -20 C"),
                    opt("UV light alone for 1 min"),
                ),
                "Moist heat at 121 C reliably kills vegetative cells and spores.",
            ),
        ),
    },
    final=(
        q(
            "A chemostat is most useful because it:",
            (
                opt("holds cells in a defined, steady physiological state", correct=True),
                opt("kills all microbes"),
                opt("prevents any growth"),
                opt("requires no nutrients"),
            ),
            "Continuous culture fixes mu = D, ideal for studying physiology and evolution.",
        ),
        q(
            "Which process yields the most ATP per glucose?",
            (
                opt("Aerobic respiration", correct=True),
                opt("Lactic acid fermentation"),
                opt("Ethanol fermentation"),
                opt("Substrate-level phosphorylation alone"),
            ),
            "A full electron-transport chain to O2 generates the largest proton-motive force.",
        ),
        q(
            "The lac operon combines which two control logics?",
            (
                opt("negative control by LacI and positive control by CAP", correct=True),
                opt("two repressors and no activator"),
                opt("only positive control"),
                opt("post-translational control only"),
            ),
            "LacI represses; CAP-cAMP activates under low glucose.",
        ),
        q(
            "Antibiotic-resistance genes spread rapidly among bacteria mainly via:",
            (
                opt("horizontal gene transfer on plasmids and transposons", correct=True),
                opt("vertical inheritance only"),
                opt("spontaneous generation"),
                opt("ribosome duplication"),
            ),
            "Mobile elements carry resistance genes across cells and species.",
        ),
        q(
            "Filtration (0.22 um membranes) is used to sterilize:",
            (
                opt("heat-sensitive liquids without killing", correct=True),
                opt("solid surgical instruments"),
                opt("bacterial spores by heat"),
                opt("air by chemical fumigation"),
            ),
            "Filtration physically removes microbes from fluids that heat would damage.",
        ),
        q(
            "Quorum sensing lets bacteria:",
            (
                opt("coordinate gene expression based on population density", correct=True),
                opt("kill all neighboring cells"),
                opt("replicate their chromosome faster"),
                opt("become eukaryotic"),
            ),
            "Accumulating autoinducers signal density and trigger collective behaviors.",
        ),
    ),
)
