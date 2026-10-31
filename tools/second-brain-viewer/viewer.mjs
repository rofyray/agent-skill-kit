import ForceGraph3D from '3d-force-graph';
import { BufferGeometry, Float32BufferAttribute, LineBasicMaterial, LineSegments, Group, Vector2, Color } from 'three';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { brainSurface, positionFor, randomFor, neighborhood, endpoint, cameraForNodes } from './layout.mjs';

const $ = id => document.getElementById(id);
const palette = ['#e7b680', '#9bcbb7', '#b9b3db', '#d9998c', '#9dbfd1', '#d0c68b'];
const MAX_NODES = 1200, MAX_LINKS = 6000;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
let snapshot, graph, shell, bloom, annotation, selected, focusId, mode = 'brain', pageSize = listBatchSize();
let visibleNodes = [], visibleLinks = [], matching = [], pulseLinks = new Set();
let hasGPU = true, searchTimer, loading = false;
const nodeMap = new Map();
const colors = new Map();
let selectedNeighbors = new Set();

function listBatchSize() { return innerWidth <= 600 ? 6 : 60; }

function element(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}

function colorFor(group) {
  if (!colors.has(group)) colors.set(group, palette[Math.floor(randomFor(group)() * palette.length)]);
  return colors.get(group);
}

function makeShell() {
  const object = new Group();
  const vertices = [];
  for (const side of [-1, 1]) {
    for (let ring = 1; ring < 39; ring++) {
      const theta = ring/39 * Math.PI;
      for (let j = 0; j < 140; j++) {
        const a = brainSurface(side, theta, j/140 * Math.PI * 2);
        const b = brainSurface(side, theta, (j + 1)/140 * Math.PI * 2);
        vertices.push(a.x, a.y, a.z, b.x, b.y, b.z);
      }
    }

  }
  const geometry = new BufferGeometry();
  geometry.setAttribute('position', new Float32BufferAttribute(vertices, 3));
  const material = new LineBasicMaterial({ color: '#7faaa1', transparent: true, opacity: .055, depthWrite: false });
  const lines = new LineSegments(geometry, material);
//The anatomical outline is not knowledge and must not capture selection.
  lines.raycast = () => {};
  object.add(lines);
  return object;
}

function initGraph() {
  try {
    graph = new ForceGraph3D($('graph'), { controlType: 'orbit', extraRenderers: [new CSS2DRenderer()], rendererConfig: { antialias: true, powerPreference: 'low-power' } })
      .backgroundColor('#0b1112').showNavInfo(false).enableNodeDrag(false)
      .nodeId('id').nodeColor(n => selected && !selectedNeighbors.has(n.id) ? '#41534f' : colorFor(n.group))
      .nodeVal(n => n.kind === 'cluster' ? 10 + Math.sqrt(n.count) : n.kind === 'source' ? 1.4 : 2.6 + Math.min(n.degree || 0, 15) * .3)
      .nodeRelSize(1.05).nodeResolution(8).nodeOpacity(.96)
      .nodeLabel(n => element('span', n.title))
      .linkLabel(e => element('span', e.kind === 'evidence' ? 'Page cites source' : `${e.count || 1} explicit reference${e.count > 1 ? 's' : ''}`))
      .linkColor(e => selected && [endpoint(e.source), endpoint(e.target)].includes(selected.id) ? '#edbc82' : e.kind === 'evidence' ? '#91afa0' : '#688477')
      .linkWidth(e => selected && [endpoint(e.source), endpoint(e.target)].includes(selected.id) ? .35 : 0).linkOpacity(.19)
      .linkDirectionalParticleWidth(.8).linkDirectionalParticleResolution(4)
      .linkDirectionalParticleColor(() => '#f7d9a5').linkDirectionalParticleSpeed(.004)
      .linkDirectionalParticles(e => pulseLinks.has(e) ? 1 : 0)
      .warmupTicks(0).cooldownTicks(0)
      .onNodeClick(selectNode).onBackgroundClick(clearSelection);
    graph.renderer().setPixelRatio(Math.min(devicePixelRatio, 1.5));
    graph.scene().background = new Color('#0b1112');
    graph.controls().enableDamping = true;
    graph.controls().dampingFactor = .12;
    graph.controls().minDistance = 20;
    graph.controls().maxDistance = 1600;
    shell = makeShell();
    graph.scene().add(shell);
    bloom = new UnrealBloomPass(new Vector2(512, 512), .65, .5, .45);
    bloom.enabled = false;
    graph.postProcessingComposer().addPass(bloom);
    graph.postProcessingComposer().addPass(new OutputPass());
    new ResizeObserver(() => {
      graph.width($('graph').clientWidth).height($('graph').clientHeight);
    }).observe($('graph'));
    $('graph').querySelector('canvas').setAttribute('aria-hidden', 'true');
    $('graph').querySelector('canvas').addEventListener('webglcontextlost', event => {
      event.preventDefault();
      hasGPU = false;
      $('message').textContent = '3D graphics paused. Your knowledge list is still available. Reload this page to restore the view.';
    });
    homeCamera();
  } catch (error) {
    hasGPU = false;
    $('message').textContent = '3D graphics are unavailable in this browser. Explore every page through the knowledge list below or beside this view.';
    $('glow').disabled = true;
    $('activity').disabled = true;
  }
}

