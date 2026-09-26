# Verification and Completion

Select checks from the actual site and requested mode. In audit mode report findings without modifying files. In build/revise mode repair failures within scope and repeat affected checks. Record artifact/version, test conditions, observation, and pass/fail/unverified status. A planned check is not a result.

## Content and visual inspection

Inspect the rendered page with its actual copy and media. Check the opening, transitions, final hero state, lower sections, navigation, and footer. Confirm identity and factual claims against the brief. Review headings, error messages, forms, and action labels as carefully as the hero.

Inspect representative wide, narrow, and short viewports, such as 1440 by 900, 1280 by 720, 390 by 844, and 844 by 390, adapting to the audience. Include zoom and long text. Record exact sizes tested. Device emulation is not a physical-device test.

Look for collisions, accidental empty regions, truncated glyphs, incoherent imagery, inconsistent equivalent components, and crop damage. Keep deliberate brand choices while removing decoration that weakens hierarchy or behavior. A distinctive signature should have a purpose; no site needs every possible effect.

## Accessibility and readable motion

Check semantic landmarks, heading order, accessible names, skip navigation, keyboard reachability, visible focus, and sensible reading order. Decorative media should not become an unnecessary tab stop; meaningful video needs appropriate controls and alternatives for its content. Do not hide essential information with `aria-hidden` merely because it is visually animated.

For normal text, require at least 4.5:1 contrast; qualifying large text can use 3:1. Large text means at least 18 point or 14 point bold, approximately 24 or 18.7 CSS pixels. Apply the appropriate threshold to each caption, not one universal 3.5:1 floor. See [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Check meaningful control boundaries and indicators separately from text.

Inspect composited text regions across the relevant frames, crops, and transition states. Sampling opening/middle/end frames is a diagnostic, not exhaustive proof. If uncertain, provide a backing surface or move the text to a region with predictable contrast. A screenshot with hidden glyphs may omit their shadow; a flat-alpha mathematical estimate may omit gradient falloff. Label approximations and avoid claiming formal accessibility conformance from a partial test.

Test keyboard and touch equivalents for custom interactions. Keep focus visible and avoid horizontal clipping of controls. A touch-target design target around 44 CSS pixels is useful, but verify the actual layout and spacing rather than confusing a design preference with a universal standard.

## Motion, failures, and lifecycle

| Scenario | Evidence to seek |
| --- | --- |
| Initial load and direct entry midway | Readable content immediately; media synchronizes to the current position when ready. |
| Slow and fast forward/reverse scrolling | Caption holds remain useful; no accumulating seeks, missed end state, or visible seam failures. |
| Keyboard paging and anchor jumps | Ordinary navigation works; essential information remains accessible even if beats are skipped. |
| Reduced motion at load | Designed static reading path; unnecessary heavy motion assets are not requested. |
| Preference changed both ways mid-session | Drivers stop/restart correctly; no overlapping captions, stale pinned states, or blank stage. |
| Resize and orientation changes | CSS and controller choose the same mode; crop, spacing, and asset policy remain coherent. |
| Video blocked, invalid, or stalled | Loading state ends in a usable alternative with content and actions intact. |
| Script unavailable | Baseline content and navigation remain accessible. |
| Hidden tab, off-screen section, return | Decorative work pauses; resuming does not cause a jump or free-running loop. |
| Route exit and re-entry in a framework | Listeners, timers, fetches, and object URLs are cleaned up; remount does not duplicate controllers. |

Use actual supported browser controls for emulated media, input, and request blocking when available. Avoid editing accepted media just to simulate a failure when request interception provides a reversible check. Inspect pixels and behavior, not only DOM variables. A changing target time is not proof of visibly decoded footage.

## Functions and integrations

Exercise links, menus, buttons, and meaningful custom controls. Verify real form pending/error/success states without contacting people or submitting real data beyond the user's authorization; use a test endpoint or appropriate stub when needed and record that limitation. An accessible demo state must explicitly say it does not send a message.

Check responsive navigation, focus restoration, form labels, validation errors, and whether the requested action reaches the intended destination. Preserve the existing site's required behavior. Use the project's normal build, type, or runtime checks when applicable; do not claim a framework build passed from reviewing source alone.

## Performance evidence

Record total transferred resources, media size, initial rendering behavior, and observed responsiveness under stated conditions. Distinguish cold from cached runs, local from remote previews, and emulated from actual network/device conditions. A single document's byte count is not total page weight. A successful file download is not a page-load measurement.

Test whether the poster and useful content appear before heavy media finishes. Look for layout shifts, main-thread work, repeated downloads, and large memory requirements. Confirm the static path does not request assets it never displays. Do not promise a speed score or subsecond load time without measuring it.

## Completion and handoff

Deliver the requested artifact first. Include the available preview, important changed behavior, meaningful checks, and material limitations. If a local server is required for full behavior, use a supported existing preview tool and provide the actual link. Explain when opening a file directly exercises only the static path. If previewing is unavailable, deliver source with explicit runtime limitations.

Keep the design package, approved copy, asset origins, processing settings, and outstanding integration requirements available with the project. Use an already supplied canonical URL only where appropriate; do not invent absolute metadata URLs. Ordinary titles, descriptions, and a preview image can still be prepared.

Before finishing, review as a first-time visitor: is the subject clear, can the visitor use the site, does the motion contribute, and does the entire page feel coherent? Ask for feedback when useful without substituting the user's review for your own checks. Stop after the requested outcome and bounded polish, rather than adding an indefinite improvement loop.
