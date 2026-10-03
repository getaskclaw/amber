# 案件清单 schema 与校验器

> 从首页 [README](../README.md) 移来，正文未改。下面的命令请在**仓库根目录**运行。English: [manifest-schema.en.md](manifest-schema.en.md)

案件清单（Case Manifest）是控制面记录，属私域、永不进考生视野（Distribution §1、Core §2）。字段集**全部取自协议原文**：`protocols/distribution.md` §3（provenance、`cutoff_utc`、解析后的 cutoff commit、time-to-topology 映射规则及其证据类、预注册 cutoff 规则及其脚本输出哈希、`spec_sha256`、两件产物的 sha256、声明的 `candidate_input_bundle`、available-information manifest、资格判定及其证据类、生产者身份与签名密钥标识、泄漏检查程序/上次运行日/结果、退役状态、本协议文档的 sha256），§3.1（构造参数：git 版本、bundle 格式版本、哈希算法、bundle 大小），§3.2、§5.1、§5.2。**没有自造字段。**

- [schemas/manifest.schema.json](../schemas/manifest.schema.json) — 清单的 JSON Schema（2020-12）；顶层与各字段块均封闭（`additionalProperties: false`），多一个协议未列举的字段即报错。
- [tools/validate_manifest.py](../tools/validate_manifest.py) — 校验器。校验清单是否符合 schema，并额外拒绝任何越出 Distribution §5.1 闭集字段的**脱敏摘要**。
- [schemas/shre-amber-mapping.md](../schemas/shre-amber-mapping.md) — Core §9.3 要求的 `shre`↔`amber` 标识映射表，无法从公开材料映射的项标 TBD 并注明缺什么。
- [schemas/examples/](../schemas/examples/) — 回归样例：1 个合法清单 + 3 个畸形清单（缺必填字段 / 字段类型与枚举错 / 多出闭集外字段）+ 1 个带越界字段的脱敏摘要。

用法（YAML 与 JSON 都吃）：

```bash
python3 tools/validate_manifest.py schemas/examples/manifest.valid.yaml        # 过，退出码 0
python3 tools/validate_manifest.py schemas/examples/manifest.wrong-types.yaml  # 不过，退出码 1 + stderr 指出违规字段
python3 tools/validate_manifest.py schemas/examples/summary.invalid-fieldset.yaml   # 脱敏摘要越界字段
```

退出码：**0** 合规；**1** 不合规（schema / 闭集 / 跨字段违规）；**2** 无法读取或解析、类型无法判定、schema 载入失败。JSON 输入零依赖；YAML 在装有 PyYAML 时走 PyYAML，否则退回自带的保守解析器（遇到锚点/别名/折叠标量等它看不懂的结构会明确报错，不猜）。装 PyYAML：`python3 -m pip install pyyaml` 或 `uv run --with pyyaml python3 tools/validate_manifest.py <file>`。
