# AMBER — 琥珀式封存的历史回放评测

`封进琥珀，重做当时的题。`

**一句话**：拿真实发生过的事故和任务，让 AI 模型只用当时手里的信息重做一遍。比如一次真实的运维故障：模型只能拿当时的监控和日志找根因，事后才揭晓的证据一律封存不给看。题目永不公开，但每题有哈希指纹，分数和指纹全部公开，谁都能核对题没被换、分不是编的。

**案集** 24 案 · **规范** v0.2.2（草案） · **哈希索引** [v2026-09](hash-index/v2026-09.md) · **成绩仓** × 13 · **纪律** 只发分数，不发题 · English: [README.en.md](README.en.md)

> ⚠️ **更正**（原文与受影响车道清单见[榜单全文](docs/leaderboard-notes.md)）
> - **[2026-10-02](docs/corrections-2026-10-02.md)**：22 张已发布的考卷在作答时越出考卷、接触了判分材料，改记 NA（不计胜负）。责任在我们；2026-10-01 起已改为隔离容器作答。
> - **[2026-10-02（另一项）](docs/corrections-2026-10-02-a-d511f9e8.md)**：防御轴的一案 A-d511f9e8 在所有车道上改记 NA。分母不变，**过案数不变**，每条道的总分都带 `'`。
> - 更早：[2026-09-18](docs/corrections-2026-09-18.md)（swe-2-low 实为 swe-2-high）· [2026-W38](docs/corrections-2026-W38.md)（全库复核，逐仓特刊）

## 现在谁领先

![当前前五 2026-W40（含 2026-10-02 更正、2026-10-02 考试与 A-d511f9e8 全车道挂起）](docs/images/top5-2026-w40g.png?v=20261003)

| # | 总分 | 模型 @ 端点 |
|---|---|---|
| 1 | 19'/24 | swe-2-max @ Devin<br>claude-sonnet-5-5 @ Anthropic 订阅道<br>claude-opus-5-5 @ Anthropic 订阅道 |
| 2 | 18'/24 | glm-5.3-flash @ Ollama Cloud<br>k3 @ Kimi<br>hy4-preview-f @ WorkBuddy |
| 3 | 17'/24 | gpt-6-sol-900k @ OpenAI Codex<br>swe-2-high @ Devin<br>doubao-seed-evolving @ 火山方舟 |
| 4 | 16'/24 | gpt-5.6-luna-900k（high）@ OpenAI Codex<br>gpt-6-astra-900k @ OpenAI Codex<br>gpt-6.1-sol @ OpenAI Codex<br>claude-fable-5-1 @ Anthropic 订阅道<br>deepseek-v4-flash:0731 @ Ollama Cloud<br>swe-2-medium @ Devin<br>deepseek-v4.1-flash @ Ollama Cloud ▼<br>deepseek-flash @ DeepSeek ▼<br>mimo-v2.6-pro @ CommandCode ▼ |
| 5 | 15'/24 | kimi-for-coding（K2.8）@ Kimi<br>gpt-6-luna-900k @ OpenAI Codex<br>swe-1-7-medium @ Devin<br>Qwen3.8-27B @ GoldenPotato 自部署<br>deepseek-flash @ OpenCode Go ▼<br>step-5-preview @ StepFun ▼ |

`'` = 其中有案暂不计分（NA），不算输；现在每条道都带，因为 A-d511f9e8 在所有车道上暂不计分。同名模型换个端点可能是另一个脑，所以成绩一律按「端点 × 名字」记。claude-opus-5-5 取 W40 重考一场（W39 首考 17'/24）：两场各考一次、考场不同，**不据此判断强弱**，见 [amber-claude W40](https://github.com/getaskclaw/amber-claude/blob/main/results/2026-W40.md)。▼ = 经 2026-10-02 更正下调。各车道出处、脚注、冻结道：[榜单全文](docs/leaderboard-notes.md)。

## 同分不同款

总分相同的车道，强项和短板可以完全不同。点越大、颜色越深，完成度越高；NA = 该轴没有可计分的案，不是零分。

![完成度矩阵：榜上总分 18 以上的 6 条车道，十轴，24 案，2026-10-02](docs/images/completion-matrix-top6-2026-w40.png?v=20261003)

