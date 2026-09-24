# AMBER — 琥珀式封存的历史回放评测

`封进琥珀，重做当时的题。`

> **30 秒版**：我们把历史上真实发生过的事故/任务封进「琥珀」——现场精确还原到答案揭晓之前，让 AI 模型只用当时人们手里的信息重做一遍。比如：一次真实的运维故障，模型只能拿当时的监控和日志找根因，事后才揭晓得证据一律封存不给看。题目永不公开（防止背题），但每题有哈希指纹，分数和指纹全部公开——谁都能核对题没被换、分不是编的。这个仓放方法规范和公开哈希索引；各家的成绩单在 12 个成绩仓（见下）。English: [README.en.md](README.en.md)

**案集** 24 案 / 27 卷（headline 记分已并入 /24，死道/停道标 ∅ 冻结） · **规范** v0.2.2（草案） · **哈希索引** [v2026-09](hash-index/v2026-09.md) · **成绩仓** × 12 · **纪律** 只发分数，不发题

> ⚠️ **[更正 2026-09-18](docs/corrections-2026-09-18.md)**：已发布的「swe-2-low @ Devin」成绩实为 **swe-2-high**——该模型 id 不存在，服务端静默路由至默认档。榜单 medium 15 < high 16 < max 18 不受影响。
> ⚠️ **[更正 2026-W38](docs/corrections-2026-W38.md)**：全库复核第一波改判与挂起，逐仓特刊见 12 个成绩仓；本仓 docs 筛查文档 4 个观察点只加注、非成绩格。

*English readers: the normative documents are in English — start with [AMBER-Core-Specification.md](AMBER-Core-Specification.md); repo orientation in English: [README.en.md](README.en.md).*

## 这是什么

一种正式的评测方法：取一个**真实、可审计**的历史事件，把现场精确还原到「答案揭晓之前」那一刻。应考者只能拿到当时可得的信息，揭晓后的证据与评分材料全部**物理封存**；诊断、决策、行动、弃权、拒绝、升级，都只能用当时的所知。评分标准在看到任何输出之前就已冻结，全程留档、可审计。

## 三分钟看懂 AMBER（给第一次来的你）

**① 当前榜首** —— **swe-2-max @ Devin，19'/24**（2026-09-21 起收敛轴首案 A-3f2a9cdd 并入记分：swe-2-max ✓ fast 37s；原 23 案口径 18/23，档线 medium 15 < high 16 < max 18）。同名模型换个端点，可能就是另一个脑：成绩一律按「端点 × 名字」记。

![当前前五 2026-W39](docs/images/top5-2026-w39.png?v=corrections-20260924-r2)

**② 完成度画像：同分 ≠ 同款** —— 十轴完成度矩阵（09-21 起九轴升十轴，新增**收敛**轴）七家同场；原 17/23 五家并列在收敛补测后分流：k3 / glm-5.3-flash / v4.1-flash @ Ollama / hy4 四家 18/24，CommandCode 道 owner 令冻结 ∅，同分五种形状（钉级完成度；找茬分拿了负分也照记）。新补的 k3 行一眼读：UI 是空点（交付缺文件那案）、归因低于头部两家、视觉与 glm-5.3-flash 并列最高。09-16 再补 doubao 16/23 行：施工四轴（编码/交付/运维/需求）满格与头部对齐，但 UI/视觉空点、审查仅三分之一——形状是同场最偏科的一条；核验两轴（归因/防御）初扫考墙 ∅，3600s 补考落到真值 0.47/0.50（低分但真实，见 [amber-doubao W38 addendum](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38.md)）；找茬分负分按 0 落点。09-17 再补 gp27b 14/23 行（Qwen3.8-27B @ goldenpotato 社区自部署）：偏科比 doubao 更极端——施工组四轴贴着头部（编码 0.83 / 交付满 / 运维 0.97 / 需求满），审查/视觉/UI 三轴全零，归因/防御落在全场最低档；NVFP4 激进量化在动手面无损，在判断面全灭（[amber-goldenpotato W38](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38.md)）：

![完成度矩阵 五家 17/23 + doubao 16/23 + gp27b 14/23](docs/images/completion-matrix-7way.png?v=20260921c)

**十轴怎么读（白话版）** —— 每格 = 该轴全部案子的完成度（0–1），按钉数折算：

- **编码** · 按菜谱做菜：照着需求把功能写对（6 案均分）
- **交付** · 做完 ≠ 交卷：没产出就是 0，思路再对也没用（1 案）
- **防御** · 保安巡夜：把校验器的漏网口全堵死，还不许误伤好人（2 案均分）
- **归因** · 医生按症状归病灶：每条毛病对到正确根因，张冠李戴扣钉（1 案 15 钉）
- **审查** · 当验收官：给别人的交付物挑错，漏看和冤枉都扣分，可为负（2 案，找茬分）
- **运维** · 照规程干脏活：备份、切换、对账，一步不省（6 案均分）
- **需求** · 客户说要 A 不要 B，交上去的得是 A（1 案）
- **UI** · 照设计稿做页面，像素级验收（1 案 12 钉）
- **视觉** · 给真截图挑毛病：元素重叠、画面裁切、缺图例——考它真看见了什么（1 案，找茬分）
- **收敛** · 真干完还是绕圈装忙：活落没落袋、多快落袋、有没有原地打转刷临时文件（1 案；2026-09-21 入轴，已考车道全员通过，空白格 = 该道未考不是零分）

