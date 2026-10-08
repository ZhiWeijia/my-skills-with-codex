# Reproducible Runs, Tables And Figures

Read when creating a master, exporting or combining tables, debugging alignment, producing figures or correlations, or executing Stata on Windows.

## Separate Construction, Estimation And Presentation

Reuse existing helpers where their behavior is verified. A useful dependency graph is:

```text
raw inputs -> normalized/validated panels -> annual source merges
           -> fixed pre-shock measures and peer metrics
           -> audited workfile + saved cutoff/group data
           -> regressions + structured estimates + coverage
           -> presentation CSV/XLSX + same-source figures + method note
```

A master coordinates these steps; it must not conceal unknown external datasets. Parameterize root, raw version, output namespace and run mode. Avoid copying the whole project unless an isolated runtime is actually needed; if copied, enumerate transformations and check every output path.

Possible modes are `fromraw`, `reuse_workfile`, and `exportonly`. Describe what each rebuilds. Cache use is legitimate when named as such. Do not claim a script runs raw-to-results merely because it has `use workfile.dta` or a comment that workfile originally came from raw. Test the fromraw chain in an isolated intermediate directory; validate every dependency and prerequisite output before proceeding.

For a new raw-data version, redirect both generated intermediates and outputs. Replacing only final result filenames risks contaminating frozen workfiles. Record hashes or size/timestamps for fixed inputs, code and protected results; compare after the run. Folder renames require resolving current paths, not creating a second stale directory that happens to match old hardcoded strings.

## Software Responsibilities

- **Stata:** empirical data transformations, panel operations, estimation, stored-result capture, `.dta` outputs and native graphs when requested.
- **PowerShell:** Windows process orchestration, path validation, manifests/hashes, declared runtime copies and file-lock fallback. Do not use screen scraping or Ctrl+C output as the canonical model data.
- **Python/R:** structured CSV/XLSX parsing, formatting or tests when useful and available; a numerical implementation of a different estimator is not an unnoticed fallback for missing Stata packages.
- **Excel:** presentation and QA, not hidden/manual changes to estimates. A locked workbook requires an alternate output, not terminating Excel or overwriting unrelated open work.
- **UI tools:** use only if command/API execution is unavailable or actual interactive inspection is required; preserve the log-based audit trail.

No particular plugin, executable path or library is assumed in another project. Locate available tools first. Record package versions with `which` and local help. Check current primary documentation when syntax or method is uncertain.

## Stata Execution On Windows

Quote paths containing spaces and launch the actual installed executable. For the project's known batch style, adapt this process pattern after verifying the Stata edition's command-line syntax:

```powershell
$stataExe = 'C:\Program Files\Stata18\StataSE-64_old.exe'
$doPath = 'D:\Project\analysis\master.do'
if (!(Test-Path -LiteralPath $stataExe)) { throw 'Stata executable missing' }
if (!(Test-Path -LiteralPath $doPath)) { throw 'Master do-file missing' }
$stataRun = Start-Process -FilePath $stataExe `
    -ArgumentList ('/e do "{0}"' -f $doPath) `
    -WindowStyle Hidden -PassThru
```

This executable/path is an example from the source project, not a requirement. Monitor the launched process and task-specific log; do not accidentally attach to or terminate another Stata session. Keep the user updated during long runs. Do not announce completion while a required estimator is still running.

The process exit code alone may not show a Stata script's error. Inspect the current run's log for the first error and a deliberately written completion marker, plus required artifacts. Open the log before builders so upstream failures are captured. Explicitly propagate shell-helper failures; existence of a stale helper CSV is not proof the newest extraction succeeded.

Avoid changing machine date/time. Use user timezone for human-facing timestamps and a unique run ID. A reproducible random seed does not freeze package versions, data order, numerical convergence or sample selection.

## Structured Result Schema

Prefer one row per model/term over parsing a pretty fulltable. A practical schema:

```text
run_id, test_id, panel_id, outcome_id, split_id, column_id, column_order,
column_label, term, beta, se, p, ci_low, ci_high,
raw_eligible_N, regression_N, unit_N, treated_unit_N, control_unit_N,
cluster_N, r2, r2_a, rc, status, missing_reason
```

Store long labels as strings, not Stata variable names (which have length limits). Keep numeric quantities numeric and stars/format strings separate. Export coverage even when a model fails. Initialize model-specific locals to missing and clear/store results deliberately so prior estimates cannot populate a failed model.

