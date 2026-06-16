/**
 * 🛰️ Project Atlas - Core UI Logic (Sync with blueprint.css)
 */

function initBlueprint() {
    const container = document.getElementById('blueprint-tree');
    if (!container) return;
    container.innerHTML = '';
    
    // Побудова ієрархії
    const nodeMap = {};
    ATLAS_DATA.nodes.forEach(node => {
        nodeMap[node.id] = { ...node, children: [] };
    });
    
    const rootNodes = [];
    ATLAS_DATA.nodes.forEach(node => {
        if (node.parent_id && nodeMap[node.parent_id]) {
            nodeMap[node.parent_id].children.push(nodeMap[node.id]);
        } else {
            rootNodes.push(nodeMap[node.id]);
        }
    });
    
    // Сортування: спочатку папки, потім файли
    const sortNodes = (nodes) => {
        return nodes.sort((a, b) => {
            if (a.type === b.type) return a.name.localeCompare(b.name);
            return a.type === 'folder' ? -1 : 1;
        });
    };

    const renderTree = (nodes, parentEl) => {
        sortNodes(nodes).forEach(node => {
            if (node.type === 'folder') {
                const folderItem = document.createElement('div');
                folderItem.className = 'tree-item tree-folder';
                folderItem.onclick = (e) => {
                    e.stopPropagation();
                    toggleFolder(folderItem, node.id);
                };
                folderItem.innerHTML = `
                    <span class="toggle-icon">▶</span>
                    <span class="node-icon">📁</span>
                    <span class="node-name">${node.name}</span>
                `;
                parentEl.appendChild(folderItem);

                const content = document.createElement('div');
                content.className = 'folder-content';
                content.id = `folder-content-${node.id}`;
                parentEl.appendChild(content);
                
                if (node.children.length > 0) {
                    renderTree(node.children, content);
                }
            } else {
                const isPython = node.name.endsWith('.py');
                const fileIcon = isPython ? '🐍' : '📄';
                
                const fileItem = document.createElement('div');
                fileItem.className = 'tree-item tree-file';
                fileItem.onclick = (e) => {
                    e.stopPropagation();
                    showDetails(node.id, fileItem);
                };
                fileItem.innerHTML = `
                    <span class="node-icon">${fileIcon}</span>
                    <span class="node-name">${node.name}</span>
                `;
                parentEl.appendChild(fileItem);
            }
        });
    };

    renderTree(rootNodes, container);
}

function toggleFolder(el, folderId) {
    const content = document.getElementById(`folder-content-${folderId}`);
    const icon = el.querySelector('.toggle-icon');
    if (content.classList.contains('expanded')) {
        content.classList.remove('expanded');
        icon.textContent = '▶';
    } else {
        content.classList.add('expanded');
        icon.textContent = '▼';
    }
}

function showDetails(nodeId, el) {
    const node = ATLAS_DATA.nodes.find(n => n.id === nodeId);
    if (!node) return;
    
    document.getElementById('details-placeholder').style.display = 'none';
    const contentBox = document.getElementById('details-content');
    contentBox.style.display = 'block';
    
    document.getElementById('details-type').textContent = node.type.toUpperCase();
    document.getElementById('details-name').textContent = node.name;
    document.getElementById('details-path').textContent = node.path;
    
    // Смарт-парсинг тексту
    const rawDesc = node.short_description || "";
    const lines = rawDesc.split('\n');
    let htmlResult = '';

    lines.forEach(line => {
        const trimmedLine = line.trim();
        if (!trimmedLine) return;

        if (trimmedLine.match(/^[^\w\s\d]/) || (trimmedLine === trimmedLine.toUpperCase() && trimmedLine.length > 5)) {
            htmlResult += `<div class="desc-title">${trimmedLine}</div>`;
        }
        else if (trimmedLine.includes(':') && !trimmedLine.startsWith('-')) {
            const [label, ...valParts] = trimmedLine.split(':');
            const value = valParts.join(':').trim();
            htmlResult += `
                <div class="desc-row">
                    <span class="desc-label">${label}:</span>
                    <span class="desc-value">${value}</span>
                </div>`;
        }
        else if (trimmedLine.startsWith('-') || trimmedLine.startsWith('*')) {
            const item = trimmedLine.substring(1).trim();
            htmlResult += `<div class="desc-list-item"><span class="bullet">▹</span> ${item}</div>`;
        }
        else {
            htmlResult += `<div class="desc-text">${trimmedLine}</div>`;
        }
    });

    document.getElementById('details-desc').innerHTML = htmlResult;
    
    // Динамічне відображення кнопки паспорта
    const btnContainer = document.getElementById('details-links');
    if (node.detail_link) {
        btnContainer.style.display = 'block';
        
        // Dynamically compute correct base path relative to system/atlas_final
        let basePath = "";
        const path = window.location.pathname;
        const systemIndex = path.indexOf("/system/atlas_final");
        if (systemIndex !== -1) {
            basePath = path.substring(0, systemIndex);
        }
        
        const origin = window.location.origin && window.location.origin !== 'null' ? window.location.origin : '';
        const finalUrl = origin + basePath + node.detail_link;
        
        document.getElementById('details-btn').setAttribute('data-url', finalUrl);
    } else {
        btnContainer.style.display = 'none';
    }
    
    // Підсвітка активного вузла
    document.querySelectorAll('.tree-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
}

// Пошук
document.addEventListener('DOMContentLoaded', () => {
    initBlueprint();
    
    const searchInput = document.getElementById('blueprint-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            document.querySelectorAll('.tree-file').forEach(item => {
                const name = item.querySelector('.node-name').textContent.toLowerCase();
                if (name.includes(term)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
});
