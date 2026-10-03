---
name: supply-chain-governance
description: Governed supply chain ontology skill for evaluating multi-persona metrics, supplier contract SLA breach liabilities, and assembly stockout risks.
---

# Supply Chain Governance Skill

## Capabilities
1. Resolves canonical supply chain metrics (OTIF %, Days of Inventory, Landed Cost) using `SUPPLY_CHAIN_DB.CORE.supply_chain_semantic_model.yaml`.
2. Inspects real-time plant stockout risks via `SUPPLY_CHAIN_DB.CORE.DT_PLANT_STOCKOUT_RISK`.
3. Evaluates supplier contract penalties and grace periods using Cortex Search Service `SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS_SEARCH`.
4. Invokes external action tools via MCP (`expedite_purchase_order`, `send_supplier_sla_breach_alert`).

## Prompt Patterns
* "Check Days of Inventory for [Plant] on [Part Number]" -> Queries `DT_PLANT_STOCKOUT_RISK`.
* "Evaluate delay penalties for [Supplier]" -> Performs Cortex Search on `SUPPLIER_CONTRACTS_SEARCH` and computes liquidated damages from `DT_SUPPLIER_PERFORMANCE`.
