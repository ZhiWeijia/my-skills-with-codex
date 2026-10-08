# Data, Timing And Partitioners

Read for merges, pre-shock measures, cutoffs, peer metrics, exits and invariant groups. Adapt names and years to the baseline contract.

## 1. Identify The Unit Before Computing Anything

Maintain an explicit crosswalk among firm ID, unit ID, country, year and any real establishment ID. Numeric group IDs generated independently in two datasets are not reliable merge keys; normalize stable identifiers such as ISIN/CUSIP while preserving leading zeros. An ISIN identifies a security and may not be a permanent economic-firm identifier across corporate events; audit mappings when the research question requires firm continuity.

Check panel uniqueness before applying lags or selecting pre/post observations:

```stata
assert !missing(unit_id, year)
isid unit_id year
```

If the analysis moves from firm-country-year to firm-year, use an appropriate firm aggregate input or a documented aggregation of genuine additive country outcomes. Do not sum repeated firm-wide totals. Rebuild firm-level pre-shock cutoffs rather than importing old High/Low indicators generated on repeated country rows. Reconsider weights, treatment, FE and cluster for the new unit; changing only the Y column is insufficient.

A firm-country grouping cannot serve as a fallback for missing firm IDs when computing a unique-firm cutoff without changing that cutoff's meaning. Audit missing IDs and use a documented firm crosswalk or exclude them from the cutoff universe. Do not invent IDs that pretend to link countries.

## 2. Treat Duplicates As A Question About Data

First distinguish identical duplicates from conflicting values, including disagreement about missingness. Remove identical redundant records only after recording counts. For conflicts, export their IDs, years, source rows and component values, then resolve under the user's instructions. Do not use `collapse (mean)` or `destring, force` to conceal conflicts or failed parses.

For a firm pre-shock measure, choose the declared measurement year, check cross-country consistency, then deduplicate:

```stata
keep if year == pre_year
assert !missing(firm_id)
bys firm_id: egen double x_min = min(raw_score)
bys firm_id: egen double x_max = max(raw_score)
assert abs(x_min - x_max) < 1e-8 if !missing(x_min, x_max)
bys firm_id: egen byte x_any_missing = max(missing(raw_score))
bys firm_id: egen byte x_any_observed = max(!missing(raw_score))
assert !(x_any_missing & x_any_observed)
keep firm_id raw_score
duplicates drop
isid firm_id
```

The mixed-missing assertion can instead feed a diagnostic if the baseline explicitly permits filling a repeated missing value from the same firm's observed value. Such propagation is a declared data rule, not automatically valid averaging.

When firm-specific shock timing differs, select by `firm_id × pre_year` and audit that the intended firm-level base1 is unique. `min(year if post==1)` in a truncated panel can be the first observed post year rather than the actual adoption year. Prefer a verified treatment schedule; report observed-year fallback use.

If the user specifies a pause on a source's duplicate firm-years, stop that source-dependent branch and save diagnostics; unrelated approved branches can continue. Never silently pick the first conflicting carbon-emissions row.

## 3. Merge Without Expanding The Main Panel

Check the using-file key and then preserve the main universe:

```stata
* Validate the using dataset separately: isid firm_id year.
use main_panel, clear
isid unit_id year
local n_before = _N
merge m:1 firm_id year using annual_scores, ///
    keep(master match) generate(merge_score)
assert _N == `n_before'
isid unit_id year
```

Do not overwrite an existing main variable unnoticed. Select `keepusing()` where appropriate; decide whether the source or main value is authoritative before merge.

For every new Y, distinguish within the declared main sample:

- unmatched records: `merge_score == 1`;
- matched records with a missing source Y;
- transformation-invalid records, such as finite salary <= 0 for `ln(salary)`;
- total missing Y, with mutually exclusive components summing to the total.

Report shares with a common denominator. The main sample normally follows the baseline restriction before dropping the new Y, not its final `e(sample)`.

```stata
gen double ln_salary = ln(salary) if !missing(salary) & salary > 0
gen byte main_sample = region == "EU" & regsample == 1
count if main_sample
local nmain = r(N)
count if main_sample & merge_score == 1
local nunmatched = r(N)
count if main_sample & merge_score == 3 & missing(salary)
local nsource_missing = r(N)
count if main_sample & merge_score == 3 & !missing(salary) & salary <= 0
local ninvalid = r(N)
count if main_sample & missing(ln_salary)
assert r(N) == `nunmatched' + `nsource_missing' + `ninvalid'
```

Guard an empty denominator before calculating shares. A missing gate, such as pause at 10%, is user-specific; save the report before stopping. If the user later authorizes proceeding, record that override, retaining missing values. Never translate that override into zero filling.

## 4. Build Pre-Shock Measures Once

Store `shock_year`, `pre_year`, `post_year`, annual raw measure and constructed `*_base1`. After `isid unit_id year`, a conditional `egen max()` can propagate the one pre-year observation; its purpose is not to choose among conflicting rows.

```stata
bys unit_id: egen double score_base1 = ///
    max(cond(year == shock_year - 1, annual_score, .))
