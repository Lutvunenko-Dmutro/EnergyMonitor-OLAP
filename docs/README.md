<p align="right">
  <a href="README.md"><img src="https://flagcdn.com/24x18/us.png" alt="English"> English</a> |
  <a href="README.uk.md"><img src="https://flagcdn.com/24x18/ua.png" alt="Українська"> Українська</a>
</p>

---

# 📚 Architecture & System Documentation (`docs/`)

Welcome to the central repository for the EnergyMonitor-OLAP documentation. This folder serves as the single source of truth for the system's architecture, UI/UX designs, and module specifications. We use a strict "Documentation as Code" approach, ensuring documentation evolves synchronously with the codebase.

## 🗺️ The ProperDocs System (System Passports)
We use a custom documentation architecture called **ProperDocs** (located in `system/map/`).
Every critical Python module in the `src/` directory has a corresponding Markdown "Passport" here.

**What a Passport includes:**
- Component definition and responsibilities.
- Data flow architecture.
- Interfaces and dependencies.
- Known limitations or future upgrade paths.

These passports can be automatically validated for structural integrity by running `scripts/audit_passports.py` via the Developer Dashboard.

## 🎨 UI/UX Mockups & Exports
The `ui/` directory contains exported interactive HTML mockups and structural overviews of the frontend views. These are used to align the design language before implementing the Streamlit components.

- `ui.html`: Main application layout overview.
- `ui/views/`: Individual component mockups (Finance, Generation, Alerts).

## 🚀 Keeping Docs Updated
To ensure documentation never falls out of sync, developers must run the `rebuild_master_index.py` script after adding new passports, which automatically regenerates the master index navigation tree.
