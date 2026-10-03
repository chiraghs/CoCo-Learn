# Track 5: Supply Chain Ontology & Governed Conversational Analytics
## Master Architecture & Implementation Plan

---

## 1. Executive Summary & Narrative Hook

### The Real-World Crisis Scenario
* **Enterprise Context:** A global high-tech / EV manufacturer assembling battery packs and powertrains across 3 assembly plants (Fremont, Austin, Berlin).
* **The Disruption:** A critical maritime bottleneck and port congestion delay key lithium-ion cells and microcontrollers from Southeast Asian suppliers.
* **The Classic Enterprise Failure:**
  * **Procurement VP asks:** *"What is our supplier delay exposure and penalty liability?"* $\to$ pulls PO promised dates, calculates \$2.4M delay penalties.
  * **Logistics Director asks:** *"What is our On-Time In-Full (OTIF) rate and container transit delay?"* $\to$ pulls Carrier Bill of Lading arrival dates, reports 81% OTIF.
  * **Plant Operations Manager asks:** *"How many days of inventory do we have before Plant 2 assembly lines halt?"* $\to$ pulls local warehouse buffer, estimates 4.5 days until stockout.
  * **The Problem:** Three leaders receive conflicting numbers with inconsistent definitions of "Delivery Date", "Landed Cost", and "Defect Rate".

### The Solution: CoCo Governed Supply Chain Ontology
We build an end-to-end industry ontology and governed conversational analytics engine in Snowflake that:
1. **Grounds Business Semantics:** Encodes relationships ($\text{Supplier} \to \text{Part} \to \text{Plant} \to \text{Shipment} \to \text{Order}$) and canonical metrics so every persona receives mathematically consistent, auditable answers.
2. **Combines Structured + Unstructured:** Unifies real-time ERP/WMS tables with supplier contract Master Service Agreements (MSAs) and Bills of Lading to automatically evaluate SLA breach penalties via Snowflake Cortex.
3. **Closes the Loop via MCP:** Takes real action by triggering expedited freight orders and issuing contractual SLA breach alerts to supplier reps on Slack.

---

## 2. Target Personas & Core Workflows

| Persona | Primary Questions | Critical Metrics Needed | Action Required |
|---|---|---|---|
| **VP of Procurement** | "Which suppliers are causing the highest financial risk, and can we claim liquidated damages?" | Landed Cost, Supplier Lead Time Variance, SLA Penalty Exposure | Issue Contractual Breach Notice |
| **Logistics Director** | "Which shipping lanes have failed OTIF thresholds, and what are alternative air routes?" | OTIF (On-Time In-Full %), Transit Time Deviation, Demurrage Cost | Expedite Shipment / Re-route |
| **Plant Operations Manager**| "When will Plant 2 run out of Battery Module B-402, and what is our stockout burn rate?" | Days of Inventory (DOI), Stockout Risk Date, Buffer Run-rate | Reroute Parts Between Plants |

---

## 3. Data Architecture & Entity Relationship Ontology

```
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│  SUPPLIERS   │──1:N────▶│    PARTS     │──M:N────▶│    PLANTS    │
│ (Vendor Master)         │ (Catalog/BOM)│          │ (Facilities) │
└──────┬───────┘          └──────┬───────┘          └──────┬───────┘
       │                         │                         │
      1:N                       1:N                       1:N
       │                         │                         │
       ▼                         ▼                         ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│PURCHASE_ORDER│──1:N────▶│  SHIPMENTS   │──1:N────▶│  INVENTORY   │
│  (Contracts) │          │  (Logistics) │          │ (Stock/WMS)  │
└──────────────┘          └──────────────┘          └──────────────┘
       ▲
       │ (References SLA Clauses)
┌──────────────┐
│  MSAs / PDFs │ (Unstructured Contracts & Bills of Lading)
└──────────────┘
```

### Core Structured Tables (Synthetic Data Plan)
1. **`DIM_SUPPLIERS`**: `supplier_id`, `name`, `tier`, `country`, `lead_time_days`, `contract_msa_id`.
2. **`DIM_PARTS`**: `part_id`, `part_number`, `category`, `criticality` (High/Medium/Low), `unit_cost_usd`.
3. **`DIM_PLANTS`**: `plant_id`, `name`, `location`, `daily_production_target`, `daily_burn_rate`.
4. **`FACT_PURCHASE_ORDERS`**: `po_id`, `supplier_id`, `part_id`, `order_date`, `promised_delivery_date`, `quantity_ordered`, `po_status`.
5. **`FACT_SHIPMENTS`**: `shipment_id`, `po_id`, `carrier`, `origin_port`, `dest_port`, `etd`, `eta`, `actual_arrival_date`, `quantity_shipped`, `quantity_received`, `demurrage_charges`.
6. **`FACT_INVENTORY_LEVELS`**: `snapshot_date`, `plant_id`, `part_id`, `on_hand_qty`, `safety_stock_qty`, `in_transit_qty`.

### Unstructured Documents (Cortex Search & Document Intelligence)
* **`SUPPLIER_CONTRACTS` (PDFs/Text):** Master Service Agreements containing:
  * Grace periods (e.g. 72-hour delay allowance).
  * Liquidated damage penalties (e.g. \$1,500/day per delayed container).
  * Force Majeure clauses.
