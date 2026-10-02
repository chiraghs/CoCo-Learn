# Snowflake CoCo (Cortex Code) Capabilities & Skills Reference Guide

This comprehensive reference catalogs the full spectrum of built-in skills, agent capabilities, and operational domains natively supported by **Snowflake CoCo (Cortex Code CLI & Desktop)**.

---

## 1. Snowflake Data & SQL

* **SQL Authoring, Execution & Debugging:** Native generation, syntax validation, dialect optimization, and execution of Snowflake SQL with automated error remediation.
* **Object Discovery:** Deep introspection across Snowflake schemas to discover and describe tables, views, semantic views, Cortex agents, Streamlit apps, stored procedures, UDFs, stages, streams, tasks, and pipes.
* **Cortex Analyst:** High-accuracy natural language-to-SQL translation grounded strictly within semantic models and YAML metadata.
* **Semantic Views & Models:** Author, infer, validate, describe, and deploy governed semantic views and canonical metrics.
* **Cortex Agents:** Discover, configure, describe, and interactively query autonomous agent definitions directly within Snowflake.
* **Lineage & Impact Analysis:** Automated dependency tracing across upstream tables and downstream views, dynamic tables, and reports to assess schema changes.
* **Data Diff:** Row-by-row and schema-level comparisons between two Snowflake tables or partitions to verify data parity during migrations.

---

## 2. AI & Machine Learning

* **Cortex AI Functions:** Direct invocation and pipeline integration of LLM primitives:
  * `AI_COMPLETE` / `AI_CHAT`: General reasoning and multi-turn completion.
  * `AI_SENTIMENT`: Tone and customer sentiment classification.
  * `AI_CLASSIFY`: Multi-class categorization and taxonomy mapping.
  * `AI_EXTRACT`: Structured entity extraction from free-form text.
  * `AI_PARSE_DOCUMENT`: Multimodal OCR, layout parsing, and tabular extraction from PDFs and scans.
  * `AI_TRANSLATE`: Cross-lingual document translation.
  * `AI_EMBED`: High-dimensional vector embedding generation for semantic search.
* **Document Intelligence:** Ingest, parse, OCR, and classify unstructured PDFs, images, medical records, and legal contracts.
* **AI Pipeline Builder:** Construct continuous self-updating feature and inference pipelines combining Streams, Tasks, and Dynamic Tables.
* **Machine Learning & MLOps:** Model training in Snowpark Python, Model Registry tracking, Feature Store authoring, time-series forecasting, and anomaly detection.
* **AI Readiness Scoring:** Automated audit of your Snowflake account's data quality, metadata completeness, and semantic readiness for generative AI.

---

## 3. Data Engineering

* **Dynamic Tables:** Declarative pipeline creation, lag target optimization, refresh monitoring, and dependency troubleshooting.
* **Snowflake Tasks:** Task scheduling, CRON configurations, complex DAG orchestration, and run history monitoring.
* **Snowpipe Streaming:** Sub-second real-time streaming ingestion setup, error handling, and pipeline troubleshooting.
* **Openflow:** Integration and operational management of Apache NiFi-based data ingestion and routing.
* **dbt Ecosystem:** Analysis of dbt projects (via `fdbt`), deployed dbt runs, manifest parsing, and Cosmos orchestration.
* **Spark Migration:** Automated translation of legacy PySpark and Databricks code into native Snowpark Python and optimized Snowflake SQL.

---

## 4. Application Development

* **Streamlit in Snowflake (SiS):** Rapid scaffolding, prototyping, styling, state management, and deployment of interactive Streamlit apps.
* **Snowflake Apps (SAR):** Build and deploy modern full-stack web applications (e.g., Next.js, React) running on Snowpark Container Services (SPCS).
* **Native Apps:** Complete lifecycle management for Native Apps Framework, encompassing both Provider (package, manifest, version) and Consumer installation workflows.
* **Snowpark Python:** Scalable data pipelines, custom User-Defined Functions (UDFs), User-Defined Table Functions (UDTFs), and Stored Procedures.
* **SPCS Deployment:** Docker containerization, image registry pushing, compute pool provisioning, and service specification authoring.
* **Notebooks:** Create, edit, and orchestrate native Snowflake Jupyter Notebooks with integrated GPU/CPU compute.

