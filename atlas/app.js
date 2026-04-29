var cy;

function initCy() {
    try {
        if (typeof CODE_GRAPH === 'undefined') {
            document.getElementById('loader-status').innerText = 'Data not found';
            return;
        }

        cy = cytoscape({
            container: document.getElementById('cy'),
            style: [
                { selector: 'node[type="folder"]', style: { 'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#1e293b', 'background-opacity': 0.5, 'border-width': 2, 'border-color': 'rgba(255, 255, 255, 0.1)', 'color': '#ffffff', 'font-family': 'Inter', 'font-size': '20px', 'font-weight': '900', 'text-valign': 'top', 'text-halign': 'center', 'text-margin-y': -15, 'padding': 40, 'z-index': 5 } },
                { selector: 'node[type="file"]', style: { 'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#0d1117', 'background-opacity': 0.8, 'border-width': 1, 'border-color': 'rgba(148, 163, 184, 0.3)', 'color': '#ffffff', 'font-family': 'Inter', 'font-size': '14px', 'font-weight': 'bold', 'text-valign': 'top', 'text-halign': 'center', 'text-margin-y': -10, 'padding': 20, 'z-index': 10 } },
                { selector: 'node[type="file"]:childless', style: { 'background-opacity': 0.4, 'border-color': 'rgba(148, 163, 184, 0.1)', 'color': '#64748b' } },
                { selector: 'node.cy-expand-collapse-collapsed-node', style: { 'border-color': '#10b981', 'border-style': 'dashed', 'border-width': 2, 'background-color': '#131e2e' } },
                { selector: 'node[type="function"]', style: { 'label': 'data(label)', 'color': '#8b949e', 'font-family': 'JetBrains Mono', 'font-size': '10px', 'background-color': '#94a3b8', 'width': '10px', 'height': '10px', 'text-valign': 'bottom', 'text-margin-y': 6, 'z-index': 100 } },
                // Domain Colors
                { selector: 'node[domain="ml"][type="function"]', style: { 'background-color': '#c084fc', 'shadow-color': '#c084fc', 'shadow-blur': 10 } },
                { selector: 'node[domain="ui"][type="function"]', style: { 'background-color': '#38bdf8', 'shadow-color': '#38bdf8', 'shadow-blur': 10 } },
                { selector: 'node[domain="core"][type="function"]', style: { 'background-color': '#fb923c', 'shadow-color': '#fb923c', 'shadow-blur': 10 } },
                { selector: 'node[domain="tests"][type="function"]', style: { 'background-color': '#4ade80', 'shadow-color': '#4ade80', 'shadow-blur': 10 } },
                { selector: 'node[domain="scripts"][type="function"]', style: { 'background-color': '#f472b6', 'shadow-color': '#f472b6', 'shadow-blur': 10 } },
                
                { selector: 'edge', style: { 'width': 1.5, 'line-color': 'rgba(148, 163, 184, 0.5)', 'curve-style': 'taxi', 'taxi-direction': 'vertical', 'taxi-turn': 20, 'taxi-turn-min-distance': 10, 'target-arrow-shape': 'triangle', 'target-arrow-color': 'rgba(148, 163, 184, 0.5)', 'arrow-scale': 0.5, 'opacity': 0.05, 'z-index': 50 } },
                { selector: '.highlight', style: { 'width': '14px', 'height': '14px', 'font-size': '12px', 'z-index': 1000, 'color': '#fff' } },
                { selector: '.active-edge-in', style: { 'line-color': '#f87171', 'width': 3, 'opacity': 1, 'z-index': 500, 'target-arrow-color': '#f87171', 'arrow-scale': 1 } },
                { selector: '.active-edge-out', style: { 'line-color': '#4ade80', 'width': 3, 'opacity': 1, 'z-index': 500, 'target-arrow-color': '#4ade80', 'arrow-scale': 1 } },
                { selector: '.hover-node', style: { 'background-color': '#fff', 'width': '12px', 'height': '12px', 'z-index': 999 } },
                { selector: '.dimmed', style: { 'opacity': 0.03 } }
            ]
        });

        // Add nodes: Folders first, then Files, then Functions to maintain correct DOM layering
        const sortedNodes = [...CODE_GRAPH.nodes].sort((a, b) => {
            const getRank = t => t === 'folder' ? 1 : t === 'file' ? 2 : 3;
            return getRank(a.type) - getRank(b.type);
        });
        sortedNodes.forEach(n => { try { cy.add({ group: 'nodes', data: n }); } catch(e){} });
        
        CODE_GRAPH.edges.forEach((e, i) => {
            if (cy.getElementById(e.source).length > 0 && cy.getElementById(e.target).length > 0) {
                try { cy.add({ group: 'edges', data: { id: 'e'+i, source: e.source, target: e.target } }); } catch(e){}
            }
        });

        document.getElementById('stat-nodes').innerText = cy.nodes().length;

        // CUSTOM DETERMINISTIC ARCHITECTURE LAYOUT
        // 1. Grid functions inside files
        cy.nodes('[type="file"]').forEach(parent => {
            const children = parent.children();
            if (children.length > 0) {
                const cols = Math.ceil(Math.sqrt(children.length));
                const sortedChildren = children.toArray().sort((a, b) => a.data('label').localeCompare(b.data('label')));
                
                sortedChildren.forEach((n, idx) => {
                    const row = Math.floor(idx / cols);
                    const col = idx % cols;
                    n.position({ x: col * 150, y: row * 80 });
                });
            }
        });

        // 2. Arrange files by Architectural Domain Layers
        const domainOrder = ['ui', 'scripts', 'ml', 'core', 'other', 'tests'];
        let currentY = 0;
        
        domainOrder.forEach(domain => {
            const files = cy.nodes(`[type="file"][domain="${domain}"]`);
            if (files.length === 0) return;
            
            const sortedFiles = files.toArray().sort((a, b) => a.data('label').localeCompare(b.data('label')));
            let currentX = 0;
            let maxRowHeight = 0;
            const maxFilesPerRow = 4; // Перенос на новий рядок після 4 файлів
            let fileCountInRow = 0;
            
            sortedFiles.forEach(file => {
                const children = file.children();
                let width = 200;
                let height = 80;
                let bb = null;
                
                if (children.length > 0) {
                    bb = children.boundingBox();
                    width = bb.w || 200;
                    height = bb.h || 80;
                }
                
                // Якщо файлів в рядку забагато — переносимо вниз
                if (fileCountInRow >= maxFilesPerRow) {
                    currentX = 0;
                    currentY += maxRowHeight + 200; // Відступ між рядами одного домену
                    maxRowHeight = 0;
                    fileCountInRow = 0;
                }
                
                if (children.length > 0) {
                    const deltaX = currentX - bb.x1;
                    const deltaY = currentY - bb.y1;
                    children.forEach(n => {
                        n.position({ x: n.position('x') + deltaX, y: n.position('y') + deltaY });
                    });
                } else {
                    file.position({ x: currentX, y: currentY });
                }
                
                currentX += width + 150; // Відступ між файлами
                if (height > maxRowHeight) maxRowHeight = height;
                fileCountInRow++;
            });
            
            currentY += maxRowHeight + 500; // Великий відступ між архітектурними шарами (доменами)
        });
        
        cy.fit(cy.elements(), 50);
        
        // Initialize Expand/Collapse API (Foldable Files)
        const api = cy.expandCollapse({
            layoutBy: null, // We handle layout manually
            fisheye: false,
            animate: true,
            undoable: false,
            expandCollapseCuePosition: 'top-left',
            expandCollapseCueSize: 16,
            expandCueImage: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23ffffff" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>',
            collapseCueImage: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23ffffff" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="8" y1="12" x2="16" y2="12"></line></svg>'
        });
        
        // Collapse all by default to clear clutter
        api.collapseAll();
        
        hideLoader();

        setupEvents();

        setTimeout(hideLoader, 5000);

    } catch(e) { console.error(e); hideLoader(); }
}