轴随题库长：每进一族新案，矩阵就可能多一列——到时候照这张单子加一行。

十轴各自的榜首是谁？复算 40 条已发布车道：[九轴榜首 2026-09-18](docs/nine-axis-top3-2026-09-18.md)（成文于收敛轴入册前，覆盖前九轴）——只有防御/归因/审查/视觉四轴排得出名次，四个冠军分属四家厂商，总分榜首一面没赢；收敛轴已考车道全员满分并列，区分度等后续案。

**③ 它是什么** —— 私有题库 + 公开成绩：题目永不公开，分数与哈希永远可查。

![AMBER 是什么](docs/images/what-is-amber.png?v=20260917)

**④ 一期成绩怎么炼成** —— 像一场考试：出卷封存、净室应考、逐卷验脑、脱敏发布、人人可核对。

![一期成绩怎么炼成](docs/images/trust-chain.png?v=20260915b)

**⑤ 一个反直觉发现，但有边界** —— 已测家族里「想更久 ≠ 考更好」：high 档是甜点，顶档反噬（图中四家族其三）。是经验规律，不是定律：swe-2 的档线单调到底（medium 15 < high 16 < max 18，见 [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md)）；k3 是平线家族（low 15 ≈ high 17，差 2 案其一为骑线案抖动，token/墙钟约为 high 一半——选档按成本和速度，见 [amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)）；也有的模型全档随机带，选档按成本和速度，不按分；WorkBuddy 道、Kimi 的 K2.8、以及 stepfun plan 道目前都只考了一档，尚无曲线可画（stepfun 端点 usage 不返回 `reasoning_tokens`，声明 high 而燃烧量不可验）。

![effort 曲线](docs/images/effort-curves-20260911.png?v=20260917)

**⑥ 分数 × 思考预算** —— 同 high 档、同全库，输出 token 账单跨 17 倍（147K vs 2.5M），分数却差不过一案（各道 token 数出自其期文）。横轴是 token 不是美元：各家计费混杂（订阅道没有边际价；devin 与 workbuddy 道都不上报用量，swe-2 与 wb 双模不上这张图）。家族内部，更多 token 没换来分（luna 平线、astra 顶档反噬）；家族之间形状各异——所以 ⑤ 只是经验规律。

![分数 × 思考预算 W37](docs/images/score-vs-tokens-2026-w37.png?v=20260918)

**⑦ 高 TPS 只在简单题上成立** —— 同一题库、逐题耗时（log 轴）：厂商的高 TPS 是简单题上的吐字速度，难题想得多，吐字当场变慢，耗时跟着翻倍。点=一题，横线=中位数；题号匿名（编号对照留私域，逐点数据见 [wallclock-2026-w37.csv](docs/data/wallclock-2026-w37.csv)）。已测家族里，swe-2 档越高越慢但破题越多（medium 82s → max 280s，中位数）；v4.1-flash 顶档反噬（中位 68s 反掉两案）。形状因家族而异——这只是已测家族的样子，不是定律。

![高 TPS 只在简单题上成立 W37](docs/images/wallclock-strip-2026-w37.png?v=20260911)

图的源文件（PlantUML 的 `.puml`、Vega 的 `.vega-lite.json` / `.vg.json`）就放在 PNG 同目录，改图 = 改源文件再渲染。

## 为什么需要它

公开基准是静态的公开题库：训练污染普遍且无法审计，分数持续通胀；静态问答也测不出真实工作要求的能力——多步诊断、弃权、拒绝、在不确定中升级。AMBER 回放**来源受控**的真实事件，泄漏状态可核查。它和公开基准互补，不取代它们。

## 两条绕不开的警告

- **运行时密封 ≠ 训练数据纯净**：我们封存的是运行时证据；模型训练时有没有见过未来，我们证明不了。
- **历史结果是证据，不是唯一正解**。

## 状态

草案 v0.2.2。Core 规范已稳定；`profiles/` 和建案/运行工具**尚未发布**，目前仅凭本仓库无法执行一次合规运行。路线图与里程碑见 [PLAN.md](PLAN.md)。

`schemas/` 已起步：案件清单的 JSON Schema、校验器，以及 Core §9.3 要求的 SHRE→AMBER 标识映射表（见下节）。

## 案件清单 schema 与校验器

案件清单（Case Manifest）是控制面记录，属私域、永不进考生视野（Distribution §1、Core §2）。字段集**全部取自协议原文**：`protocols/distribution.md` §3（provenance、`cutoff_utc`、解析后的 cutoff commit、time-to-topology 映射规则及其证据类、预注册 cutoff 规则及其脚本输出哈希、`spec_sha256`、两件产物的 sha256、声明的 `candidate_input_bundle`、available-information manifest、资格判定及其证据类、生产者身份与签名密钥标识、泄漏检查程序/上次运行日/结果、退役状态、本协议文档的 sha256），§3.1（构造参数：git 版本、bundle 格式版本、哈希算法、bundle 大小），§3.2、§5.1、§5.2。**没有自造字段。**

