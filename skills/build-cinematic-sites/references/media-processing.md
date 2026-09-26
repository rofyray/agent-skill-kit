# Media Processing

Use an available editor or command-line processor only when needed. The examples below require a shell, FFmpeg with libx264, and FFprobe. Check available versions and filters first. They are configurable recipes for local files, not automatic installation instructions or a claim that one encoding fits every project.

Use quoted paths and separate output files. Create the intended output directories before running. Preserve raw assets and review files outside the public asset directory. Commands use `-n` to avoid silently overwriting an accepted file. Choose new version names for revisions.

## Inspect the input

```text
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,sample_aspect_ratio,color_space,color_transfer,color_primaries:format=duration,size -of json "raw.mp4"
```

Record actual dimensions, cadence, duration, aspect, and color characteristics. Check rotation and HDR material when applicable before deciding how it will become a web asset. Inspect visually; metadata cannot detect deformed objects or bad composition.

## Encode a seekable web candidate

For an inspected SDR source, this produces an H.264 candidate at an explicit 30 fps with frequent keyframes. Adapt scale/crop and cadence to the approved material rather than distorting its aspect:

```text
ffmpeg -n -i "raw.mp4" -map 0:v:0 -vf "fps=30,scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1" -c:v libx264 -crf 20 -preset slow -g 8 -keyint_min 8 -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart -an "hero-scrub.mp4"
```

This assumes square-pixel input or an approved conversion to it; normalize anamorphic input deliberately. For another output cadence, reassess keyframe spacing in time. Shorter keyframe intervals generally improve random access at a file-size cost; browsers can decode interframes, so they are not restricted to displaying keyframes. Measure seeking in the actual browser.

Set size and quality budgets from the page and target devices. Tune one factor at a time, starting with quality and dimensions while retaining usable seek behavior. Inspect both moving detail and smooth gradients. Do not promise that a given CRF or duration yields a particular file size. Fast-start metadata does not make a fully downloaded Blob display before that download finishes.

For a trim, add the approved duration as an output `-t` argument in the same encode. Rebuild dependent posters, endings, and progress maps from the final result. Local editing may fix a weak tail without a new generation.

## Poster, chosen review frame, and exact decoded tail

```text
ffmpeg -n -i "hero-scrub.mp4" -frames:v 1 -update 1 "hero-poster.png"
ffmpeg -n -i "raw.mp4" -ss 2.4 -frames:v 1 -update 1 "review-middle.png"
ffmpeg -n -i "raw.mp4" -vf "reverse" -frames:v 1 -update 1 "last-frame.png"
```

The last command decodes and buffers the clip, so use it only for short clips that fit available memory. For long inputs, use a frame-aware editor or enumerate decoded timestamps and extract the verified final frame. Seeking a fixed fraction of a second before EOF selects a near-tail frame, not necessarily the exact last one. When chaining, choose the actual handoff frame intentionally and retain it losslessly.

Choose a static hero for composition, not merely because it is frame zero. Inspect it with the site's copy, header, and intended crop. Preserve a separate full-quality reference for generation; optimize only the site's displayed derivative.

## Join normalized segments once

Normalize the clips to the same dimensions, cadence, pixel aspect, color treatment, and zero-based timestamps. Decide whether to crop or pad from the design. This example pads two SDR clips to a shared 1920 by 1080 canvas; choose a different treatment if padding violates the composition:

```text
ffmpeg -n -i "segment-a.mp4" -i "segment-b.mp4" -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS,fps=30[a];[1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]" -map "[v]" -c:v libx264 -crf 20 -preset slow -g 8 -keyint_min 8 -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart -an "hero-joined.mp4"
```

Color metadata and pixel-format conversion alone do not perform every needed color-space or HDR conversion. Resolve those separately when the inputs differ. Concatenation can normalize encoding but cannot fix discontinuous geometry, lighting, or motion.

For a deliberate dissolve, replace the final concat filter with `xfade=transition=fade:duration=0.25:offset=5.75` only when the first normalized clip is exactly six seconds long. General rule: offset equals the accumulated timeline duration minus the overlap. Recompute from actual processed durations; every overlap shortens the result. Inspect for ghosting at every join and test reverse scrubbing. Do not copy fixed offsets into clips of unknown length.

Copying already encoded segments without re-encoding requires compatible stream parameters and timestamps. Use that route only when compatibility and the resulting seams are verified. Otherwise join the normalized sources and encode once.

## Web stills and exact graphics

For photographic source material at least 1600 pixels wide, this is one optional JPEG derivative:

```text
ffmpeg -n -i "photo-source.png" -vf "scale=1600:-2" -frames:v 1 -q:v 2 -update 1 "photo-web.jpg"
```

Choose dimensions for the actual rendered size and pixel density. Avoid unnecessary upscaling. Use responsive derivatives when useful. Keep transparency and sharp UI/lettering in an appropriate lossless or vector format. Inspect color, edges, and transparency after conversion; never infer alpha from a checkerboard visible in the image.

## Verify processed outputs

Run FFprobe on every final asset, inspect the processed frames, and decode the complete video to catch errors:

```text
ffmpeg -v error -i "hero-scrub.mp4" -f null -
```

Confirm duration, dimensions, cadence, audio presence/absence, visual identity, joins, and file size. For a quiet ending, inspect the actual tail in motion; frame-difference statistics can help locate activity but cannot determine artistic arrival or distinguish intended ambient movement from a mistake. Review forward and reverse scrubbing in the final page before treating an encode as accepted.

Filter requirements and options should be checked against the installed version and [FFmpeg's filter documentation](https://ffmpeg.org/ffmpeg-filters.html), particularly `concat`, `xfade`, `reverse`, `fps`, and `setpts`.
