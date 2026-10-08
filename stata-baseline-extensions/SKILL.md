---
name: stata-baseline-extensions
description: Extend a fixed empirical baseline into subgroup, peer-exposure, alternative-outcome, DID or SDID tests in Stata, with audited data construction, versioned results and reproducible exports. Use when building or diagnosing additional empirical tests from an existing paper's baseline results.
---

# 从固定 Baseline 扩展实证检验

把已有论文的 baseline 变成可核查、可复现的扩展检验。先识别新项目的真实设定，再实现用户要求的变动。工作语言跟随用户；变量名、路径和数学条件保留精确拼写。

## 先建立 Baseline Contract

阅读产生 baseline 的 master、builder、estimator/exporter、最近一次成功 log 和 coverage。表格只能证明展示结果，不能单独证明样本或变量如何生成。

记录以下内容，优先复用已存在的配置或 method note：

- raw input 的版本、ID、merge key、observation unit，以及实际是否唯一。
- Y 的来源、单位、raw/log/比例口径和变换链。
- treated、post、adoption/shock year、pre/post 测量年份和分析窗口。
- main sample、weights、controls、FE、cluster、estimator 与软件版本。
- 每个 partitioner 的来源、时间、层级、cutoff universe、ties、missing 和 coverage。
- builder 依赖、结果列标签与顺序、coef name、推断方法、随机种子和重复次数。

对照用户要求写清这次改变哪些设定、哪些设定固定。基于已有证据能确定的事项直接推进；缺少会改变 estimand 的信息时，只询问关键点并继续独立的核查工作。

如果用户要求“固定旧版、新生成一版”，新建独立 output 和 intermediate namespace；不要覆盖旧结果。其他场景依用户授权更新，不强制每个小改动都复制整套项目。

## 按任务读取参考文件

- raw-data/merge、pre-shock 分组、peer 构造、缺失、退出或 time invariance：读 [data-and-partitioners.md](references/data-and-partitioners.md)。
- DID、bdiff、SDID、SE 异常、异质性解释：读 [estimation-and-inference.md](references/estimation-and-inference.md)。
- master、软件执行、CSV/XLSX 对齐、组合表、图和 correlation：读 [results-and-execution.md](references/results-and-execution.md)。
- standalone 交付、详细中英文 notes 或换项目：读 [documentation-and-handoff.md](references/documentation-and-handoff.md)。

按需要读，不要求每次加载全部文件。这些参考包含项目经验和一般化的核查方法，不授权额外检验。

## 实施流程

1. **核查输入。** 确认数据存在、key 唯一、ID 类型、变量测量时间、duplicate/conflict 和 main-sample missing。先解决异常的 treated/control 数量，再估计。
2. **构造分组。** 在正确的唯一单位和明确的 reference sample 上计算 cutoff；保留 cutoff、metric 和 eligibility 为可审计变量。验证互斥、覆盖、嵌套和 time invariance。
3. **固定可比口径。** 换 Y、过滤 firms 或单纯重新展示时，按约定复用原 cutoff。只有用户要求换 cutoff 或分析单位时重建并记录变化。
4. **估计并记录。** 保留项目的 estimator、weights、controls、FE、cluster；仅实施授权变更。每次 captured estimation 后立即保存 `_rc`；记录成功、失败和不可推断，而不是让上一模型的结果留在新列。
5. **导出再验证。** 先保存结构化的估计结果和 coverage，再按显式 column map 导出。检查 block/column 数、系数与 SE 对齐、bdiff pair 和实际保存路径。
6. **交付。** 说明新结果路径、改变的定义、样本损失和异常。用户要求 standalone 时交付真实 raw-to-results 链、依赖文件及方法说明，并验证这条链。

## 几个不能混淆的口径

- firm-year、firm-country-year 和真正 establishment-year 不同。`firm × country` 聚合数据不能未经说明称为单个 establishment。
- firm-level cutoff 不应重复加权一家公司的多个国家或年份；country cutoff 应按唯一国家计算，并明确 EU 或 worldwide universe。
- pre-shock firm score 与 post-shock peer labor change 的角色不同。后者可能是 shock 的结果，不能仅凭分组回归宣称预先决定的因果异质性或中介效应。
- 原 High、纯 prior-peer subgroup、metric Eligible、最终 PeerLow/PeerHigh 不能只改标签混为一组；coverage 中保留样本漏斗。
- percentile 是样本分位数；p25 不等于数值 `0.25`。`>= / <` 和 `> / <=` 两种 ties 规则都可能合理，严格按授权选择。
- Stata numeric missing 大于任何有限数；`metric > 0`、`peer_n >= 3`、`metric >= cutoff` 等条件须排除 missing。
- missing employment、明确零就业、企业退出、失去数据覆盖、EU delisting 是不同事件。不能悄悄相互替代。
- `_rc == 0` 不等于有效推断；还要检查目标系数是否存在、是否 omitted、SE/VCE、clusters 和估计样本。
- 只改变列顺序、重命名或组合已有表时，直接后处理保存结果；不要重新估计固定的 panel。

## 本项目经验不是新项目默认参数

CSRD 项目曾使用 shock 2023、2017-2025 窗口、T3/T5 peer thresholds、p75 score split、bdiff `reps(20)` 和 SDID bootstrap `reps(100)`。这些只适用于相应已固定版本。

不要把它们、旧路径、EU restriction、RS_High 等于 1 或 `id2` 的含义直接移植到新项目。新项目应读取其 baseline contract。有限重复次数可用于复刻或探索；最终推断要报告精度限制，不能把 20 次得到的 p=0 解释为真实概率为零。

## 跨项目调用示例

“使用 $stata-baseline-extensions，先读取本项目 baseline master 和结果，在保持原样本、weights、FE 和 cluster 的基础上，新增一个 pre-shock score 异质性检验。新版本单独保存；交付 raw-to-results master、变量定义、coverage、CSV/XLSX 和中英文方法说明。”
