# 三个发现：思考档位、token 账单、耗时

> 从首页 [README](../README.md) 移来，正文未改。English: [findings-effort-and-speed.en.md](findings-effort-and-speed.en.md)

**⑤ 一个反直觉发现，但有边界** —— 已测家族里「想更久 ≠ 考更好」：high 档是甜点，顶档反噬（图中四家族其三）。是经验规律，不是定律：swe-2 的档线单调到底（medium 15 < high 16 < max 18，见 [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md)）；k3 是平线家族（low 15 ≈ high 17，差 2 案其一为骑线案抖动，token/墙钟约为 high 一半——选档按成本和速度，见 [amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)）；也有的模型全档随机带，选档按成本和速度，不按分；WorkBuddy 道、Kimi 的 K2.8、以及 stepfun plan 道目前都只考了一档，尚无曲线可画（stepfun 端点 usage 不返回 `reasoning_tokens`，声明 high 而燃烧量不可验）。

![effort 曲线](images/effort-curves-20260911.png?v=20260917)

**⑥ 分数 × 思考预算** —— 同 high 档、同全库，输出 token 账单跨 17 倍（147K vs 2.5M），分数却差不过一案（各道 token 数出自其期文）。横轴是 token 不是美元：各家计费混杂（订阅道没有边际价；devin 与 workbuddy 道都不上报用量，swe-2 与 wb 双模不上这张图）。家族内部，更多 token 没换来分（luna 平线、astra 顶档反噬）；家族之间形状各异——所以 ⑤ 只是经验规律。

![分数 × 思考预算 W37](images/score-vs-tokens-2026-w37.png?v=20260918)

**⑦ 高 TPS 只在简单题上成立** —— 同一题库、逐题耗时（log 轴）：厂商的高 TPS 是简单题上的吐字速度，难题想得多，吐字当场变慢，耗时跟着翻倍。点=一题，横线=中位数；题号匿名（编号对照留私域，逐点数据见 [wallclock-2026-w37.csv](data/wallclock-2026-w37.csv)）。已测家族里，swe-2 档越高越慢但破题越多（medium 82s → max 280s，中位数）；v4.1-flash 顶档反噬（中位 68s 反掉两案）。形状因家族而异——这只是已测家族的样子，不是定律。

![高 TPS 只在简单题上成立 W37](images/wallclock-strip-2026-w37.png?v=20260911)

图的源文件（PlantUML 的 `.puml`、Vega 的 `.vega-lite.json` / `.vg.json`）就放在 PNG 同目录，改图 = 改源文件再渲染。
