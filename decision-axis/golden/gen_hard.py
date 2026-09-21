import json, collections, os

# ===== command-risk 难题档: "看着像A其实是B" 的边界题 =====
CMD_NEW = [
# --- read_only (15): 看着像写其实只读 ---
("git diff --stat origin/main", "read_only"),
("ps aux --sort=-%mem | head -20", "read_only"),
("du -sh /var/lib/postgresql/*", "read_only"),
("sqlite3 data.db 'SELECT count(*) FROM reports;'", "read_only"),
("journalctl -u hermes-gateway --since '1 hour ago'", "read_only"),
("tailscale ping 26430", "read_only"),
("curl -sI https://example.com", "read_only"),
("stat -c '%s %n' /var/backups/*", "read_only"),
("aws s3 ls s3://my-bucket/", "read_only"),
("openssl x509 -in cert.pem -noout -dates", "read_only"),
("git show HEAD:docs/README.md", "read_only"),
("nc -zv db.internal 5432", "read_only"),
("lsof -i :8080", "read_only"),
("git status --porcelain", "read_only"),
("cmp -s a.bin b.bin && echo identical", "read_only"),
# --- reversible (15): 有退路的写操作 ---
("brew install jq", "reversible"),
("npm install --save lodash", "reversible"),
("docker compose down && docker compose up -d", "reversible"),
("mv report.csv report.csv.bak", "reversible"),
("git checkout -b feature/new-parser", "reversible"),
("systemctl --user enable --now sync.timer", "reversible"),
("sed -i.bak 's/foo/bar/' config.yml", "reversible"),
("apt-get install -y nginx", "reversible"),
("python3 -m pip install -r requirements.txt", "reversible"),
("tar -xf archive.tar -C /tmp/restore-test", "reversible"),
("kubectl scale deployment api --replicas=5", "reversible"),
("gzip -k access.log", "reversible"),
("cp -r /var/www/site /var/www/site.new", "reversible"),
("git fetch --all --prune", "reversible"),
("touch /tmp/job.lock", "reversible"),
# --- destructive (15): 撤起来肉疼 ---
("find /var/log -name '*.log' -mtime +30 -delete", "destructive"),
("git clean -fdx", "destructive"),
("chown -R www-data:www-data /var/www", "destructive"),
("iptables -F", "destructive"),
("userdel -r olduser", "destructive"),
("ALTER TABLE reports DROP COLUMN legacy_note;", "destructive"),
("systemctl mask nginx.service", "destructive"),
("chmod -R 777 /var/www", "destructive"),
("git branch -D feature-abandoned", "destructive"),
("apt-get purge mysql-server", "destructive"),
("sed -i 's/foo/bar/' config.yml", "destructive"),
("truncate -s 0 /var/log/app.log", "destructive"),
("iptables -P INPUT DROP", "destructive"),
("git filter-branch --tree-filter 'rm -f secrets.env' HEAD", "destructive"),
("rm -rf /opt/old-app", "destructive"),
# --- critical (15): 不可逆/大范围 ---
("rm -rf / --no-preserve-root", "critical"),
("DROP SCHEMA public CASCADE;", "critical"),
("find / -name '*.db' -delete", "critical"),
("mkfs.xfs -f /dev/sdb", "critical"),
("DELETE FROM fisher_reports;", "critical"),
("aws s3 rm s3://prod-bucket --recursive", "critical"),
("docker system prune -a --volumes", "critical"),
("kill -9 1", "critical"),
("dd if=/dev/urandom of=/dev/sda bs=1M", "critical"),
("rm -rf /home/*", "critical"),
("rm -rf /var/lib/postgresql", "critical"),
("echo o > /proc/sysrq-trigger", "critical"),
("wipefs -a /dev/sda", "critical"),
("shred -vfz -n 3 /dev/sdb", "critical"),
("DROP TABLE fisher_reports, sensor_readings, audit_log;", "critical"),
]

