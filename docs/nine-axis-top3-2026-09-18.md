# 九轴榜首：每轴前三名是谁（2026-09-18）

**一句话结论：九轴里只有四轴真能排出名次**——编码、交付、运维、需求、UI 五轴的头部是大面积并列（满分或全员同分），Top 3 在这五轴上没有意义；真正有区分度的是**防御、归因、审查、视觉**四轴，而这四个「判官面」的冠军分属四家不同的厂商——总分榜首并没有通吃任何一面。

## 口径与数据源

- 数据：11 个成绩仓已发布期文（2026-W36 ~ W38），40 条已发布车道逐案复算
- 归一：钉案按「得钉 / 总钉」；找茬分（d2）案按已发布案面画像同口径 `(d2 + 4) / 9`
- 同一「模型 @ 端点」多档、多跑的，取该车道已发布的最佳一趟
- 复算锚点与已发布值核对一致（例：doubao 核验两轴 0.47 / 0.50、gp27b 施工 0.83 / 运维 0.97）
- 已知限制：跨周快照、21→23 案口径过渡、单跑车道的抖动未复测（逐项在下文标注）
- **「厂商」栏 = 标称模型的厂商，@ 后为官道或转发渠道；对标称道不作身份背书。** 特别是 CrofAI：2026-09-13 ktibow 的 [wire 级取证](https://kendell.dev/blog/crofaifalse)指其为 OpenRouter 套壳、多款在售模型指纹指向完全不同的上游；我们自己的[行为指纹分析](https://github.com/getaskclaw/amber-crof/blob/main/docs/model-identity-cosine-2026-09.md)独立旁证了这一点（crof `glm-5.3-flash` 三度量下都最像 `deepseek-v4.1-flash @ ollama`；`qwen3.8-27b` 可疑未坐实）。下文凡 CrofAI 车道一律带 ⚠，其成绩真实有效，但「它是谁」未被证实

## 有区分度的四轴

### 防御 · 堵校验器漏网口（2 案均分）

| 名次 | 模型 @ 端点 | 完成度 | 厂商 |
|---|---|---|---|
| 1 | deepseek-v4.1-flash @ WorkBuddy | 0.667 | DeepSeek |
| 2 | deepseek-v4.1-flash @ CommandCode | 0.611 | DeepSeek |
| 3 | deepseek-flash @ OpenCode Go / deepseek-v4-flash:0731 @ Ollama Cloud / kimi-for-coding（K2.8）@ Kimi 官方（并列 0.556） | 0.556 | DeepSeek ×2、月之暗面 |

### 归因 · 按症状归病灶（1 案 15 钉）

| 名次 | 模型 @ 端点 | 完成度 | 厂商 |
|---|---|---|---|
| 1 | qwen3.8-27b @ CrofAI ⚠ | **1.000**（全场唯一 15/15） | **标称**阿里 Qwen——身份未坐实：行为指纹最像 DeepSeek 0731 道（[指纹分析](https://github.com/getaskclaw/amber-crof/blob/main/docs/model-identity-cosine-2026-09.md)） |
| 2 | glm-5.3-flash @ Ollama Cloud / gpt-6-astra @ OpenAI Codex / hy4-preview-f @ WorkBuddy（并列） | 0.933 | 智谱、OpenAI、WorkBuddy 通道 |

### 审查 · 当验收官挑错（2 案找茬分均分）

| 名次 | 模型 @ 端点 | 完成度 | 厂商 |
|---|---|---|---|
| 1 | swe-2-low @ Devin | 0.722（**单次未复测**，复测前不进路由结论） | Devin |
| 2 | glm-5.3-flash @ Ollama Cloud / deepseek-v4.1-flash @ Ollama Cloud（并列） | 0.667 | 智谱、DeepSeek |

值得点破：swe-2-low 总分在梯队末尾，这轴却是它全家最佳——判官面与施工面不相关。

### 视觉 · 给真截图挑毛病（1 案找茬分）

| 名次 | 模型 @ 端点 | 完成度 | 厂商 |
|---|---|---|---|
| 1 | gpt-5.6-luna（max 档，09-17）@ OpenAI Codex | **1.000**（d2=5.0，该案已发布历史最高） | OpenAI |
| 2 | swe-2-medium @ Devin / gpt-5.6-luna（high 档，09-12）@ OpenAI Codex（并列 d2=4.0） | 0.889 | Devin、OpenAI |

## 头部饱和的五轴

- **编码**：24 条车道同分 0.958——A-87c472cb 的 2 颗钉全场合伙丢，无人 6/6。这轴当前不区分头部
- **交付**：满分 1.000 并列 29 条车道（反向信息才有价值：零交付的当场出局）
- **运维**：满分并列 14 条车道（swe-2-max、k3、doubao-seed-evolving、gpt-5.6-luna、hy4-preview-f、DeepSeek 各道等）
- **需求**：满分并列约 26 条车道
- **UI**：满分并列 12 条车道（swe-2 全系、gpt-6-astra、gpt-5.6-sol/luna-max、glm-5.3-flash @ CrofAI ⚠、deepseek-v4.1-flash 两道、hy4-preview-f、glm-5-2 @ Devin）

## 读法提醒

单日数字是快照，不是定律：「想更久 ≠ 考更好」「同分 ≠ 同款」之后，这组数字补的是第三刀——**总分榜首在四个判官面一个冠军都没拿到**（swe-2-max 的强项在饱和轴）。选模型按你要的活挑轴，别看总分下单。

English mirror: [nine-axis-top3-2026-09-18.en.md](nine-axis-top3-2026-09-18.en.md)
