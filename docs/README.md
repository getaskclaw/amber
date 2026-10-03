# 文档索引

> 从首页 [README](../README.md) 的「内容」一节移来，正文未改。English: [README.en.md](README.en.md)

- [榜单全文](leaderboard-notes.md) — 当前前五的完整名单、脚注、更正横幅原文
- [十个轴与完成度矩阵](axes.md)
- [三个发现：档位、token、耗时](findings-effort-and-speed.md)
- [案件清单 schema 与校验器](manifest-schema.md)

- [AMBER-Core-Specification.md](../AMBER-Core-Specification.md) — 规范本体：目的、定义、机制、8 条不变量、8 条边界、认识论限制、命名评审、采用规则
- [protocols/distribution.md](../protocols/distribution.md) — 案件跨主机分发协议（v0.3）：公开/私有频道划分、固定构造的 git bundle、分离式签名清单、公开索引、密封探针、泄漏窗口的裁定规则、运行记录、可比性与验证矩阵
- [protocols/stability.md](../protocols/stability.md) — 稳定性协议草案（v0.1）：同臂复跑、失败后恢复率、副作用计数、基建废卷分列、样本量按决策反推
- [docs/instability-memo-2026-09-14.md](instability-memo-2026-09-14.md) — $0 历史漂移证据 memo：900 个已发布矩阵格、31 个规范臂（转载列已标记），证明「分数快照 ≠ 稳定性」
- [docs/stage0-flip-analysis-2026-09-14.md](stage0-flip-analysis-2026-09-14.md) — stage-0 翻转清单：17 条漂移/恢复事件（矩阵派生 + 散文标注），含 stage-1 筛查候选
- [docs/stage1-v001-screen-20260915.md](stage1-v001-screen-20260915.md) — 首个设计型稳定性数据：`A-ea80d793` × `glm-5.3-flash@ollama` n=20 同臂复跑，8/20 过（~40%，判决纪律 20/20 稳定）——边界格案例须报分数分布而非二元翻转
- [docs/stage1-reqdrift-screen-20260915.md](stage1-reqdrift-screen-20260915.md) — `A-0676097b` × `luna-high` n=5 复跑：3/5 过，回归在同一坐席复现两次且同为两个变体（变体名留私域）——升级分类边界案；协议新增多变体逐变体向量与 no-deliverable 分列
- [docs/stage1-sfail-screen-20260915.md](stage1-sfail-screen-20260915.md) — 稳定挂科集 6 案 × `glm-5.3-flash@ollama` n=5 筛查：5 案零复活保住标签（A-87c472cb/A-d511f9e8 钉分纹丝不动），**A-d9b79b46 三过一挂标签被撕**（stage-2 n=20 已收：合计 6/20 过≈30%，Wilson [14.5%, 51.9%]——n=5 的 75% 过率是虚高，筛查档只有二元结论可信）；A-a317e74b 需 3600s 帽才能完卷——协议补逐案超时表与撞 billing 即停
- [docs/nine-axis-top3-2026-09-18.md](nine-axis-top3-2026-09-18.md) — 九轴榜首（40 车道复算，成文于收敛轴入册前）：只有防御/归因/审查/视觉四轴有区分度，四个冠军分属四家厂商；其余五轴头部饱和并列
- [hash-index/v2026-09.md](../hash-index/v2026-09.md) — 公开哈希索引：当前题集（24 案，含收敛轴首案）每案的别名 + bundle/oracle 双哈希；结果仓每期矩阵以此为准对照
- [schemas/manifest.schema.json](../schemas/manifest.schema.json) · [tools/validate_manifest.py](../tools/validate_manifest.py) · [schemas/shre-amber-mapping.md](../schemas/shre-amber-mapping.md) — 案件清单 JSON Schema、校验器（含 Distribution §5.1 闭集脱敏摘要校验）、SHRE→AMBER 标识映射表
- [PLAN.md](../PLAN.md) — 状态、里程碑（建案工具 → 参考运行器 → 评分与裁判 → 统计 → 公开索引）、待决设计问题
- [CONTRIBUTING.md](../CONTRIBUTING.md) — 贡献规则：**本仓库绝不接收案件内容**、规范文档的版本与修订政策、Core 规范按字节哈希锁定的含义

图的源文件（PlantUML 的 `.puml`、Vega 的 `.vega-lite.json` / `.vg.json`）就放在 PNG 同目录，改图 = 改源文件再渲染。
