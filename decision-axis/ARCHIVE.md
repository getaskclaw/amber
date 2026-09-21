# AMBER 决策轴 · 封存档（2026-09-19 owner 令「封存收工」）

> ## ⚠️ 合规性判定（2026-09-19 owner 指出后自查）
> **本目录下 300 题的成绩不是 AMBER 成绩**，只是方法前摸底。禁止混入 AMBER 成绩账。
> 四条 Core 违规（对照 `~/2606/amber/AMBER-Core-Specification.md` §5 + 真案
> `~/2608/sandbox/amber-run/case-AMBER-BE-001/`）：
> 1. **§5.1 Real history**：题是 Vesper 自编（`source: vesper-authored`），
>    非真实可审计事件回放。自编题连 `synthetic_supplement` 都够不着（合成补充也得基于真实事件改），
>    **永不计入 Core 成绩**。
> 2. **§4.2 cutoff**：无 `cutoff_utc`、无 base_snapshot、无 candidate_visible/evaluator_only 双清单、
>    无 fixture sha256。只有一个 state + 一个 gold = 没有封存。
> 3. **§4.6 / oracle**：`gold` 是静态字符串 = **锚定式评分**，正是红道 r1 抓过的同款病。
>    真案 oracle 运行时自造篡改/扰动（BE-001 有 P0/B1/B2 三道「必须放行」闸 + H1/H2 隐藏变体），
>    并配 base_control 3/11 / reference_control 11/11 双对照。
> 4. **无隐藏变体与反蒙混良性对照**：只出题不设防 → 实测 253/300 两家模型同时答对。
>    **「区分度不足」的真因不是题太简单，是卷子没设防。**
>
> **要造真合规案**，走制案流程（真实源事件 + cutoff + 双快照 + 自算 oracle + 隐藏变体），
> 模板照 `case-AMBER-BE-001`。owner 09-19 已判：暂不做。

> ## ⚠️ 红道裁决（2026-09-19 终局）
> **双红 verdict 冲突**：Iris SHIP / Reviewer FIX。Vesper 裁决 = **FIX，未放行**。
> **诚信闸仍未锁死，本目录任何分数现在不可对外发。** Reviewer 抓到 7 条可伪造分数的路径
> （原文 `~/.hermes/red-lane/adjudications/dec001-r1.md` / 红道原始证据 `/tmp/dec001-r1-reviewer.log`）：
> - B1 改判分口径（noul `>` 放宽成 `>=`、choice 回退 argmax）→ verify 仍绿，分数变好看
> - B2 跨 run 拼接换血（取低分 run 换入高分行）→ verify 全绿
> - B3 verify 在「验不了签」「manifest 被伪造」「run_nonce 全 0」下仍判绿
> - B4 REPORT.md 是发布级产物却零校验（改名accuracy没人管）
> - B5 report.json 非标量区段（by_family/by_type/buckets/threshold_scan）可任意改写
> - B6 同 tag 并发无锁（TOCTOU）+ `--force` 一次 dry-run 就把真 Jev 证据整目录替换成空
> - B7 append-only manifest 被 selftest 脚本以 "w" 整表重写（自相矛盾）
>
> **owner 09-19 决策：封存收工，不派 r2 修复。** 这 7 条钉死为「已知未修」警示——
> 重启本线时**必须先堵死这 7 条**才能用分数。N1-N7 非阻塞项（同 uid 持钥可重签 /
> env secret 轮换致全史红 / --force 无二次确认等）同归档。

评的对象：**决策模型 / System One**——不生成文本，只对给定 state 回答封闭问题
（Choice 选项 / Score 量表 / Noul 0-1 概率），返回带校准概率。代表=TypeSafe Jev。

## 状态：封存（不再投金标时间）
owner 09-19 决策：**近期无生产环节需要这套答案**（告警=哨兵硬规则分级，派单=Vesper 人工判断，
agent shell 无自动风险门）。价值=方法论储备，不是生产依赖。
**重启条件**：真要上「命令风险自动门」或「告警自动分级」那天再开卷——素材/管道全在盘上，可续。

## 目录
```
~/2606/amber/decision-axis/
  golden/   金标题集 + 造题脚本（可复现）
  runs/     各模型跑分 + 红道自测 + mock 错误码分类证据（x-401…x-500）
  raw-jev-expired-key/  Jev 原始响应（钥匙已过期，数据永久有效）
  driver.py / adapters/ / scoring/  管道本体
```

## 管道用法
`python3 driver.py --dataset golden/golden-300-20260919.jsonl --adapter <typesafe-native|openrouter|openai-compatible-baseline> --model M --tag T`
支持 `--dry-run` / `--empty-state`（区分度基线）/ `--score-only`（重算）/ `--verify-run <tag>`

## Jev 原生 API 实证（2026-09-19 真调，钥匙已过期但结论有效）
- `POST https://api.typesafe.ai/v1/systemone`，Bearer key
- body = `{state, model:"jev-latest", questions:{<name>:{type,instructions,criteria}}}`
- **Choice/Score 用 `criteria`，不是 `options`**：Choice 的 criteria={选项:描述} 字典，
  Score 的 criteria=描述数组。写 options → 422。
