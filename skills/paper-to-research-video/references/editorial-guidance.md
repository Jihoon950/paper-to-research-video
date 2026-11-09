# Editorial decisions for research films

Use this when designing scenes or resolving ambiguity in evidence.

## Claim hierarchy

For each key result, record the population/setting, control or baseline, intervention, unit, aggregation window or statistic, denominator, direction, and uncertainty if reported. If the paper reports a graph without underlying data, animate the graph or a faithfully extracted subset; do not draw precise interpolated points and imply they were measured. Keep results from separate experiments visually separate. Include null or adverse results when leaving them out would reverse the paper's conclusion.

An author-proposed mechanism is a hypothesis unless experimentally isolated. An architectural drawing is not live telemetry. A screen recording from a different run or day is archival. If a diagnostic trace samples one representative event, label it as such rather than as a typical runtime. When using a conceptual timeline to explain a failure, label it “Illustration” or an equivalent term.

## Film grammar

- Opening (usually 0–6 s): paper identity and the concrete question. An animation hook may precede the full title, but the title and authors still need a readable moment.
- Establish the system: where input arrives, what computes or changes, and what is measured. Use only the components necessary to understand the result.
- Demonstrate the tension: make the baseline visible. Animate cause and effect, but do not portray a hypothetical failure as observed.
- Reveal the method: show the actual design or policy choice and its inputs. Avoid a cluster of technology logos as the main “result.”
- Prove the claim: the key chart must state metric, condition, and baseline in large type. Reveal one comparison at a time; use data labels where possible rather than microscopic axes.
- Resolve: show benefit, cost, and applicability boundary in the same visual language. Close on a scientific claim, not a generic slogan.

Match the paper: some work needs a hardware tour, some a workflow animation, and some a mathematical idea. Allocate time accordingly. A video of static cards with moving backgrounds is still a slide deck. Use motion to track an entity, change a parameter, follow a data flow, or expose the next piece of evidence.

## Visual evidence labels

Place a small but readable persistent badge on scenes that could be mistaken for recorded experiments: `Recorded run`, `Archived recording`, `Paper figure`, `Simulation`, or `Illustration`. A measured number should have a short source note on-screen or in an accompanying source ledger. Preserve the paper's terminology and units. The badge is not permission to invent data.

Do not fabricate a live dashboard to stand in for absent data. A designed dashboard may show supplied logs or plots as playback if the source and time mapping are accurate and labeled. If audio is included, captions and screen text should not contradict it.

## Quality pass

Check at full resolution and at roughly one-third preview size. Main labels and values must remain readable. Ensure adequate contrast, avoid more than one primary visual question per moment, and leave a beat after numbers appear. Check every first/last frame of a cut and the first frame after a transition. A source/rights inventory and completed claim ledger are part of the deliverable, not decorative paperwork.
