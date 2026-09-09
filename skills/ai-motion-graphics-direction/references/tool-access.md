# Tool Access and Provider Adaptation

## Separate directing from rendering

The host's reasoning model directs and compiles. The image, video, audio, 3D, or editing model performs its supported operation. A platform or aggregator exposes particular endpoints and workflow features. An MCP connection is one access route, not a video model or a guarantee of automatic production.

Respect the user's choices independently: planning model, platform, render model and version, editor, and output destination. The skill works through native tools, a connected plugin or MCP service, an API or CLI, a supported browser interface, or a manual prompt handoff. Check which are actually available; do not assume a local shell, browser, account, or editor exists.

## Capability discovery

Inspect the active tool and the exact selected model's official schema for:

- Generation type: text, image, reference, video editing, extension, motion control, lip sync, audio, 3D, or deterministic animation.
- Reference roles and limits: identity, style, motion, geometry, first frame, last frame, image count, clip count, audio count, formats, size, and duration.
- Controls: prompt length and language, aspect, resolution, native fps, duration, cuts, seed, negatives, audio, and any documented camera or motion settings.
- Output: actual media type, raster or editable geometry, alpha support, audio track, source layers, asynchronous state, expiry, status lookup, downloads, and persistence.
- Practical fit: available credit or budget context, expected cost when exposed, authentication, asset processing destination, and project permissions.

Do not infer that a model available in a platform's website is available through its API or connected tool. A renderer supporting reference images may not support end frames or motion references. A video's 3D appearance does not establish mesh output.

Use current official documentation to resolve missing capability details. Avoid hardcoded rankings, prices, model versions, or provider-wide promises. Keep factual lookups close to production because schemas and catalogs change.

Official lookup entry points, not runtime dependencies:

- Higgsfield workflows and access: https://higgsfield.ai/creator-hub/help-center/tools/which-higgsfield-tool-should-i-use
- Higgsfield MCP entry: https://higgsfield.ai/mcp
- fal model catalog and per-endpoint schemas: https://fal.ai/models
- fal API documentation: https://docs.fal.ai/
- Kie per-model API documentation: https://docs.kie.ai/
- WaveSpeed model catalog: https://wavespeed.ai/models
- WaveSpeed model IDs and schema guidance: https://wavespeed.ai/docs/what-are-models

The same discovery procedure applies to another provider or a user's local model. This package contains no fixed provider dependency and does not supply credentials.

## Connect only as needed

For connection help, identify the current host and chosen service, inspect available connectors, and use the host's current documented setup path. Web-hosted connectors and local CLI configurations may have different reachability and authentication. Do not assume one client's setup propagates to another. Check the resulting tool list and authentication state before claiming connection success.

Use an already connected suitable service where it satisfies the user's choices. Installing this skill does not authorize account creation, a new subscription, or a provider switch. Keep credentials out of prompts, command arguments, logs, and manifests. Use the host's supported credential mechanisms. Send only the assets required for declared reference roles; retain existing permission for an authorized destination rather than asking repeatedly.

## Route by the missing capability

| Gap | Response |
| --- | --- |
| Clip too short or prompt too long | Segment at natural seams; restate identity and leaving states. |
| Exact type or chart unsupported | Use a clean plate and a controlled graphics layer. |
| No end-image conditioning | Composite the approved end card with a designed transition. |
| No voice or lip-sync support | Use a separately authorized audio and lip-sync path or preserve source performance. |
| No faithful geometry | Use approved model renders or a limited supported view; flag conceptual additions. |
| No editable vectors or meshes | Deliver raster video accurately labeled; provide a construction specification if needed. |
| No authenticated generator or inspection tool | Return a complete manual package and identify which output or check remains unavailable. |

Do not select a different model silently when it changes cost, capability, reference handling, or output. If the chosen model cannot meet an essential constraint, explain the viable route and any decision that actually remains with the user.

## Execute and persist

Map inputs to the actual schema, verify required attachments, submit within the requested scope, and record the returned job ID and settings. Use supported status checks or callbacks with reasonable backoff. On an ambiguous submission response, check for the existing job before retrying so a network failure does not duplicate paid renders.

A completed status establishes that an output exists, not that it passes the brief. Retrieve through the host's authorized mechanism, inspect media when possible, and save into the requested project destination when that is part of the task. Preserve originals and version revisions. Check expiring outputs and report inaccessible media accurately.

Stay within the agreed attempts or budget. An additional paid generation needs existing authorization or a new user choice; diagnostic reads and local repairs within scope can continue. Do not publish, share, or contact people as an implied part of video creation.
