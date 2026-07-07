# AAAI-27 审稿模拟 Skill

`aaai2027-review-simulation-repo` 是一个用于 **AAAI-27 风格论文审稿模拟** 的 Agent Skill。它面向 AI 会议论文的投稿前评估、红队审稿、回复审稿意见准备和修改计划制定。

它生成的是**模拟审稿结果**，不是 AAAI 官方审稿，也不代表实际录用概率。

## 它能做什么

给定一篇论文（PDF、LaTeX、DOCX、Markdown 或纯文本），Skill 会以多个独立角色模拟审稿，并输出：

- 论文证据地图：任务、创新点、方法闭环、假设、实验协议与证据缺口；
- 多位独立模拟审稿人意见；
- 综合 Meta-review；
- 主要问题矩阵与严重等级；
- P0 / P1 / P2 优先级修改计划；
- 对 RAG、LLM Agent、因果、迁移学习、具身智能等论文的专项风险检查。

默认完整模式会使用 5 个互相独立的模拟审稿角色：

1. **R1：创新性与相关工作**：检查贡献是否真正区别于相邻工作，论文主张是否可证伪且边界清晰。
2. **R2：技术正确性与可复现性**：检查公式、算法、目标函数、假设、实现闭环和复现细节。
3. **R3：实验严谨性与因果审计**：检查数据切分、泄漏、基线公平性、消融、显著性、oracle 边界与成本核算。
4. **R4：领域专家**：根据论文所属方向调用相应检查清单。
5. **R5：AAAI 通用审稿人 / Senior PC**：评估重要性、清晰度、广泛影响与潜在审稿分歧。

## 输出结构

一次完整审稿通常会生成如下文件：

```text
reviews/<论文文件名>/
├── 00_preflight.md                 # 初步风险扫描
├── 01_evidence_map.md              # 论文证据地图
├── review_r1_novelty.md            # 创新性审稿
├── review_r2_technical.md          # 技术与复现审稿
├── review_r3_experiments.md        # 实验与因果审稿
├── review_r4_domain.md             # 领域专家审稿
├── review_r5_generalist.md         # AAAI 通用审稿
├── meta_review.md                  # 综合意见与模拟结论
├── concerns_matrix.csv             # 问题矩阵
├── revision_plan.md                # P0/P1/P2 修改计划
└── results.json                    # 结构化结果索引
```

## 安装方法

将整个仓库目录复制或软链接到所使用 Agent 的 skills 目录中。

### Claude Code（项目级）

```bash
mkdir -p .claude/skills
cp -R aaai2027-review-simulation-repo .claude/skills/aaai2027-review-simulation-repo
```

### Cursor（项目级）

```bash
mkdir -p .cursor/skills
cp -R aaai2027-review-simulation-repo .cursor/skills/aaai2027-review-simulation-repo
```

安装后，如宿主工具要求，请重新打开或重启 Agent 会话。

## 使用方式

### 完整审稿

```text
Use aaai2027-review-simulation-repo to run a full AAAI-27 review simulation on paper/main.pdf.
Focus on novelty, technical correctness, leakage, baseline fairness, and revision priorities.
```

### 中文请求示例

```text
使用 aaai2027-review-simulation-repo 对 main.pdf 做完整 AAAI-27 模拟审稿。
重点检查创新性、公式闭环、数据泄漏、基线公平性、成本核算和实验严谨性。
请输出中文执行摘要，并保留英文审稿工件。
```

### 审稿回复准备

```text
Use aaai2027-review-simulation-repo in rebuttal mode on main.pdf.
Identify the strongest likely objections, distinguish fixable writing issues from experiment-critical issues, and propose the minimum evidence needed for a rebuttal.
```

### 根据已有审稿意见生成修改计划

```text
Use aaai2027-review-simulation-repo in revision mode on main.tex and these external reviews.
Produce a ranked P0/P1/P2 revision plan with concrete manuscript locations and required experiments.
```

### Camera-ready 检查

```text
Use aaai2027-review-simulation-repo in camera-ready mode on main.pdf and supplement.pdf.
Focus on clarity, reproducibility, claim calibration, figure/table readability, anonymity, and consistency between the main paper and supplement.
```

