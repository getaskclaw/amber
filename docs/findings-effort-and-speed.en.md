# Three findings: effort bands, token bills, wall time

> Moved from the front-page [README](../README.en.md); text unchanged. 中文: [findings-effort-and-speed.md](findings-effort-and-speed.md)

**⑤ A counterintuitive finding, with limits** — on the families measured so far, high is the sweet spot and top bands backfire (three of the four families plotted). A pattern, not a law: swe-2's band curve is monotone to the top (medium 15 < high 16 < max 18, [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md)), k3 is a flat-line family (low 15 ≈ high 17; its failing set differs from high by 2 cases, one of them a line-riding vision case that jitters; tokens and wall-clock are about half of high's — the band is chosen by cost and speed, see [amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)); and on some models the band barely moves the score — pick your band by cost and speed, not score; the WorkBuddy lane, Kimi's K2.8, and the stepfun plan lane all have only one band scored so far, no curve to plot (the stepfun endpoint's usage carries no `reasoning_tokens`, so `high` is declared but the burn is unverifiable).

![effort curves](images/effort-curves-20260911.en.png?v=20260917)

**⑥ Score vs thinking budget** — same band (high), same library, and the output-token bill spans 17× (147K vs 2.5M) for scores within a case of each other (token totals from each lane's published issue). The axis is tokens, not dollars: billing is mixed (subscription lanes have no marginal price; the devin and workbuddy lanes report no usage at all, so swe-2 and the wb pair sit this one out). Within a family, more tokens bought no score (luna flat; astra's top bands lose four cases); across families the shape varies — which is why ⑤ is a pattern, not a law.

![score vs thinking budget W37](images/score-vs-tokens-2026-w37.en.png?v=20260918)

**⑦ High TPS only holds on easy problems** — same library, per-problem wall time (log axis): a vendor's high TPS is decode speed measured on easy problems, and hard problems mean more thinking, slower effective decoding, and ballooning wall time. Dot = one problem, bar = median; problem IDs are anonymized (the mapping stays private; per-point data in [wallclock-2026-w37.csv](data/wallclock-2026-w37.csv)). On the families measured so far, swe-2 gets slower with each higher band yet solves more (median 82 s → 280 s), while v4.1-flash backfires at the top band (68 s median, two fewer solves). Shapes vary by family — a pattern on these families, not a law.

![High TPS only holds on easy problems](images/wallclock-strip-2026-w37.en.png?v=20260911)

Chart sources (`.puml` for PlantUML, `.vega-lite.json` / `.vg.json` for Vega) sit next to the PNGs in `docs/images/` — edit a source, re-render, done.
