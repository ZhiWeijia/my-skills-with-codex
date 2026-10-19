# my-skills-with-codex

Reusable Codex skills developed from practical research workflows.

从实际研究工作中整理的可复用 Codex skills。

## Skills

| Skill | Description |
| --- | --- |
| [stata-baseline-extensions](stata-baseline-extensions/README.md) | 基于固定 baseline 扩展 Stata 实证检验，涵盖数据与分组核查、DID/SDID、推断、导出、作图和中英文方法说明。 / Audited empirical extensions from a fixed baseline, with reproducible data construction, estimation and exports. |
| [read-accounting-finance-paper](read-accounting-finance-paper/README.md) | English paper analysis with a bilingual abstract, replication-level variable construction, original empirical models, identification evidence, and screenshots of every main-text table. / 英文论文精读，含双语摘要、详细变量构建、原始实证模型、识别证据及正文逐表截图。 |

## Usage

Each skill lives in its own folder with a `SKILL.md` entry point. Read that skill's README for usage, and place the selected skill folder in your personal Codex skills directory.

每个 skill 都放在独立文件夹中，入口是 `SKILL.md`。阅读对应 README，将需要的 skill 子文件夹放入个人 Codex skills 目录后使用。

Example / 示例：

```text
使用 $stata-baseline-extensions，读取本项目 baseline，
完成以下扩展检验，并交付可复现代码、结果和方法说明：……
```

Paper reading / 论文精读：

```text
Use $read-accounting-finance-paper to analyze this uploaded PDF in English,
with the bilingual abstract, original models, detailed variable construction,
and every main-text table.
```

This repository contains reusable instructions and generic examples, not research datasets or fitted empirical results.

本仓库仅包含可复用说明和通用示例，不包含研究数据或已估计的实证结果。