---

## 5. Governance, Security & Quality

* **Data Governance & RBAC:** Automated PII classification, dynamic data masking, row-access policies, object tagging, and role-based access control.
* **Data Quality (DMFs):** Author and schedule Data Metric Functions (DMFs) for automated expectations, schema drift alerts, and quality dashboards.
* **Security & Threat Investigation:** Automated detection of anomalous logins, suspicious credential spikes, and data exfiltration patterns.
* **Trust Center:** Security scanner management, CIS benchmark alignment, posture reporting, and recommended remediations.
* **Authentication & Network Security:** Network rules, network policies, SCIM, and SAML SSO integration.
* **Intent-Driven Governance:** Natural language translation of business security policies into enforced Snowflake governance policies.

---

## 6. Cost & Cloud Operations

* **Cost Intelligence & FinOps:** Granular warehouse credit consumption analysis, automated budget quotas, and spend anomaly alerts.
* **Billing & Financials:** Organization-level dollar spend tracking, contract burn-down tracking, and invoice itemization.
* **Warehouse Management:** Virtual warehouse sizing, multi-cluster auto-scaling, adaptive/Gen2 warehouse tuning, and auto-suspend optimization.
* **Workload Performance Analysis:** Identification of query spilling (local/remote storage), partition pruning efficiency, warehouse cache hit rates, and clustering health.

---

## 7. Sharing & Data Clean Rooms

* **Data Sharing:** Direct cross-account shares, declarative sharing models, and public/private Snowflake Marketplace listings.
* **Data Clean Rooms (DCR):** Full lifecycle deployment of secure, privacy-preserving multi-party analytics clean rooms.
* **Internal Marketplace:** Cataloging and distributing internal organization data products with governed discovery.
* **Marketplace Search:** Natural language search to identify third-party datasets, external connectors, and SaaS apps.
* **Listing Observability:** Telemetry on share replication status, consumer query volume, and associated compute cost.

---

## 8. DevOps & Workflow Tooling

* **CI/CD Integrations:** Automated delivery pipelines for GitHub Actions, GitLab CI, and Azure DevOps using keyless OIDC authentication.
* **Database Change Management (DCM):** Version-controlled schema migrations and declarative object state synchronization.
* **Automation & Scheduled Runs:** Schedule unattended, recurring CoCo runs directly as native Snowflake `AGENT TASK`s.
* **Git & Workspace Management:** Snowflake Git repository integration, worktrees, workspace environments, and secrets management.
* **Cross-Platform SQL Migration:** Automated code transpilation from Oracle, SQL Server, BigQuery, Redshift, Teradata, and PostgreSQL into Snowflake SQL.
* **Team Workflow:** Multi-agent parallel orchestration with clean agent handoffs and shared execution context.

---

## 9. General Coding & Execution

* **File Operations:** Native workspace file read, write, intelligent contiguous patch editing, glob matching, ripgrep search, and semantic code search.
* **Shell Execution:** Direct sandboxed execution of shell commands, scripts, and build tools.
* **Web Fetch:** Retrieve, parse, and summarize web documentation and REST API payloads.
* **Notebook Execution:** Programmatic execution of Jupyter notebooks with parameter injection and output verification.
* **HTML & Executive Reporting:** Author rich HTML widgets, charts, and interactive reports publishable directly to Snowflake Intelligence.

---

## 10. Additional & Advanced Infrastructure

* **Apache Iceberg:** Manage Apache Iceberg external tables, catalog integrations (Polaris / AWS Glue), and parquet file layouts.
* **Snowflake Postgres & Interactive Warehouses:** Hybrid transactional and analytical (HTAP) table management and low-latency interactive warehouses.
* **Lifecycle & Notification Services:** Storage lifecycle policies, Snowflake Alerts, and cloud notification integrations (SNS, EventBridge, Webhooks).
* **Observability Tables:** Structured logging and distributed tracing with Event Tables and Error Tables.
* **Organization & Key Management:** Multi-account org administration, Tri-Secret Secure (TSS), and Customer-Managed Keys (CMK).
* **Custom Skill Authoring:** Develop, test, package, and distribute reusable domain-specific CoCo skills and tool definitions.
