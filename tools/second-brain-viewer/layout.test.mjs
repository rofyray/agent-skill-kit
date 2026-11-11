import test from 'node:test';
import assert from 'node:assert/strict';
import { positionFor, neighborhood } from './layout.mjs';

test('adding pages does not move existing identities', () => {
  const a = { id: 'wiki/a.md', group: 'Learning' }, b = { id: 'wiki/b.md', group: 'Learning' };
  const before = positionFor(a);
  positionFor(b);
  assert.deepEqual(positionFor(a), before);
  assert.notDeepEqual(positionFor(b), before);
  assert.notDeepEqual(positionFor(a, 'explore'), before);
});

test('neighborhood includes incoming and outgoing references without crossing depth', () => {
  const edges = [{ source: 'a', target: 'b' }, { source: 'c', target: 'a' }, { source: 'b', target: 'd' }];
  assert.deepEqual([...neighborhood('a', edges)].sort(), ['a', 'b', 'c']);
  assert.deepEqual([...neighborhood('a', edges, 2)].sort(), ['a', 'b', 'c', 'd']);
  assert.deepEqual([...neighborhood('alone', edges)], ['alone']);
});

test('neighborhood framing keeps every endpoint inside landscape and portrait views', async () => {
  const { cameraForNodes } = await import('./layout.mjs');
  const { PerspectiveCamera, Vector3 } = await import('three');
  const nodes = Array.from({ length: 30 }, (_, i) => positionFor({ id: String(i), group: String(i % 4) }));
  for (const aspect of [.5, 1, 2.4]) {
    const fit = cameraForNodes(nodes, aspect);
    const camera = new PerspectiveCamera(50, aspect, .1, 2000);
    camera.position.set(fit.position.x, fit.position.y, fit.position.z);
    camera.lookAt(fit.target.x, fit.target.y, fit.target.z);
    camera.updateMatrixWorld();
    for (const n of nodes) {
      const p = new Vector3(n.x, n.y, n.z).project(camera);
      assert.ok(Math.abs(p.x) < .85 && Math.abs(p.y) < .85 && p.z < 1);
    }
  }
  assert.equal(cameraForNodes([], 1), null);
});

test('anatomical model includes cortex, cerebellum and brainstem with valid normals', async () => {
  const { makeBrain, setBrainOpacity } = await import('./brain-model.mjs');
  const brain = makeBrain();
  assert.equal(brain.children.length, 5);
  assert.equal(brain.children.filter(p => p.name.includes('cerebral')).length, 2);
  assert.equal(brain.children.filter(p => p.name.includes('cerebellar')).length, 2);
  assert.equal(brain.children.filter(p => p.name.includes('brainstem')).length, 1);
  for (const part of brain.children) {
    assert.ok([...part.geometry.attributes.normal.array].every(Number.isFinite));
    const hits = [];
    part.raycast(null, hits);
    assert.equal(hits.length, 0);
  }
  setBrainOpacity(brain, .12);
  assert.ok(brain.children.every(part => part.material.opacity === .12 && !part.material.depthWrite));
});

test('sampled knowledge nodes stay inside the cortical surfaces in the shared coordinate frame', async () => {
  const { makeBrain } = await import('./brain-model.mjs');
  const { Mesh, MeshBasicMaterial, DoubleSide, Raycaster, Vector3 } = await import('three');
  const parts = makeBrain().children.filter(p => p.name.includes('cerebral')).map(p => new Mesh(p.geometry, new MeshBasicMaterial({ side: DoubleSide })));
  parts.forEach(part => part.updateMatrixWorld());
  for (let i = 0; i < 400; i++) {
    const p = positionFor({ id: String(i), group: String(i % 9) });
    const ray = new Raycaster(new Vector3(p.x, p.y, p.z), new Vector3(.22, .73, .47).normalize());
    assert.equal(ray.intersectObjects(parts).length % 2, 1, `Node ${i} lies outside the cortex`);
  }
});
