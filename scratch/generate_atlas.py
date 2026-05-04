import os

def generate_atlas():
    base_dir = "d:/yhoba/1/Test/Py"
    src_dir = os.path.join(base_dir, "src")
    scripts_dir = os.path.join(base_dir, "scripts")
    tests_dir = os.path.join(base_dir, "tests")

    zones = {
        "CORE": {"files": [], "color": "#fb923c", "pos": (320, 250), "size": (360, 320)},
        "ML": {"files": [], "color": "#c084fc", "pos": (650, 20), "size": (330, 250)},
        "UI": {"files": [], "color": "#4ade80", "pos": (700, 420), "size": (280, 330)},
        "SERVICES": {"files": [], "color": "#38bdf8", "pos": (20, 450), "size": (280, 300)},
        "SCRIPTS": {"files": [], "color": "#f472b6", "pos": (20, 20), "size": (280, 350)},
        "TESTS": {"files": [], "color": "#94a3b8", "pos": (320, 600), "size": (360, 150)},
    }

    # Scan and categorize
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), base_dir).replace("\\", "/")
                
                if rel_path.startswith("src/core"): zones["CORE"]["files"].append(rel_path)
                elif rel_path.startswith("src/ml"): zones["ML"]["files"].append(rel_path)
                elif rel_path.startswith("src/ui"): zones["UI"]["files"].append(rel_path)
                elif rel_path.startswith("src/services"): zones["SERVICES"]["files"].append(rel_path)
                elif rel_path.startswith("scripts"): zones["SCRIPTS"]["files"].append(rel_path)
                elif rel_path.startswith("tests"): zones["TESTS"]["files"].append(rel_path)

    # Generate SVG
    svg_parts = []
    for name, data in zones.items():
        x, y = data["pos"]
        w, h = data["size"]
        color = data["color"]
        
        svg_parts.append(f'<g class="zone" transform="translate({x}, {y})">')
        svg_parts.append(f'  <rect width="{w}" height="{h}" rx="15" class="zone-bg" style="stroke:{color}; fill:{color}0D"/>')
        svg_parts.append(f'  <text x="{w/2}" y="25" text-anchor="middle" class="zone-title">{name}</text>')
        
        # Add chips
        for i, file_path in enumerate(data["files"]):
            row = i // 3
            col = i % 3
            chip_x = 10 + col * (w/3 - 10)
            chip_y = 40 + row * 25
            if chip_y + 25 > h: continue # Skip if out of bounds for now
            
            label = file_path.split("/")[-1]
            svg_parts.append(f'  <g class="file-chip" transform="translate({chip_x}, {chip_y})" onclick="window.open(\'https://github.com/Lutvunenko-Dmutro/EnergyMonitor-OLAP/blob/main/{file_path}\')">')
            svg_parts.append(f'    <rect width="{w/3 - 15}" height="20" rx="4"/>')
            svg_parts.append(f'    <text x="{(w/3 - 15)/2}" y="14">{label[:15]}</text>')
            svg_parts.append(f'  </g>')
        svg_parts.append(f'</g>')

    # Write to file
    md_header = """# 🗺️ Повний Інженерний Атлас Проєкту (v4.2)

Це автоматично згенерована мапа всіх програмних компонентів системи.

<div class="atlas-v4-container full-atlas">
    <svg viewBox="0 0 1000 800" xmlns="http://www.w3.org/2000/svg" class="atlas-svg">
        <defs>
            <filter id="glow-full"><feGaussianBlur stdDeviation="1.5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
"""
    md_footer = """
    </svg>
</div>

<style>
.full-atlas { background: #020617 !important; overflow: hidden; }
.zone-bg { fill: #0f172a; stroke-width: 1; stroke-opacity: 0.5; }
.zone-title { fill: #64748b; font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 900; letter-spacing: 1px; }
.file-chip { cursor: pointer; transition: 0.2s; }
.file-chip rect { fill: #1e293b; stroke: rgba(148, 163, 184, 0.2); stroke-width: 1; }
.file-chip text { fill: #94a3b8; font-family: 'JetBrains Mono', monospace; font-size: 8px; pointer-events: none; text-anchor: middle; }
.file-chip:hover rect { fill: #334155; stroke: #fff; filter: url(#glow-full); }
.file-chip:hover text { fill: #fff; }
</style>
"""
    with open("d:/yhoba/1/Test/Py/docs/system/atlas_v4.md", "w", encoding="utf-8") as f:
        f.write(md_header)
        f.write("\n".join(svg_parts))
        f.write(md_footer)

generate_atlas()
print("Atlas v4.2 generated successfully!")
