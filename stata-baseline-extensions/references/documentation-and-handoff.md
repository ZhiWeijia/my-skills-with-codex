# Documentation And Transfer To A New Project

Read for detailed code notes, a standalone raw-to-results deliverable or a reusable handoff. Match the user's language and required outputs; this project's user repeatedly requested Chinese/English explanations with an empirical-paper style.

## A Standalone Deliverable

When requested, include in one versioned folder:

```text
master.do
required builders/helpers, or explicit stable dependency references
method_note.txt
variable dictionary and cutoff/sample audit
structured estimates and coverage
fulltable.csv / fulltable.xlsx
bdiff coverage, if requested
means/figures, if requested
run log and run manifest
```

Use only files the requested analysis needs. A short export-only task should not generate a raw-data rebuild, inference or many extra formats. If the user asks for `.dta` only, produce Stata datasets and necessary checks without unsolicited CSV/XLSX/regressions.

The folder is self-contained only if all its helpers and required inputs are supplied or explicitly resolvable in the target project. A do-file that points into a previous runtime can be a valid cached-workfile runner, but not a portable raw-to-results package. Reuse shared code when appropriate and document the exact path/version; avoid both hidden dependencies and needless duplication.

## Code Notes At The Point Of Use

Add succinct, substantive comments before selection/merge, base1 extraction, cutoff estimation, eligibility, group assignment, estimation, bdiff and figure means. Keep top notes consistent with executed code. Remove explanations of dropped output columns from final-specific notes, while preserving definitions of all retained columns.

Every generated variable needs:

- exact variable name and economic/statistical interpretation;
- source field/file, original unit and transformations;
- observation level and measurement year/window;
- formula, denominator, selected peer pool and leave-one-out rule if relevant;
- nonmissing/coverage requirements;
- cutoff reference universe, deduplication unit and weighting;
- ties, zero values, negative values and missing treatment;
- parent sample, final group condition and output-column mapping.

Use “net employment contraction” for signed pre-minus-post employment. Use “exit” only for the declared observed event. An average peer scope classification is not a statement that all peers individually satisfy a score cutoff.

A claimed invariant variable needs a reported check at its actual key. A fixed subgroup constructed using post-shock data may be time invariant after construction yet not predetermined before treatment. These are different properties.

## Bilingual Method Note Pattern

Replace the bracketed labels with verified project values. Do not leave unresolved fields in a delivered final method note.

**English: empirical objective and sample**

“We examine whether the treatment-associated change in [outcome] differs across firms classified by [pre-treatment measure]. The unit of observation is [unit] by [time]. The analysis uses [source/version] over [window], with eligibility defined by [restriction]. The subgroup comparisons preserve the baseline controls, weights, fixed effects and clustering, except for the explicitly specified changes described below.”

**中文：检验目的与样本**

“本文考察，按处理前的[指标]划分的企业，其[结果变量]在政策冲击后的处理效应是否存在差异。观测单位为[单位]与[年份]，数据来自[来源及版本]，分析窗口为[年份]。样本条件为[限制]。除下文明确说明的变更外，检验沿用基准回归的控制变量、权重、固定效应及标准误聚类层级。”

**English: cutoff and timing**

“The classification uses the value observed in [pre-treatment year rule]. We compute the [quantile] among unique [reference units] in [reference sample], thereby avoiding duplicate weighting from repeated [countries/years]. High is defined as [exact condition] and Low as [exact condition]. Missing values are not imputed. Ties are assigned to [group], so the groups need not contain equal numbers of firms.”

**中文：分组与测量时间**

“分组指标取自[处理前测量年份规则]。本文在[参考样本]的唯一[参考单位]层面计算[分位数]，避免同一企业因跨国家或年度重复出现而被重复加权。High 定义为[精确条件]，Low 定义为[精确条件]。指标缺失不进行填补；等于阈值的观测归入[组]，因此各组规模不必相等。”

**English: realized peer change**

“Peer employment contraction equals employment in [pre year] minus employment in [post year], aggregated over [peer definition] excluding the focal firm. Positive values denote net contraction and negative values denote expansion. Because this partitioner is measured after treatment, the subgroup estimates describe heterogeneity conditional on realized peer outcomes; they do not by themselves identify a causal mechanism.”

**中文：同行就业变化**

“同行就业收缩定义为[前期]就业减去[后期]就业，并在[同行范围]内汇总，排除 focal firm 自身。正值表示净收缩，负值表示扩张。该分组依据包含处理后的信息，因此结果反映给定实际同行就业变化的条件异质性，不能仅凭该分组检验识别因果机制。”

**English: inference**

“Each column estimates [equation/command] with [FE], [weights] and standard errors clustered at [level]. We compare [pair] using [method] with [repetitions] and seed [seed]. The reported difference is the coefficient in the second group minus that in the first group. We report unavailable estimates and failed inference explicitly.”

**中文：估计与推断**

“各列采用[方程或命令]，吸收[固定效应]，使用[权重]，并在[层级]聚类标准误。组间差异使用[方法]检验，重复[次数]次，随机种子为[种子]。报告的差值方向为第二组系数减去第一组系数；无法估计或推断失败的情况单独记录。”

Document finite-repetition p-value precision, overlap resampling, SDID balanced-sample selection and any missing override when applicable. Do not use academic language to mask descriptive identification limits.

## Baseline-To-Extension Handoff Checklist

Before a new project run, establish a short decision record:

```text
Baseline master/results/log:
Raw input versions and merge keys:
Unit and treatment schedule:
Y meaning/unit/transform:
Original restriction, weights, controls, FE, cluster:
Requested change:
Fixed definitions/cutoffs:
New metric source and pre/post timing:
Cutoff universe, unique unit, ties, missing:
Inference method/reps/seed:
Expected panels/column labels/order:
Output/intermediate namespace:
Raw-to-results dependencies and run mode:
Unresolved empirical questions:
```

Fill from files and existing user instructions. Do not require the user to restate already known choices or complete a questionnaire when the baseline supplies them.

## Lessons From The Origin Project

The source project concerned CSRD, manufacturing labor and ESG subgroup tests. Its final ReportingScope table combined a unique-firm pre-shock p25/maximum split, pre-shock environmental/social p75 splits and country-industry post-shock peer labor change. Separate versions explored country ESG, source updates, DID-only, SDID and firm listing stability. Several experiences inform this skill:

- Changes to tie rules can leave N almost unchanged when cutoff values have few ties; inspect the distribution before diagnosing the code.
- A fixed parent column can fail clustered inference even when two child regressions succeed; pooling changes the estimation matrix and singleton removal.
- Reestimating nominally unchanged full-interaction panels can expose numerical problems; use frozen saved estimates for presentation-only changes and diagnose sample/specification instability explicitly.
- A raw-data update needs isolated intermediates as well as a new results folder.
- A figure corresponding to a table column must use the same source and cutoff logic, not a convenient old means/median file.
- Parsing fulltable CSV with a token reader that discards empty cells misaligns headers, coefficients and standard errors.
- Company names require an ID-to-name crosswalk; a long firm ID alone is insufficient for an economically interpretable outlier list.

These are transferable decisions, not a mandate to reproduce the source project's paths, shock year, quantiles, repetitions or assumptions in a different paper.
