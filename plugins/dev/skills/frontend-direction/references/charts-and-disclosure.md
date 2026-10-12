# Choose the representation before the decoration

Select a visual by the question and data, not by available chart components. Treat [charts.csv](charts.csv), the UI UX Pro Max catalog, as an on-demand shortlist; its suggested libraries and thresholds are not dependencies or universal rules.

| User question | Start with | Keep visible |
|---|---|---|
| What is the value/status? | Number or short labeled status | Unit, period, scope, estimate/freshness when material |
| Which category costs/performs more? | Sorted horizontal bars | Category names, common scale, values/units |
| How did it change over time? | Line chart | Time scale, units, breaks/missing data |
| How is a whole divided? | Stacked bar; pie/donut for a few clear shares | Total, shares, denominator; no color-only distinction |
| What are the exact values or many attributes? | Table | Headers, units, sort/filter state |
| How are two variables related? | Scatter plot | Axes, units, sample context; no unsupported causal claim |
| How does a total turn into another? | Waterfall | Starting total, signed contributions, final total; no double counting |
| What happens next / what connects to what? | Timeline, flow or architecture diagram | Meaningful sequence/links, short node labels |
| Where is it located? | Map when location matters | Scale/context and accessible list equivalent |

Use a sentence or simple value when it already answers the question. Avoid 3D, gauges without a useful reference range, decorative Sankeys, arbitrary bubble areas and a separate card for every number. Encode size by area for area-based marks; keep bar baselines honest and disclose meaningful axis truncation.

## Detail through interaction

- Level 1 answers the main question; do not surround it with paragraphs repeating the chart.
- Level 2 selects a category, period or component for its breakdown.
- Level 3 exposes the relevant formula, assumptions, sources or history.
- Keep labels and a discoverable detail control outside hover. Support focus, Enter/Space, touch and a return path.
- Include a concise text summary or accessible data equivalent; do not render a full duplicate data table by default unless exact comparison is the task.
- Keep qualifiers that change the conclusion in level 1. Never simplify by hiding uncertainty, omitted costs or a different denominator.
- For print/export, keep the main conclusion understandable without interaction; make required supporting detail available in the export or companion document.

Record the question, chosen representation and disclosure behavior in the companion spec. Reuse the project's chart library when one exists.
