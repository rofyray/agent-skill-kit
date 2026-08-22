# Create and Edit Images Help

Use this reference to answer help mode. Present the explanation, modes, start guidance, and examples in a detailed but scannable user-facing form. Include every named mode and both example columns; do not collapse or omit them for brevity. Do not generate or edit an image while answering help.

## What this skill does

This skill creates photorealistic images and makes precise, physically believable edits. For edits, it inspects the source, defines the exact change, preserves every unrequested detail, integrates the change through correct scale, perspective, lighting, contact, texture, and occlusion, and verifies the resulting artifact when visual inspection is available.

When the host has an image tool, the skill creates the artifact rather than returning only instructions. When the user wants a prompt—or no suitable tool exists—it produces a structured prompt and clearly states that no image was generated.

## Modes

| Mode | Use it for |
| --- | --- |
| `create` | Generate a new image from a description. |
| `edit` | Change a supplied image, remove something, replace content, relight, restyle, restore, or combine references. |
| `revise` | Correct a defect in a prior result while preserving the parts that already work. |
| `prompt-only` | Write a ready-to-run prompt for another image model without generating the image here. |
| `help` | Display this guide without generating, editing, or revising an image. |

The user can name a mode or describe the outcome naturally. No slash command is required.

## Start here

For a new image, describe the subject, setting, intended use, composition, and aspect ratio if they matter. For an edit, attach every required source and state what should change and what must remain exact. For a revision, provide the original and latest result when both are needed to restore drift.

The skill asks only about ambiguities that materially affect the visual result. Image creation, editing, and visual verification depend on capabilities available in the active host.

## Examples

| Mode | Starter | Another example |
| --- | --- | --- |
| `create` | `Create a photorealistic editorial portrait of a ceramic artist in a sunlit studio with headline space on the left.` | `Generate a premium kitchen campaign image for this concept in a 4:5 portrait crop.` |
| `edit` | `Change only the blue sweater to dark green wool and preserve the face, pose, framing, and lighting.` | `Remove the orange traffic cone behind the bicycle and reconstruct the sidewalk naturally.` |
| `revise` | `Restore the original face and crop while keeping the accepted outfit from the latest version.` | `Keep the product and layout, but correct only the contact shadow so the bottle no longer floats.` |
| `prompt-only` | `Write a prompt for another model to turn this sketch into a photorealistic oak dining room.` | `Give me a strict prompt to composite the lamp from Image 2 into Image 1 without changing the base scene.` |
| `help` | `Help` | `Show me every image mode and examples without generating or editing an image.` |

End the help response by asking which mode the user wants or inviting them to attach an image and adapt an example.