## 支持的模式

| 模式 | 用途 | 默认输出 |
|---|---|---|
| `fast` | 快速找关键风险 | 证据审计 + 3 位审稿人 + 简短 Meta-review |
| `full` | 投稿前完整模拟审稿 | 5 位审稿人 + Meta-review + 矩阵 + 修改计划 |
| `rebuttal` | 准备回复审稿意见 | 最强质疑、可回应点、最小补充证据 |
| `revision` | 根据外部意见规划修改 | P0/P1/P2 可执行任务列表 |
| `camera-ready` | 终稿检查 | 叙事、复现、图表、匿名与一致性审计 |

## 特别适合检查的问题

### RAG、LLM、Agent 论文

- 测试标签、测试 query、测试文档、测试实体、检索索引或 memory 是否泄漏；
- oracle 是否使用 gold label、gold evidence、未来信息或特权元数据；
- LLM 调用次数、token、延迟、批处理和重试预算是否统一计入；
- 各方法是否使用相同 backbone、解码配置、上下文预算和测试约束；
- 外部迁移是否真正冻结超参数，且无目标任务调参；
- “因果”主张是否定义了干预、估计量、假设与替代解释。

### 时序迁移、因果机制学习论文

- 跨域切分是否完整，是否存在表示或实体泄漏；
- 因果术语是否与所做实验和假设匹配；
- 干预、反事实和学到图结构的解释是否成立；
- 公式、模型输入输出、训练与推理步骤是否闭合。

### 具身智能论文

- 训练/测试场景是否泄漏；
- 性能是否依赖额外特权观测或检索记忆；
- 环境、动作预算、仿真依赖和安全风险是否交代清楚；
- 结果是否能说明真实机器人或跨环境价值。

## 本地预检（可选）

仓库附带一个保守的本地扫描脚本，用于提前标出潜在问题。它只能辅助人工检查，不会认证匿名、格式或 AAAI 合规性。

```bash
python3 scripts/preflight.py paper/main.pdf --out reviews/main/00_preflight.md
python3 scripts/preflight.py paper/main.tex --out reviews/main/00_preflight.md
```

## 使用原则

- **证据优先**：每个主要问题都应落到论文的章节、公式、图、表或明确文字上；没有证据时应标记为“不确定”，而非武断断言。
- **不编造缺失事实**：不能在未检索全文的情况下断言“缺少某个实验”或“没有使用某个基线”。
- **区分论文事实与审稿推断**：明确什么是论文已经报告的，什么是审稿人可能担心的，什么需要补充证据。
- **不为了负面而负面**：每个主要问题都应提供最小可行修复方案。
- **认真审计泄漏与成本**：对 Agent、RAG、迁移学习和因果论文尤其重要。
- **保护匿名性**：不尝试反向识别作者；仅提示可能破坏匿名性的内容，例如致谢、单位、路径、自引表述或可识别仓库链接。

## 评分说明

Skill 中的评分只是为了统一模拟审稿角色之间的表达，**不是 AAAI 官方评分标准**：

| 分数 | 含义 |
|---:|---|
| 8–10 | Strong Accept 倾向：证据充分，核心问题很少 |
| 6–7 | Accept 倾向：贡献可信，剩余问题大多可修复 |
| 5 | Borderline：取决于审稿人组合与关键证据可信度 |
| 3–4 | Reject 倾向：存在中心有效性、创新性或证据问题 |
| 1–2 | Strong Reject 倾向：核心主张缺乏支撑、无效或难以复现 |

## 仓库结构

```text
.
├── SKILL.md                         # Skill 主定义与审稿流程
├── prompts/                         # 证据地图、审稿人、Meta-review 提示模板
├── references/                      # 领域检查清单与结果 JSON schema
├── scripts/preflight.py             # 可选的本地预检脚本
├── examples/example_request.md      # 调用示例
└── README.md                        # 中文说明（本文件）
```

## 许可证

MIT License，详见 [LICENSE](LICENSE)。
