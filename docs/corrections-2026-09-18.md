# 更正声明 2026-09-18：「swe-2-low」成绩实为 swe-2-high

> Correction notice. English version: [corrections-2026-09-18.en.md](corrections-2026-09-18.en.md)

## 更什么事

AMBER 已发布成绩中所有标注为 **swe-2-low @ Devin** 的结果（amber-devin 2026-W37 期文 Addendum、
本站 README 榜单与脚注、nine-axis 2026-09-18 期文、case-run-matrix / flip-list 数据表），
实际运行的模型是 **swe-2-high**。

**swe-2-low 这个模型不存在。** Devin 官方目录（`devin models list` 活查，以及 Cognition 的
SWE-2 发布文）中 SWE-2 家族只有 medium / high / max 三档。

## 怎么发现的、怎么验证的

1. 读者举报「Devin 没有 swe-2-low，请求会被转移」后，我们做了活探针 + 服务端落账对拍。
2. Devin 后端自己的会话账本（CLI sessions.db，记录的是**解析后实际运行**的模型）显示：
   有史以来 swe-2-low 记录 **0 条**；09-12 所谓「swe-2-low 全库首考」当天的 82 条考场会话
   全部记为 **swe-2-high**。
3. 机制：考具按请求方指定的 id 向 ACP 通道发 `session/set_config_option`；当 id 不在服务端
   广告的可选清单里时，选择请求被**静默跳过**，会话保持服务端默认档（现为 swe-2-high）——
   全程零报错、零拒绝。
4. 同期对照：09-10/09-11 跑的 swe-2-medium（62 条）与 swe-2-max（22 条+36 条）在服务端账本中
   均忠实落账，证明账本列反映的是解析结果而非回显请求值，也证明 medium/max 两轮成绩为真档位、
   **不受本次更正影响**。
5. 独立复测（更正发布当日）：合法 id 经同一通道路由全部正确（medium→medium、max→max），
   即「通道不分辨合法 id」并不成立；问题仅出在「请求不存在的 id 时静默落默认」。

## 成绩怎么改

- 「swe-2-low 15/23」= swe-2-high 的第二次全库跑。与 09-10 的 swe-2-high 首跑 16/23 对比，
  是**同一模型的两轮方差**（16 vs 15，落在已知 ±2 抖动带内），不是档位差异。
- 「档线 low 15 = medium 15 < high 16 < max 18」更正为 **medium 15 < high 16 ≈ high 二跑 15
  < max 18**；medium / high / max 的单调档线结论不受影响。
- 「swe-2-low 与 medium 同分不同画像」的画像对比叙事，实为「swe-2-high 二跑 vs medium」，
  画像差异仍真实存在，但归属应记在 high 的二跑头上。
- nine-axis 期文审查轴榜首「swe-2-low @ Devin 0.722」更正为 swe-2-high。该分数原文已标注
  「单次未复测，不进路由结论」，处置不变。
- ORCH 类单案成绩中「swe-2 low 29/32 冠军」更正为 swe-2-high；「low 29 vs high 24」系同模型
  两轮方差。

## 审计纪律的教训（机制修复）

本次验脑审计核的是**请求侧**账本（考具发出的 model 参数），未核**服务端解析侧**账本，
因此静默替换穿透了「26/26 验脑」。自本更正起，Devin 道的验脑口径增加一条：
**服务端会话账本的解析模型必须与请求模型逐条一致**；选模前先对官方活目录校验 id 存在性。

## 受影响文件

- `README.md` / `README.en.md`：榜单并列行与脚注（本次提交修正并指向本声明）
- `docs/nine-axis-top3-2026-09-18.md` / `.en.md`：审查轴归属（本次提交修正）
- `docs/data/case-run-matrix-2026-09-14.csv`、`docs/data/flip-list-2026-09-14.csv`、
  `docs/data/build-case-run-matrix.py`、`docs/data/build-flip-list.py`：模型标签修正
- `docs/stage0-flip-analysis-2026-09-14.md`、`docs/instability-memo-2026-09-14.md`：
  提及处为历史叙事，保留原文并在此备案
- amber-devin 仓 `results/2026-W37.md`：顶部横幅 + Addendum 2026-09-18（正文保留为历史记录）
