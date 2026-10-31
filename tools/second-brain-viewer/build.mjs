import { build } from 'esbuild';
import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const output = path.resolve(here, '../../skills/build-and-maintain-a-second-brain/assets/brain-viewer');
await mkdir(output, { recursive: true });
const result = await build({
  absWorkingDir: here, entryPoints: ['viewer.mjs'], outfile: path.join(output, 'viewer.js'),
  bundle: true, minify: true, format: 'iife', target: ['es2020'], metafile: true,
  legalComments: 'none',
});
await Promise.all(['index.html', 'viewer.css'].map(file => copyFile(path.join(here, file), path.join(output, file))));
const packages = new Set(Object.keys(result.metafile.inputs).filter(p => p.startsWith('node_modules/')).map(p => {
  const parts = p.split('/');
  return parts[1].startsWith('@') ? `${parts[1]}/${parts[2]}` : parts[1];
}));
const notices = ['Bundled second-brain viewer dependencies. Source versions are pinned in tools/second-brain-viewer/package-lock.json.'];
for (const name of [...packages].sort()) {
  const directory = path.join(here, 'node_modules', name);
  const metadata = JSON.parse(await readFile(path.join(directory, 'package.json'), 'utf8'));
  let license;
  for (const file of ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'LICENSE-MIT', 'license', 'license.md']) {
    try { license = await readFile(path.join(directory, file), 'utf8'); break; } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  if (!license) throw Error(`Missing license for bundled dependency ${name}`);
  notices.push(`${name} ${metadata.version}\n${metadata.repository?.url || metadata.homepage || ''}\n\n${license}`);
}
await writeFile(path.join(output, 'THIRD_PARTY_NOTICES.txt'), notices.join('\n\n' + '='.repeat(72) + '\n\n') + '\n');
console.log(`Built ${Object.keys(result.metafile.inputs).length} modules into ${output}`);
