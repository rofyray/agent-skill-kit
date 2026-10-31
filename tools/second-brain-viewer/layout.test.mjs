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