```

Check both nonmissing values and missingness patterns for invariance at the level promised by the variable. A company-global score should agree across countries; its country-specific employment decline need only be constant within `unit_id`.

Composite scores require all components unless a different definition is authorized:

```stata
gen double env_plus_social = env + social if !missing(env, social)
```

`egen rowtotal()` can turn incomplete components into a misleading observed total. Verify raw units and whether employment has been logged before summing peers. A name ending in `_log` or a suggestive label does not settle its provenance.

## 5. Compute Cutoffs On The Right Reference Sample

Specify four independent decisions: measurement time; deduplication unit; eligibility/reference universe; tie rule. Record whether percentile cutoffs are unweighted or explicitly weighted. Do not use regression weights automatically for a cutoff.

If annual `regsample` varies, define membership before collapsing:

```stata
bys unit_id: egen byte ever_regsample = max(regsample)
```

Audit whether a missing `regsample` means unknown or ineligible. For a firm-level cutoff use the corresponding ever-membership at firm level and one validated value per firm. For country indicators, use one country per declared reference region, never firm-count-weighted country rows. EU and worldwide medians are different objects.

For unique firms already verified as one row per firm:

```stata
summarize score_base1 if cutoff_sample == 1 & !missing(score_base1), detail
local p50 = r(p50)
local p75 = r(p75)
gen byte score_low = score_base1 < `p75' if !missing(score_base1)
gen byte score_high = score_base1 >= `p75' if !missing(score_base1)
assert score_low + score_high == 1 if !missing(score_base1)
```

Only create indicators if the reference universe is nonempty and the cutoff is finite. Empty or sparse cells get a documented unavailable status.

High `>= cutoff` / Low `< cutoff`, or High `> cutoff` / Low `<= cutoff`, must be explicit and mutually exclusive. Ties can make groups very unequal. Report p25/p50/p75, finite unique values, zero share, ties and group Ns before estimating; do not force identical values apart with `xtile`.

Three groups in one project's bounded ReportingScope measure were:

```stata
gen byte rs_low = rs_base1 <= rs_p25 if !missing(rs_base1, rs_p25)
gen byte rs_med = rs_base1 > rs_p25 & rs_base1 < 1 ///
    if !missing(rs_base1, rs_p25)
gen byte rs_high = rs_base1 == 1 if !missing(rs_base1)
assert rs_low + rs_med + rs_high == 1 if !missing(rs_base1)
```

This requires the expected support and `rs_p25 < 1`; if p25 equals 1, the definitions overlap. Diagnose and obtain a substantive rule rather than manipulating values to force populated groups. The value `0.25` is not interchangeable with the p25 statistic.

Compute shared cutoffs outside outcome loops. A cutoff based on unique eligible units should not change when a new Y is missing or when HDFE drops observations. For a sample-filter robustness test, fix the original cutoffs when the user asks for the sample exclusion to be the only change.

## 6. Peer Construction: Two Distinct Designs

Document market, pre-shock activity, timing and leave-one-out exclusion. Under firm-country data, a country-industry market often has one record per firm; verify this before subtracting the focal record. If several establishments belong to a firm in the market, subtract the entire focal firm when the design calls for other firms.

**Peer-average scope design:** average peers' pre-shock scope, then compare that peer-average variable with its own median in the declared unique-focal-unit/coverage universe. Do not compare it with the median of individual-firm scope. Labor change is subsequently averaged over the declared labor peer pool and split in eligible focal subgroups. A low average peer scope does not mean every peer individually has low scope.

**Low/High-scope peer-pool design:** first classify each peer firm using a firm-level pre-shock scope cutoff, then aggregate employment/exit only for the chosen pool. A focal firm need not itself have high scope unless the specification says so. Having at least three low-scope peers and having a low average scope are not equivalent.

For a peer mean, subtract the focal value and its nonmissing-count contribution:

```stata
bys market_id: egen double scope_sum = total(scope_pre)
bys market_id: egen long scope_n = total(!missing(scope_pre))
gen long peer_scope_n = scope_n - !missing(scope_pre)
gen double peer_scope_mean = ///
    (scope_sum - cond(missing(scope_pre), 0, scope_pre)) / peer_scope_n ///
    if !missing(peer_scope_n) & peer_scope_n > 0
