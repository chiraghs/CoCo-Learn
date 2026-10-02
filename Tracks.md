# Snowflake CoCo CLI Hackathon Tracks

---

## Hackathon Overview & Universal Evaluation

### Judging Focus Across All Tracks
1. **Real-World Relevance**: Clear business problem, applicability, realistic scenarios, and tangible ROI/impact.
2. **Technical Execution**: Architectural elegance, proper utilization of Snowflake primitives (Dynamic Tables, Streams, Tasks, Cortex, Semantic views), code quality, and robustness.
3. **Solution Completeness**: End-to-end functionality from raw data ingestion to interactive user interface and action workflows.

### Snowflake CoCo Usage Guidelines (Mandatory Lifecycle)
All hackathon solutions must use **CoCo (CLI / Desktop app)** across the full lifecycle:
- **Planning**: Explore schema, frame problem, draft solution design, outline ontology/data models before coding begins.
- **Development**: Generate pipelines, semantic models, agents, and application code iteratively through CoCo CLI or Desktop app rather than by hand.
- **Execution**: Run and orchestrate the complete end-to-end solution through CoCo, including scheduled or automated runs.
- **Testing & Validation**: Validate outputs, test accuracy, handle errors/edge cases, and confirm governed behavior with CoCo.

### Key CoCo Tasks to Demonstrate
- **Synthetic Data Generation**: Generate realistic, referentially consistent synthetic or de-identified datasets with CoCo.
- **Data Pipeline Creation**: Build and orchestrate ingestion/transformation pipelines (Dynamic Tables, Streams, Tasks) directly through CoCo.
- **Semantic Model & Ontology Authoring**: Infer and generate semantic views, verified queries, and ontology from schema; validate against NL queries.
- **Streamlit Report & App Generation**: Scaffold and run an interactive Streamlit UI through CoCo to present insights and trigger actions.
- **Connecting to Additional Sources via MCP**: Wire external systems (Jira, Slack, Google Drive, REST APIs) so agents can read and act across tools.
- **Document & Unstructured Processing**: Parse, extract, and enrich unstructured text/documents and combine them with structured data.

### Ways to Showcase Ingenuity in CoCo Tool Usage (Bonus Impact)
- **Reusable & Shareable Skills**: Publish custom reusable skills or agent skills.
- **MCP Connectors to External Tools**: Connect CoCo to external platforms turning analysis into cross-tool action.
- **Automations & Scheduled Runs**: Unattended operations and scheduled triggers.
- **Custom Tools & Function Calling**: Register custom tools for real-world automated actions.
- **Multi-Agent Orchestration**: Coordinate multiple specialized agents with clean handoffs and shared context.
- **Working Across Surfaces**: Demo across CoCo CLI, Desktop app, Snowsight Cloud Agents, and Slackbot.
- **Guardrails & Graceful Fallback**: Confidence checks, hallucination safeguards, and audit trails.

---

## Track 1: Risk, Fraud and Regulatory Intelligence Copilot

### Problem Statement
Banking and NBFC teams manage real-time fraud, liquidity and credit risk, and regulatory reporting (AML, Basel, and local regulations), largely manual today.
Build a copilot that surfaces risk and fraud signals and produces audit-ready regulatory outputs from natural language questions.

### Key Deliverables & Flow
- Combine transaction and account data with policy and filing text.
- Let business or compliance users ask questions and get governed, explainable, evidence-backed answers.
- Cover the end-to-end flow: **Signal $\to$ Evidence $\to$ Documented Finding or Regulatory Report**.

### Architecture & CoCo Execution Touchpoints
- **Data**: Ingest transactions, account histories, SAR (Suspicious Activity Report) templates, and regulatory PDF guidelines.
- **Semantic Views**: Accounts, Counterparties, High-risk Transactions, AML Rules, Sanction Lists.
- **Cortex AI**: Vector search over compliance manuals + SQL queries over transactional tables.
- **MCP Action**: Auto-file SAR tickets in Jira or alert compliance teams via Slack.

---

## Track 2: Customer 360 and Next Best Action Engine

### Problem Statement
Insurers and lenders want a unified customer view to drive personalization, smarter underwriting, and churn reduction.
Build an application that unifies structured and unstructured touchpoints (including call transcripts) into a 360 view and recommends the next best action.

