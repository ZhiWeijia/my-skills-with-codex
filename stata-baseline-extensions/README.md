# Stata Baseline Extensions

A reusable Codex skill for extending a fixed empirical baseline into additional tests in Stata.

一个用于经济学与金融学实证研究的 Codex skill：基于已有 baseline，构造可审计、可复现的扩展检验。

## What It Covers

- Trace the baseline from raw sources to sample construction, estimation and exports.
- Build pre-treatment measures, unique-unit cutoffs and explicit tie rules.
- Audit merges, missing outcomes, peer coverage, employment decline and exit definitions.
- Extend subgroup and peer-exposure tests while documenting which settings stay fixed.
- Run or diagnose DID, coefficient-difference tests and SDID.
- Preserve result-column alignment, combine frozen tables and produce same-source figures.
- Deliver standalone workflows and Chinese/English empirical method notes.

The skill contains instructions and worked patterns, not a ready-made estimator or a dataset. Project-specific paths, treatment timing, outcome definitions, cutoffs, weights and inference settings must be resolved from the target project's baseline.

## 使用方式 / Usage

将本仓库中的 `stata-baseline-extensions/` 子文件夹放入个人 Codex skills 目录，并确保 `SKILL.md` 位于该 skill 文件夹根目录。在能识别此 skill 的会话中调用：

Place this repository's `stata-baseline-extensions/` subfolder in your personal Codex skills directory, with `SKILL.md` at the skill folder root. Invoke it in a session where the skill is available:

```text
使用 $stata-baseline-extensions，读取本项目 baseline master 和结果，
新增以下扩展检验：……
请说明固定与变化的设定，核查分组和 missing，
并交付可复现代码、coverage、结果和中英文方法说明。
```

```text
Use $stata-baseline-extensions to inspect this project's baseline and
implement the following empirical extension: ...
Document fixed and changed settings, audit samples and missing data,
and deliver reproducible code, coverage, results and method notes.
```

## Files

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Entry point, scope and workflow |
| [agents/openai.yaml](agents/openai.yaml) | Skill display metadata and example invocation |
| [Data and partitioners](references/data-and-partitioners.md) | IDs, merges, timing, cutoffs, peers, missing, exits and invariance |
| [Estimation and inference](references/estimation-and-inference.md) | DID, bdiff, numerical diagnostics and SDID |
| [Results and execution](references/results-and-execution.md) | Stata/Windows runs, tables, CSV/XLSX, figures and correlations |
| [Documentation and handoff](references/documentation-and-handoff.md) | Raw-to-results delivery and bilingual academic notes |

## Design Principles

本 skill 先读取目标项目的 baseline，再决定分析单位、时点、cutoff、样本及估计设定。这里的示例参数不应被直接当作新项目的默认值。缺失、明确零值和退出分别处理；分组、数据层级和推断失败均需可核查。

The workflow treats reproducibility, sample definitions and inference as separate tasks. It preserves requested baseline choices, explicitly documents changes, and distinguishes a presentation change from re-estimation. Numerical success does not by itself establish valid inference or causal identification.

## Software

Use the software available in the target project. Stata is the primary empirical tool; PowerShell, Python/R and Excel may support orchestration, parsing or presentation. Check installed package versions and the project's dependencies before running examples. No licensed software or data is bundled in this repository.

## Data And Privacy

This repository contains reusable instructions and generic examples. It does not contain research datasets, fitted regression results, private identifiers or account credentials. Keep each target project's raw data and empirical outputs in that project's own workspace.
