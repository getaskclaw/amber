# 更正声明 2026-09-21：astra 的 W36 UI 搭建案三格「✓」实为 fallback 替身交付

> Correction notice. English version: [corrections-2026-09-21.en.md](corrections-2026-09-21.en.md)

## 更什么事

AMBER 已发布成绩中，**gpt-6-astra-900k @ OpenAI Codex** 车道的 UI 搭建案 A-d9b79b46 在
2026-W36 期文与派生榜单中的 **low / medium / high 三格「✓」**，实际交付者不是 astra 本体，
而是该考场的 fallback 模型 **glm-5.3-flash @ Ollama Cloud**。这三格作废。

连带影响：本站 README 榜单 astra 的 headline 由 **16/23 更正为 15/23**，从 #3 并列移入 #4 并列组。

## 怎么发现的、怎么验证的

1. 09-20/21 应 owner 要求对 astra 做全库复核（medium 档 23 案 28 跑），其中 A-d9b79b46
   两跑均失败（输出未按契约带 ```vue 围栏，oracle 无卷可判）——与 W36 「低中高过」的记录矛盾。
2. 回查考场账本（session_model_usage，记录**实际服务**的模型与计费道）：W36 该案三个档位的
   交付会话，主任务行全部钉在 `glm-5.3-flash @ ollama-cloud`（输入约 8.1K、输出 6.8K–8.3K 的
   真实施工），astra 本体在会话中仅出席 `title_generation`（747 in / 21–56 out）。
   high 档会话连标题生成都是 glm——整条会话零 astra 施工行。
3. 机制：W36 考场的客户端看门狗会把 astra 的小提示词+长静默推理请求误判掐死（该缺陷至
   考具 v0.3 才修复，见 amber-gpt W38 期文），主道失败后 fallback 静默接手交卷，成绩按车道名
   记入 astra 名下。这是记录归属缺陷，不是有意造假；同期同案的 max/xhigh 两格「no delivery」
   即是同一看门狗的另一种死法。
4. 破检方向也做了：若复核日（09-20/21，线路遥测确认健康）astra 本体具备该案能力，则今天的
   low/medium/high 三档干净实测应至少一过——实际三档四跑全灭、同因同形，佐证 W36 三格非本体所为。

## 成绩怎么改

- amber-gpt W36 期文该案 low/medium/high 三格：标记作废，指向本声明与 W38 Addendum 5。
- 本站 README 榜单：astra 16/23 → **15/23**，移出 #3 并列，列入 #4 并列组。
- nine-axis-top3-2026-09-18 期文：astra 在 UI 轴的「满分并列」成员身份作废（该轴满分并列名单
  应剔除 astra）；其余轴（归因并列 #2 等）不受本更正影响。
- 完成度矩阵图（docs/images/completion-matrix-7way.png）中 astra 行的 UI 格同样源自替身格，
  图的重绘列入欠账，下次矩阵更新一并修。
- 同期待复核：A-0676097b 两个变体与 A-ea80d793 在 09-05/06 的会话亦见 fallback 行，
  复核结论另行发布。

## 机制整改

成绩归属不再只看「车道名」：每期验脑增加**主任务行钉**校验——会话主任务（非标题生成等辅助
任务）的模型与计费道必须等于受考车道，否则该格记 driver_exception 而非成绩。
