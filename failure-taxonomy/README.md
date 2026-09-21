# AMBER failure-taxonomy — 硬事实层（v0.1，2026-09-21）

挂案归因第一版：从存量 bench transcript 里抽**规则化硬事实**，与各 lane 已发布的
`✗` 成绩交叉，产出「挂案归因表」。**不跑新案，纯挖掘存量；不调 LLM。**

## 交付物

| 文件 | 说明 |
|---|---|
| `extract_hard_facts.py` | 硬事实提取器（只读 state.db，逐 bench 会话） |
| `hard-facts.jsonl` | 每行一个 bench 会话（1918 行） |
| `build_lane_registry.py` / `lane-registry.json` | profile→lane→model 实证映射（manifest session-id join） |
| `build_profile_lane_map.py` / `profile-lane-map-W38.md` | **第 0 步**：profile → lane → bench 会话数 映射表 |
| `build_attribution.py` / `attribution-W38.md` | **第 2/3 步**：挂案归因表 + 完成声明一致性 |

## 复跑

```bash
cd ~/2606/amber/failure-taxonomy
python3 extract_hard_facts.py          # -> hard-facts.jsonl
python3 build_lane_registry.py         # -> lane-registry.json
python3 build_profile_lane_map.py      # -> profile-lane-map-W38.md
python3 build_attribution.py           # -> attribution-W38.md
```

## hard-facts.jsonl 记录格式

```json
{"profile": "amber-ollama-g53f", "session_id": "2026...", "source": "amber-lib-BD-001-ollama-g53f-high",
 "case_hint": "BD-001", "case_alias": "A-77d62143", "face": "build",
 "lane_token": "ollama", "band_token": "high", "model": "glm-5.3-flash",
 "started_at": 1788..., "ended_at": 1788..., "wall_s": 165.4, "end_reason": "cli_close",
 "message_count": 30, "tool_call_count": 16, "cwd": null,
 "signals": {
   "timeout":            {"hit": false, "evidence": []},
   "billing_exhausted":  {"hit": false, "evidence": []},
   "tool_failure":       {"count": 3, "evidence": [...], "last_fail_ts": 1788...},
   "test_modified":      {"hit": true, "paths": [".../tests/test_custody_guard.py"]},
   "completion_claimed": {"hit": true, "snippet": "...", "timestamp": 1788...},
   "verification_run":   {"hit": true, "count": 2, "last_ts": 1788...}
 }}
```

## 信号口径（全是规则，无 LLM）

- **timeout**：工具结果 exit_code=124 且 output 命中**帽长文本**（1800/3600/7200s），
  或会话墙钟落在 1800/3600/7200s 帽 ±窗口内。**候选自己 command 超时（180s）不算帽墙**，归 `tool_failure`。
- **billing_exhausted**：只扫工具结果的 `error` 机器信封；**不扫正文**——OPS-08 这类
  「配额分诊」案正文天然含 `no_credits` 字样，扫正文会全线假阳性。
- **tool_failure**：工具结果 exit_code≠0 或 status=error（端点/环境故障，非能力判定）。
- **test_modified**：write_file/patch 的**入参路径**命中测试文件模式（`tests/`、`test_*.py`、`*.test.ts`…）。
- **completion_claimed**：最后一条 assistant 文本含完成声明（中/英句式）。
- **verification_run**：候选自己执行了 checker（pytest / oracle_test / npm test / 自测…），用于第 3 步分类。

## 只读纪律

所有 state.db 用 `sqlite3.connect("file:<path>?mode=ro", uri=True)` 打开，一个字节不写。
（SQLite 在 WAL 模式下打开任意连接都会 touch `state.db-shm` 共享内存索引文件——
这是 SQLite 机制，不是数据写入；`state.db` / `state.db-wal` 的 mtime 全程未变，见回报。）

## 纪律

- 内部案号（BD-/BE-/OPS-/FTM-/REQ-…）**不出现在 attribution 与 profile map 里**，只有公开别名 `A-xxxxxxxx`。
- 信号不够 → `unknown`；无 transcript → `no_transcript`；跨厂商引用列 → `ref_column`；
  列粒度只能到 profile 级 → 附加 `scope=profile`。**不硬塞标签。**