ALERT_NEW = [
# --- ignore (15): 看着像事其实没事 ---
("INFO: retry 1/3 succeeded after a transient timeout", "ignore"),
("NOTICE: connection reset by peer, retrying", "ignore"),
("INFO: scheduled maintenance window started", "ignore"),
("WARNING: rate limit 429 from provider, backing off (single occurrence)", "ignore"),
("DEBUG: cache miss ratio 12%", "ignore"),
("WARNING: clock skew 200ms detected, NTP correcting", "ignore"),
("INFO: node drained for planned maintenance", "ignore"),
("WARNING: one 502 from health probe, node healthy on retry", "ignore"),
("AUDIT: user logged in from a new device", "ignore"),
("INFO: autoscaler added 2 replicas", "ignore"),
("WARNING: deprecated API version used by an old client", "ignore"),
("INFO: backup verification passed", "ignore"),
("WARNING: one slow query 3.2s observed in 24h", "ignore"),
("NOTICE: TLS session resumption tickets rotated", "ignore"),
("INFO: configuration reloaded successfully", "ignore"),
# --- soon (15): 在恶化但还没坏 ---
("WARNING: disk 78% full, growing 2GB/week", "soon"),
("WARNING: TLS certificate expires in 14 days", "soon"),
("WARNING: 5% of requests exceed 1s; p95 SLO is 500ms", "soon"),
("WARNING: memory at 82% on 2 of 8 nodes", "soon"),
("WARNING: 3 failed login attempts for one user in the last hour", "soon"),
("WARNING: queue depth 500 and stable", "soon"),
("WARNING: nightly job took 3x longer than usual", "soon"),
("WARNING: replica lag 30 seconds", "soon"),
("WARNING: dependency with known CVE, not externally exposed", "soon"),
("WARNING: 2 pods restarted in 24h, OOM at 80% of limit", "soon"),
("WARNING: third-party API key expires in 7 days", "soon"),
("WARNING: log volume doubled; storage fine for now", "soon"),
("WARNING: 1 of 4 health checks flapping intermittently", "soon"),
("WARNING: stale lock file older than 6 hours", "soon"),
("WARNING: backup size dropped 10% compared to yesterday", "soon"),
# --- now (15): 已经坏了 ---
("ERROR: 8% of checkout requests failing with 500 for 20 minutes", "now"),
("ERROR: replica has not synced in 2 hours", "now"),
("ERROR: cron job missed 2 consecutive scheduled runs", "now"),
("ERROR: API p99 latency 12s against a 1s SLO for 30 minutes", "now"),
("ERROR: disk 94% full on the primary database host", "now"),
("ERROR: 3 nodes unreachable from monitoring", "now"),
("ERROR: outbound email queue at 20k, provider returning 421", "now"),
("ERROR: schema migration failed midway; app still on old schema", "now"),
("ERROR: webhook deliveries failing for one tenant since 08:00", "now"),
("ERROR: S3 upload failures at 15% for 45 minutes", "now"),
("ERROR: connection pool at 100%, requests queueing", "now"),
("ERROR: nightly ETL skipped 2 days in a row", "now"),
("ERROR: 2 of 5 replicas crashlooping", "now"),
("ERROR: search index is 3 days stale", "now"),
("ERROR: internal CA certificate expired; mTLS failing on one service", "now"),
# --- page (15): 叫人 ---
("CRIT: PostgreSQL primary and both replicas unreachable", "page"),
("CRIT: 100% of payment requests failing for 5 minutes", "page"),
("CRIT: admin role granted to an unknown principal", "page"),
("CRIT: ransomware canary file modified on the file server", "page"),
("CRIT: data checksum mismatch detected across 3 tables", "page"),
("CRIT: all API nodes returning 503", "page"),
("CRIT: no database restore point exists for the last 48 hours", "page"),
("CRIT: a private key was committed to a public repository 10 minutes ago", "page"),
("CRIT: 100k records deleted by an unidentified job", "page"),
("CRIT: production traffic is being routed to the staging database", "page"),
("CRIT: storage array offline, all 3 paths down", "page"),
("CRIT: CPU steal at 100%, all nodes unresponsive", "page"),
("CRIT: audit log tampering detected", "page"),
("CRIT: DNS hijack suspected — domain resolving to an unknown IP", "page"),
("CRIT: auth provider fully down; no new sessions can be established", "page"),
]

