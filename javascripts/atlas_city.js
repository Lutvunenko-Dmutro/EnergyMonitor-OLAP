// EnergyMonitor-OLAP CyberCity Engine v4.1
// Feature: Physical Size Scaling (LOC + KB) and Ultra-Visible Labels

let scene, camera, renderer, labelRenderer, controls, raycaster, mouse;
const buildings = {}; 
let composer;

function initCity() {
    const container = document.getElementById('city-container');
    if (!container) return;

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x010409);
    
    camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 1, 40000);
    camera.position.set(2000, 1500, 2000);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    labelRenderer = new THREE.CSS2DRenderer();
    labelRenderer.setSize(container.clientWidth, container.clientHeight);
    labelRenderer.domElement.style.position = 'absolute';
    labelRenderer.domElement.style.top = '0px';
    labelRenderer.domElement.style.pointerEvents = 'none'; // FIX: Allow camera control
    container.appendChild(labelRenderer.domElement);

    addStarfield();
    addCityGround();

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const renderScene = new THREE.RenderPass(scene, camera);
    const bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(container.clientWidth, container.clientHeight), 1.0, 0.4, 0.85);
    composer = new THREE.EffectComposer(renderer);
    composer.addPass(renderScene);
    composer.addPass(bloomPass);

    scene.add(new THREE.AmbientLight(0xffffff, 0.6));

    if (typeof CITY_DATA !== 'undefined') {
        renderCity(CITY_DATA);
    }

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    window.addEventListener('mousemove', onMouseMove, false);
    window.addEventListener('click', onMouseClick, false);
    window.addEventListener('resize', onWindowResize, false);

    // Search and Jump Logic
    const searchInput = document.getElementById('city-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            for (let id in buildings) {
                const b = buildings[id];
                if (b.userData.name.toLowerCase().includes(query) && query.length > 2) {
                    b.material.emissiveIntensity = 5; // Highlight
                    if (query === b.userData.name.toLowerCase()) focusOnFile(id);
                } else {
                    b.material.emissiveIntensity = 0.8;
                }
            }
        });
    }

    animate();
}

function jumpTo(districtName) {
    // Find first building in district
    for (let id in buildings) {
        const b = buildings[id];
        if (b.userData.id.includes(districtName)) {
            focusOnFile(id);
            break;
        }
    }
}

function addCityGround() {
    const grid = new THREE.GridHelper(20000, 60, 0x1e293b, 0x0f172a);
    grid.position.y = -1;
    scene.add(grid);
}

