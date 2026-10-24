#!/usr/bin/env python3
import re

README_PATH = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/README.md"

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace markdown relative image links with absolute raw GitHub image links with responsive <img> tags
content = content.replace(
    "![Connected Digital Twin & Command Center](docs/screenshots/01_connected_digital_twin.png)",
    '<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/01_connected_digital_twin.png" alt="Connected 3D Digital Twin & Real-Time Command Center" width="100%"/></p>'
)

content = content.replace(
    "![Ask CoCo Copilot Modal](docs/screenshots/02_ask_coco_cortex_modal.png)",
    '<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/02_ask_coco_cortex_modal.png" alt="Ask CoCo Copilot with 3-Way Reconciliation Ledger" width="100%"/></p>'
)

content = content.replace(
    "![Cortex What-If Simulator](docs/screenshots/03_what_if_simulator.png)",
    '<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/03_what_if_simulator.png" alt="Cortex What-If Mitigation Simulator" width="100%"/></p>'
)

content = content.replace(
    "![Governed Decision Approvals Queue](docs/screenshots/04_governed_approvals_mcp.png)",
    '<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/04_governed_approvals_mcp.png" alt="Governed Decision Approvals Queue & Action MCP" width="100%"/></p>'
)

content = content.replace(
    "![CoCo CLI in VS Code Terminal](docs/screenshots/05_coco_cli_vscode.png)",
    '<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/05_coco_cli_vscode.png" alt="CoCo CLI Working Live in VS Code Terminal" width="100%"/></p>'
)

content = content.replace(
    "![Snowflake Horizon Audit Trail](docs/screenshots/06_snowflake_horizon_audit.png)",
    '<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/06_snowflake_horizon_audit.png" alt="Snowflake Horizon Audit Trail & Cryptographic Governance" width="100%"/></p>'
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated README.md image links to robust raw.githubusercontent.com tags.")
