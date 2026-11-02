# Report contract

Read this only after the user has supplied the article's full text. These are report requirements, not a license to infer undisclosed information. Use English except for the Chinese abstract translation. Preserve the paper's names and notation. Distinguish and source-locate original evidence and authored explanation. X/Y definitions, proxies, and construction descriptions must be screenshots or verbatim extracts, never paraphrases or verbal-definition restatements.

Throughout authored analysis, apply the `SKILL.md` rule **full English name (abbreviation) at every occurrence** for article-specific X/Y, proxy, and setting abbreviations. This includes headings, diagram nodes, captions and authored table cells. Keep original quotations, screenshots, titles/labels used as evidence, and equation notation intact; put the expanded name in an adjacent authored label or legend. Do not invent missing full names.

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

Use a source matrix with variable role, original variable name, database/source, raw inputs or fields if reported, coverage years, estimation years, and unit of observation. Separate X, Y, important controls, alternative measures, mechanisms, and identification variables. Sources may be administrative records, hand collection, surveys, filings, or text corpora rather than databases. For X/Y-related entries, use the exact source wording or link to an evidence block within this section; an authored source matrix is an index, not a substitute for the original passages.

For every passage in the article's data/sample discussion that contributes to constructing X or Y or their proxies, reproduce the full relevant sentences and formulas as original screenshots or verified verbatim extracts **in this data section**. Include data sources and fields, population and filters, merges, date alignment, duplicate handling, sample losses, aggregation, measurement windows, transformations, scaling, and missing/extreme-value treatment wherever those are described. Do not replace them with a summary or reorganized recipe. Shared evidence may be linked from multiple variables, but must remain visibly available in this section.

Other sample context may be explained **as disclosed**, separately from the protected construction evidence. Record periods separately when different variables or tables use different samples. Do not use a database's known historical coverage as the article's coverage.

## 6. Variable Construction — Replication-Level Definitions

Make a separate variable card for each core X and Y, every analyzed alternative measure, important control, mechanism variable, and variable essential to identification (treatment, post, instrument, running variable, event time, etc.). Group only truly identical construction rules and cite their shared scope.

### Original evidence for X and Y

For each X and Y, cover both the underlying construct and every primary or alternative proxy, including any component or estimated input needed to build it. Search the full supplied article, not just the variable-definition subsection: data/sample sections, measurement discussions, equations, footnotes, table notes, variable appendices, and supplied supplementary material can each contain required evidence.

- Make a coverage inventory linking each variable/proxy, each defining or construction passage, and its source location to the report evidence block. Include every concrete definition and construction description in the supplied material. Distinct or conflicting versions must appear separately; identical repeated passages may share an evidence block only if all their locations are recorded.
- Put an **Original evidence — verbatim** block at the start of each X/Y card. Use original PDF crops or exact source-text extracts for all relevant sentences; include complete definitional sentences, necessary antecedent sentences, qualifications, formula numbering, symbol definitions, footnotes and continued portions. Use as many separately located blocks as needed.
- Use original PDF captures for every X/Y definition/construction formula when a PDF is supplied. Verified MathML/LaTeX transcriptions may accompany, never replace, those captures. If the supplied full text has no PDF, preserve the exact supplied formula text and label the absence of a screenshot; do not invent one.
- Verbatim means no paraphrase, summary, translation, shortening with ellipses, bracketed insertions, silent typo correction, abbreviation expansion, normalized numbers/symbols, or conversion of prose into a new equation or ordered recipe. Preserve the source's wording and within-passage order. Keep different source passages separate. If extraction or optical character recognition cannot preserve the printed text faithfully, use the screenshot rather than repair a quotation by guessing.
- Add the full English name and parenthesized abbreviation outside the evidence, not inside it. Put locators outside the quoted text: printed/PDF pages, section, equation, table/panel/note or appendix.
- Any separate explanation may discuss the variable's role in the argument or test, but must not rewrite or summarize its definition, proxy or construction. Missing choices and source inconsistencies belong in a separate gap note. Do not reconcile conflicting definitions on the authors' behalf.