- [schemas/manifest.schema.json](schemas/manifest.schema.json) — 清单的 JSON Schema（2020-12）；顶层与各字段块均封闭（`additionalProperties: false`），多一个协议未列举的字段即报错。
- [tools/validate_manifest.py](tools/validate_manifest.py) — 校验器。校验清单是否符合 schema，并额外拒绝任何越出 Distribution §5.1 闭集字段的**脱敏摘要**。
- [schemas/shre-amber-mapping.md](schemas/shre-amber-mapping.md) — Core §9.3 要求的 `shre`↔`amber` 标识映射表，无法从公开材料映射的项标 TBD 并注明缺什么。
- [schemas/examples/](schemas/examples/) — 回归样例：1 个合法清单 + 3 个畸形清单（缺必填字段 / 字段类型与枚举错 / 多出闭集外字段）+ 1 个带越界字段的脱敏摘要。

用法（YAML 与 JSON 都吃）：

```bash
python3 tools/validate_manifest.py schemas/examples/manifest.valid.yaml        # 过，退出码 0
python3 tools/validate_manifest.py schemas/examples/manifest.wrong-types.yaml  # 不过，退出码 1 + stderr 指出违规字段
python3 tools/validate_manifest.py schemas/examples/summary.invalid-fieldset.yaml   # 脱敏摘要越界字段
```

退出码：**0** 合规；**1** 不合规（schema / 闭集 / 跨字段违规）；**2** 无法读取或解析、类型无法判定、schema 载入失败。JSON 输入零依赖；YAML 在装有 PyYAML 时走 PyYAML，否则退回自带的保守解析器（遇到锚点/别名/折叠标量等它看不懂的结构会明确报错，不猜）。装 PyYAML：`python3 -m pip install pyyaml` 或 `uv run --with pyyaml python3 tools/validate_manifest.py <file>`。

## 内容

- [AMBER-Core-Specification.md](AMBER-Core-Specification.md) — 规范本体：目的、定义、机制、8 条不变量、8 条边界、认识论限制、命名评审、采用规则
- [protocols/distribution.md](protocols/distribution.md) — 案件跨主机分发协议（v0.3）：公开/私有频道划分、固定构造的 git bundle、分离式签名清单、公开索引、密封探针、泄漏窗口的裁定规则、运行记录、可比性与验证矩阵
- [protocols/stability.md](protocols/stability.md) — 稳定性协议草案（v0.1）：同臂复跑、失败后恢复率、副作用计数、基建废卷分列、样本量按决策反推
- [docs/instability-memo-2026-09-14.md](docs/instability-memo-2026-09-14.md) — $0 历史漂移证据 memo：900 个已发布矩阵格、31 个规范臂（转载列已标记），证明「分数快照 ≠ 稳定性」
- [docs/stage0-flip-analysis-2026-09-14.md](docs/stage0-flip-analysis-2026-09-14.md) — stage-0 翻转清单：17 条漂移/恢复事件（矩阵派生 + 散文标注），含 stage-1 筛查候选
- [docs/stage1-v001-screen-20260915.md](docs/stage1-v001-screen-20260915.md) — 首个设计型稳定性数据：`A-ea80d793` × `glm-5.3-flash@ollama` n=20 同臂复跑，8/20 过（~40%，判决纪律 20/20 稳定）——边界格案例须报分数分布而非二元翻转
- [docs/stage1-reqdrift-screen-20260915.md](docs/stage1-reqdrift-screen-20260915.md) — `A-0676097b` × `luna-high` n=5 复跑：3/5 过，回归在同一坐席复现两次且同为两个变体（变体名留私域）——升级分类边界案；协议新增多变体逐变体向量与 no-deliverable 分列
- [docs/stage1-sfail-screen-20260915.md](docs/stage1-sfail-screen-20260915.md) — 稳定挂科集 6 案 × `glm-5.3-flash@ollama` n=5 筛查：5 案零复活保住标签（A-87c472cb/A-d511f9e8 钉分纹丝不动），**A-d9b79b46 三过一挂标签被撕**（stage-2 n=20 已收：合计 6/20 过≈30%，Wilson [14.5%, 51.9%]——n=5 的 75% 过率是虚高，筛查档只有二元结论可信）；A-a317e74b 需 3600s 帽才能完卷——协议补逐案超时表与撞 billing 即停
- [docs/nine-axis-top3-2026-09-18.md](docs/nine-axis-top3-2026-09-18.md) — 九轴榜首（40 车道复算，成文于收敛轴入册前）：只有防御/归因/审查/视觉四轴有区分度，四个冠军分属四家厂商；其余五轴头部饱和并列
- [hash-index/v2026-09.md](hash-index/v2026-09.md) — 公开哈希索引：当前题集（24 案，含收敛轴首案）每案的别名 + bundle/oracle 双哈希；结果仓每期矩阵以此为准对照
- [schemas/manifest.schema.json](schemas/manifest.schema.json) · [tools/validate_manifest.py](tools/validate_manifest.py) · [schemas/shre-amber-mapping.md](schemas/shre-amber-mapping.md) — 案件清单 JSON Schema、校验器（含 Distribution §5.1 闭集脱敏摘要校验）、SHRE→AMBER 标识映射表
- [PLAN.md](PLAN.md) — 状态、里程碑（建案工具 → 参考运行器 → 评分与裁判 → 统计 → 公开索引）、待决设计问题
- [CONTRIBUTING.md](CONTRIBUTING.md) — 贡献规则：**本仓库绝不接收案件内容**、规范文档的版本与修订政策、Core 规范按字节哈希锁定的含义