```

Missing market IDs must not create one artificial missing-ID market. Total peer count, nonmissing-scope count and usable-labor count need separate fields. Count thresholds must guard missing: `!missing(peer_n) & peer_n >= threshold`.

## 7. Labor Decline, Released Capacity And Exit

Define signed decline as raw pre employment minus raw post employment. Positive means contraction, zero means no change, negative means expansion. This is not a count of workers physically leaving or an observed exit unless additional evidence exists.

If the baseline authorizes conservative post-missing imputation for peers:

```stata
gen byte post_imputed = !missing(labor_pre) & missing(labor_post)
gen double labor_post_cons = labor_post
replace labor_post_cons = labor_pre if post_imputed == 1
gen double labor_decline = labor_pre - labor_post_cons ///
    if !missing(labor_pre, labor_post_cons)
```

Retain raw post labor. Report imputed count/share and the pre-employment-weighted share, with denominator definitions. Pre-missing is not solved by this rule. If a user asks for pre/post missing to fall into a zero-category dummy, keep the numerical decline missing and label the dummy as no observed change/missing, not confirmed no change.

For a selected LowRS pool, after consistent leave-one-out and post treatment:

- exposure = selected-pool pre employment / all-market-peer pre employment;
- contraction = selected-pool net released employment / selected-pool pre employment;
- released capacity = selected-pool net released employment / all-market-peer pre employment;
- count exit rate = explicit-zero exits / active selected-pool peers;
- employment exit rate = exiting peers' pre employment / selected-pool pre employment.

An explicit exit requires positive pre employment and observed raw post equal to zero. Missing post is a separate event. Net released capacity may be negative. A market with no selected-pool peers can have exposure/released capacity zero if the baseline allows it and the total denominator is positive; its selected-pool contraction is undefined.

Preserve `released_emp`, not only normalized capacity. Test matching-denominator identities using finite values and a scale-appropriate tolerance:

```text
released_capacity = exposure * contraction
released_emp = exit_emp + survivor_net_release
survivor_net_release = survivor_gross_downsize - survivor_gross_expansion
```

Report metric-specific coverage. Exposure may require total peers; exit rates/contraction selected peers; total-market capacity and selected-pool robustness can use different minimum-count rules.

Zero-median labels must reflect support: nonnegative exit/exposure can use No/Any; signed decline/release should use Nonpositive/Positive under `<= / >`, or Negative/Nonnegative under `< / >=`.

## 8. Cell Medians And Nested Samples

On one validated row per unit, use a declared parent eligibility and, if specified, market-time cell:

```stata
gen byte eligible = ever_regsample == 1 & parent == 1 ///
    & !missing(peer_metric, peer_n, country, industry_pre, post_year) ///
    & peer_n >= min_peers
bys country industry_pre post_year: egen double cell_median = ///
    median(peer_metric) if eligible == 1
gen byte peer_low = eligible == 1 & !missing(cell_median) ///
    & peer_metric < cell_median
gen byte peer_high = eligible == 1 & !missing(cell_median) ///
    & peer_metric >= cell_median
assert peer_low + peer_high == 1 if eligible == 1 & !missing(cell_median)
```

Audit number of eligible focal units in every cell, sparse cells, ties and how missing/cell exclusions affect the parent. A two-focal-unit cell rule is an additional decision, not implied by a three-peer rule.

Merge the fixed cutoff/split back into the panel by its validated unit key. If focal-score High/Low subcolumns are intended to partition pooled parent PeerLabor columns, create parent columns as their disjoint union and exclude missing focal scores consistently. Test sample-N additivity. `e(N)` may not add because singletons are removed differently across regressions.

## 9. Exit, Delisting And Stability Diagnostics

Before proposing an exit regression, show treated/control counts by year, positive pre employment, observed-zero post, missing post, missing panel rows and availability of weights/controls. Explain anomalous counts first.

`tsfill, full` creates rows, not evidence of an economic exit. Mark original rows before filling; newly created rows have missing firm covariates/IDs and must be handled explicitly. Lags refer to the immediately preceding calendar period after correct `xtset`; require an observed prior at-risk status.

EU delisting on a verified firm-year listing universe can be `L.listed==1 & listed==0`. Disappearance from a source panel is a separate ambiguous event. Unmatched listed source rows mean nonlisted only if that source is known to be exhaustive over the raw universe.

For stability, classify always listed, never listed and switchers using observed annual statuses; report years observed, gaps and switches. “Always in observed years” does not prove always over every year in a nominal window. Map the firm status back without expanding rows.

For invariant variables, inspect min/max plus any-missing/any-observed within the promised key. All missing is unavailable, not conflicting; a mix of missing and finite values must be audited separately. Output `.dta` only when requested; a panel file, unit file and audit serve distinct purposes and should not be multiplied without need.