**读法**：动手干活的「施工面」几乎全满，差别在「判断面」。每格 = 该轴全部案子的完成度（0–1）。官方榜 [askclaw.dev](https://askclaw.dev/) 也用这十个轴。

| 面 | 轴 | 考什么 |
|---|---|---|
| 施工面 | 编码 | 照需求把功能写对 |
| | 交付 | 做完要交卷，没产出就是 0 |
| | 运维 | 照规程干脏活，一步不省 |
| | 需求 | 客户要 A 不要 B，交上去得是 A |
| | 收敛 | 真干完，还是绕圈装忙 |
| 判断面 | UI | 照设计稿做页面，像素级验收 |
| | 视觉 | 给真截图挑毛病 |
| | 防御 | 堵死校验器的漏洞，还不误伤好人 |
| | 归因 | 把每条毛病对到正确根因 |
| | 审查 | 给别人的交付物挑错，漏看和冤枉都扣分 |

各轴的详细读法、每条车道的数字：[十个轴与完成度矩阵](docs/axes.md)。

## 它怎么运作

私有题库 + 公开成绩：题目永不公开，分数与哈希永远可查。评分标准在看到任何输出之前就已冻结，全程留档。

![AMBER 是什么](docs/images/what-is-amber.png?v=20260917)

一期成绩像一场考试：出卷封存、净室应考、逐卷验脑、脱敏发布、人人可核对。

![一期成绩怎么炼成](docs/images/trust-chain.png?v=20260915b)

另有三个发现（思考档位、token 账单、耗时与分数的关系）：[docs/findings-effort-and-speed.md](docs/findings-effort-and-speed.md)。

## 成绩仓

成绩与题目分开发布：结果公开，题目永不公开。别名 + bundle 哈希逐案对照本仓的公开哈希索引。

[amber-claude](https://github.com/getaskclaw/amber-claude)（Claude）· [amber-gpt](https://github.com/getaskclaw/amber-gpt)（GPT）· [amber-devin](https://github.com/getaskclaw/amber-devin)（Devin）· [amber-kimi](https://github.com/getaskclaw/amber-kimi)（Kimi）· [amber-deepseek](https://github.com/getaskclaw/amber-deepseek)（DeepSeek）· [amber-ollama](https://github.com/getaskclaw/amber-ollama)（Ollama Cloud）· [amber-opencode](https://github.com/getaskclaw/amber-opencode)（OpenCode Go）· [amber-commandcode](https://github.com/getaskclaw/amber-commandcode)（CommandCode）· [amber-workbuddy](https://github.com/getaskclaw/amber-workbuddy)（WorkBuddy）· [amber-doubao](https://github.com/getaskclaw/amber-doubao)（豆包）· [amber-stepfun](https://github.com/getaskclaw/amber-stepfun)（阶跃星辰）· [amber-nous](https://github.com/getaskclaw/amber-nous)（Nous Portal）· [amber-goldenpotato](https://github.com/getaskclaw/amber-goldenpotato)（社区自部署 Qwen3.8-27B）

## 常见问题

**题目不公开，凭什么信分数？** 靠可验证的过程：净室考场、逐卷验脑（替身 = 整卷作废）、收卷闸、别名 + 哈希公开、harness 版本每期钉死（现役 [Hermes](https://github.com/NousResearch/hermes-agent)）。考场条件的变更逐条公开，最近一次：[方法变更 2026-10-01](docs/method-change-2026-10-01.md)。

**为什么不公开题目？** 公开题库会被训练数据吃掉，分数通胀、无法审计。题目私有，泄漏状态才可核查。

**两个模型的分能直接比吗？** 只在同档、同题集版本、尽量同日时可比。跨周对比必须带日期和档位。

**能复现或加入吗？** 目前不能：仅凭公仓还跑不通一次合规运行（见 [PLAN.md](PLAN.md)）。追结果请订阅成绩仓；方法论问题欢迎开 issue。

## 规范与文档

- [AMBER-Core-Specification.md](AMBER-Core-Specification.md) — 规范本体（English）
- [protocols/distribution.md](protocols/distribution.md) · [protocols/stability.md](protocols/stability.md) — 分发协议、稳定性协议
- [hash-index/v2026-09.md](hash-index/v2026-09.md) — 公开哈希索引（24 案）
- [PLAN.md](PLAN.md) · [CONTRIBUTING.md](CONTRIBUTING.md) — 路线图；贡献规则（**本仓绝不接收案件内容**）
- [docs/](docs/README.md) — 全部文档索引（榜单全文、十个轴、研究笔记、更正声明、案件清单 schema 与校验器）


- **状态**：草案 v0.2.2。Core 规范已稳定；`profiles/` 和建案/运行工具尚未发布。
- **两条绕不开的警告**：① 运行时密封 ≠ 训练数据纯净——我们封存的是运行时证据，模型训练时有没有见过未来，我们证明不了。② 历史结果是证据，不是唯一正解。
- **为什么需要它**：公开基准是静态题库，污染普遍且无法审计，也测不出多步诊断、弃权、拒绝、在不确定中升级。AMBER 回放来源受控的真实事件，与公开基准互补，不取代它们。

## 许可

Apache-2.0 — 见 [LICENSE](LICENSE)。
