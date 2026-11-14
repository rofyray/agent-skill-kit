# Package and verify the PRD handoff

Deliver one downloadable ZIP for every multi-file PRD set, including a single written PRD with companion assets. Only a single small self-contained Markdown file can be delivered alone. If a single document has become lengthy, split it at useful reading boundaries and ZIP the set. Do not substitute several individual downloads for the requested complete archive.

## Stage only the deliverables

Use a dedicated directory named for the project with `PRD.md` at its root. Include referenced specs, original assets, examples, fixtures, and required notices. Keep existing sources intact. Record externally hosted resources and access limitations in the handoff; they are not bundled merely because a link exists.

Review the inventory before archiving. Exclude unrelated project files, repository metadata, caches, credentials, and private data. Do not archive the entire workspace. The helper deliberately rejects symlinks, hidden entries other than harmless operating-system metadata, common cache directories, and non-regular files; stage any intended material as reviewed ordinary files with portable names. It does not detect sensitive content inside an otherwise normal file.

## Create the ZIP

Use an available archive capability. With Python 3.10 or newer, from the installed skill directory:

```sh
python3 scripts/package_prd.py ./project-prd ./project-prd.zip
```

Replace the example paths with actual destinations. The output must be outside the input folder and must not already exist. Use a new versioned filename for a revision. The helper uses only the standard library, includes one top-level project folder, and verifies the file inventory, ZIP integrity, and archived bytes against source files. It reports a SHA-256 for the archive.

The helper checks container integrity, not PRD semantics or Markdown links. Native archive tools are acceptable when the same delivery checks can be performed. A missing Python runtime should not block another available packaging method.

## Verify the extracted handoff

Extract the archive to a fresh temporary directory and start at `PRD.md`. Check that:

- every intended file is present, with no unintended material;
- relative document, image, and sample links still resolve, including section targets;
- images and binary files open or match their originals;
- required external and repository inputs are clearly declared, with access checks reported honestly;
- each task leads directly to its needed specifications, resources, and tests;
- the driver contains execution, resume, branch, and final integrated acceptance rules without assuming this skill is installed.

When revising, verify the regenerated archive against the current sources, not a prior package. Keep structural checks separate from product implementation tests.

If the host cannot create files or ZIPs, return named file blocks and an assembly inventory, explain exactly what remains unbundled, and say ZIP delivery is incomplete. Do not fabricate an attachment or claim the archive was inspected. If the package exists, link it as the primary deliverable and name the extracted entry point.
