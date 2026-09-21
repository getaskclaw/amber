import json, collections

ALERT = [
# ignore (10) —— 常规噪音/已恢复/预期内的拒绝
("INFO  cron.scheduler: Job 'a1b2c3' completed in 0.4s", "ignore"),
("RESOLVED|spine|bad-line:repo-watch|episode 7ba199be closed: 2 clean ticks", "ignore"),
("WARNING plugins.memory: skill_manage refused a patch: skill is not curator-managed (expected)", "ignore"),
("INFO  gateway: heartbeat ok, 3 platforms connected", "ignore"),
("WARNING qqbot.adapter: WebSocket closed: code=4009 Session timed out (reconnecting)", "ignore"),
("INFO  backup: nightly snapshot finished, 12GB written", "ignore"),
("WARNING model_tools: coerce_tool_args fell back to single-element list; recovered", "ignore"),
("INFO  apt: 3 packages upgraded successfully", "ignore"),
("WARNING ssh: Connection to host closed by remote host (retry scheduled)", "ignore"),
("INFO  systemd: Started Daily apt download activities.", "ignore"),
# soon (10) —— 该看但不急
("WARNING memory_tool: USER.md exceeds char limit: 2086/2048. Further additions blocked.", "soon"),
("WARNING tools.checkpoint_manager: Git command failed: git add -A (rc=128) Permission denied on a systemd-private dir", "soon"),
("WARNING cron.scheduler: Job 'af8abdae': delivery target lost thread_id", "soon"),
("WARNING skill_manage: SKILL.md content is 101,413 characters (limit 100,000)", "soon"),
("WARNING agent: Reached maximum iterations (16). Requesting summary...", "soon"),
("WARNING web_search: rate limited, falling back to cached results", "soon"),
("WARNING disk: /var/lib/postgresql is 81% full", "soon"),
("WARNING certbot: certificate for example.com expires in 21 days", "soon"),
("WARNING pg: 4 slow queries detected (>2s) in the last hour", "soon"),
("WARNING deploy: canary pod restarted once in the last 30 minutes", "soon"),
# now (10) —— 今天必须处理, 功能已降级
("ERROR tools.checkpoint_manager: Git command failed: git add -A (rc=128); working tree changes not captured", "now"),
("ERROR payment-gateway: 5xx from provider for 12 consecutive requests over 6 minutes", "now"),
("ERROR db: connection pool exhausted; new requests are being rejected", "now"),
("ERROR auth: token refresh failing for all sessions since 09:00", "now"),
("ERROR queue: consumer lag 45,000 messages and rising", "now"),
("ERROR backup: nightly snapshot failed 2 nights in a row", "now"),
("ERROR api: 3 of 6 replicas unhealthy; traffic being shed", "now"),
("ERROR etl: nightly import aborted; yesterday's data not loaded", "now"),
("ERROR dns: resolution failing for internal service names", "now"),
("ERROR cron: scheduled job 'nightly-report' has not run for 3 scheduled times", "now"),
# page (10) —— 立即叫人, 数据/安全/全站
("CRIT|spine|exec_failed:fallback-watch|spawn failed: Permission denied on monitor check script", "page"),
("CRIT db: primary PostgreSQL instance unreachable from all app nodes", "page"),
("CRIT security: 40 failed root SSH logins from 3 unknown IPs in 2 minutes", "page"),
("CRIT storage: RAID array degraded, 2 disks failed", "page"),
("CRIT billing: charge endpoint returning 500 for 100% of requests", "page"),
("CRIT data: unexpected row count drop in fisher_reports: 128,400 -> 3,100 overnight", "page"),
("CRIT cert: TLS certificate expired; all HTTPS traffic failing", "page"),
("CRIT memory: OOM killer terminated the main API process 4 times in 10 minutes", "page"),
("CRIT deploy: production serving a build from 6 days ago after a bad rollback", "page"),
("CRIT secrets: a service account key appears in a public repository", "page"),
]

rows = []
for i, (text, gold) in enumerate(ALERT, start=1):
    qid = "dec003-alert-%03d" % i
    rows.append({
        "id": qid, "family": "alert-triage-balanced", "state": text,
        "question": {"id": qid, "type": "choice",
            "instructions": "How urgently does this operations alert need a human? Choose the single best level.",
            "criteria": {
                "ignore": "Expected noise, informational, or already resolved; no action needed.",
                "soon": "Worth a look during normal working hours; nothing is broken yet.",
                "now": "Something is degraded or failing; handle today before it gets worse.",
                "page": "Outage, data loss/corruption, or a security incident; wake someone now."}},
        "gold": gold, "source": "vesper-authored-2026-09-19", "difficulty": "clear"})

print(len(rows), collections.Counter(r['gold'] for r in rows))
with open('/tmp/dec003/alert-triage-balanced.jsonl', 'w') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print("saved")
