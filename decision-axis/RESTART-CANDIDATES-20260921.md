# AMBER 决策轴 · 重启候选素材挖掘（2026-09-21）

> 触发：owner 问「trace sqlite 过去 100 天，看哪些 AMBER 案例能加进决策轴，它的范围和定义是什么」。
> 方法：子代理挖 Vesper state.db（只读，窗口 2026-06-13 → 2026-09-21，18.3 万条消息）+ Vesper 复核裁决。
> 关联档：本目录 ARCHIVE.md（封存令+7 条诚信闸+四条 Core 违规）、私有 amber-run 仓 INDEX.md。

## 决策轴定义与范围（封存档原文）

评「决策模型 / System One」——不生成文本，只对给定 state 回答封闭问题：
Choice（选项判断）/ Score（量表）/ Noul（0-1 概率），返回校准概率。代表 = TypeSafe Jev。

- 评「判断」不评「生成」，与在册各轴（视觉/交付/ops 归因/收敛）分工互补
- 真案必须过 Core 闸：§5.1 真实历史（禁自编题）、§4.2 cutoff 双快照封存、§4.6 oracle 运行时自算、隐藏变体+良性对照
- 重启扳机（owner 09-19 定）：生产侧真出现「命令风险自动门」或「告警自动分级」需求才开卷——**目前未出现**

## 挖掘结果：能过 Core 闸的候选族（ground truth 事后真落地、可审计）

| 族 | 题型 | 具体事件（100 天内） | gold 来源 | 锻造难度 |
|---|---|---|---|---|
| 事故归因 | Choice（根因是哪层/哪端） | user@1000 cgroup blackout（09-18，根因=madp docker 容器每 5s 健康检查搬进程，已锻校验案 MustPass 闸先例）；ID162/TDOA 丢包（09-19，设备端漏装 21%，gold=sqlite 无断号+logger fail-closed） | 修复 commit/日志/账本证据链 | 低-中 |
| 红道裁决 | Choice（SHIP/FIX） | 13 份裁决档 ~/.hermes/red-lane/adjudications/（含 conv001-r1、pr175、dec001-r1 等） | 该 PR/案后续实际崩坏或存活 | 中 |
| 部署 go/no-go | Choice/Noul | askclaw.dev 部署史、网关重启哨兵史 | 事后健康检查/日志 | 中 |

量级估计：**数十案级 casebook**，撑不起 300 题校准卷。

## 黑名单（看着像素材，合规硬伤）

- owner 批准/否决/口味类（设计稿、方案选型）：gold 是主观判断，oracle 无法运行时自算
- 派单选席位：「选对没有」无客观落点
- quota 切脑时机：gold 仍是 owner 裁定

## 若重启，前置顺序（子代理建议，Vesper 复核认可）

1. owner 确认重启扳机出现（封存档自定条件）
2. 修 B1-B7 诚信闸（r2）——否则任何分数不可对外
3. Jev 新 key（旧 key 09-19 已过期 401）；候选平替=Kev（Cognition 开源，System One API 兼容，改 base_url 即可）
4. 先解方法论矛盾：黑话题考黑话（Jev 必输无意义）、通用题无区分度（253/300 两家同对）——须从「模型实际答错什么」造题
5. 窄族（归因+go/no-go）造 10-30 案 Core 合规 casebook，模板照校验案系列
6. 补 ECE/阈值扫描验证（Jev 独家卖点，封存前从未验过）

## 状态

- 2026-09-21 owner 令：记录存档 + 10 天后（2026-10-01）提醒重审。
- 提醒=cron 一次性任务，到点在 TG 本 thread 重报本文件要点+问「重启扳机出现没有」。
