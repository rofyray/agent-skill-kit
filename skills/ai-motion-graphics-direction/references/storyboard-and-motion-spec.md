# Storyboard and Motion Specification

## Plan observable states

For each beat record its purpose, duration, entering state, focal subject, action trigger, motion path, contact or transformation, exact copy IDs, reference IDs, audio cue, exit state, and continuity into the next beat. Keep camera, object motion, graphic movement, and sound separately identifiable even when combined into a readable prompt.

Specify the causal order. For an assembly, the next component lands on the state left by the prior component. For an explainer, a cause is demonstrated before its effect. For typography, arrival ends before the reading hold begins; the exit cannot consume the full reading window. Do not force long phrases into arbitrary two-second beats.

Use time in seconds for a production timeline and frames only after the intended cadence is known. Quantize events to actual frames when exporting. A prompt can communicate timing intent but does not prove the resulting generator honored subsecond cues. A deterministic editor owns exact frame placement.

For narration, time a plausible reading or use the actual approved recording. Identify semantic cues by phrase as well as approximate time so the sequence can be aligned after synthesis. Never speed a long script into unintelligibility to preserve a guessed duration.

## Style frames and storyboards

Choose frames that answer real questions: opening occupancy, a high-risk transition, complex overlap, peak action, densest typography, and final state. A nine-frame board is useful for a multi-beat short, but adapt the count. State time, frame ratio, crop, copy, reference roles, and what the frame tests. Keep storyboard panel numbers and labels outside the image supplied as a generation reference.

An animatic tests reading time and narrative rhythm. Still frames do not prove motion, tracking, or lip sync. Approve design and pacing through the user's requested workflow; reuse existing approvals. For a direct prompt request, describe the recommended board without generating one unasked.

## Segmentation

Choose seams at intentional cuts, completed actions, occlusions, or designed transition boundaries. Avoid splitting mid-morph, during an unresolved impact, or between a spoken syllable and its matching mouth shape. Each segment repeats necessary identity and style constraints and has explicit entering and leaving states. Use end or start frames only with supported conditioning and inspect the seam.

An assembled sequence may simulate a continuous take, but its visual continuity still needs verification. Do not downgrade an explicit one-take requirement into visible cuts without identifying the changed treatment. A long editorial piece usually needs scenes and a shared data and typography system, not one enormous prompt.

## Optional machine-checkable plan

Use the helper for multi-beat timelines, exact copy, references, or percentage graphics when execution adds value. It reads JSON without modifying files. Python 3.10+ and the standard library are sufficient. No model, network, fonts, browser, or editor is needed.

From the skill folder:

```text
python3 scripts/validate_motion_plan.py "/absolute/path/motion-plan.json"
python3 scripts/validate_motion_plan.py - --format json
```

The second form reads JSON from standard input. Exit 0 means the declared plan passes; exit 1 means a plan error; exit 2 means the file or JSON could not be read. If Python or local files are unavailable, use the table below to perform the checks manually. This is a compact validation manifest, not the full creative treatment or a provider request schema.

| Field | Contract |
| --- | --- |
| `schema_version` | Integer `1`. |
| `duration_seconds` | Finite number greater than zero. |
| `fps` | Optional finite number greater than zero; identifies intended cadence but does not enforce frame alignment. |
| `references` | Array of objects with unique nonempty `id` and nonempty `role`. Empty is valid. |
| `copy` | Array of objects with unique nonempty `id` and exact nonempty `text`. Empty is valid for text-free work. |
| `beats` | Nonempty, chronological array of objects with unique `id`, numeric `start` and `end`, nonempty `action`, `copy_ids`, and `reference_ids`. |
| Beat `copy_ids` and `reference_ids` | Arrays of declared IDs, with no duplicate within the same array. Use empty arrays when none are needed. |
| Beat `copy_text` | Optional object mapping active copy IDs to text as emitted by a compiled prompt. When supplied, every value must exactly equal its declaration. Use for checking compilation, not for translation. |
| Beat `hold` | Optional boolean. `true` declares a reading or ending hold; it does not assert the whole image is frozen. |
| `final_hold_seconds` | Optional nonnegative duration. The contiguous declared hold at the end must be at least this long. Allocate any later fade or tail separately; if it follows the hold, do not declare this field as a final hold. |
| `percent_bars` | Optional array of objects with unique `id`, `percent` between 0 and 100, positive `track_length`, and `filled_length` between 0 and the track length. Both lengths use the same unit. |
| `metadata` | Optional object at the root or within a reference, copy item, beat, or bar. Holds creative notes or source links outside the helper's checks. |

Reject undeclared fields outside `metadata` so misspelled controls do not silently pass. References and copy IDs are local to their respective catalogs. Beat intervals must cover the full duration without gaps or overlaps, within 0.000001 seconds of numeric tolerance. Design intentional overlaps as layer events inside a beat, not overlapping beat intervals. A bar's fill must equal its percentage of its track within 0.000001 percentage points.

Example, a fictional survey supplied in an approved brief:

```json
{
  "schema_version": 1,
  "duration_seconds": 8,
  "fps": 30,
  "references": [{"id": "style", "role": "palette and typography only"}],
  "copy": [{"id": "result", "text": "40% chose refill"}],
  "beats": [
    {"id": "reveal", "start": 0, "end": 6, "action": "Reveal the survey result and complete the chart.", "copy_ids": ["result"], "reference_ids": ["style"]},
    {"id": "read", "start": 6, "end": 8, "action": "Hold the complete result for reading.", "copy_ids": ["result"], "reference_ids": ["style"], "hold": true, "copy_text": {"result": "40% chose refill"}}
  ],
  "final_hold_seconds": 1,
  "percent_bars": [{"id": "refill", "percent": 40, "filled_length": 80, "track_length": 200}],
  "metadata": {"source": "User-approved fictional survey fixture: 80 of 200 replies."}
}
```

The helper does not inspect pixels, spoken words, chart labels embedded in prose, source truth, stacked totals, safe zones, simultaneous layer events, or physical feasibility. A passing manifest cannot certify a video. Inspect those properties in the treatment and final media. Do not imply unsupported manual checks were automated.
