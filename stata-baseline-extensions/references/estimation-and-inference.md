# Estimation, Inference And Numerical Diagnostics

Read for DID/SDID changes, cross-column tests or missing SEs. Preserve the baseline estimand and distinguish a numerical diagnostic from an authorized specification change.

## DID Specification

`c.treat##c.post` includes both main effects and their interaction; `c.treat#c.post` includes only the interaction. The latter is equivalent only when the specified FE or other regressors span the omitted main effects on the actual estimation sample. Verify treatment invariance and the time/group structure of post. A firm-specific or country-specific post may not be absorbed by calendar-year FE. A sample-derived first observed post year must not silently replace the true policy timing.

Do not prescribe interaction-only universally, or promise it repairs VCE problems. If the user requests a new DID-only version, change every estimator and every bdiff model consistently, record the model change, then compare coefficients, samples and inferential status.

Generic adaptation of a project regression:

```stata
capture noisily reghdfe outcome c.treat#c.post controls [pw=weight] ///
    if main_sample == 1 & subgroup == 1, ///
    absorb(unit_id industry#year country#year) vce(cluster unit_id)
local rc = _rc
```

Resolve the actual variable list and FE structure from the contract. Save `rc` before any count, display or auxiliary command. On success, verify the coefficient exists and is not omitted; then read `_b[]`, `_se[]`, `e(V)`, `e(N)`, `e(df_r)` and relevant cluster count. Store `e(sample)` for any exact sample comparison before another estimator overwrites it.

Select cluster level according to treatment assignment and dependence, while preserving authorized baseline replication. A firm-country cluster differs from a firm cluster across countries. Flag this distinction as an inference-design question when appropriate, not an automatic unrequested model replacement.

A significant coefficient in one subgroup and an insignificant coefficient in another does not establish a difference. Use a declared coefficient-difference test. Heterogeneity across realized post-shock peer outcomes is descriptive/conditional unless the identification strategy justifies more; treatment can affect both the partitioner and Y.

Keep exploratory cutoff variants and outcome families labeled and traceable. Choose or justify cutoffs using measurement support and the research design, not which version produces stars. If many outcomes, metrics or splits are reported, document the test family and any requested multiplicity adjustment; do not silently present a selected exploratory variant as a prespecified test.

## Diagnose Missing Coefficients And SEs

First determine whether a blank cell is an export error, empty sample, estimation failure, omitted coefficient, missing SE, or stale stored model. Do not explain every blank as collinearity.

For a model with absent or huge SEs:

1. Reproduce the exact sample, variables, weights, FE, cluster and software version; save warning messages, `_b`, `_se`, `e(V)` and `e(sample)`.
2. Check treated/control units and years, transition variation, clusters, small cells, weights, outliers, variable scales and within-FE variation.
3. On a fixed diagnostic sample compare clustered and conventional/robust VCE. Freeze the sample or show which observations change; a successful conventional SE localizes a problem but does not justify replacing clustered inference in the formal result.
4. Compare without controls, then add controls in blocks on the same complete-case sample to isolate numerical issues rather than confuse them with sample changes.
5. Inspect verbose collinearity output and FE absorption, particularly redundant treat/post main effects. Test justified solver/scaling adjustments in a new diagnostic version and document them.

Point estimates can exist while VCE is invalid. Use `estimated_no_valid_se` or similarly precise status, not success-with-stars. No inference should be fabricated for omitted terms, zero SE, invalid df or singular VCE. Do not accept a changed ATT as proof that a display-only edit was harmless.