function setupEvents() {
    cy.on('mouseover', 'node', function(evt){
        const node = evt.target;
        if (node.data('type') === 'function') {
            node.addClass('hover-node');
            node.connectedEdges().style('opacity', 1).style('line-color', 'var(--accent)');
        }
    });

    cy.on('mouseout', 'node', function(evt){
        const node = evt.target;
        node.removeClass('hover-node');
        node.connectedEdges().removeStyle('opacity').removeStyle('line-color');
    });

    cy.on('tap', 'node', function(evt){
        focusNode(evt.target.id());
    });
}

function hideLoader() {
    const loader = document.getElementById('loader');
    if (!loader || loader.style.display === 'none') return;
    document.getElementById('progress-bar').style.width = '100%';
    document.getElementById('loader-status').innerText = 'READY';
    setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => { loader.style.display = 'none'; }, 1000);
    }, 500);
}

function runLayout() {
    const layout = cy.layout({ name: 'cose', animate: true, nodeRepulsion: 15000, idealEdgeLength: 150 });
    layout.run();
}

function focusNode(id) {
    const node = cy.getElementById(id);
    const data = node.data();
    cy.elements().removeClass('dimmed active-edge-in active-edge-out highlight');
    
    const selection = node.neighborhood().add(node).add(node.ancestors()).add(node.descendants());
    cy.elements().not(selection).addClass('dimmed');
    node.addClass('highlight');
    
    if (data.type === 'function') {
        node.incomingEdges().addClass('active-edge-in');
        node.outgoingEdges().addClass('active-edge-out');
    }
    
    document.getElementById('inspector').classList.add('active');
    document.getElementById('i-label').innerText = data.label;
    
    const domainColors = { 'ml': '#c084fc', 'ui': '#38bdf8', 'core': '#fb923c', 'tests': '#4ade80', 'scripts': '#f472b6', 'other': '#22d3ee' };
    const dColor = domainColors[data.domain] || '#94a3b8';
    
    document.getElementById('i-module').innerHTML = `<span style="color:${dColor}; font-weight:bold; text-transform:uppercase;">[${data.domain || 'SYSTEM'}]</span> ` + (data.type === 'file' ? 'FILE: ' : 'FUNCTION: ') + id;
    
    const docContainer = document.getElementById('i-doc-container');
    const codePre = document.getElementById('i-code');
    
    if (data.type === 'function') {
        docContainer.style.display = data.docstring ? 'block' : 'none';
        if (data.docstring) document.getElementById('i-doc').innerText = data.docstring;
        codePre.parentElement.style.display = 'block';
        codePre.innerText = data.code || "// No source available";
        
        const depsList = document.getElementById('i-deps');
        depsList.innerHTML = '';
        node.incomingEdges().forEach(edge => {
            const li = document.createElement('li');
            li.className = 'dep-item';
            li.innerHTML = `<span style="background:#f87171; color:white; padding:2px 4px; border-radius:4px; font-size:0.5rem; margin-right:8px;">CALLED BY</span> <b style="color:#e2e8f0">${edge.source().data('label')}</b> <span style="color:#64748b; font-size:0.6rem;">(${edge.source().data('domain')})</span>`;
            depsList.appendChild(li);
        });
        node.outgoingEdges().forEach(edge => {
            const li = document.createElement('li');
            li.className = 'dep-item';
            li.innerHTML = `<span style="background:#4ade80; color:white; padding:2px 4px; border-radius:4px; font-size:0.5rem; margin-right:8px;">CALLS</span> <b style="color:#e2e8f0">${edge.target().data('label')}</b> <span style="color:#64748b; font-size:0.6rem;">(${edge.target().data('domain')})</span>`;
            depsList.appendChild(li);
        });
        
        document.getElementById('execution-panel').style.display = 'block';
        window.currentExecNode = data;
        
    } else {
        document.getElementById('execution-panel').style.display = 'none';
        window.currentExecNode = null;
        docContainer.style.display = 'none';
        codePre.parentElement.style.display = 'none';
        document.getElementById('i-deps').innerHTML = `<li style="opacity:0.5;">${data.type === 'folder' ? 'Контейнер для модулів проекту' : 'Файл з визначеннями функцій'}</li>`;
    }
}

