# Report contract

Read this only after the user has supplied the article's full text. These are report requirements, not a license to infer undisclosed information. Use English except for the Chinese abstract translation. Preserve the paper's names and notation. Quotations, paraphrases, and verbal-definition restatements must be identifiable and source-located.

## 1. Article Information

Record the original title, every author in published order, each author's affiliation(s) as printed, publication journal, publication year, DOI, and analyzed version. Distinguish online-first year from issue year when different. For an unpublished paper, mark the journal/year as not yet published rather than treating an intended outlet as a publication.

Record the handling/responsible editor and the article-specific source. If multiple editorial roles are listed, retain the roles rather than collapsing them into one editor. Use `Not confirmed from article-specific evidence` when unverified. A present-day editorial board is not evidence of who handled an older article.

Include a source inventory with supplied filenames, version labels, PDF page counts when available, and any supplementary files consulted. External metadata citations are explicitly labeled as such.

## 2. Abstract — Original English and Chinese Translation

Use two clearly labeled blocks: `Original English` and `Chinese Translation`. Reproduce the complete English abstract from the supplied version and translate it completely. Preserve qualifications, uncertainty, effect directions, and magnitudes. Do not insert explanation into either block. If the supplied abstract is incomplete or illegible, request the missing source rather than repairing it from another version.

## 3. Research Questions and Hypotheses

State the population, unit of analysis, X, Y, research question, and contribution in the authors' language. Cover every formal hypothesis, including H1a/H1b, nondirectional/null hypotheses, conditions, and competing predictions. Prefer original hypothesis wording with quotation formatting and a locator.

If the article has no formal hypotheses, label its actual questions or predictions; do not invent numbered hypotheses. Distinguish an empirical prediction from a newly formulated hypothesis.

## 4. Theoretical Foundations and Hypothesis Logic

For each hypothesis/prediction, report:

- Original label and statement; source location.
- Basis: explicitly named theory, explicit mechanism without a named theory, intuition/verbal reasoning, prior empirical evidence, or not stated. Allow several bases when the authors combine them.
- Exact English theory name and reference(s) cited in the article; no theory name supplied from general knowledge.
- Each stated premise and mechanism, and why the authors argue it predicts the hypothesized sign or conditional relationship.

Use English arrow diagrams, e.g. `Stated premise → Mechanism → Behavioral response → Predicted Y → H1`. Adapt node counts to the actual argument; do not add missing links just to fill the pattern. Include support and opposition as separate labeled branches when the authors discuss both. Identify any expressly stated assumption or boundary condition. Every causal arrow needs a corresponding passage, not just a plausible intuition.

## 5. Data Sources and Sample Construction

Use a source matrix with variable role, original variable name, database/source, raw inputs or fields if reported, coverage years, estimation years, and unit of observation. Separate X, Y, important controls, alternative measures, mechanisms, and identification variables. Sources may be administrative records, hand collection, surveys, filings, or text corpora rather than databases.

Explain initial population, inclusion/exclusion criteria, linking/merge keys, date alignment, duplicate treatment, and sample losses/counts **as disclosed**. Record periods separately when different variables or tables use different samples. Do not use a database's known historical coverage as the article's coverage.

## 6. Variable Construction — Replication-Level Definitions

Make a separate variable card for each core X and Y, every analyzed alternative measure, important control, mechanism variable, and variable essential to identification (treatment, post, instrument, running variable, event time, etc.). Group only truly identical construction rules and cite their shared scope.

Each card includes:

| Field | Required evidence |
| --- | --- |
| Original name and role | Exact variable label, meaning, unit of observation, and interpretation of larger values |
| Source inputs | Source/database, exact field codes when reported, components, data vintage when stated |
| Original definition/formula | Original equation and number, or quoted verbal definition; every symbol defined |
| Construction sequence | Ordered raw-to-final steps: linkage, filtering, grouping, aggregation, transformations |
| Timing | Measurement date, fiscal/calendar alignment, windows, lags/leads, event-time alignment |
| Scale and units | Numerator/denominator, levels vs ratios vs percentages, scaling factors, currency/base year if reported |
| Transformations | Exact log form, standardization/reference population, demeaning, residualization, industry adjustments |
| Indicators/interactions | Exact cutoffs/inequalities, eligible universe, tie rules, reference category, interacting components |
| Missing/exceptional values | Missing vs zero, undefined denominators, exclusions, winsorization/trimming thresholds and grouping |
| Sample/usage | Applicable sample/subsample, model and table references |
| Replication details not reported | Specific missing choices that would prevent an exact reconstruction |