The official [reghdfe help](https://scorreia.com/help/reghdfe.html) documents FE absorption, singleton handling and numerical options. Inspect local `which`, help and ado versions for the run actually being reproduced; do not upgrade packages silently.

## Bdiff

Read the installed `bdiff` help and ado before interpreting stored matrices, resampling or p-value direction. Save the command/version and use an explicit coefficient name. A project may require `reps(20) seed(12345)` for replication; keep that choice when fixed, report it, and do not treat it as generally adequate publication precision.

For each pair record `first_group`, `second_group`, `coef_tested`, `beta_first`, `beta_second`, `second_minus_first`, p-value, method, requested/completed reps, seed, raw/sample Ns, status and rc. Verify the observed pair estimates match the displayed columns within a justified tolerance.

Possible statuses include:

```text
success
skipped_no_obs
skipped_no_coeff
skipped_bdiff_unavailable
skipped_bdiff_failed
estimated_no_valid_se
```

Never silently substitute pooled-interaction inference when the user specifically asks for bdiff. Failure logging does not justify labeling an unexecuted test `bdiff_reps20` without a skipped status.

For disjoint groups, a simple group indicator suffices. For overlapping samples, independently copied pair-specific stacks can preserve the two displayed group memberships, but naive permutation of duplicated rows may be invalid. Preserve original unit IDs, audit overlaps and dependence, and check whether the implemented resampling honors the paired/cluster structure. If not, report the limitation and resolve the inference design before treating the p-value as valid. Do not equate sample matching with valid resampling.

Twenty permutations produce coarse p-values, and a returned zero may mean no simulated statistic exceeded the observed statistic. Preserve software-reported p-values for replication, state repetitions and convention, and do not claim p=0 in a population. Do not change to a plus-one convention without declaring the change. Increasing reps is a methodological/run-cost change, not a display edit.

## SDID Is A Different Estimator

Use the verified treatment path, typically `treat * post` for a binary absorbing treatment:

```stata
gen byte treatment_on = treat * post if !missing(treat, post)
assert inlist(treatment_on, 0, 1) if !missing(treatment_on)
```

Check invariance of treatment-group assignment, adoption cohorts, no treatment reversal, pre-treatment support, permanently untreated controls and enough treated units for the requested inference. Inspect the installed `sdid` requirements instead of assuming all DID samples qualify.

Changing to SDID also changes weighting and covariate adjustment. Do not carry over `reghdfe` FE labels or pweights as though the same model were estimated. If the baseline main-sample restriction itself required an entropy-balancing weight, report that continuing to use it affects eligibility even when SDID no longer uses that weight.

### Balance After All Required Missing Drops

For a fixed annual window, after the group restriction and complete-case checks for Y, treatment and requested covariates:

```stata
local first_year 2017
local last_year 2025
local n_years = `last_year' - `first_year' + 1
keep if inrange(year, `first_year', `last_year')
assert !missing(unit_id, year)
isid unit_id year
egen int required_missing = rowmiss(outcome treatment_on controls)
drop if required_missing > 0
bys unit_id: gen int observed_years = _N
bys unit_id: egen int first_observed = min(year)
bys unit_id: egen int last_observed = max(year)
keep if observed_years == `n_years' & first_observed == `first_year' ///
    & last_observed == `last_year'
isid unit_id year
assert observed_years == `n_years'
```

Here `controls` represents an expanded variable list. Count balancing works only after unique integer annual periods and an exact window are verified. For nonannual/gapped designs, test presence in each declared period. `tsfill` with invented outcomes does not create a valid balanced sample.

Apply column-specific balancing when required, and report how that changes cross-column comparability. An optional common balanced sample is a different requested robustness design. Keep missing as missing; do not interpolate attrition away.

Audit original subgroup N, missing exclusions, unbalanced-unit exclusions, balanced N, units, treatment/control units and cohorts. Exclusion of exiting units can induce survivor selection, especially for a paper about employment exit; SDID is not automatically a remedy for endogenous attrition.

### Run And Extract

An example matching the project's requested SDID setup is:

```stata
capture noisily sdid outcome unit_id year treatment_on, ///
    cluster(unit_id) vce(bootstrap) reps(100) seed(123) ///
    covariates(controls)
local rc = _rc
if `rc' == 0 {
    ereturn list
    local att = e(ATT)
    local se = e(se)
}
```

Use `ereturn list` and the installed help to confirm returned fields, not invented `e()` scalars. Extract ATT, bootstrap SE, CI and p using the implemented inferential convention; label normal-approximation p/CI if calculated from ATT/SE. The [official SDID help](https://github.com/Daniel-Pailanir/sdid/blob/main/sdid.sthlp) describes syntax, covariate methods, inference and adoption handling. The input group already defines the default inference unit; an explicit same-unit cluster option may be redundant. Retain it when reproducing the requested command and check availability in the installed version.

Report SDID ATT rows, not DID control coefficients or FE Yes rows. Failed columns remain in their intended positions with status. Package installation should follow existing project/user authorization; pin or record versions, and log installation failures. Do not overwrite a working frozen environment with an unsolicited `replace` install.