TICKET_NEW = [
# --- coding (15): 双性任务但归代码 ---
("Add structured logging to the import pipeline so failures are debuggable in production.", "coding"),
("Fix the off-by-one error that drops the last row of every paginated response.", "coding"),
("Implement exponential backoff in the SDK wrapper and cover it with tests.", "coding"),
("Replace the hand-rolled date parser with a well-tested library and fix the callers.", "coding"),
("Add a database index and rewrite the query that is causing the slow endpoint.", "coding"),
("Write a migration script that backfills the new column for existing rows.", "coding"),
("Make the CLI accept --config so operators stop editing source to change settings.", "coding"),
("Refactor the duplicate validation logic in three handlers into one shared function.", "coding"),
("Fix the race condition where two workers can process the same job.", "coding"),
("Add integration tests that exercise the full import-to-report path.", "coding"),
("Change the exporter to stream rows instead of loading the whole table into memory.", "coding"),
("Implement the retry queue the ops team asked for, with dead-letter handling.", "coding"),
("Patch the dependency that has the CVE and verify the tests still pass.", "coding"),
("Add pagination metadata to the API response so clients stop guessing.", "coding"),
("Fix the flaky test that fails roughly one run in ten.", "coding"),
# --- ops (15) ---
("Increase the connection pool size and restart the service to stop the queueing.", "ops"),
("Move the database to the new host and cut over with minimal downtime.", "ops"),
("Add disk capacity to the primary database host before it hits 100%.", "ops"),
("Set up offsite backups with immutable snapshots for the production database.", "ops"),
("Configure the load balancer health checks that are currently flapping.", "ops"),
("Rotate the expiring TLS certificates across all public endpoints.", "ops"),
("Scale the worker pool from 3 to 10 to drain the backlog.", "ops"),
("Install and configure monitoring agents on the three new nodes.", "ops"),
("Restore the database from last night's snapshot after the failed migration.", "ops"),
("Set resource limits on the containers that keep getting OOM-killed.", "ops"),
("Join the new VPS to the tailnet and verify SSH access.", "ops"),
("Fail over to the replica and promote it after the primary died.", "ops"),
("Reclaim space by archiving and removing logs older than 90 days.", "ops"),
("Apply the OS security patches and reboot the fleet in batches.", "ops"),
("Set up alert routing so CRIT alerts page the on-call phone.", "ops"),
# --- research (15) ---
("Determine why our measured accuracy differs from the vendor's published benchmark.", "research"),
("Compare three message queues and recommend one, with reasons and tradeoffs.", "research"),
("Investigate what caused Thursday's outage and write up the timeline.", "research"),
("Find out whether the row count discrepancy is a timezone bug or real data loss.", "research"),
("Survey how other teams do multi-tenant isolation in Postgres and summarize options.", "research"),
("Read the upstream changelog and list the breaking changes between 1.8 and 2.0.", "research"),
("Research the rate limits and pricing of the three LLM providers we are evaluating.", "research"),
("Dig through six months of logs to find the trend behind the growing queue depth.", "research"),
("Evaluate whether moving to the new storage backend is worth the migration cost.", "research"),
("Find the source of the duplicate records appearing in the reports table.", "research"),
("Compare backup providers that support immutable, offsite snapshots.", "research"),
("Read the RFC and determine whether our implementation conforms to the spec.", "research"),
("Collect published benchmarks for the two candidate models on classification tasks.", "research"),
("Trace how a record flows from MQTT ingest to the dashboard and document the gaps.", "research"),
("Investigate whether the flapping health check is a real fault or a probe misconfiguration.", "research"),
# --- review (15) ---
("Audit this pull request for privilege-escalation bugs before it merges.", "review"),
("Verify the migration is reversible by actually running the down path on a copy.", "review"),
("Check the vendor's accuracy claims against the measurements we collected ourselves.", "review"),
("Read this postmortem and say whether the root cause is actually identified.", "review"),
("Reproduce the reported bug independently and confirm whether it is real.", "review"),
("Review the incident timeline and flag any gaps between what is claimed and the logs.", "review"),
("Check whether the new API contract breaks any existing client.", "review"),
("Verify the claimed 90% test coverage by running coverage yourself.", "review"),
("Blind-review this change against its acceptance matrix and give a pass/fail with evidence.", "review"),
("Read the quarterly report and reconcile its numbers against the source database.", "review"),
("Audit the IAM policy changes for overly broad permissions.", "review"),
("Confirm the backup restore actually worked by verifying data, not just exit codes.", "review"),
("Review the threat model and point out the attack paths it misses.", "review"),
("Check whether the red-team findings were genuinely fixed or just silenced.", "review"),
("Independently score this candidate's submission without seeing its self-report.", "review"),
]

