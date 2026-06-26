"""Quiz questions for the Statistics & Biostatistics - Advanced course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Experimental design & power analysis": (
            q(
                "Randomisation in an experiment primarily serves to:",
                (
                    opt("Break confounding by balancing groups on average", correct=True),
                    opt("Increase the effect size"),
                    opt("Reduce measurement units"),
                    opt("Eliminate the need for replication"),
                ),
                "Random assignment balances measured and unmeasured factors across arms.",
            ),
            q(
                "Holding other factors fixed, detecting a smaller effect size requires:",
                (
                    opt("A larger sample size", correct=True),
                    opt("A smaller sample size"),
                    opt("A larger alpha"),
                    opt("No change in n"),
                ),
                "Required n grows roughly as 1/delta^2, so tiny effects need large studies.",
            ),
            q(
                "An underpowered study tends to produce:",
                (
                    opt("Noisy, hard-to-reproduce results", correct=True),
                    opt("Guaranteed false positives only"),
                    opt("Perfectly precise estimates"),
                    opt("Zero Type I error"),
                ),
                "Low power means real effects are often missed and significant findings are unreliable.",
            ),
        ),
        "Survival analysis: Kaplan–Meier & Cox": (
            q(
                "A subject who is followed but has not had the event by study end is:",
                (
                    opt("Censored", correct=True),
                    opt("An outlier"),
                    opt("A false positive"),
                    opt("Excluded from all analysis"),
                ),
                "Right-censoring means the event time is only known to exceed the follow-up.",
            ),
            q(
                "The Kaplan–Meier estimator produces:",
                (
                    opt("A non-parametric step estimate of the survival function", correct=True),
                    opt("A linear regression line"),
                    opt("A hazard ratio"),
                    opt("A p-value only"),
                ),
                "KM is a non-parametric step curve for S(t) that drops at each event time.",
            ),
            q(
                "In a Cox proportional-hazards model, exp(beta_j) is interpreted as a:",
                (
                    opt("Hazard ratio", correct=True),
                    opt("Odds ratio"),
                    opt("Relative risk over the whole study"),
                    opt("Survival probability"),
                ),
                "Cox coefficients exponentiate to hazard ratios; the baseline hazard is unspecified.",
            ),
        ),
        "Multiple testing & FDR in genomics": (
            q(
                "Testing 20,000 genes at alpha = 0.05 with no true effects yields about:",
                (
                    opt("1,000 false positives by chance", correct=True),
                    opt("Zero false positives"),
                    opt("20,000 false positives"),
                    opt("Exactly 50 false positives"),
                ),
                "0.05 x 20,000 = 1,000 expected false positives under the null.",
            ),
            q(
                "The Benjamini–Hochberg procedure controls the:",
                (
                    opt("False discovery rate", correct=True),
                    opt("Family-wise error rate"),
                    opt("Type II error rate"),
                    opt("Sample size"),
                ),
                "BH controls the expected proportion of false positives among rejections (the FDR).",
            ),
            q(
                "Compared with Bonferroni, FDR control in discovery genomics typically:",
                (
                    opt(
                        "Recovers more true signals at the cost of a small known false fraction",
                        correct=True,
                    ),
                    opt("Is always more conservative"),
                    opt("Guarantees zero false positives"),
                    opt("Ignores the number of tests"),
                ),
                "FDR is less strict than FWER, trading a controlled false fraction for far more power.",
            ),
        ),
        "Mixed models & generalised linear models": (
            q(
                "Random effects in a mixed model are added to:",
                (
                    opt(
                        "Account for correlation among observations within a cluster", correct=True
                    ),
                    opt("Increase the effect size"),
                    opt("Replace the fixed effects entirely"),
                    opt("Remove the need for a link function"),
                ),
                "Random effects model grouping (repeated measures, nesting) for honest standard errors.",
            ),
            q(
                "Which GLM is the default for overdispersed RNA-seq counts (DESeq2, edgeR)?",
                (
                    opt("Negative binomial", correct=True),
                    opt("Ordinary least squares"),
                    opt("Logistic regression"),
                    opt("Standard Poisson"),
                ),
                "RNA-seq counts are overdispersed, so the negative binomial replaces the Poisson.",
            ),
            q(
                "Under a log link, the effect of a predictor on the expected count is:",
                (
                    opt("Multiplicative", correct=True),
                    opt("Additive on the count scale"),
                    opt("Always zero"),
                    opt("Defined only for binary outcomes"),
                ),
                "A log link makes E[y] = exp(linear predictor), so effects multiply the mean.",
            ),
        ),
        "Bayesian & machine-learning methods": (
            q(
                "Bayesian inference produces a posterior by combining the likelihood with:",
                (
                    opt("A prior distribution", correct=True),
                    opt("A p-value"),
                    opt("A hazard ratio"),
                    opt("A contingency table"),
                ),
                "Posterior is proportional to likelihood times prior.",
            ),
            q(
                "LASSO regression is especially useful in p >> n problems because it:",
                (
                    opt(
                        "Drives many coefficients to exactly zero, selecting features", correct=True
                    ),
                    opt("Always keeps every predictor"),
                    opt("Requires no tuning"),
                    opt("Only works for survival data"),
                ),
                "The L1 penalty performs variable selection, ideal for high-dimensional biomarker discovery.",
            ),
            q(
                "Cross-validation is used primarily to:",
                (
                    opt("Estimate out-of-sample error and guard against overfitting", correct=True),
                    opt("Increase the training error"),
                    opt("Compute the prior"),
                    opt("Replace randomisation"),
                ),
                "CV estimates generalisation performance on held-out folds.",
            ),
        ),
    },
    final=(
        q(
            "Fisher's core principles of experimental design include:",
            (
                opt("Randomisation, replication and blocking", correct=True),
                opt("Censoring, shrinkage and boosting"),
                opt("Bonferroni, BH and q-values"),
                opt("Priors, likelihoods and posteriors"),
            ),
            "Randomisation, replication, blocking (and blinding) are the classic design principles.",
        ),
        q(
            "The log-rank test is used to:",
            (
                opt("Compare survival curves between groups", correct=True),
                opt("Compare two means"),
                opt("Control the false discovery rate"),
                opt("Fit a logistic model"),
            ),
            "The log-rank test compares Kaplan–Meier survival between groups.",
        ),
        q(
            "A q-value reported for a gene represents:",
            (
                opt("The minimum FDR at which that gene is called significant", correct=True),
                opt("The raw p-value"),
                opt("The hazard ratio"),
                opt("The prior probability"),
            ),
            "q-values express significance on the FDR scale.",
        ),
        q(
            "The key assumption to check in a Cox model is:",
            (
                opt("Proportional hazards over time", correct=True),
                opt("Equal group variances"),
                opt("Normality of the raw counts"),
                opt("Independence of all genes"),
            ),
            "Cox assumes hazard ratios are constant over time (proportional hazards).",
        ),
        q(
            "A generalised linear mixed model (GLMM) is appropriate for data that are:",
            (
                opt("Non-Normal and clustered", correct=True),
                opt("Always perfectly Normal and independent"),
                opt("Only categorical with two levels"),
                opt("Free of any correlation"),
            ),
            "GLMMs combine a GLM (non-Normal outcome) with random effects (clustering).",
        ),
        q(
            "Before claiming a biomarker from high-dimensional omics data, you should:",
            (
                opt("Validate it on an independent cohort", correct=True),
                opt("Report only the training accuracy"),
                opt("Skip regularisation"),
                opt("Use a single uncorrected p-value"),
            ),
            "Independent validation is essential to avoid overfitting and false discoveries.",
        ),
    ),
)