- 响应 `answers[name] = {choice|score|noul, confidence, probabilities, legend}`，回显 `jev-1.13.0`
- p50 ≈ **0.6s**；**fan-out**：50 题一发，延迟 0.58→0.84s（问 50 个≈问 1 个的价钱和时间）——**这是它最狠的卖点**
- 输入 $0.042/M，输出免费；限流 250k tok/s、1200 req/min
- 930 次调用总花费 ≈ **$0.011**

## 制卷铁律：答案必须均衡
第一条 300 条素材卷（Porter 挖的真实语料）**废弃不可用**：command-risk 42/50 是 read_only、
alert 41/50 是 soon —— 「全选最常见答案」的笨基线能拿 84%/82%，裸准确率毫无意义。
另：真实素材易出重复（ticket-routing 50 条里 25 条是同一工单切两段），制卷后必查子串去重。

**规矩**：每族各档等量；报告必须并列「笨基线」列，报**净胜**而非裸准确率。
现存 300 题卷：三族各 100，每族四档各 25，笨基线钉死 **0.250**。

## 金标规矩（Vesper 亲标，判断内核不外包）
- 只标「无争议题」：答案不依赖舰队内部背景。依赖内部黑话的分歧题**剔除**，不硬判模型错。
  实测：18 条两家都错的题里至少 3 条是我标错（`chmod 600` 收紧权限实为安全加固、
  `DELETE FROM x;` 有备份可恢复不该算 critical）。
- 题面自足，选项不写「不许动 X 表」这类需要内部知识的东西。

## 成绩（2026-09-19）
**120 题均衡卷**（三族各 40）：
| 模型 | 准确率 | p50 |
|---|---|---|
| Jev 1.13 | 0.875 | 0.59s |
| glm-5.3-flash | 0.875 | 1.76s |
| deepseek-v4.1-flash | 0.850 | 1.47s |

**300 题卷**（+180 难题档，仅两家基线跑过，Jev 钥匙已死未跑）：
| 模型 | 总 | 简单档120 | 难题档180 |
|---|---|---|---|
| glm-5.3-flash | 0.910 | 0.883 | 0.928 |
| deepseek-v4.1-flash | 0.874 | 0.842 | 0.894 |

**三条结论**：
1. **Jev 没有准确率优势**（0.875 vs 0.875/0.850）。优势是**快 3 倍 + 输出免费**。
   卖点=高频重复判定（一天几万次的路由/审核/分级），不是更聪明。
2. **「难题档」反而更简单**（0.928 > 0.883）——我造的是「换了说法的常识题」，不是真边界题。
   造题必须从「模型实际答错什么」出发，不能从「我觉得什么难」出发。
3. **区分度不足**：300 题里 253 题两家都对（送分题），仅 28 题有区分度。
   84% 的卷子内容无法拉开模型，排名是噪音。

## 场景取自项目，题目不专属项目
三族对应真实工作流（派工单/看告警/agent 执行 shell），但 180 道新题是**通用运维常识题**
（`rm -rf /`、`DROP DATABASE`），任何训练过的模型都会。
**真矛盾**：带舰队黑话的题（「CRIT|spine|exec_failed:fallback-watch」）才是专属的，
但那种题考的是「熟不熟我们的黑话」而非判断力，Jev 没见过必输，分数同样无意义。
→ 这是本轴未解的方法论问题。重启时先解这个。

## 基线模型坑（实测，会浪费整轮）
glm-5.3-flash / deepseek-v4.1-flash 走 ollama OpenAI 兼容道：
**`max_tokens` 给小了会 120/120 全空**——token 全烧进 `reasoning`，`content=""` 且
`finish_reason=length`，看起来像「模型零分」实为 harness 错。**必须给 3000**。

## 诚信闸（红道 r1 双 FIX 已修）
旧版漏洞：unkeyed sha256 可重算绕过、score-only 删行可把 0.5 刷成 1.0、
401/404 误记 `valid_task_failure`（等于给「答不对就弃答」开刷分通道）、
概率平票时判定依赖 dict 键序。
r1 已改：HMAC（secret 走环境变量/0600 文件）、id 集合对账、4xx 全归 `invalid_infrastructure`、
tie 确定性裁决 + 非裸 round。**红道复检 verdict 见 `red-lane/adjudications/dec001-r1.md`。**

## 待办（重启时按序）
1. 复核 18 条可疑金标（至少 3 条确认我标错）
2. 从模型实际答错的题出发造真难题，目标把区分度从 28/300 拉到 50%+
3. **ECE / 阈值扫描**（「它说九成把握到底对不对」）——Jev 独家卖点，从未验过
4. 火山方舟 Agent Plan 更多模型入对比（本机 `amber-a` 席已在 `volc-ark-plan`/doubao-seed-evolving，key 在盘上，随时可跑）
5. Jev 需新 key 才能续跑（旧 key 2026-09-19 过期，401）