CRITERIA = {
 "command-risk-balanced": {
   "read_only": "Only reads or prints; changes nothing on any system.",
   "reversible": "Writes, installs, or starts something that is normally easy to undo (backup exists, package manager can remove it, service can be restarted).",
   "destructive": "Disables, removes, or changes configuration/permissions/data in ways that are costly to undo or affect security; a careful admin would want to confirm first.",
   "critical": "Destroys data at scale or takes systems down in ways that cannot be undone; no backup implied."},
 "alert-triage-balanced": {
   "ignore": "Expected noise, informational, or already resolved; no action needed.",
   "soon": "Worth a look during normal working hours; nothing is broken yet.",
   "now": "Something is degraded or failing; handle today before it gets worse.",
   "page": "Outage, data loss/corruption, or a security incident; wake someone now."},
 "ticket-routing-balanced": {
   "coding": "Writing, fixing, refactoring, or testing code.",
   "ops": "Servers, deployments, backups, monitoring, migrations, or infrastructure.",
   "research": "Investigating, comparing options, or summarizing findings.",
   "review": "Auditing, verifying, or challenging someone else's output."},
}
INSTR = {
 "command-risk-balanced": "Classify this shell command by blast radius. Choose the single best level.",
 "alert-triage-balanced": "How urgently does this operations alert need a human? Choose the single best level.",
 "ticket-routing-balanced": "Which kind of worker should own this task? Choose the single best category.",
}
PREFIX = {"command-risk-balanced": "dec004-cmd", "alert-triage-balanced": "dec004-alert", "ticket-routing-balanced": "dec004-ticket"}

allrows = []
for fam, items in [("command-risk-balanced", CMD_NEW), ("alert-triage-balanced", ALERT_NEW), ("ticket-routing-balanced", TICKET_NEW)]:
    for i, (text, gold) in enumerate(items, start=1):
        qid = "%s-%03d" % (PREFIX[fam], i)
        allrows.append({
            "id": qid, "family": fam, "state": text,
            "question": {"id": qid, "type": "choice", "instructions": INSTR[fam], "criteria": CRITERIA[fam]},
            "gold": gold, "source": "vesper-authored-2026-09-19-hard-tier", "difficulty": "hard"})

print("new:", len(allrows))
for fam in CRITERIA:
    sub = [r for r in allrows if r['family'] == fam]
    print(" ", fam, len(sub), dict(collections.Counter(r['gold'] for r in sub)))

# 合并旧 120 + 新 180 = 300
old = []
for n in ['command-risk-balanced', 'alert-triage-balanced', 'ticket-routing-balanced']:
    old += [json.loads(l) for l in open('/tmp/dec003/%s.jsonl' % n)]
merged = old + allrows
print("\nTOTAL", len(merged))
for fam in CRITERIA:
    sub = [r for r in merged if r['family'] == fam]
    print(" ", fam, len(sub), dict(collections.Counter(r['gold'] for r in sub)))
with open('/tmp/dec003/all-300.jsonl', 'w') as f:
    for r in merged:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print("saved /tmp/dec003/all-300.jsonl")