## 周测成绩（结果仓库）

成绩与题目分开发布：结果公开，题目永不公开。以下仓库按周发布全库实测（别名 + bundle 哈希逐案对照本仓[公开哈希索引](hash-index/v2026-09.md)）：

- [amber-crof](https://github.com/getaskclaw/amber-crof) — CrofAI 在售模型周测
- [amber-commandcode](https://github.com/getaskclaw/amber-commandcode) — CommandCode 模型周测
- [amber-deepseek](https://github.com/getaskclaw/amber-deepseek) — DeepSeek 官方 API 模型周测
- [amber-devin](https://github.com/getaskclaw/amber-devin) — Devin 模型周测
- [amber-doubao](https://github.com/getaskclaw/amber-doubao) — 火山方舟 Agent Plan 豆包系模型实测
- [amber-kimi](https://github.com/getaskclaw/amber-kimi) — Kimi 官方 coding 端点模型周测
- [amber-ollama](https://github.com/getaskclaw/amber-ollama) — Ollama Cloud 模型周测
- [amber-opencode](https://github.com/getaskclaw/amber-opencode) — OpenCode Go 模型周测
- [amber-gpt](https://github.com/getaskclaw/amber-gpt) — GPT 系模型 × 推理档位周测
- [amber-workbuddy](https://github.com/getaskclaw/amber-workbuddy) — WorkBuddy（CodeBuddy）ACP 通道模型周测
- [amber-stepfun](https://github.com/getaskclaw/amber-stepfun) — StepFun 阶跃星辰 stepfun plan 端点模型实测
- [amber-claude](https://github.com/getaskclaw/amber-claude) — Anthropic Claude 订阅道模型实测

**当前前五**（源榜截至 2026-09-23，本期 24 案¹；收敛轴首案 A-3f2a9cdd 并入 headline；案 = 一道独立计分任务；∅ = 收敛未考／冻结道；' = contested（安全拒答挂起）或 invalid（基建相关（考场 harness 或判分环境）的挂起、作废或待重评），均不计胜负；所有含 NA 的道都带撇号，包括冻结展示行；挂起不表示死因已定）：

| # | 模型 @ 端点 | 通过 | 出处 |
|---|---|---|---|
| 1 | swe-2-max @ Devin | 19'/24 | [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md) |
| 2 | glm-5.3-flash @ Ollama Cloud | 18/24 | [amber-ollama W37](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W37.md)（并列 18/24：deepseek-v4.1-flash @ Ollama Cloud，[amber-ollama W37 Addendum 09-11](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W37.md)；k3 @ Kimi 官方 coding 端点，[amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)；hy4-preview-f @ WorkBuddy（429 冷却后再考通过，[amber-workbuddy W37](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W37.md)）。收敛未考冻结 17/23∅：deepseek-v4.1-flash @ CommandCode（owner 令冻结，[amber-commandcode W37](https://github.com/getaskclaw/amber-commandcode/blob/main/results/2026-W37.md)）） |
| 3 | deepseek-flash @ DeepSeek 官方 | 17/24 | [amber-deepseek W37](https://github.com/getaskclaw/amber-deepseek/blob/main/results/2026-W37.md)（并列 17/24：deepseek-flash @ OpenCode Go，[amber-opencode W37](https://github.com/getaskclaw/amber-opencode/blob/main/results/2026-W37.md)；swe-2-high @ Devin，[amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md)；doubao-seed-evolving @ 火山方舟 Agent Plan（17'/24，3 NA），[amber-doubao W38](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38.md)；claude-opus-5-5 @ Anthropic 订阅道（17'/24²，模型发布日当日全库首考，[amber-claude W39](https://github.com/getaskclaw/amber-claude/blob/main/results/2026-W39-correction.md)）；**gpt-6-sol-900k @ OpenAI Codex**（17/24 干净无挂起，6 系首发次日全库首考，[amber-gpt W39](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W39.md)）；**mimo-v2.6-pro @ CommandCode**（17'/24³，1 案 invalid 挂起待重评，[amber-commandcode W39](https://github.com/getaskclaw/amber-commandcode/blob/main/results/2026-W39.md)）。冻结 16/23∅：qwen3.8-27b @ CrofAI（CrofAI 道停用，[amber-crof W37](https://github.com/getaskclaw/amber-crof/blob/main/results/2026-W37.md)）） |
| 4 | gpt-5.6-luna-900k @ OpenAI Codex (high) | 16'/24³ | [amber-gpt W37³](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38-correction-luna-high.md)（并列 16/24：**gpt-6-astra-900k @ OpenAI Codex**（[2026-09-21 更正](docs/corrections-2026-09-21.md)：W36 UI 案三格系 fallback 替身交付，16/23→15/23，+收敛 1 案；全库复核见 [amber-gpt W38 Addendum 5](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38.md)；**2026-09-23 同日全库新跑复核 16/24 一致**，双跑对过挂集合零翻转，见 [amber-gpt W39](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W39.md)）；deepseek-v4-flash:0731 @ Ollama Cloud，[amber-ollama W37](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W37.md)；swe-2-medium @ Devin，[amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md)；deepseek-v4.1-flash @ WorkBuddy，[amber-workbuddy W37](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W37.md)；step-5-preview @ stepfun plan 端点（16'/24¹，4 挂起格），[amber-stepfun W38¹](https://github.com/getaskclaw/amber-stepfun/blob/main/results/2026-W38-correction-20260923.md)。冻结/暂停 15'/23∅：gpt-5.6-sol-900k @ OpenAI Codex（3 NA；owner 令暂停）。其它冻结 15/23∅ 道：deepseek-v4-flash-0731 @ CrofAI（CrofAI 道停用）；swe-2-low @ Devin（[2026-09-18 更正](docs/corrections-2026-09-18.md)：swe-2-low 不存在，该轮实为 swe-2-high 二跑，收敛轴不单独补测）） |
| 5 | kimi-for-coding（K2.8 Preview）@ Kimi 官方 coding 端点 | 15/24 | [amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)（并列 15/24：**gpt-6-luna-900k @ OpenAI Codex**（6 系首发次日全库首考，[amber-gpt W39](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W39.md)）；swe-1-7-medium @ Devin，[amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md)；Qwen3.8-27B @ goldenpotato 社区自部署端点，[amber-goldenpotato W38](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38.md)。冻结 14/23∅：glm-5.3-flash @ CrofAI（CrofAI 道停用）；deepseek-v4.1-flash-exp（预览）@ DeepSeek 官方（该 id 已从官方端点下架，owner 令冻结，[amber-deepseek W37](https://github.com/getaskclaw/amber-deepseek/blob/main/results/2026-W37.md)）） |

暂未参评：Fable 等模型因 token 考费不足，本期未送上考场；考费到位即补考，成绩随期发布。（kimi-k3 已于 2026-09-15 首考入榜，见上表 #2 并列。）

¹ 2026-09-08 起，榜单口径从 21 案公共子集切换为全库 23 案：CrofAI / Ollama / astra 三条道已补考 09-07 新增的 2 个运维案（12/12 卷验脑 + bundle 哈希全绿）。astra 的 16/23 = W36 -900k 的 14 案 + W37 裸 gpt-6-astra 补考 2 案（-900k 变体已被服务端收回，口径混合已在期文中标注）。2026-09-10 新增：DeepSeek V4.1-Flash GA 当日三车道对拍——CommandCode / OpenCode Go 两条转发道与 DeepSeek 官方道，同日同档全库（各 26/26 卷验脑全绿；CommandCode 17/23 进入 #2 并列，OpenCode Go 与官方道 16/23 进入 #3 并列，成绩仓见上表）。2026-09-11 新增：deepseek-v4.1-flash @ Ollama Cloud 首考 17/23 入 #2 并列（同日复测 glm-5.3-flash 16/23，落在已知抖动带内；amber-ollama W37 Addendum）；swe-2-max @ Devin 18/23（公共 21 案子集 16/21）登顶——档线 medium 15 < high 16 < max 18 单调到底、OPS 面 6/6 全清（道内唯一；全场非首——gpt luna 与 ollama g53f 更早），墙钟约 5 小时 ≈ 前任榜首的 4 倍（25/25 会话行验脑、哈希 26/26 对公开索引）；swe-2-high 16/23 入 #3 并列。Devin 道 harness 不转发 effort，真实档 = UID 后缀；该道不上报 token 用量。跌出 / 未入：glm-5.3-flash @ CrofAI 14/23（原 #3 并列）、devin swe-1-7-medium 14/23、deepseek-v4.1-flash-exp（预览，官方道）14/23、gpt-5.6-sol-900k 15/23（2026-09-16 重测修正：UI 案原「零交付」实为 harness 客户端看门狗按提示文本量选档误杀静默推理中的健康请求，放宽补考真交付 12/12 满分；对拍旧跑零能力回退，详见 amber-gpt W38；上游 hermes-agent#112909）、gpt-5.6-luna-900k 15/23、deepseek-v4-flash-0731 @ CrofAI 15/23、deepseek-v4-flash:0731 @ Ollama Cloud 15/23（原 #3 并列）、swe-2-medium 15/23（视觉案 4.0 史上最高）、swe-2-low 15/23（[2026-09-18 更正](docs/corrections-2026-09-18.md)：swe-2-low 是不存在的 id，该轮服务端静默落默认档，实为 swe-2-high 二跑——与 09-10 首跑 16/23 是同模型两轮方差，非档位差异；画像与 medium 不同仍属实：保住 A-442d4aab 7/7 与 A-a317e74b 7/15 两个重判断案，丢运维考古案；2026-09-12 Addendum，26/26 验脑、23/23 哈希对公开索引）、deepseek-v4.1-flash @ WorkBuddy 15/23（见下）。2026-09-12 补：gpt-5.6-luna-900k 第三遍 high 15/23（挂科名单跨日 ±2 漂移，前三构成不变；sol 应 owner 要求暂停，9/26 未记分——该车道 09-16 已一次性全库新跑完成，15/23 零回退）。 2026-09-13 新增：WorkBuddy ACP 通道 W37 首考双模型——hy4-preview-f 17/23 入 #2 并列（OPS 6/6 全清、A-d9b79b46 12/12 满分；A-a317e74b 主跑撞 1800s 帽、3600s 帽补考 14/15 并列该案已发布第二高分，唯一过案为 crof q38 的 15/15）；deepseek-v4.1-flash 15/23 未入前三，但交出 A-be92627f 9/9——该案史上首个过案、核验面第二席（此前 15+ 条已发布成绩无一过案，最高 8/9；核验面首破为 crof q38 的 A-a317e74b 15/15）。验脑：82/82 usage 行全在钉住车道，A-ea80d793 两卷走 direct-acp 旁路（manifest 标注 `runner`）；23/23 哈希对公开索引。车道特性：token 用量不回传、effort 经 ACP set_config_option 侧通道钉入、原生工具面为 bypassPermissions。hy3 应 owner 要求中止，未记分。2026-09-15 新增：k3 @ Kimi 官方 coding 端点首考 17/23（公共 21 案子集 15/21）入 #2 并列——编码面 5/6（硬区分器 A-442d4aab 7/7 与 A-569dbe0d 10/10 双满分）、OPS 面 6/6 全清、视觉骑线案 A-ea80d793 3.0 过线；核验面 0/3、A-d9b79b46 交付缺文件、A-cdc3d11a -2。26/26 会话行核验 (k3, kimi-coding) 零替身、23/23 哈希对公开索引；26 卷墙钟 sum 约 2.8 小时（[amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)）。2026-09-15 补：k3 同日 low 档 15/23——档线判平（挂科集与 high 仅差 2 案，其一为视觉骑线案压线抖动，token/墙钟均约为 high 一半）；k3 由此归入「平线家族」，选档按成本与速度不按分（[amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)「档线复测」节）。2026-09-16 新增：doubao-seed-evolving @ 火山方舟 Agent Plan 首考 16/23 入 #3 并列——官方公告该通道与 Doubao-Seed-2.1-pro-0915 同版（套餐目录无版本锁定 ID，官方套餐文档实证）；形态极端分裂：施工/文本/运维/需求漂移 15 案细目分 92/94（97.9%）、hard 区分器 A-442d4aab 满分 7/7，审查/视觉/前端三案净 −2，核验系三案全部考墙零交付（3600s 大帽补考结果见其成绩仓 addendum）；reasoning tokens 占输出 65%、均卷墙钟 557s 约为同档 GPT 道 2 倍；23/23 会话行验脑钉 (doubao-seed-evolving, …/api/plan/v3) 零替身、0/26 哈希不符（[amber-doubao W38](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38.md)）。2026-09-17 新增：kimi-for-coding（K2.8 Preview，09-11 起该 ID 静默换脑）@ Kimi 官方 coding 端点首考 14/23（公共子集 12/21）未入前三——编码 / 文本 / 需求漂移三面与 k3 逐卷同分、墙钟快 27%，防御校验案 A-be92627f 7/9 反超 k3 的 4/9；但对抗审查案 A-cdc3d11a 拿 -17（k3 为 -2，幻觉洪水级，全场历史最差带），审查面判不可用；与 k3 的 3 案差全在已知抖动 / 骑线案带。26/26 卷验脑（净室 profile，零 fallback 替身）、26/26 哈希对公开索引（[amber-kimi W38 Addendum 09-17](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)）。2026-09-17 补：gpt-5.6-luna-900k max 档首考 16/23——+1 案为 UI 案 A-d9b79b46 的 12/12 首交付（luna 成该案第五个满分已发布车道），但与 09-16 harness 看门狗修复同日混杂、任何档位重跑都会交付，剔除混杂后 15/23 与 high 打平，headline 15/23 不变（格级修正欠一次同档重测）；视觉案 A-ea80d793 拿 5.0 刷该案已发布历史最高（原纪录 swe-2-medium 4.0），归因案 A-a317e74b 14/15→7/15 顶档反噬再现（[amber-gpt W38 Addendum 4](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38.md)）。2026-09-17 新增：榜单展示从前三扩为前五——#4（15/23，七条并列道）与 #5（14/23，五条并列道）首次上表上图。同日新增：Qwen3.8-27B @ goldenpotato 社区自部署端点首考 14/23 入 #5 并列——个人玩家 3×V100 32G 魔改 vLLM TP3 跑 NVIDIA 官方 NVFP4 权重（KV cache FP8）；施工面 5/6 含 hard 区分器 A-442d4aab 满分 7/7，判断面（审查/核验/视觉/前端）零案通过；effort 旋钮实证无效（57 条用量记录 reasoning_tokens 全 0，按端点默认档记账）；端点为限时压测（公告称约一天），此行属一次性快照、不可复测；26/26 卷验脑钉 (Qwen3.8-27B, custom, 27b.goldenpotato.cn) 零替身、0/26 哈希不符（[amber-goldenpotato W38](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38.md)）。2026-09-20 新增：step-5-preview @ stepfun plan 端点首考 15/23（公共 21 案子集 13/21）入 #4 并列——StepFun 阶跃星辰新旗舰（600B/27B MoE，官宣 1M 上下文 + 视觉）在官方 plan 端点（OpenAI 兼容面）首考全库；施工面顶级：运维 6/6 全清、需求漂移四变体全过、编码 5/6（含全库唯一硬区分器 A-442d4aab 7/7 满分）、交付满分；判断面掉队：**归因轴 0.800 反超对照锚 k3 的 0.667**（同一案 12/15 对 10/15），但核验 0/3、审查净 −2、视觉 −2、前端废卷。三条口径随行：① 端点 usage 不返回 `reasoning_tokens`（72 行用量记录该字段全 0/缺失），「high」仅为请求标签，行按端点默认档记；② 视觉面发车前在本端点零字节挂死（同端点另一模型同图正常答对），该案先判 not run（非失败），端点复测恢复后单案补考取真值 d2 = −2；③ 核验三案主跑撞标准帽后放大帽收敛（7200→4326s / 10800→5353s / 3600s），全卷墙钟约 5.9 小时为较重成本。26/26 卷 bundle 哈希对公开索引一致；72/72 用量行钉 (step-5-preview, stepfun) 零替身（[amber-stepfun W39](https://github.com/getaskclaw/amber-stepfun/blob/main/results/2026-W39.md)）。2026-09-21 新增：收敛轴首案 A-3f2a9cdd 入册，题库 24 案；同日晚 owner 批 headline 并入 /24——25 条上榜道中 17 条活道全数补考且全过（fast~medium、零绕圈），hy4@WorkBuddy 429 五连后 11:18 UTC 复测通过（fast 51s）入 18/24，d41f@CommandCode 由 owner 令冻结 ∅（17/23 封存），6 条死道/停道标 ∅ 冻结（CrofAI ×3、ds-v4.1-exp 官方下架、sol 暂停、swe-2-low 假 id；同日晚 CommandCode 道亦由 owner 令冻结），完成度矩阵九轴升十轴。**2026-09-21 更正**：astra W36 的 A-d9b79b46 low/medium/high 三格经账本复核系 fallback 替身（glm-5.3-flash @ Ollama Cloud）交付，作废——astra headline 16/23→**15/23**，移出 #3 列入 #4 并列；三档四跑干净实测全灭（格式围栏缺失，非看门狗），详见[更正声明](docs/corrections-2026-09-21.md)与 [amber-gpt W38 Addendum 5](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38.md)（含 09-20/21 medium 档全库 28 跑复核：其余各案与基线逐钉一致）。2026-09-23 新增：claude-opus-5-5 @ Anthropic 订阅道（OAuth，订阅配额道无单价表、不报美元成本）首考 **17'/24²** 入 #3 并列——09-22 模型发布日当日全库首考，计分窗约 50 分钟排完 27 卷；施工 5/6 含硬区分器 A-442d4aab 满分 7/7，UI 搭建案 A-d9b79b46 满分 12/12，需求漂移 4/4 全绿，视觉案 A-ea80d793 4/5 hits 零误报；短板如实：核验 0/3（含 A-be92627f 无交付真负）、审查案 A-cdc3d11a 结论判对但 22 条意见 18 条误报砸到 -17、归因钉 A-a317e74b 7/15。验脑：30/30 考场会话钉 (claude-opus-5-5, Anthropic 订阅道) 零替身、零限流、全部正常收场（截尾法医 0 冤案）；2 案共 3 次首考尝试因案级基建问题作废、修复后重考、废卷从未计分；bundle 哈希随期文逐卷公开、对照 hash-index（[amber-claude W39](https://github.com/getaskclaw/amber-claude/blob/main/results/2026-W39.md)）。2026-09-23 新增（二）：OpenAI 6 系首发次日全库首考三连——**gpt-6-sol-900k 17/24 入 #3 并列**（24 案零挂起；归因轴 0.93 接近榜首带、视觉轴 1.0 未过线为短板）、**gpt-6-luna-900k 15/24 入 #5 并列**（5.6 时代「luna ≥ sol」家族规律在 6 系翻转）、gpt-6-astra-900k 同日双跑复核 16/24 与既有榜值一致（过挂集合零翻转，复现性实据）；验脑闸本轮起焊死进 harness（声明脑 ≠ 考场脑即拒跑）；54 卷账本钉 gpt-6-sol/luna-900k 零替身，bundle 哈希对公开索引（[amber-gpt W39](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W39.md)）。同日新增：**mimo-v2.6-pro @ CommandCode 17'/24³ 入 #3 并列**——OPS 6/6 全清、文本面全过、A-47eea242 并列该案最佳；1 案（A-d511f9e8）案级基建 invalid 挂起待重评；同道 grok-4.7 腿撞配额墙未完赛、mimo-v2.6-flash 在考（[amber-commandcode W39](https://github.com/getaskclaw/amber-commandcode/blob/main/results/2026-W39.md)）。

¹ 补注：周标签统一表示基线考试周。step-5-preview 全库考试为 2026-09-20（W38），发文与收敛补测为 2026-09-21（W39）；16'/24，4 挂起格不计胜负。luna 的 W37 基线与 W39 补测见 ³；既有挂起不因本次勘误解除。

² Claude 更正：A-1fd3683a（`6a980035b42f`）改注 invalid／NA（考场(harness)基建）：原卷未落盘、零流量闸误判。拒答观察仅留诊断附注；owner 已签撤回安全边界部署建议。17'/24 = 17 胜 · 6 负 · 1 案作废。[详情](https://github.com/getaskclaw/amber-claude/blob/main/results/2026-W39-correction.md)。

³ ' = contested（安全拒答挂起）或 invalid（基建相关（考场 harness 或判分环境）的挂起、作废或待重评），均不计胜负；所有含 NA 的道都带撇号，包括冻结展示行；挂起不表示死因已定。MiMo（mimo-v2.6-pro）17'/24：A-d511f9e8 仍为判分环境基建 invalid／NA，挂起待重评，不是考场 harness 故障。5.6-luna high：2026-09-07 基线考试（W37），2026-09-21 同档补测（W39）；16'/24 = 16 胜 · 4 负 · 4 挂起。三案 exonerated_infra 为首次公开改判、能力分暂停采用；A-ea80d793 维持挂起，视觉为 NA，不计有效负。见 [该项更正及总账引用](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38-correction-luna-high.md)。其它道保留各自具名状态。

5.6-luna high 画像更正：完成度为 0–1 的归一化得分，不是通过案数；NA 不计分，不是零。原七家画像不含 luna，本表单独澄清，不替换其它模型。

| 编码 | 交付 | 运维 | 需求 | UI | 视觉 | 防御 | 归因 | 审查 | 收敛 |
|---|---|---|---|---|---|---|---|---|---|
| 0.958 | 1.000 | 1.000 | 1.000 | NA | NA | 0.292 | 0.667 | NA | 1.000 |


## 怎么读一期成绩（结果仓矩阵）

每个结果仓每期一篇 `results/YYYY-Www.md`，核心是一张矩阵。读法有五条：

- **别名（A-xxxxxxxx）** — 案件对外的公开称呼。内部案号永不出现，从分数反推不出题面。
- **bundle_sha** — 该案题面的内容哈希。与本仓[公开哈希索引](hash-index/v2026-09.md)逐案对照：一致 = 题集没换。
- **✓ / ✗（案级）** — 通过线是「必检项全绿」：8/9 也是挂——防线漏一颗钉就是漏。
- **找茬分（审查/视觉案）** — 命中 − 误报 − 恭维 − 判错罚分（最终结论判错方向再倒扣）。正分难得，负分常见。（成绩仓已发布期文与图表里它写作 `d2`，同一把尺。）
- **口径三件套** — 只在同 effort 档、同题集版本下对比，还要看日期；同名模型换个端点，可能就是另一个脑。单日数字是快照，不是定律。

## 常见问题

**题目不公开，凭什么信分数？** 信任不靠「把题给你看」，靠的是链条：净室考场（无 fallback 链）、逐卷验脑（每次调用对账，替身 = 整卷作废）、收卷闸（零污染才入库）、别名 + 哈希发布（你可逐案核对题集未变）、harness 身份每期公开钉账（现役 = [Hermes](https://github.com/NousResearch/hermes-agent)，版本 + commit 随期钉死）。题目保密的代价，用可验证的过程补回来。

**为什么不公开题目？** 公开题库会被训练数据吃掉，分数通胀、无法审计——这是公开基准的通病。题目私有，泄漏状态才可核查。

**两个模型的分能直接比吗？** 只在同档、同题集版本、尽量同日时可比。跨周对比必须带日期和档位声明（各期都钉了），跨仓引用同理。

**能复现或加入吗？** 目前不能：仅凭公仓还跑不通一次合规运行（规范 v0.2.2 草案，`schemas/`、`profiles/` 与工具未发布，见 [PLAN.md](PLAN.md)）。追结果请订阅上面的结果仓；方法论问题欢迎开 issue。

## 许可

Apache-2.0 — 见 [LICENSE](LICENSE)。