For a composite index, list components, signs, weights, normalization, and aggregation. For text-based measures, include document selection, dictionary/model/procedure and version if stated, counting/normalization and aggregation. For estimated measures, include the first-stage model, estimation population/window, and how fitted values/residuals become the measure. Apply these only when relevant; do not create new requirements for unrelated variables.

Preserve original formulas, notation, sums, timing, denominators, and definitions. If the article supplies only prose, an ordered recipe is acceptable. Any mathematical reconstruction must be labeled `Restated from the authors' verbal definition` and contain no new assumptions. An ambiguous log definition, unreported database code, unspecified winsorization order, or missing matching key stays a documented gap. Never assert complete replicability solely because a detailed-looking card was produced.

## 7. Institutional Setting

Explain country/region, institutions, policy or historical event, key dates, affected units, eligibility, treatment and comparison groups, and the setting's timing. Distinguish announcement, enactment, implementation, and exposure dates when the article does. Explain why the authors chose the setting and how it makes their mechanism observable or provides identifying variation. No policy shock is required if the paper studies a different kind of setting.

## 8. Empirical Models and Identification Strategy

Display each original main equation and additional equations necessary to understand the reported evidence. Preserve the authors' equation numbering, notation, indices, summation limits, interactions, lag/lead structure, fixed effects, error terms, and functional form. Do not silently substitute a familiar textbook model.

For every model, explain the outcome, regressors, controls, fixed effects, index definitions, key coefficient/contrast and expected direction, estimator, observation unit, estimation sample/period, weights, standard-error method and cluster level(s), and any other disclosed estimation setting. Map it to hypotheses and tables/panels/columns. Distinguish displayed notation from additional implementation details stated in table notes.

Describe the identifying comparison/variation and the authors' claimed identifying assumptions separately from the regression equation. Include the necessary design-specific components: IV first/second stages and stated instrument rationale; DID treatment/timing/comparison; event-study reference period/window/binning; RD running variable/cutoff/bandwidth/specification; matching variables and procedure, when those designs are used and disclosed. Do not infer software, estimator defaults, or undisclosed diagnostics.

If no equation is printed, label the absence. An optional reconstruction must say `Restated from the authors' model description`. Compare each transcription with the source image. Preserve readable LaTeX as a transcription for inspection; do not call it the authors' actual source code. If a symbol cannot be read reliably, show a source crop and flag the uncertainty instead of presenting a guessed exact equation.

For noncausal studies, describe the reported associations and design without inventing a causal identification claim. For theoretical/review papers, preserve applicable sections and explain non-applicability.

## 9. Main Tests and Additional Evidence

First explain the main test(s), estimates, uncertainty as reported, and the authors' interpretation. Then map additional evidence using:

`Authors' stated concern / alternative explanation → Test or design feature → Finding → Authors' interpretation`

Use a matrix with purpose, hypothesis/model, table/panel/column, relevant result, and source location. Distinguish main tests, mechanisms, heterogeneity, robustness, placebo/falsification, selection tests, and alternative-measure analyses by their actual role. If the authors do not explicitly tie a test to a specific concern, say so rather than inventing one. Note acknowledged limitations in the authors' terms, not as an independent audit.

## 10. Table-by-Table Walkthrough

Inventory every **main-text** table before rendering, including descriptive statistics and correlation tables, in the paper's original order. Do not select only significant or identification-related tables. Appendices may inform the report but their tables are not included in this walkthrough unless the user changes scope.

For each table:

- Include original table number/title and every panel, page continuation, and note. Preserve units, column headings, stars, standard-error conventions, and sample sizes. Use separate readable images for fragments rather than shrinking a long table into one illegible image.
- Place original PDF captures on the left and English commentary on the right on wide screens; stack on narrow screens. Clicking a capture opens a zoomable full-resolution view.
- Explain the authors' stated purpose, linked question/hypothesis/model, row/column/panel organization, focal estimates and units, reported uncertainty, and authors' conclusion. For descriptive tables, explain the actual descriptive role without forcing a causal interpretation.
- State whether the authors use it as main evidence, a mechanism test, additional evidence, or to address a named concern, with the passage giving that rationale. If unstated, label that fact and describe only observable table content.
- Distinguish raw coefficients from economic magnitudes interpreted by the authors. Do not invent a marginal effect, economic translation, significance level, or hypothesis verdict.

Keep the manuscript's own labels even if numbering is irregular. Do not reorder by guessed numbers, combine separate tables, or count a continued table as a new table. Notes located separately may be captured as additional fragments with their own page locator.