function homeCamera() {
  if (!hasGPU || !graph) return;
  const aspect = $('graph').clientWidth/Math.max(1, $('graph').clientHeight);
  const scale = (mode === 'brain' ? (innerWidth <= 600 ? .82 : 1) : 2.5) * Math.max(1, .9/aspect);
  graph.cameraPosition({ x: 150 * scale, y: 73 * scale, z: 185 * scale }, { x: 0, y: 0, z: 0 }, reduced.matches ? 0 : 650);
}

function currentMatches() {
  const query = $('search').value.trim().toLocaleLowerCase();
  const group = $('domain').value, status = $('status').value;
  const neighbors = focusId ? neighborhood(focusId, snapshot.links) : null;
  return snapshot.nodes.filter(n =>
    (n.kind === 'page' || $('sources').checked) &&
    (!group || n.group === group) && (!status || n.status === status) &&
    (!$('orphans').checked || (n.kind === 'page' && n.degree === 0)) &&
    (!neighbors || neighbors.has(n.id)) &&
    (!query || `${n.title} ${n.summary} ${n.tags.join(' ')} ${n.id}`.toLocaleLowerCase().includes(query)));
}

function rebuild() {
  if (!snapshot) return;
  matching = currentMatches();
  renderList();
  const clustered = matching.length > MAX_NODES && !$('domain').value && !focusId && !$('search').value.trim();
  const ids = new Set(matching.map(n => n.id));
  const candidates = snapshot.links.filter(e => ids.has(e.source) && ids.has(e.target));
  if (clustered) {
    const groups = new Map();
    for (const n of matching) {
      if (!groups.has(n.group)) groups.set(n.group, { id: `cluster:${n.group}`, title: n.group, group: n.group, kind: 'cluster', count: 0 });
      groups.get(n.group).count++;
    }
    visibleNodes = [...groups.values()].slice(0, MAX_NODES);
    const clusterIds = new Set(visibleNodes.map(n => n.id));
    const links = new Map();
    for (const e of candidates) {
      const source = `cluster:${nodeMap.get(e.source).group}`, target = `cluster:${nodeMap.get(e.target).group}`;
      if (source === target || !clusterIds.has(source) || !clusterIds.has(target)) continue;
      const key = JSON.stringify([source, target, e.kind]);
      if (!links.has(key)) links.set(key, { source, target, kind: e.kind, count: 0 });
      links.get(key).count++;
    }
    visibleLinks = [...links.values()].slice(0, MAX_LINKS);
    $('graph-count').textContent = `${matching.length.toLocaleString()} items in ${visibleNodes.length} visible regions · Select a region to expand`;
  } else {
//Limit only rendering, never the searchable snapshot or library.
    let subset = matching.slice(0, MAX_NODES);
    if (selected && ids.has(selected.id) && !subset.some(n => n.id === selected.id)) subset = [selected, ...subset.slice(0, MAX_NODES - 1)];
    visibleNodes = subset.map(n => ({ ...n }));
    const visibleIds = new Set(visibleNodes.map(n => n.id));
    const allLinks = candidates.filter(e => visibleIds.has(e.source) && visibleIds.has(e.target));
    visibleLinks = allLinks.slice(0, MAX_LINKS).map(e => ({ ...e }));
    $('graph-count').textContent = `${visibleNodes.length.toLocaleString()} of ${matching.length.toLocaleString()} items · ${visibleLinks.length.toLocaleString()} of ${candidates.length.toLocaleString()} connections shown${matching.length > MAX_NODES ? ' · Filter to reveal more' : ''}`;
  }
  visibleNodes.forEach(n => {
    const position = positionFor(n, mode);
    Object.assign(n, position, { fx: position.x, fy: position.y, fz: position.z });
  });
  if (hasGPU && graph) {
    graph.graphData({ nodes: visibleNodes, links: visibleLinks });
    updateAnnotation();
    shell.visible = mode === 'brain' && matching.length > 0 && !focusId;
    shell.children[0].material.opacity = selected ? .025 : .055;
    setActivity();
    $('message').textContent = matching.length ? '' : snapshot.nodes.some(n => n.kind === 'page') ? 'No matching pages. Try another search or reset the view.' : 'Your brain is ready for its first idea. Ingest a source, then regenerate this snapshot.';
  }
  $('view-label').textContent = focusId ? 'ONE IDEA, AND ITS CONNECTIONS' : clustered ? 'YOUR KNOWLEDGE, BY REGION' : mode === 'brain' ? 'PAGES AND THE THREADS BETWEEN THEM' : 'REGIONS IN OPEN SPACE';
  $('view-hint').textContent = selected && !visibleLinks.length ? 'Connections may be outside this filter. Choose Show neighborhood to reveal them.' : mode === 'brain' ? (matchMedia('(pointer: coarse)').matches || innerWidth <= 600 ? 'Drag to orbit · Pinch to zoom · Two fingers to pan' : 'Drag to orbit · Scroll to zoom · Right-drag to pan') : 'Regions spread apart · Select a page to follow its thread';
}

