# 🏙️ Cyber-Metropolis: Архітектура Проєкту v4.0

Це повномасштабна 3D-візуалізація вашого програмного комплексу у стилі цифрового міста. Кожен район — це функціональний домен, кожна будівля — унікальний модуль коду.

> [!TIP]
> **Навігація:**
> - **Mouse Wheel**: Масштаб (зум).
> - **Left Click**: Огляд (панорама).
> - **Right Click**: Переміщення камери.
> - **Клік на будівлю**: Технічний паспорт файлу.

<div id="city-container" style="width: 100%; height: 800px; background: #010409; border-radius: 24px; position: relative; overflow: hidden; border: 1px solid #30363d; box-shadow: 0 30px 60px rgba(0,0,0,0.9);">
    <!-- UI Overlay -->
    <div style="position: absolute; top: 20px; left: 20px; z-index: 100; display: flex; gap: 10px; flex-direction: column;">
        <input type="text" id="city-search" placeholder="🔍 Пошук файлу..." style="padding: 10px 15px; background: rgba(15, 23, 42, 0.9); border: 1px solid #fb923c; border-radius: 8px; color: white; width: 250px; outline: none; box-shadow: 0 0 15px rgba(251, 146, 60, 0.2);">
        <div style="display: flex; gap: 5px;">
            <button onclick="jumpTo('core')" style="background:#fb923c; border:0; color:white; padding:5px 10px; border-radius:4px; cursor:pointer; font-size:11px; font-weight:bold;">CORE</button>
            <button onclick="jumpTo('ml')" style="background:#c084fc; border:0; color:white; padding:5px 10px; border-radius:4px; cursor:pointer; font-size:11px; font-weight:bold;">ML</button>
            <button onclick="jumpTo('ui')" style="background:#4ade80; border:0; color:white; padding:5px 10px; border-radius:4px; cursor:pointer; font-size:11px; font-weight:bold;">UI</button>
        </div>
    </div>
    <div id="city-info" style="position: absolute; top: 20px; right: 20px; width: 260px; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(15px); border: 1px solid rgba(251, 146, 60, 0.3); padding: 20px; border-radius: 12px; display: none; z-index: 100; box-shadow: 0 15px 35px rgba(0,0,0,0.6); color: #fff;">
        <!-- Сюди завантажується інфо -->
    </div>
    <div id="city-loader" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #fb923c; font-family: 'JetBrains Mono', monospace; text-align: center;">
        <div class="spinner" style="border: 4px solid rgba(251, 146, 60, 0.1); border-left-color: #fb923c; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px;"></div>
        Ініціалізація нейронного міста...
    </div>
</div>

<style>
@keyframes spin { to { transform: rotate(360deg); } }
#city-container canvas { display: block; outline: none; }
</style>

<!-- Основні бібліотеки -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/renderers/CSS2DRenderer.js"></script>

<!-- Пост-обробка (Bloom) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/tween.js/18.6.4/tween.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/ShaderPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/CopyShader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>

<!-- Дані та Двигун -->
<script src="../../javascripts/city_data.js"></script>
<script src="../../javascripts/atlas_city.js"></script>

<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('city-loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => loader.style.display = 'none', 500);
        }
    }, 2000);
});
</script>

---

## 🏙️ Естетика "Cyber-Core"
- **Висота**: Кількість логічних операцій та складність алгоритму.
- **Сяйво**: Активність та важливість модуля в загальній архітектурі.
- **Колір**: Приналежність до функціонального шару (Core, ML, UI).
