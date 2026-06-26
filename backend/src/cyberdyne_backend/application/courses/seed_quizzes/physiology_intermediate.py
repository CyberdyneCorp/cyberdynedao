"""Quiz questions for the Human Physiology - Intermediate course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The action potential and Hodgkin–Huxley": (
            q(
                "What drives the rapid upstroke of the action potential?",
                (
                    opt("Influx of Na+ through voltage-gated Na+ channels", correct=True),
                    opt("Efflux of K+ through leak channels"),
                    opt("Active pumping by the Na+/K+-ATPase"),
                    opt("Cl- entry through aquaporins"),
                ),
                "Voltage-gated Na+ channels open at threshold, driving a regenerative depolarisation.",
            ),
            q(
                "What ends the upstroke and begins repolarisation?",
                (
                    opt("Na+ channel inactivation plus delayed K+ channel opening", correct=True),
                    opt("Closure of all K+ channels"),
                    opt("A sudden rise in extracellular Ca2+"),
                    opt("Loss of the resting potential"),
                ),
                "Na+ channels inactivate while slower K+ channels open to repolarise the cell.",
            ),
            q(
                "In the Hodgkin-Huxley model, what are m, h and n?",
                (
                    opt("Voltage- and time-dependent gating variables", correct=True),
                    opt("Fixed membrane capacitances"),
                    opt("Constant ion concentrations"),
                    opt("Names of three neurotransmitters"),
                ),
                "m, h and n are gating variables with first-order kinetics governing conductances.",
            ),
        ),
        "Synaptic transmission and muscle": (
            q(
                "What triggers neurotransmitter vesicle fusion at the presynaptic terminal?",
                (
                    opt("Ca2+ entry through voltage-gated Ca2+ channels", correct=True),
                    opt("K+ leaving the terminal"),
                    opt("ATP binding to actin"),
                    opt("Cooling of the membrane"),
                ),
                "The AP opens Ca2+ channels; Ca2+ triggers SNARE-mediated vesicle fusion.",
            ),
            q(
                "Which protein does Ca2+ bind to initiate skeletal-muscle contraction?",
                (
                    opt("Troponin C", correct=True),
                    opt("Myosin heavy chain"),
                    opt("Acetylcholinesterase"),
                    opt("Aquaporin-2"),
                ),
                "Ca2+ binds troponin C, shifting tropomyosin to expose actin-binding sites.",
            ),
            q(
                "Why does muscle force depend on sarcomere length?",
                (
                    opt("Length sets the degree of actin-myosin filament overlap", correct=True),
                    opt("Length changes the resting membrane potential"),
                    opt("Length alters the speed of acetylcholinesterase"),
                    opt("Length determines blood pressure"),
                ),
                "The length-tension curve peaks at optimal overlap of thick and thin filaments.",
            ),
        ),
        "Cardiac output and the pressure–volume loop": (
            q(
                "How is cardiac output calculated?",
                (
                    opt("Heart rate multiplied by stroke volume", correct=True),
                    opt("Heart rate divided by stroke volume"),
                    opt("Stroke volume minus heart rate"),
                    opt("Mean pressure times resistance"),
                ),
                "CO = HR x SV.",
            ),
            q(
                "The Frank-Starling mechanism states that increased preload does what?",
                (
                    opt("Increases stroke volume through greater stretch and force", correct=True),
                    opt("Decreases stroke volume"),
                    opt("Has no effect on the ventricle"),
                    opt("Stops the heart from filling"),
                ),
                "Greater end-diastolic stretch yields greater contractile force and stroke volume.",
            ),
            q(
                "Which factor is NOT a primary determinant of stroke volume?",
                (
                    opt("Plasma sodium concentration", correct=True),
                    opt("Preload"),
                    opt("Afterload"),
                    opt("Contractility"),
                ),
                "Stroke volume is set by preload, afterload and contractility.",
            ),
        ),
        "Vascular haemodynamics and blood pressure": (
            q(
                "Mean arterial pressure is approximately the product of which two quantities?",
                (
                    opt("Cardiac output and total peripheral resistance", correct=True),
                    opt("Heart rate and respiratory rate"),
                    opt("Stroke volume and plasma pH"),
                    opt("Preload and afterload"),
                ),
                "MAP is approximately CO x TPR.",
            ),
            q(
                "By Poiseuille's law, resistance depends most strongly on what?",
                (
                    opt("Vessel radius, as 1/r^4", correct=True),
                    opt("Vessel length, as length squared"),
                    opt("Blood pH"),
                    opt("Heart rate"),
                ),
                "Resistance scales with 1/r^4, so arterioles dominate as resistance vessels.",
            ),
            q(
                "Which reflex provides fast, beat-to-beat blood-pressure control?",
                (
                    opt("The baroreceptor reflex", correct=True),
                    opt("The renin-angiotensin system alone"),
                    opt("The length-tension reflex"),
                    opt("The myotatic reflex"),
                ),
                "Baroreceptors signal the medulla, which adjusts autonomic outflow within seconds.",
            ),
        ),
        "Renal filtration and clearance": (
            q(
                "What is a normal glomerular filtration rate in a healthy adult?",
                (
                    opt("About 125 mL/min", correct=True),
                    opt("About 5 mL/min"),
                    opt("About 1000 mL/min"),
                    opt("About 12 L/min"),
                ),
                "GFR is normally around 125 mL/min and is tightly autoregulated.",
            ),
            q(
                "Which substance's clearance best estimates GFR because it is filtered but not reabsorbed or secreted?",
                (
                    opt("Inulin (or clinically, creatinine)", correct=True),
                    opt("Glucose"),
                    opt("Albumin"),
                    opt("Para-aminohippurate at low load"),
                ),
                "Inulin clearance equals GFR; creatinine is the clinical surrogate.",
            ),
            q(
                "If a solute's clearance exceeds GFR, what must be occurring?",
                (
                    opt("Net tubular secretion", correct=True),
                    opt("Net tubular reabsorption"),
                    opt("No handling beyond filtration"),
                    opt("Complete blockade of filtration"),
                ),
                "Clearance above GFR means the tubule adds the solute by secretion.",
            ),
        ),
    },
    final=(
        q(
            "The all-or-none action-potential upstroke is an example of what control?",
            (
                opt("Positive feedback via voltage-gated Na+ channels", correct=True),
                opt("Negative feedback via K+ leak"),
                opt("Feedforward inhibition only"),
                opt("Passive diffusion of glucose"),
            ),
            "Na+ entry depolarises further, opening more Na+ channels - positive feedback.",
        ),
        q(
            "Excitation-contraction coupling links the T-tubule signal to Ca2+ release from where?",
            (
                opt("The sarcoplasmic reticulum", correct=True),
                opt("The mitochondrial matrix"),
                opt("The nucleus"),
                opt("The extracellular fluid only"),
            ),
            "The DHP receptor couples to the ryanodine receptor, releasing SR Ca2+.",
        ),
        q(
            "Stroke volume rises with increased preload because of which mechanism?",
            (
                opt("Frank-Starling", correct=True),
                opt("Poiseuille's law"),
                opt("The Nernst relation"),
                opt("First-order elimination"),
            ),
            "Frank-Starling: greater filling stretches fibres and increases contractile force.",
        ),
        q(
            "Arterioles are the chief resistance vessels mainly because resistance scales as what?",
            (
                opt("1/r^4 (strong dependence on radius)", correct=True),
                opt("r^4 (rising with radius)"),
                opt("Linear in vessel length only"),
                opt("Independent of radius"),
            ),
            "Poiseuille's 1/r^4 means small radius changes greatly change resistance.",
        ),
        q(
            "Renal clearance C_x is defined by which expression?",
            (
                opt("(urine concentration x urine flow) / plasma concentration", correct=True),
                opt("plasma concentration / urine flow"),
                opt("GFR times plasma volume squared"),
                opt("heart rate times stroke volume"),
            ),
            "C_x = (U_x x V) / P_x, the plasma volume cleared per unit time.",
        ),
        q(
            "Which hormone, via aquaporin-2, lets the collecting duct fine-tune water reabsorption?",
            (
                opt("Antidiuretic hormone (ADH/vasopressin)", correct=True),
                opt("Insulin"),
                opt("Acetylcholine"),
                opt("Troponin"),
            ),
            "ADH inserts aquaporin-2 channels, increasing water reabsorption in the collecting duct.",
        ),
    ),
)