function renderList() {
  $('node-list').replaceChildren();
  $('result-count').textContent = matching.length.toLocaleString();
  $('mobile-results').textContent = `View ${matching.length.toLocaleString()} matches ↓`;
  for (const node of matching.slice(0, pageSize)) {
    const button = element('button', undefined, 'node-row');
    button.append(element('span', node.title), element('small', `${node.group} · ${node.status}`));
    button.setAttribute('aria-pressed', String(selected?.id === node.id));
    button.onclick = () => selectNode(node);
    $('node-list').append(button);
  }
  if (!matching.length) $('node-list').append(element('p', 'No matching pages.', 'muted'));
  $('more').hidden = pageSize >= matching.length;
}

function updateAnnotation() {
  if (annotation) { graph.scene().remove(annotation); annotation = null; }
  if (!selected || !visibleNodes.some(n => n.id === selected.id)) return;
  const label = element('div', selected.title, 'node-annotation is-selected');
  label.setAttribute('aria-hidden', 'true');
  annotation = new CSS2DObject(label);
  const position = positionFor(selected, mode);
  annotation.position.set(position.x, position.y + 5, position.z);
  annotation.center.set(.5, 1);
  graph.scene().add(annotation);
}

function setActivity() {
  if (!hasGPU || !graph) return;
  const activity = $('activity').value;
  const recent = new Set(snapshot.nodes.filter(n => {
    const age = Date.now() - new Date(`${n.updated}T00:00:00`).valueOf();
    return age >= 0 && age <= 7 * 86400000;
  }).map(n => n.id));
  const candidates = activity === 'off' ? [] : visibleLinks.filter(e => {
    const a = endpoint(e.source), b = endpoint(e.target);
    return activity === 'ambient' || activity === 'selected' && selected && (a === selected.id || b === selected.id) || activity === 'recent' && (recent.has(a) || recent.has(b));
  });
//Deterministically spread a bounded number of pulses throughout the graph.
  pulseLinks = new Set(candidates.filter((_, index) => index % Math.max(1, Math.ceil(candidates.length/48)) === 0).slice(0, 48));
  graph.linkDirectionalParticles(e => pulseLinks.has(e) ? 1 : 0);
}

