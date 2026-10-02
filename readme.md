# Snowflake CoCo CLI Hackathon Project

This workspace is configured for the **Snowflake CoCo Hackathon**.

The requirements, lifecycle phases, and CoCo capabilities below are **universal across all 5 tracks**. Regardless of the track selected, your submission will be evaluated on adherence to these guidelines, full-lifecycle CoCo adoption, technical completeness, and ingenuity.

---

## 1. Universal Evaluation Criteria

Judges will score submissions on three primary pillars across every track:
1. **Real-World Relevance:** Clear business problem, realistic domain data, tangible enterprise ROI, and human-in-the-loop workflows.
2. **Technical Execution:** Clean architecture, robust use of native Snowflake primitives (Dynamic Tables, Streams, Tasks, Cortex Search, Cortex Analyst, Semantic Views), and solid code quality.
3. **Solution Completeness:** True end-to-end functionality from raw synthetic ingestion to interactive UI presentation and external tool action.

---

## 2. Mandatory Full-Lifecycle CoCo Usage

Every team must demonstrate using **CoCo (CLI / Desktop app)** across all four phases of development. Teams must capture evidence (terminal logs, session history, screen recordings, generated artifacts) in each phase:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COCO END-TO-END LIFECYCLE                       │
└────────────────────────────────────────────────────────────────────────┘
       │
       ▼
 1. PLANNING PHASE
    - Explore raw schema and problem domain via CoCo CLI prompts
    - Draft solution architecture, entity relationships, and ontology
    - Outline pipeline DAGs and semantic models before writing code
       │
       ▼
 2. DEVELOPMENT PHASE
    - Generate synthetic, referentially sound data using CoCo
    - Build data pipelines (Dynamic Tables, Streams, Tasks) via CoCo CLI
    - Author semantic models, verified queries, and Cortex search services
    - Scaffold Streamlit application code directly through CoCo
       │
       ▼
 3. EXECUTION & ORCHESTRATION PHASE
    - Run and trigger end-to-end pipelines through CoCo
    - Set up automated / scheduled runs for unattended processing
    - Orchestrate agent workflows and tool invocations
       │
       ▼
 4. TESTING & VALIDATION PHASE
    - Validate output accuracy and verify hallucination guardrails
    - Test edge cases, missing data, and schema drift handling
    - Verify confidence scores and graceful error fallbacks with CoCo
```

---

## 3. Core Technical Capabilities to Demonstrate

To maximize base scoring, your solution must hit all 6 recommended CoCo tasks:

| # | Task | Purpose | Implementation Location |
|---|---|---|---|
| **1** | **Synthetic Data Generation** | Realistic, referentially consistent data respecting zero-production privacy | `data/` |
| **2** | **Data Pipeline Creation** | Dynamic Tables, Streams, and Tasks orchestrating real-time / batch flows | `pipelines/` |
| **3** | **Semantic Model & Ontology** | Business entity model, canonical metrics, and verified queries | `semantics/` |
| **4** | **Streamlit App Generation** | Interactive dashboard for insight discovery and business action dispatch | `app/` |
| **5** | **MCP Tool Integration** | Connectors to external tools (Slack, Jira, ServiceNow, Google Drive) | `mcp/` |
| **6** | **Unstructured Document Processing** | Cortex Search / chunking over PDFs, transcripts, and policies | `data/docs/` & `pipelines/` |

---

## 4. Ways to Showcase Ingenuity (Bonus Scoring)

To achieve top-tier placement, incorporate as many of these advanced CoCo patterns as possible:

* [ ] **Reusable & Shareable Skills:** Package core logic into modular, exportable CoCo agent skills located in `skills/`.
* [ ] **MCP Connectors to External Tools:** Don't just answer in chat; trigger real-world write actions (e.g., filing a Jira ticket, posting a Slack escalation).
* [ ] **Automations & Scheduled Runs:** Implement unattended scheduled background runs in CoCo CLI or Snowflake Tasks.
* [ ] **Custom Tools & Function Calling:** Register domain-specific tools the agent can invoke dynamically.
* [ ] **Multi-Agent Orchestration:** Split responsibilities into specialized agents (e.g., Forensic Analyst + Regulatory Compliance Officer) with clean handoffs.
* [ ] **Cross-Surface Workflow:** Demonstrate identical functionality across CoCo CLI, Desktop app, and Snowsight Cloud Agents.
* [ ] **Guardrails & Graceful Fallback:** Include explicit confidence scoring, source citations, and fallback safety boundaries.

---

## 5. Repository Structure

```
├── Tracks.md             # Complete track descriptions, criteria, and analysis
├── readme.md             # Universal CoCo lifecycle and project guide (this file)
├── data/                 # Raw schemas, synthetic generators, seed CSVs/JSONs
│   └── docs/             # Unstructured PDFs, regulatory texts, or manuals
├── pipelines/            # SQL scripts: Dynamic Tables, Streams, Tasks, Stored Procedures
├── semantics/            # Semantic YAML models, ontology definitions, verified queries
├── skills/               # Reusable custom CoCo agent skills and prompts
├── mcp/                  # MCP server configs and integration scripts (Jira, Slack, etc.)
├── app/                  # Streamlit application frontend and command center
├── tests/                # Validation scripts, accuracy tests, and guardrail checks
└── docs/                 # Architecture diagrams, pitch deck, and CoCo session logs
```

---

## 6. CoCo CLI Quickstart Prompts Template

### Step 1: Planning with CoCo
```bash
coco "Act as an Enterprise Solutions Architect. Analyze our domain requirements and design the entity relationship ontology, Snowflake pipeline DAG (Dynamic Tables, Streams), and semantic views."
```

### Step 2: Synthetic Data Generation
```bash
coco "Generate a referentially consistent synthetic dataset for [Domain] with tables [A, B, C], edge cases, and anomaly scenarios. Save as SQL DDL and seed scripts in data/."
```

### Step 3: Pipeline & Semantic Authoring
```bash
coco "Generate Snowflake Dynamic Tables and Streams to detect anomalies incrementally, plus a Semantic Model YAML defining canonical metrics."
```

### Step 4: Streamlit & MCP Scaffolding
```bash
coco "Scaffold a multi-page Streamlit application connecting to Snowflake with an interactive dashboard, evidence viewer, and an MCP tool trigger button."
```