### Key Deliverables & Flow
- Unify policyholder and customer data with unstructured interactions (calls, emails, tickets).
- Generate personalization, next best action, and sentiment insights.
- Move from a customer question to a recommended, automated action in one cohesive experience.

### Architecture & CoCo Execution Touchpoints
- **Data**: CRM profiles, policy/loan servicing data, and raw contact center transcripts/chat logs.
- **Semantic Views**: Customer Entity, Policy/Account, Interactions, Sentiment/Churn Risk scores.
- **Cortex AI**: Sentiment analysis, topic extraction, and prompt-driven next best action generation.
- **MCP Action**: Trigger email outreach, discount offer dispatch, or agent task creation in CRM/Slack.

---

## Track 3: Predictive Maintenance and OEE Command Center

### Problem Statement
Manufacturers lose value to unplanned downtime because OT sensor data sits apart from ERP and maintenance context.
Build a solution that converges IT and OT data to predict failures, automate work orders, and lift Overall Equipment Effectiveness (OEE).

### Key Deliverables & Flow
- Correlate real-time sensor streams (vibration, temperature, RPM, pressure) with ERP and maintenance records.
- Predict failures in advance and support root cause investigation in natural language.
- Deliver a command center experience for alert triage and automated action dispatch.

### Architecture & CoCo Execution Touchpoints
- **Data**: High-frequency synthetic OT telemetry + SAP/Maximo style ERP maintenance work orders.
- **Pipelines**: Near real-time anomaly aggregation via Snowflake Dynamic Tables & Streams.
- **Cortex AI / ML**: Anomaly detection models / threshold breach inference.
- **MCP Action**: Create maintenance tickets in Jira/ServiceNow, dispatch technician notifications via Slack.

---

## Track 4: Patient and Member 360 and Clinical or Regulatory Document Copilot

### Problem Statement
Care and life sciences teams work across siloed EHR and claims data and dense unstructured documents.
Build a copilot that unifies data into a patient or member 360 and answers clinical, safety, or regulatory questions with cited evidence. Use fully synthetic or de-identified data only.

### Key Deliverables & Flow
- Combine structured records with unstructured clinical, regulatory, or legal documents.
- Produce risk stratification, evidence retrieval, or cited answers (never opaque predictions).
- Deliver a question-and-answer experience with clear source evidence and strict guardrails.

### Architecture & CoCo Execution Touchpoints
- **Data**: Synthetic FHIR/EHR records, ICD-10/CPT billing codes, clinical PDF summaries, FDA guidelines.
- **Semantic Layer**: Patient, Claim, Encounter, Medication, Clinical Note, Protocol.
- **Cortex Search**: Cortex Search / Vector embeddings over clinical literature and patient discharge notes.
- **MCP Action**: Export audit-ready patient summaries, flag adverse event alerts to external clinical teams.

---

## Track 5: Supply Chain Ontology and Governed Conversational Analytics

### Problem Statement
Supply chain data is scattered across ERP, logistics, supplier, and IoT systems with inconsistent definitions, so the same question yields different answers across teams.
Build an industry ontology, a business entity and relationship model (Supplier $\to$ Part $\to$ Plant $\to$ Shipment $\to$ Order $\to$ Customer), expressed as governed semantic views, so that a natural language layer returns consistent, trustworthy answers grounded in shared definitions and metrics.

### Key Deliverables & Flow
- Define the supply chain ontology: core entities, relationships, hierarchies, and canonical metrics (On-Time Delivery, Fill Rate, Days of Inventory, Landed Cost).
- Encode the ontology as semantic views so business meaning, not raw column names, drives answers.
- Layer governed conversational analytics on top so any team asks cross-domain questions and gets one consistent answer.
- Demonstrate that the same metric resolves identically across personas (planning, procurement, logistics).

### Architecture & CoCo Execution Touchpoints
- **Data**: Multi-table synthetic supply chain data (Suppliers, POs, Shipments, Inventory, Orders).
- **Ontology & Semantic Views**: Rich semantic views with explicit relationships, dimensions, and governed metric definitions.
- **Conversational Analytics**: Snowflake Cortex Analyst / natural language semantic model queries.
- **MCP Action**: Update PO reorder points, send logistics supplier escalation via Slack/Jira.