function selectNode(node) {
  if (node.kind === 'cluster') {
    $('domain').value = node.group;
    pageSize = listBatchSize();
    rebuild();
    return;
  }
  selected = nodeMap.get(node.id);
  selectedNeighbors = neighborhood(selected.id, snapshot.links);
  document.querySelector('main').classList.add('has-selection');
  $('close-selection').hidden = false;
  $('inspector-label').textContent = selected.kind === 'source' ? 'SELECTED SOURCE' : 'SELECTED PAGE';
  $('selection-empty').hidden = true;
  $('selection').hidden = false;
  $('selected-kind').textContent = `${selected.type}/${selected.status}`;
  $('selected-title').textContent = selected.title;
  $('selected-summary').textContent = selected.summary || 'This page has no summary yet.';
  $('selected-meta').replaceChildren();
  for (const [label, value] of [['Region', selected.group], ['Updated', selected.updated || 'Not recorded'], ['Links', String(selected.degree)], ['Indexed', selected.indexed ? 'Yes' : 'No']]) {
    $('selected-meta').append(element('dt', label), element('dd', value));
  }
  $('selected-tags').replaceChildren(...selected.tags.map(tag => element('span', `#${tag}`)));
  $('selected-path').textContent = selected.id;
//Do not trust arbitrary URLs supplied in snapshots.
  $('open-note').href = `obsidian://open?vault=${encodeURIComponent(snapshot.name)}&file=${encodeURIComponent(selected.id)}`;
  $('connections').replaceChildren();
  const related = neighborhood(selected.id, snapshot.links.filter(e => e.kind === 'reference'));
  related.delete(selected.id);
  [...related].slice(0, 100).forEach(id => {
    const button = element('button', nodeMap.get(id).title, 'node-row');
    button.onclick = () => {
      $('search').value = ''; $('domain').value = ''; $('status').value = ''; $('orphans').checked = false; focusId = null;
      selectNode(nodeMap.get(id));
    };
    $('connections').append(button);
  });
  if (!related.size) $('connections').append(element('p', 'No explicit page connections yet.', 'muted'));
  if (related.size > 100) $('connections').append(element('p', `${related.size - 100} more. Use Show neighborhood to explore.`, 'muted'));
  $('evidence').replaceChildren(...selected.sources.map(source => element('p', source)));
  if (!selected.sources.length) $('evidence').append(element('p', selected.kind === 'source' ? 'This is a source file. Its contents stay in your vault.' : 'No evidence locators recorded.', 'muted'));
  rebuild();
  if (hasGPU && graph) {
    graph.linkColor(graph.linkColor());
  }
  if (innerWidth < 1100) document.querySelector('.inspector').scrollIntoView({ behavior: reduced.matches ? 'instant' : 'smooth', block: 'start' });
}

function clearSelection() {
  selected = null;
  document.querySelector('main').classList.remove('has-selection');
  $('close-selection').hidden = true;
  $('inspector-label').textContent = 'AT A GLANCE';
  $('selection').hidden = true;
  $('selection-empty').hidden = false;
  renderList();
  if (hasGPU && graph) { graph.linkColor(graph.linkColor()); graph.nodeColor(graph.nodeColor()); updateAnnotation(); graph.linkWidth(graph.linkWidth()); shell.children[0].material.opacity = .055; setActivity(); }
}

function validate(data) {
  if (data.version !== 1 || typeof data.name !== 'string' || !Array.isArray(data.nodes) || !Array.isArray(data.links) || !Array.isArray(data.diagnostics)) throw Error('Unsupported graph snapshot. Regenerate it with this skill.');
  const ids = new Set();
  for (const n of data.nodes) {
    if (!n || typeof n.id !== 'string' || ids.has(n.id) || !['page', 'source'].includes(n.kind) ||
        !['title', 'summary', 'group', 'status', 'type', 'updated'].every(key => typeof n[key] === 'string') ||
        !Array.isArray(n.tags) || !Array.isArray(n.sources) || ![...n.tags, ...n.sources].every(x => typeof x === 'string')) throw Error('Invalid node in graph snapshot. Regenerate the snapshot.');
    ids.add(n.id);
  }
  if (data.links.some(e => !ids.has(e.source) || !ids.has(e.target) || !['reference', 'evidence'].includes(e.kind))) throw Error('Invalid connection in graph snapshot.');
  return data;
}

