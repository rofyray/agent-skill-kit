import { BufferGeometry, Float32BufferAttribute, Mesh, MeshPhongMaterial, Group } from 'three';
import anatomy from './anatomy/brain-mesh.json' with { type: 'json' };

export function makeBrain() {
  const object = new Group();
  object.name = 'Anatomical brain';
  for (const part of anatomy.parts) {
    const geometry = new BufferGeometry();
    geometry.setAttribute('position', new Float32BufferAttribute(part.positions, 3));
    geometry.setIndex(part.indices);
    geometry.computeVertexNormals();
    const cerebellum = part.name.toLowerCase().includes('cerebellar');
    const stem = part.name.toLowerCase().includes('brainstem');
    const material = new MeshPhongMaterial({
      color: cerebellum ? '#5d8d88' : stem ? '#a28c72' : '#708a79',
      specular: '#596b61', shininess: 24, transparent: true, opacity: .56,
      depthWrite: false,
    });
    const mesh = new Mesh(geometry, material);
    mesh.name = part.name;
//Draw the translucent anatomy after graph primitives to avoid depth-order popping.
    mesh.renderOrder = 20;
//The anatomy gives context. Only knowledge nodes capture selections.
    mesh.raycast = () => {};
    object.add(mesh);
  }
  return object;
}

export function setBrainOpacity(brain, opacity) {
  for (const mesh of brain.children) {
    mesh.material.opacity = opacity;
    mesh.material.depthWrite = opacity > .4;
  }
}