Use an explicit ordered column map. Never infer model position from the count of successful `eststo` entries. Failed model 5 must remain model 5 with blank estimate/status, rather than shift model 6 left. Preserve row positions for labels, coefficients, SEs, FE, fit and N.

## CSV And XLSX Alignment

Use a proper CSV reader/writer for quoting, embedded commas, newline fields and adjacent/leading/trailing empty cells. `gettoken` that skips commas, whitespace splitting, or naive `split(',')` can turn an empty SE/row-label cell into a left-shifted table. This was a concrete failure mode in the source project.

For a combined presentation grid, use all-string import or direct cell export from a structured grid. A coefficient like `1.23***` and an SE like `(0.45)` are presentation strings; do not let Excel interpret them as formulas. Preserve identifier leading zeros and guard formula-looking untrusted labels without altering numeric negative estimates. Export UTF-8 text consistently; check Chinese comments/notes for mojibake, especially with Windows PowerShell default encodings.

Check the workbook, not merely file existence:

- row-name column A and expected models starting at B;
- explicit header order and model count for every block;
- DID/ATT values and SEs in the same model columns;
- failed columns, blank cells, metadata width and long headers;
- title/panel layout, legibility, notes and nonempty sheet content.

Keep structured data and presentation files separate. If Excel locks the target, use the established timestamp fallback, log the original error and actual saved path, then verify the alternate artifact. Only classify an error as a lock when evidence supports it; a parser error is not fixed by renaming the target.

## Combining Frozen Tables

Match blocks by stable outcome/split/panel IDs, and columns by full labels. Match coefficient rows by term and occurrence (SE rows may have empty names), not just line numbers. Reject duplicate keys and missing source blocks.

When combining baseline and extension outputs, declare which source supplies common columns. Compare common beta, SE, N, FE and fit values; save discrepancies. Differences can reflect sample or numerical issues, not just display. Use the designated source if the user has explicitly chosen it, while reporting mismatches.

Append or reorder requested columns without recalculating frozen ones. Bdiff rows use a metadata schema, not a set of model coefficients; do not run them through the same numeric-column slicing. Keep bdiff cells blank for extension columns where no test exists. If reformatting frozen Panel A/B and newly estimating Panel C/D, import saved A/B results exactly.

Check expected block count, columns per block, bdiff pairs/repetitions and retained-column relative order. A merge-check CSV should state source existence, key-match status, common-column comparison and output column mapping.

## Figures Use The Table's Sample Definitions

Use the same saved source workfile and group variables as the table. If rebuilding cutoffs, call the same construction code with the same reference universe; do not read an old median dataset from a different sample. Declare whether figures describe the raw eligible sample or the exact regression `e(sample)`, and whether means are unweighted or regression-weighted.

Event-time raw means can use:

```text
pre  = year == shock_year - 1
post = year == shock_year + 1
control = treatment group 0; treated = treatment group 1
mean of finite raw employment; show each cell's N
```

Do not silently impute descriptive Y because peer construction imputes post labor. Save means and group Ns before plotting. Verify the requested number of cells, labels, event-year mappings and finite means. A pre/post bar plot is descriptive and does not establish parallel trends.

For grouped bars with line overlays, use the bar-center x coordinates for each group's connected line. Show mean labels and use fixed raw zero-based y-axis, suitable width, outline and markers. If a small control bar is almost invisible, improve visibility through stroke/labels/markers or an explicitly separate panel; never inflate the raw bar height or hide a log/broken axis transformation. Export PNG/PDF and inspect the rendered graph for clipped labels and nonblank content.

## Correlation Tables

Specify observation unit independently for each sheet. For a firm-country-year versus firm-year comparison, first verify the country panel key, then create a documented firm-year aggregation. A simple average is appropriate only if requested for the continuous partitioners; verify that company-global pre-shock scores agree, and explain that country-specific peer metrics are averaged.

Use pairwise complete data and store a pairwise N for every coefficient. Compute Spearman on paired observations so ranks correspond to that pair, including proper ties; full-sample ranks followed by dropping missings can differ. Store p-values separately and define significance thresholds. Missing/constant pairs get a status, not invented zeros or stars; diagonal self-correlations have no inferential stars.

For Pearson/Spearman stars, follow the software's declared test and df convention. Repeated pre-shock measures over years are not independent observations; naive correlation p-values can overstate precision. Document whether stars use conventional observation-level tests or a requested cluster-aware method, and do not substitute the latter without permission. Check symmetry, [-1,1] bounds, pairwise Ns and sheet names.