async function load() {
  if (loading) return;
  loading = true;
  $('reload').disabled = true;
  try {
    const response = await fetch('graph.json', { cache: 'no-store' });
    if (!response.ok) throw Error('Cannot read graph.json. Regenerate the snapshot and try again.');
    snapshot = validate(await response.json());
    nodeMap.clear(); snapshot.nodes.forEach(n => nodeMap.set(n.id, n));
    selected = null; focusId = null; pageSize = listBatchSize();
    document.querySelector('main').classList.remove('has-selection');
    $('close-selection').hidden = true;
    $('inspector-label').textContent = 'AT A GLANCE';
    $('total-pages').textContent = snapshot.nodes.filter(n => n.kind === 'page').length.toLocaleString();
    $('total-links').textContent = snapshot.links.filter(e => e.kind === 'reference').length.toLocaleString();
    $('selection').hidden = true; $('selection-empty').hidden = false;
    $('vault-name').textContent = snapshot.name;
    document.title = `${snapshot.name} · Second Brain`;
    const timestamp = new Date(snapshot.generatedAt);
    $('snapshot-time').textContent = `Snapshot ${Number.isNaN(timestamp.valueOf()) ? '' : timestamp.toLocaleDateString()}`;
    $('domain').replaceChildren(new Option('All regions', ''));
    $('region-key').replaceChildren();
    const groups = [...new Set(snapshot.nodes.map(n => n.group))].sort();
    colors.clear();
    groups.forEach((group, index) => colors.set(group, palette[index % palette.length]));
    for (const group of groups) {
      $('domain').add(new Option(group, group));
      if (group === 'Sources') continue;
      const row = element('button', undefined, 'region');
      row.onclick = () => { $('search').value = ''; $('status').value = ''; $('orphans').checked = false; $('domain').value = group; focusId = null; pageSize = listBatchSize(); rebuild(); homeCamera(); if (innerWidth <= 1100) document.querySelector('.stage').scrollIntoView({ behavior: reduced.matches ? 'instant' : 'smooth' }); };
      const swatch = element('i'); swatch.style.background = colorFor(group);
      row.append(swatch, element('span', group), element('span', String(snapshot.nodes.filter(n => n.group === group && n.kind === 'page').length), 'region-count')); $('region-key').append(row);
    }
    $('diagnostic-count').textContent = `${snapshot.diagnostics.length} structural findings`;
    $('diagnostic-list').replaceChildren(...snapshot.diagnostics.slice(0, 200).map(d => element('li', `${d.kind}: ${d.page || ''}${d.target ? ` → ${d.target}` : ''}${d.detail ? ` (${d.detail})` : ''}`)));
    if (snapshot.diagnostics.length > 200) $('diagnostic-list').append(element('li', 'First 200 shown. The full list is in graph.json.'));
    if (!graph && hasGPU) initGraph();
    rebuild();
  } catch (error) {
    $('message').textContent = error.message || 'Unable to load this snapshot.';
  } finally {
    loading = false;
    $('reload').disabled = false;
  }
}

$('search').addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(() => { focusId = null; pageSize = listBatchSize(); rebuild(); }, 120); });
for (const id of ['domain', 'status', 'sources', 'orphans']) $(id).onchange = () => { focusId = null; pageSize = listBatchSize(); rebuild(); };
for (const name of ['brain', 'explore']) $(name).onclick = () => {
  mode = name;
  $('brain').setAttribute('aria-pressed', String(name === 'brain'));
  $('explore').setAttribute('aria-pressed', String(name === 'explore'));
  rebuild(); homeCamera();
};
$('reset').onclick = () => {
  focusId = null; $('search').value = ''; $('domain').value = ''; $('status').value = ''; $('orphans').checked = false;
  pageSize = listBatchSize(); clearSelection(); rebuild(); homeCamera();
};
$('focus').onclick = () => {
  if (!selected) return;
  focusId = selected.id; $('search').value = ''; $('domain').value = ''; $('status').value = ''; $('orphans').checked = false;
  pageSize = listBatchSize(); rebuild();
  if (hasGPU && graph) {
    const fit = cameraForNodes(visibleNodes, $('graph').clientWidth/$('graph').clientHeight, graph.camera().fov);
    if (fit) graph.cameraPosition(fit.position, fit.target, reduced.matches ? 0 : 650);
  }
  if (innerWidth < 1100) document.querySelector('.stage').scrollIntoView({ behavior: reduced.matches ? 'instant' : 'smooth' });
};
$('more').onclick = () => { pageSize += listBatchSize(); renderList(); };
matchMedia('(max-width: 600px)').addEventListener('change', () => { pageSize = listBatchSize(); if (snapshot) rebuild(); });
$('reload').onclick = load;
$('close-selection').onclick = () => { clearSelection(); rebuild(); homeCamera(); };
$('activity').onchange = setActivity;
$('glow').onchange = () => { if (bloom) bloom.enabled = $('glow').checked; };
if (reduced.matches) $('activity').value = 'off';
reduced.addEventListener('change', () => { if (reduced.matches) { $('activity').value = 'off'; setActivity(); } });
document.addEventListener('visibilitychange', () => { if (hasGPU && graph) document.hidden ? graph.pauseAnimation() : graph.resumeAnimation(); });
load();
