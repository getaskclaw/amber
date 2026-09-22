# 更正声明 2026-W38:全库复核的第一波改判与挂起(docs 筛查文档观测链加注)

> 英文版:[corrections-2026-W38.en.md](corrections-2026-W38.en.md)

## 更什么事

AMBER 对 2026-09 已发布成绩做了一次全库复核,签发日为 2026-09-22。第一波结果分两类:**改判**(失败死因归考场设备侧,能力分暂停采用)与**挂起**(证据不全,具名移出排名、补考前不计任何聚合)。逐仓的改判表与挂起表见 12 个成绩仓各自的 `results/2026-W38-correction.md`;本声明是主仓的入口与口径说明。

本仓无 `results/`,受影响的落点是 `docs/` 已发布的**方法论记录**:`docs/stage1-sfail-screen-20260915.md` 的观测链有 4 个观察点来自本次嫌疑卷。**该文档不是成绩榜**:本刊对其只做「加注」,不做改判、不进任何聚合、不计名次、不计入任何仓的标题计数。

## 4 个观察点(加注口径 · 非成绩格)

| 别名 | bundle_sha | 观察点性质 | 加注口径 |
|---|---|---|---|
| A-cdc3d11a | `dbb207a3118d` | 稳定挂科序列第 4 项(筛查序列 1 项) | 若该卷后续被裁定,序列表须加注「观察可能含基建伪影」;序列数字暂不重算 |
| A-d9b79b46 | `d6d63130ecc6` | stage-2 n=20 聚合(6/20 过)中的 1 个失败观察 | 同上,聚合率暂不重算 |
| A-d9b79b46 | `d6d63130ecc6` | stage-2 n=20 聚合中的 1 个失败观察 | 同上 |
| A-d9b79b46 | `d6d63130ecc6` | stage-2 n=20 聚合中的 1 个失败观察 | 同上 |

> 合计:筛查序列 1 项 + stage-2 聚合 3 项 = 4 个观察点。

## 口径

- **总账**:全库嫌疑 **105 卷** = **34 卷已裁定** + **71 卷挂起**;未裁定卷对公开面的影响是「**可能上移**」而非「已改判」。
- **两层严格分开**:「改判」= 已裁定,只有这一层改写公开面结论;「挂起-可能上移」= 未裁定,只具名列出,补考前不计任何聚合、不给新名次。
- **不平账不放榜**:证据不齐的卷一律具名,不许只报个数。
- **本波不涉及 amber-devin**:其已发布期文不含任何嫌疑格,以免读者误解为普遍性停榜。
- 句柄:全部受影响格 = 稳定别名 `A-xxxxxxxx` + `bundle_sha`(12 位),与 [公开哈希索引 v2026-09](hash-index/v2026-09.md) 逐案一致,零失配。
- 历史期文原文不动,改判以追加链呈现;发布顺序:主仓本声明在前,逐结果仓特刊在后。

## 方法说明

## 方法说明:为什么更正、怎么查的、以后怎么防

**为什么更正。**
成绩是我们发布的,错就得由我们改。这次复核发现,已发布成绩里有一部分失败并非模型
答不出,而是考场这侧的设备问题——判分之前的环节把健康的作答掐断了,于是卷子记成了
模型失败。这类错误有两个方向:把好的判成坏的,和把坏的判成好的;我们两个方向一起查。
更正不是为了好看或难看,是为了让榜上的数字和实际发生的事对得上。

**怎么查的。**
每一卷都由**多席位独立验证**:验证方直接读原始现场(作答记录、判分器输出、账本时间戳、
修复提交),不采信任何二手结论;两个独立方向分头查——一家找「有没有被冤枉」,
一家找「有没有被漏掉」;两家结论一致才进裁定,不一致的进挂起。
裁定由同一份证据链支撑、逐卷可复算,并留有签字确认。查完的结果分四类:
平反(死因归考场设备,能力分暂停采用)、定案不平反(确认是模型侧)、
挂起(证据不全——**不许悄悄定罪,也不许悄悄赦免**)、以及不动历史只作报告级更正的条目。

**以后怎么防。**
三件小事,一句话级:① **证据链**——每一卷的原始过程在司机够不着的地方旁录,
追加写、卷终封存,判分只认证据完整性;**死因是结论,不是事实**,可以从证据重算,
规则错了改规则重跑,原始事实永不动。② **对账闸**——批进多少卷、批出必须平
(判分卷 + 设备卷 + 挂起卷,一桶不少、一格不多),**不平账就不出榜**,没有「先发了再补」。
③ **验脑双检**——每卷必配身份断言,缺钉不算分;同时抽查「通过的卷」以防反向错案。
防线防不住所有问题(设备总会坏),能做的是让错判活不过下一个对账周期。

**一句话。** 我们卖的不是永不错判——是没有判了赖不掉的。

## 各仓特刊入口

- [amber-gpt](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38-correction.md)
- [amber-commandcode](https://github.com/getaskclaw/amber-commandcode/blob/main/results/2026-W38-correction.md)
- [amber-ollama](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W38-correction.md)
- [amber-crof](https://github.com/getaskclaw/amber-crof/blob/main/results/2026-W38-correction.md)
- [amber-deepseek](https://github.com/getaskclaw/amber-deepseek/blob/main/results/2026-W38-correction.md)
- [amber-kimi](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38-correction.md)
- [amber-stepfun](https://github.com/getaskclaw/amber-stepfun/blob/main/results/2026-W38-correction.md)
- [amber-opencode](https://github.com/getaskclaw/amber-opencode/blob/main/results/2026-W38-correction.md)
- [amber-workbuddy](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W38-correction.md)
- [amber-doubao](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38-correction.md)
- [amber-goldenpotato](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38-correction.md)
