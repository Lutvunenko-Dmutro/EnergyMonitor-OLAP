# 📘 Архітектурний Блюпрінт Проєкту (Defense Edition)

Цей документ є інтерактивним путівником по структурі та логіці системи. Використовуйте його для швидкої навігації та пояснення архітектурних рішень під час захисту.

---

<div class="blueprint-container">
    
    <!-- Ліва частина: Дерево файлів -->
    <div class="blueprint-tree-section">
        <div class="search-wrapper">
            <input type="text" id="blueprint-search" placeholder="🔍 Пошук модуля (main, loader, ml)...">
        </div>
        <div id="blueprint-tree">
            <div style="color: var(--text-dim); font-style: italic; padding: 20px;">Ініціалізація структури...</div>
        </div>
    </div>

    <!-- Права частина: Деталі -->
    <div class="blueprint-details-section">
        <div id="details-placeholder">
            <div style="font-size: 60px; margin-bottom: 25px; opacity: 0.3;">📦</div>
            <h3 style="color: #fff; margin-bottom: 10px;">Архітектурний термінал</h3>
            <p>Оберіть об'єкт у дереві зліва для <br>виведення технічної специфікації.</p>
        </div>
        
        <div id="details-content" style="display: none;">
            <div id="details-type">MODULE</div>
            <h2 id="details-name">filename.py</h2>
            <code id="details-path">src/app/main.py</code>
            
            <div class="details-card">
                <h4>Технічна специфікація</h4>
                <p id="details-desc"></p>
            </div>

            <div id="details-links">
                <button id="details-btn" class="mega-btn" data-url="" onclick="var u=this.getAttribute('data-url'); if(u) window.open(u,'_blank');">
                    <span class="btn-icon">🚀</span>
                    <span class="btn-text">Відкрити паспорт модуля</span>
                </button>
            </div>
        </div>
    </div>
</div>

<script src="../atlas_data.js"></script>
<script src="../atlas_logic.js"></script>
