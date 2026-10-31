//Stable coordinates depend on identity, never array order or graph size.
export function randomFor(value) {
  let seed = 2166136261;
  for (const c of value) seed = Math.imul(seed ^ c.charCodeAt(0), 16777619);
  return () => {
    seed += 0x6D2B79F5;
    let t = Math.imul(seed ^ seed >>> 15, seed | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0)/4294967296;
  };
}

export function brainSurface(side, theta, phi, folded = true) {
  const fold = folded ? 1 + .035 * Math.sin(theta * 19 + 2 * Math.sin(phi * 5)) * Math.sin(phi * 13) : 1;
  return {
    x: side * 38 + 35 * Math.sin(theta) * Math.cos(phi) * fold,
    y: 58 * Math.cos(theta) * fold,
    z: 83 * Math.sin(theta) * Math.sin(phi) * fold,
  };
}

export function positionFor(node, mode = 'brain') {
  const group = randomFor(node.group);
  const random = randomFor(node.id);
  const side = group() > .5 ? 1 : -1;
  const theta = .55 + group() * 2.0;
  const phi = group() * Math.PI * 2;
  const center = brainSurface(side, theta, phi, false);
  const a = random() * Math.PI * 2;
  const z = random() * 2 - 1;
  const radius = Math.cbrt(random());
  if (mode === 'brain') {
    const gx = (center.x - side * 38)/35, gy = center.y/58, gz = center.z/83;
    const ux = radius * Math.sqrt(1 - z * z) * Math.cos(a), uy = radius * z, uz = radius * Math.sqrt(1 - z * z) * Math.sin(a);
    return { x: side * 38 + 35 * (.35 * gx + .64 * ux), y: 58 * (.35 * gy + .64 * uy), z: 83 * (.35 * gz + .64 * uz) };
  }
  const spread = 39;
  const factor = 2.15;
  return {
    x: center.x * factor + spread * radius * Math.sqrt(1 - z * z) * Math.cos(a),
    y: center.y * factor + spread * radius * z,
    z: center.z * factor + spread * radius * Math.sqrt(1 - z * z) * Math.sin(a),
  };
}

export const endpoint = value => typeof value === 'object' ? value.id : value;

export function neighborhood(id, links, depth = 1) {
  const found = new Set([id]);
  let frontier = new Set([id]);
  for (let i = 0; i < depth; i++) {
    const next = new Set();
    for (const edge of links) {
      const a = endpoint(edge.source), b = endpoint(edge.target);
      if (frontier.has(a) && !found.has(b)) next.add(b);
      if (frontier.has(b) && !found.has(a)) next.add(a);
    }
    next.forEach(node => found.add(node));
    frontier = next;
  }
  return found;
}

export function cameraForNodes(nodes, aspect, fov = 50) {
  const target = { x: 0, y: 0, z: 0 };
  if (!nodes.length) return null;
  for (const axis of ['x', 'y', 'z']) {
    const values = nodes.map(n => n[axis]);
    target[axis] = (Math.min(...values) + Math.max(...values))/2;
  }
  const radius = Math.max(12, ...nodes.map(n => Math.hypot(n.x - target.x, n.y - target.y, n.z - target.z) + 8));
  const vertical = fov * Math.PI/360;
  const angle = Math.min(vertical, Math.atan(Math.tan(vertical) * Math.max(.1, aspect)));
  const distance = 1.2 * radius/Math.sin(angle);
  const length = Math.hypot(150, 73, 185);
  return { target, position: { x: target.x + 150/length * distance, y: target.y + 73/length * distance, z: target.z + 185/length * distance } };
}