async function executeFunction() {
    if (!window.currentExecNode) return;
    
    const argsStr = document.getElementById('exec-args').value || '[]';
    const kwargsStr = document.getElementById('exec-kwargs').value || '{}';
    
    let args, kwargs;
    try { args = JSON.parse(argsStr); } catch(e) { alert("Invalid ARGS JSON. Must be a list like [1, 2]"); return; }
    try { kwargs = JSON.parse(kwargsStr); } catch(e) { alert("Invalid KWARGS JSON. Must be an object like {\"a\": 1}"); return; }
    
    const parts = window.currentExecNode.id.split('.');
    const funcName = parts.pop();
    const moduleName = parts.join('.');
    
    // Switch to Terminal tab to show results
    switchTab('main');
    const consoleOut = document.getElementById('console-output');
    consoleOut.innerHTML += `\n<div style="color:#10b981;">&gt; Executing ${moduleName}.${funcName}(...)</div>`;
    
    try {
        const response = await fetch('http://localhost:8001/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                module: moduleName,
                function: funcName,
                args: args,
                kwargs: kwargs
            })
        });
        
        const resData = await response.json();
        
        if (resData.status === 'success') {
            if (resData.output) consoleOut.innerHTML += `\n<span style="color:#94a3b8">${resData.output}</span>`;
            consoleOut.innerHTML += `\n<span style="color:#38bdf8">Result: ${resData.result}</span>`;
        } else {
            if (resData.output) consoleOut.innerHTML += `\n<span style="color:#94a3b8">${resData.output}</span>`;
            consoleOut.innerHTML += `\n<span style="color:#f87171">Error: ${resData.error}\n${resData.traceback}</span>`;
        }
    } catch (e) {
        consoleOut.innerHTML += `\n<span style="color:#f87171">Fetch Error: Could not reach Atlas Server. Make sure atlas_server.py is running!</span>`;
    }
    consoleOut.scrollTop = consoleOut.scrollHeight;
}


