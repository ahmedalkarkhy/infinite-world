/* The platform panel: six capability layers stacked into one engine, in real
   3D. It illustrates the section's own claim and encodes no invented data, so
   nothing here can contradict the Corporate Book figures beside it. */
import * as THREE from "./assets/three.module.min.js";

const host = document.getElementById("engine");
if (host) {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let renderer;

  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  } catch (err) {
    renderer = null;
  }

  if (renderer && !reduce) {
    host.classList.add("live");

    const size = () => ({ w: host.clientWidth, h: host.clientHeight });
    let { w, h } = size();

    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(w, h);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    host.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(30, w / h, 0.1, 100);
    camera.position.set(0, 1.05, 6.6);
    camera.lookAt(0, -0.1, 0);

    // Studio reflections from a canvas gradient, no HDR file to ship
    const env = (() => {
      const c = document.createElement("canvas");
      c.width = 256;
      c.height = 128;
      const g = c.getContext("2d");
      const grad = g.createLinearGradient(0, 0, 0, 128);
      grad.addColorStop(0, "#2b323a");
      grad.addColorStop(0.5, "#0b0e11");
      grad.addColorStop(1, "#05070a");
      g.fillStyle = grad;
      g.fillRect(0, 0, 256, 128);
      g.fillStyle = "rgba(255,255,255,0.85)";
      g.fillRect(40, 8, 150, 22);
      g.fillStyle = "rgba(0,150,80,0.45)";
      g.fillRect(150, 60, 106, 44);
      const tex = new THREE.CanvasTexture(c);
      tex.mapping = THREE.EquirectangularReflectionMapping;
      tex.colorSpace = THREE.SRGBColorSpace;
      const pm = new THREE.PMREMGenerator(renderer);
      const map = pm.fromEquirectangular(tex).texture;
      pm.dispose();
      tex.dispose();
      return map;
    })();
    scene.environment = env;

    const rig = new THREE.Group();
    scene.add(rig);

    const LAYERS = 6;
    const GAP = 0.34;
    const slabGeo = new THREE.BoxGeometry(3.1, 0.11, 2.05);
    const edgeGeo = new THREE.BoxGeometry(3.16, 0.015, 2.11);

    const slabs = [];
    for (let i = 0; i < LAYERS; i++) {
      const layer = new THREE.Group();

      const body = new THREE.Mesh(
        slabGeo,
        new THREE.MeshPhysicalMaterial({
          color: 0x1b2026,
          metalness: 0.72,
          roughness: 0.32,
          clearcoat: 0.8,
          clearcoatRoughness: 0.25,
          envMapIntensity: 1.25,
        }),
      );
      layer.add(body);

      // A lit rim on each layer: the capability reading as active
      const rim = new THREE.Mesh(
        edgeGeo,
        new THREE.MeshBasicMaterial({
          color: i === 2 ? 0xd01028 : 0x17b866,
          transparent: true,
          opacity: 0.5,
        }),
      );
      rim.position.y = -0.062;
      layer.add(rim);

      rig.add(layer);
      slabs.push(layer);
    }

    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(3, 5, 4);
    scene.add(key);
    const fill = new THREE.DirectionalLight(0x9fe3bd, 0.7);
    fill.position.set(-4, -2, 2);
    scene.add(fill);
    scene.add(new THREE.AmbientLight(0x66707a, 0.5));

    let open = 0; // 0 solid block, 1 fully separated
    let target = 0;
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => (target = e.isIntersecting ? 1 : 0)),
      { threshold: 0.35 },
    );
    io.observe(host);

    /* ResizeObserver rather than a window listener: the panel can get its real
       height after the stylesheet lands, and a canvas sized from a zero box
       would stay wrong forever. */
    const fit = () => {
      ({ w, h } = size());
      if (!w || !h) return;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    new ResizeObserver(fit).observe(host);
    fit();

    const clock = new THREE.Clock();

    renderer.setAnimationLoop(() => {
      const t = clock.getElapsedTime();
      open += (target - open) * 0.045;

      slabs.forEach((layer, i) => {
        const centred = i - (LAYERS - 1) / 2;
        layer.position.y = centred * GAP * open;
        layer.rotation.y = Math.sin(t * 0.3 + i * 0.22) * 0.05 * open;
      });

      rig.rotation.y = -0.62 + Math.sin(t * 0.22) * 0.14;
      rig.rotation.x = 0.34;

      renderer.render(scene, camera);
    });
  }
}
