---
name: supply-chain-governance
description: Governed supply chain ontology skill for evaluating multi-persona metrics, supplier contract SLA breach liabilities, and assembly stockout risks.
---

# Supply Chain Governance Skill

## Capabilities
1. **Governed Canonical Metrics:** Resolves canonical supply chain metrics (OTIF %, Days of Inventory, Landed Cost) using `SUPPLY_CHAIN_DB.CORE.supply_chain_semantic_model.yaml`.
2. **Ontological Hierarchy & Inheritance:** Traverses concept taxonomies (`SupplyChainNode` -> `Facility` -> `Warehouse` -> `BondedWarehouse`/`ColdStorage`/`Plant`) via `SUPPLY_CHAIN_DB.ONT.CLASS_CLOSURE` and `GET_SUBCLASSES(root_class)`.
3. **Compound Supply Risk Profile:** Analyzes real-time plant stockout risks and daily burn rates via `GET_FACILITY_RISK(plant_id)` and `DT_PLANT_STOCKOUT_RISK`.
4. **Logistics & Inbound Bottlenecks:** Queries delayed in-transit shipments and demurrage risks via `GET_INBOUND_RISK(plant_id)`.
5. **Contractual SLA Intelligence:** Evaluates supplier contract penalties and grace periods using Cortex Search Service `SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS_SEARCH`.
6. **Closed-Loop Action Execution:** Invokes external action tools via MCP (`expedite_purchase_order`, `send_supplier_sla_breach_alert`).

## Core Domain Reasoning Rules
* **Taxonomy Inheritance:** `BondedWarehouse` IS-A `Warehouse` IS-A `SupplyChainNode`. Subtypes automatically inherit operational relationships.
* **Compound Risk Signal:** Low inventory buffer ($< 5\text{ days}$) combined with delayed inbound shipments is the highest severity disruption signal.
* **Network Impact:** A bottleneck on a `Route` affects every downstream assembly facility and warehouse it serves.

## Prompt Patterns & Agent Workflow
* *"What are all facility subtypes under SupplyChainNode?"* -> Calls `SUPPLY_CHAIN_DB.ONT.GET_SUBCLASSES('SupplyChainNode')`.
* *"Check Days of Inventory for [Plant] on [Part Number]"* -> Calls `SUPPLY_CHAIN_DB.ONT.GET_FACILITY_RISK([plant_id])`.
* *"Evaluate delay penalties and breach exposure for [Supplier]"* -> Performs Cortex Search on `SUPPLIER_CONTRACTS_SEARCH` and computes liquidated damages from `DT_SUPPLIER_PERFORMANCE`.