function addStarfield() {
    const vertices = [];
    for (let i = 0; i < 5000; i++) {
        vertices.push(THREE.MathUtils.randFloatSpread(30000), THREE.MathUtils.randFloatSpread(20000), THREE.MathUtils.randFloatSpread(30000));
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    scene.add(new THREE.Points(geometry, new THREE.PointsMaterial({ color: 0xffffff, size: 2 })));
}

function renderCity(data) {
    let dIdx = 0;
    const dGap = 2000;
    const cols = Math.ceil(Math.sqrt(Object.keys(data.districts).length));

    for (const [name, district] of Object.entries(data.districts)) {
        const dX = (dIdx % cols) * dGap - (cols * dGap) / 2;
        const dZ = Math.floor(dIdx / cols) * dGap - (cols * dGap) / 2;
        
        district.buildings.forEach((b, i) => {
            const row = i % 8;
            const col = Math.floor(i / 8);
            
            // SIZE LOGIC
            const height = Math.max(60, b.height * 4); // Height = Lines of Code
            const width = Math.max(40, b.complexity * 15); // Width = File Size (KB)
            
            const geometry = new THREE.BoxGeometry(width, 1, width);
            const material = new THREE.MeshStandardMaterial({ 
                color: district.color, 
                emissive: district.color,
                emissiveIntensity: 0.8,
                transparent: true,
                opacity: 0.9
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(dX + col * 180, 0.5, dZ + row * 180);
            mesh.userData = { id: b.id, name: b.name, targetHeight: height, color: district.color };
            
            scene.add(mesh);
            buildings[b.id] = mesh;

            // ULTRA-VISIBLE LABEL
            const div = document.createElement('div');
            div.className = 'city-label-v4';
            div.innerHTML = `<b style="font-size:14px;">${b.name}</b><br><small>${b.height} lines</small>`;
            div.style.color = '#fff';
            div.style.background = district.color;
            div.style.padding = '4px 10px';
            div.style.borderRadius = '6px';
            div.style.border = '2px solid #fff';
            div.style.whiteSpace = 'nowrap';
            div.style.boxShadow = '0 5px 15px rgba(0,0,0,0.5)';
            div.style.fontFamily = 'sans-serif';
            
            const label = new THREE.CSS2DObject(div);
            label.position.set(0, height + 40, 0);
            mesh.add(label);
        });
        dIdx++;
    }

    // Links
    data.links.forEach(l => {
        const s = buildings[l.source];
        const t = buildings[l.target];
        if (s && t) {
            const curve = new THREE.CubicBezierCurve3(
                new THREE.Vector3(s.position.x, s.userData.targetHeight, s.position.z),
                new THREE.Vector3(s.position.x, s.userData.targetHeight + 500, s.position.z),
                new THREE.Vector3(t.position.x, t.userData.targetHeight + 500, t.position.z),
                new THREE.Vector3(t.position.x, t.userData.targetHeight, t.position.z)
            );
            const pts = curve.getPoints(30);
            const geom = new THREE.BufferGeometry().setFromPoints(pts);
            scene.add(new THREE.Line(geom, new THREE.LineBasicMaterial({ color: s.userData.color, opacity: 0.2, transparent: true })));
        }
    });
}

function focusOnFile(path) {
    const b = buildings[path];
    if (b) {
        const targetPos = new THREE.Vector3();
        b.getWorldPosition(targetPos);
        
        // Animated Fly-to
        new TWEEN.Tween(camera.position)
            .to({ x: targetPos.x + 400, y: targetPos.y + 300, z: targetPos.z + 400 }, 1000)
            .easing(TWEEN.Easing.Quadratic.Out)
            .start();
            
        controls.target.copy(targetPos);
        showInfo(b.userData);
    }
}

function animate() {
    requestAnimationFrame(animate);
    TWEEN.update(); // Update animations
    controls.update();

    for (let id in buildings) {
        const b = buildings[id];
        if (b.scale.y < b.userData.targetHeight) {
            b.scale.y += (b.userData.targetHeight - b.scale.y) * 0.1;
            b.position.y = b.scale.y / 2;
        }
    }
    
    composer.render();
    labelRenderer.render(scene, camera);
}

function onMouseMove(e) {
    const c = document.getElementById('city-container');
    const r = c.getBoundingClientRect();
    mouse.x = ((e.clientX - r.left) / c.clientWidth) * 2 - 1;
    mouse.y = -((e.clientY - r.top) / c.clientHeight) * 2 + 1;
}

function onMouseClick() {
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(Object.values(buildings));
    if (intersects.length > 0) {
        const b = intersects[0].object;
        const info = document.getElementById('city-info');
        info.style.display = 'block';
        info.innerHTML = `
            <h3 style="margin:0; color:${b.userData.color}">${b.userData.name}</h3>
            <p style="font-size:11px; color:#94a3b8">${b.userData.id}</p>
            <div style="background:#1e293b; padding:10px; border-radius:4px; margin-top:10px;">
                📏 <b>Рядки:</b> ${Math.floor(b.userData.targetHeight/4)}<br>
                💾 <b>Файл:</b> ${b.userData.id}
            </div>
            <button onclick="window.open('https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/${b.userData.id}')" 
                    style="width:100%; margin-top:15px; padding:10px; background:${b.userData.color}; border:0; color:white; font-weight:bold; cursor:pointer;">
                ВІДКРИТИ КОД
            </button>
        `;
    }
}

function onWindowResize() {
    const c = document.getElementById('city-container');
    camera.aspect = c.clientWidth / c.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(c.clientWidth, c.clientHeight);
    labelRenderer.setSize(c.clientWidth, c.clientHeight);
    composer.setSize(c.clientWidth, c.clientHeight);
}

document.addEventListener('DOMContentLoaded', () => { setTimeout(initCity, 100); });
