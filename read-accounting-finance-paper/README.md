# Accounting & Finance Paper Reader

A reusable Codex skill for reading accounting and finance research papers, especially top-journal empirical studies, from user-supplied full text.

The analysis is in **English throughout**. Only the abstract includes a complete Chinese translation alongside the original English. The skill preserves the authors' terminology, hypotheses, variable definitions, equations, and qualifications, with source locations.

## Usage

Copy this entire `read-accounting-finance-paper/` folder into your personal Codex skills directory, keeping its subfolders intact. Invoke it in a session where the skill is available:

```text
Use $read-accounting-finance-paper to analyze this uploaded PDF.
Provide the complete English HTML report, the bilingual abstract,
replication-level variable definitions, original empirical models,
and screenshots of every main-text table.
```

With only a title, DOI, or URL, the skill searches for verified article links and asks you to supply the complete article before analyzing it:

```text
Use $read-accounting-finance-paper to locate this article: [title].
```

Automatic selection for relevant paper-reading requests is also enabled. No fixed journal ranking or journal whitelist is imposed.

## Report Contents

1. Article title, all authors and affiliations, journal, publication year, version, DOI, and verified handling editor.
2. Complete original English abstract and complete Chinese translation.
3. Research questions and every hypothesis or sub-hypothesis, preserving original labels.
4. Explicit theoretical foundations and English arrow diagrams of the authors' reasoning, including opposing predictions when discussed.
5. Separate data sources for X, Y, and important controls, coverage and estimation periods, and sample construction.
6. Replication-level variable definitions: original formulas, raw inputs, construction steps, timing, transformations, thresholds, and missing-value treatment as disclosed.
7. Institutional setting, country or region, relevant policies or historical events, and their role in the authors' argument.
8. Original empirical models, notation, estimators, fixed effects, inference settings, identifying comparisons, and stated assumptions.
9. Main tests and additional evidence linked to the authors' stated endogeneity concerns or alternative explanations.
10. Every main-text table in order, with original PDF screenshots and adjacent English commentary.

The output is a concise English chat summary plus a single-file HTML report. The HTML embeds its images, styles, diagrams, and native MathML equations for offline reading. It includes source locators, image zoom, and inspectable LaTeX transcriptions.

## Evidence Boundaries

- No substantive analysis before the user supplies full text; a URL or abstract alone does not satisfy this requirement.
- No mixing working-paper and published versions.
- No guessing of missing definitions, database fields, formulas, editors, tests, or findings. Unreported replication details are identified explicitly.
- Original formulas and model transcriptions are checked against the source. Reconstructions from verbal descriptions are labeled as restatements.
- Explanations follow the authors' claims and qualifications; independent methodological criticism is outside the default workflow.
- Provided appendices may support definitions and interpretation, but the default screenshot walkthrough includes main-text tables only.
- The skill explains replication requirements; it does not itself reproduce empirical estimates or establish causal validity.

## Files

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Entry point, full-text gate, language rules, workflow, and completion checks |
| [agents/openai.yaml](agents/openai.yaml) | Display metadata, invocation example, and automatic selection policy |
| [Report contract](references/report-contract.md) | Detailed requirements for the ten report sections |
| [Tool instructions](references/tools.md) | Screenshot coordinates, report input format, formulas, and visual checks |
| [HTML template](assets/report-template.html) | Offline layout, responsive table commentary, MathML styling, and image zoom |
| [Capture helper](scripts/render_tables.py) | Source-preserving PDF renders and an auditable capture inventory |
| [Report builder](scripts/build_report.py) | Single-file HTML packaging with embedded assets |

## Runtime Requirements

For the helper scripts, use Python 3.9 or later. PDF capture requires `Pillow`, `pypdf`, and Poppler's `pdftoppm`. The report builder uses the Python standard library. Prefer an available bundled runtime; discover its paths in the current environment rather than copying another machine's paths.

If needed, install the Python dependencies with:

```text
python -m pip install Pillow pypdf
```

Install Poppler separately and make `pdftoppm` available on PATH, or pass its path using the capture helper's `--pdftoppm` option. Open the generated report in a modern browser with native MathML support. See [Tool instructions](references/tools.md) for the complete interfaces and visual verification procedure.

Source papers, generated reports, captures, and research data belong in the user's working directory. They are not included in this skill package.