Each card includes the following fields. For X/Y, proxies and construction components, populate definition/construction fields with original evidence or links to the card's evidence blocks, not authored restatements. The field structure is an index to evidence, not permission to rewrite it.

| Field | Required evidence |
| --- | --- |
| Original name and role | Exact variable label, meaning, unit of observation, and interpretation of larger values |
| Source inputs | Source/database, exact field codes when reported, components, data vintage when stated |
| Original definition/formula | All original defining sentences and formulas as screenshots or verified verbatim extracts; retain numbering and the authors' symbol definitions |
| Construction sequence | Original construction passages in source order, including linkage, filtering, grouping, aggregation and transformations; no authored X/Y recipe |
| Timing | Measurement date, fiscal/calendar alignment, windows, lags/leads, event-time alignment |
| Scale and units | Numerator/denominator, levels vs ratios vs percentages, scaling factors, currency/base year if reported |
| Transformations | Exact log form, standardization/reference population, demeaning, residualization, industry adjustments |
| Indicators/interactions | Exact cutoffs/inequalities, eligible universe, tie rules, reference category, interacting components |
| Missing/exceptional values | Missing vs zero, undefined denominators, exclusions, winsorization/trimming thresholds and grouping |
| Sample/usage | Applicable sample/subsample, model and table references |
| Replication details not reported | Specific missing choices that would prevent an exact reconstruction |

For a composite index, list components, signs, weights, normalization, and aggregation. For text-based measures, include document selection, dictionary/model/procedure and version if stated, counting/normalization and aggregation. For estimated measures, include the first-stage model, estimation population/window, and how fitted values/residuals become the measure. Apply these only when relevant; do not create new requirements for unrelated variables.

Preserve original formulas, notation, sums, timing, denominators, and definitions. If the article supplies only prose for X/Y, quote or screenshot that prose exactly; do not produce a replacement recipe or formula. For other variables outside this original-evidence requirement, any verbal restatement must be labeled and introduce no new assumptions. An ambiguous log definition, unreported database code, unspecified winsorization order, or missing matching key stays a documented gap. Never assert complete replicability solely because a detailed-looking card was produced.

## 7. Institutional Setting

Explain country/region, institutions, policy or historical event, key dates, affected units, eligibility, treatment and comparison groups, and the setting's timing. Distinguish announcement, enactment, implementation, and exposure dates when the article does. Explain why the authors chose the setting and how it makes their mechanism observable or provides identifying variation. No policy shock is required if the paper studies a different kind of setting.

## 8. Empirical Models and Identification Strategy

Display each original main equation and additional equations necessary to understand the reported evidence. Preserve the authors' equation numbering, notation, indices, summation limits, interactions, lag/lead structure, fixed effects, error terms, and functional form. Do not silently substitute a familiar textbook model.

For every model, explain the outcome, regressors, controls, fixed effects, index definitions, key coefficient/contrast and expected direction, estimator, observation unit, estimation sample/period, weights, standard-error method and cluster level(s), and any other disclosed estimation setting. Map it to hypotheses and tables/panels/columns. Distinguish displayed notation from additional implementation details stated in table notes.

Describe the identifying comparison/variation and the authors' claimed identifying assumptions separately from the regression equation. Include the necessary design-specific components: IV first/second stages and stated instrument rationale; DID treatment/timing/comparison; event-study reference period/window/binning; RD running variable/cutoff/bandwidth/specification; matching variables and procedure, when those designs are used and disclosed. Do not infer software, estimator defaults, or undisclosed diagnostics.

If no equation is printed, label the absence. An optional empirical-model reconstruction must say `Restated from the authors' model description`; this does not permit reconstructing X/Y definitions or proxies, which follow section 6. Compare each transcription with the source image. Preserve readable LaTeX as a transcription for inspection; do not call it the authors' actual source code. If a symbol cannot be read reliably, show a source crop and flag the uncertainty instead of presenting a guessed exact equation.

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