* **`BILLS_OF_LADING` (PDFs/Text):** Customs declaration details, port demurrage clauses, and container seal IDs.

---

## 4. Governed Semantic Views & Canonical Metric Formulas

To guarantee that all three personas get identical numbers, we define strict canonical metrics in Snowflake Semantic Views:

### 1. On-Time In-Full (OTIF) Rate
$$\text{OTIF \%} = \frac{\sum (\text{Shipments where Actual Arrival} \le \text{Promised Date AND Received Qty} \ge \text{Ordered Qty})}{\text{Total Completed Shipments}} \times 100$$

### 2. Days of Inventory (DOI)
$$\text{Days of Inventory} = \frac{\text{Current On-Hand Qty}}{\text{Average Daily Plant Burn Rate}}$$

### 3. Total Landed Cost
$$\text{Landed Cost} = \text{PO Unit Cost} + \text{Freight Cost} + \text{Tariff / Duties} + \text{Demurrage Penalty}$$

### 4. Supplier SLA Penalty Liability
$$\text{Penalty Liability} = \sum \max(0, (\text{Actual Arrival} - \text{Promised Date} - \text{Grace Days})) \times \text{Daily Liquidated Damages Rate}$$

---

## 5. End-to-End Pipeline & Snowflake Primitives

```
[Synthetic Seed Generators]
         │ (CoCo Data Generation)
         ▼
[STG_RAW_TABLES]
         │
         ▼
[DYNAMIC TABLES (Near Real-Time Updates)]
  ├── DT_SUPPLIER_PERFORMANCE_HOURLY
  ├── DT_PLANT_STOCKOUT_RISK
  └── DT_LOGISTICS_LANE_STATUS
         │
         ▼
[SNOWFLAKE SEMANTIC VIEWS (Governed Ontology)]
  ├── SEMANTIC_SUPPLY_CHAIN_MODEL.yaml
  └── Verified Queries Library
         │
         ▼
[CORTEX ANALYST & CORTEX SEARCH]
  ├── Cortex Analyst: Governed NL-to-SQL over Semantic Views
  └── Cortex Search: RAG over Supplier Contracts & MSAs
         │
         ▼
[INTERACTIVE STREAMLIT COMMAND CENTER]
  ├── Multi-Persona Switcher (Procurement / Logistics / Plant)
  ├── Single-Source-of-Truth Visualizer (Governed vs Ungoverned)
  └── MCP Action Dispatch Drawer (Expedite PO / Slack Alert)
         │
         ▼
[MCP EXTERNAL ACTIONS]
  ├── Jira/ERP: Create Expedited Reorder Ticket
  └── Slack: Auto-post Contract Breach Alert to Supplier Reps
```

---

## 6. Demonstration Script (The 3-Minute Hackathon Demo)

### Minute 1: The Crisis & The Enterprise Failure
1. Introduce the crisis: Semiconductor & battery supply delays threaten assembly at Plant 2 (Austin).
2. Show the classic problem: Ask a standard generic LLM chatbot *"What is our delivery performance this month?"* $\to$ It writes ambiguous SQL, mixes up promised dates vs actual arrival dates, and gives a hallucinated 94% score.

### Minute 2: The CoCo Governed Ontology in Action
1. Switch to the **Snowflake CoCo Supply Chain Command Center**.
2. **Procurement View:** User asks: *"Which suppliers have breached delivery agreements, and what is our penalty claim?"*
   - CoCo queries `SEMANTIC_SUPPLY_CHAIN_MODEL` for delay days.
   - CoCo triggers **Cortex Search** over the supplier's contract PDF to extract Section 8.2 (Liquidated Damages: \$1,500/day).
   - Generates exact penalty claim: \$18,000 with cited contract clause!
3. **Plant Operations View:** Switch to Plant Manager persona and ask: *"How many days of battery inventory remain before Plant 2 stops?"*
   - Instantly resolves: **3.8 days of inventory** using the exact same underlying governed metrics.

### Minute 3: The MCP Action (Closing the Loop)
1. The Plant Manager clicks **"Mitigate Stockout Risk"**.
2. CoCo invokes the registered **MCP Tool**:
   - Creates an emergency air-freight expedited PO in Jira/ERP.
   - Dispatches a formatted contractual SLA breach notice directly into the `#supplier-escalations` Slack channel with the contract clause citation.
3. Show evidence of CoCo full lifecycle: planning docs, synthetic data scripts, dynamic table pipelines, and validation tests.

---

## 7. Phased Implementation Roadmap

* [ ] **Phase 1: Planning (Current):** Lock in schema, ontology relationships, and metrics.
* [ ] **Phase 2: Synthetic Data Generation (CoCo):** Generate realistic, referentially sound tables & contract documents in `data/`.
* [ ] **Phase 3: Pipelines & Dynamic Tables:** Build ingestion and continuous aggregation pipelines in `pipelines/`.
* [ ] **Phase 4: Semantic Views & Cortex Services:** Author semantic YAML specifications and Cortex Search services in `semantics/`.
* [ ] **Phase 5: MCP Tooling & Actions:** Register Slack / ERP action tools in `mcp/`.
* [ ] **Phase 6: Streamlit Command Center:** Scaffold the multi-persona interactive dashboard in `app/`.
* [ ] **Phase 7: Testing & Guardrails:** Validate accuracy, persona consistency, and auditability in `tests/`.