function focusMain() {
    const mainNode = cy.nodes().filter(n => n.id().includes('main.py') || n.id() === 'main');
    if (mainNode.length === 0) return;
    cy.elements().addClass('dimmed');
    const collection = mainNode.successors().add(mainNode);
    collection.removeClass('dimmed');
    collection.ancestors().removeClass('dimmed');
    cy.animate({ fit: { eles: collection, padding: 50 } }, { duration: 800 });
}

function resetFilter() {
    cy.elements().removeClass('dimmed');
    cy.animate({ fit: { padding: 50 } }, { duration: 800 });
}

function filterGraph() {
    const term = document.getElementById('search-input').value.toLowerCase();
    if (!term) { resetFilter(); return; }
    cy.elements().addClass('dimmed');
    cy.nodes().filter(n => n.data('label').toLowerCase().includes(term)).removeClass('dimmed').neighborhood().removeClass('dimmed').ancestors().removeClass('dimmed');
}

function closeInspector() {
    document.getElementById('inspector').classList.remove('active');
    cy.elements().removeClass('dimmed active-edge-in active-edge-out highlight');
}

let currentTab = 'main';
function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.console-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('tab-' + tab).classList.add('active');
    renderLogs();
}

function renderLogs() {
    if (typeof ATLAS_LOGS === 'undefined') return;
    const container = document.getElementById('console-output');
    const logs = currentTab === 'main' ? ATLAS_LOGS.main : ATLAS_LOGS.errors;
    container.innerHTML = logs.map(line => `<div class="log-entry">${line}</div>`).join('');
    container.scrollTop = container.scrollHeight;
}

function updateData() {
    const s1 = document.createElement('script');
    s1.src = "logs_data.js?t=" + Date.now();
    s1.onload = () => { renderLogs(); s1.remove(); };
    document.head.appendChild(s1);

    const s2 = document.createElement('script');
    s2.src = "status.js?t=" + Date.now();
    s2.onload = () => {
        if (typeof SYSTEM_STATUS !== 'undefined') {
            document.getElementById('led-ml').className = 'status-led ' + (SYSTEM_STATUS.ml_engine === 'online' ? 'led-green' : 'led-dim');
            document.getElementById('led-ui').className = 'status-led ' + (SYSTEM_STATUS.ui_dashboard === 'online' ? 'led-green' : 'led-dim');
            document.getElementById('led-sim').className = 'status-led ' + (SYSTEM_STATUS.simulation === 'online' ? 'led-blink' : 'led-dim');
        }
        s2.remove();
    };
    document.head.appendChild(s2);
}

window.onload = () => {
    initCy();
    lucide.createIcons();
    setInterval(updateData, 3000);
    let p = 0;
    const iv = setInterval(() => {
        p += (95 - p) * 0.1;
        const pb = document.getElementById('progress-bar');
        if (pb) pb.style.width = p + '%';
        if (p > 90) clearInterval(iv);
    }, 200);
};
