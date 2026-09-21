import json, collections

TICKET = [
# coding (10)
("Add a --dry-run flag to the deploy script so operators can preview changes before applying them.", "coding"),
("Fix: the import job crashes with KeyError when a CSV row is missing the 'species' column.", "coding"),
("Refactor the auth middleware so session checks live in one place instead of four.", "coding"),
("Write a Python script that reads the MQTT topic list and emits a Markdown table of topics and payload shapes.", "coding"),
("The pagination cursor breaks on page 3 when sort order is descending. Find and fix it.", "coding"),
("Add unit tests for the date-parsing helper, which currently has none.", "coding"),
("Upgrade the HTTP client library to 2.x and fix the breaking API changes.", "coding"),
("Implement a retry with exponential backoff around the payment provider call.", "coding"),
("The dashboard chart renders blank when the dataset has a single point. Debug and fix.", "coding"),
("Change the API to return 409 instead of 500 when a unique constraint is violated.", "coding"),
# ops (10)
("The nightly backup job has not completed for two nights. Investigate and get it running again.", "ops"),
("Provision a new VPS, install Docker, and join it to the tailnet.", "ops"),
("Postgres disk usage is at 81%. Find what is growing and reclaim space.", "ops"),
("Rotate the expiring TLS certificate on the public site.", "ops"),
("Set up monitoring and alerting for the new ETL pipeline.", "ops"),
("Migrate the database from the old host to the new one with minimal downtime.", "ops"),
("The service is timing out under load. Profile it and tune the connection pool.", "ops"),
("Add a health check endpoint and wire it into the load balancer.", "ops"),
("Restore the database from last night's snapshot after a bad migration.", "ops"),
("Harden SSH on the new node: disable password login, add fail2ban.", "ops"),
# research (10)
("Find out which of the three candidate vector databases best fits our query patterns and write up a comparison.", "research"),
("Summarize what changed in the upstream library between 1.8 and 2.0.", "research"),
("Look into why our Kaggle-style leaderboard scores disagree with the vendor's published numbers.", "research"),
("Research how other teams handle multi-tenant row-level security in Postgres and report options.", "research"),
("Find the current rate limits and pricing for the three LLM providers we are evaluating.", "research"),
("Dig into the logs and figure out what actually caused Thursday's outage.", "research"),
("Survey the market for offsite backup providers that support immutable snapshots.", "research"),
("Read the RFC and explain whether our implementation matches the spec.", "research"),
("Collect benchmarks comparing the two candidate models on classification tasks.", "research"),
("Investigate whether the discrepancy in report counts comes from timezone handling.", "research"),
# review (10)
("Audit this pull request for security issues before we merge it.", "review"),
("Check whether the new importer handles malformed input gracefully, and report what it gets wrong.", "review"),
("Review the migration plan and point out anything that could lose data.", "review"),
("Verify the claimed test coverage by actually running the suite and reading the results.", "review"),
("Independently reproduce the bug report and confirm whether it is real.", "review"),
("Read this incident postmortem and tell me whether the root cause is actually identified.", "review"),
("Check the vendor's benchmark claims against our own measurements and report any gaps.", "review"),
("Review the new API contract for backwards-compatibility breaks.", "review"),
("Double-check the numbers in this quarterly report against the source data.", "review"),
("Blind-review this change: does it meet the acceptance matrix, yes or no, with evidence?", "review"),
]

rows = []
for i, (text, gold) in enumerate(TICKET, start=1):
    qid = "dec003-ticket-%03d" % i
    rows.append({
        "id": qid, "family": "ticket-routing-balanced", "state": text,
        "question": {"id": qid, "type": "choice",
            "instructions": "Which kind of worker should own this task? Choose the single best category.",
            "criteria": {
                "coding": "Writing, fixing, refactoring, or testing code.",
                "ops": "Servers, deployments, backups, monitoring, migrations, or infrastructure.",
                "research": "Investigating, comparing options, or summarizing findings.",
                "review": "Auditing, verifying, or challenging someone else's output."}},
        "gold": gold, "source": "vesper-authored-2026-09-19", "difficulty": "clear"})

print(len(rows), collections.Counter(r['gold'] for r in rows))
with open('/tmp/dec003/ticket-routing-balanced.jsonl', 'w') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print("saved")
