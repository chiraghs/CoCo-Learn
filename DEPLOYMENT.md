# SupplyChainIQ — Deployment & Live Prototype Links

**Team:** Aegis  
**Project:** SupplyChainIQ  
**Track:** Track 5 — Supply Chain Ontology & Governed Analytics  
**Snowflake Account:** `ZJXLXUZ.JV50315`  

---

## 🌐 Live Prototype Links for Submission

1. **Live Streamlit in Snowflake (SiS) Command Center (Native Enterprise Deployment):**
   - **URL:** [https://app.snowflake.com/ZJXLXUZ/JV50315/#/streamlit-apps/SUPPLY_CHAIN_DB.CORE.SUPPLY_CHAIN_COMMAND_CENTER](https://app.snowflake.com/ZJXLXUZ/JV50315/#/streamlit-apps/SUPPLY_CHAIN_DB.CORE.SUPPLY_CHAIN_COMMAND_CENTER)
   - **Warehouse:** `COMPUTE_WH`
   - **Database & Schema:** `SUPPLY_CHAIN_DB.CORE`

2. **Public Static Web Showcase & Interactive Simulator:**
   - **GitHub Pages URL (Instant Free Hosting):** [https://chiraghs.github.io/CoCo-Learn/](https://chiraghs.github.io/CoCo-Learn/)
   - **Render Deployed URL:** `https://supplychainiq.onrender.com` (Follow instructions below)

---

## 🚀 How to Deploy on Render (Free & Fast)

The repository includes a ready-to-use [`render.yaml`](file:///Volumes/DiskD/HACKATHONS/Snowflake%20CoCo%20CLI/render.yaml) blueprint.

### Option A: 1-Click Render Blueprint
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** &rarr; **Blueprint**.
3. Connect your GitHub repository: `https://github.com/chiraghs/CoCo-Learn`.
4. Render will automatically detect [`render.yaml`](file:///Volumes/DiskD/HACKATHONS/Snowflake%20CoCo%20CLI/render.yaml) and configure the static web service.
5. Click **Apply**. Your site will be live at `https://supplychainiq.onrender.com` in ~30 seconds with automatic HTTPS!

### Option B: Manual Static Site on Render
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** &rarr; **Static Site**.
3. Connect `https://github.com/chiraghs/CoCo-Learn`.
4. Configure the settings:
   - **Name:** `supplychainiq`
   - **Branch:** `main`
   - **Build Command:** `echo "Ready"` (or leave empty)
   - **Publish Directory:** `./`
5. Click **Create Static Site**.

---

## 🐙 How to Enable GitHub Pages (Instant 0-Configuration)

1. Go to the GitHub repository settings: [https://github.com/chiraghs/CoCo-Learn/settings/pages](https://github.com/chiraghs/CoCo-Learn/settings/pages)
2. Under **Build and deployment** &rarr; **Source**: Select **Deploy from a branch**.
3. Under **Branch**: Select `main` and folder `/ (root)`.
4. Click **Save**.
5. Your public interactive prototype is instantly available at:
   👉 **`https://chiraghs.github.io/CoCo-Learn/`**

---

## 📦 What the Public Web App Includes

- **Interactive Command Center Simulator:** Switch between plants (Austin Giga 1, Fremont, Berlin, Shanghai) with real-time KPI updates.
- **Conversational Cortex AI Dual-Brain Demo:** Test natural language queries with the **3-Way Reconciliation Ledger** (Conversational narrative + deterministic SQL + ground-truth table proof).
- **Cortex Search Legal Mining:** Interactive Section 8 liquidated damages penalty extraction for Apex Battery Cells ($140,000 recovery).
- **Closed-Loop Action MCP Simulator:** Interactive button to execute emergency PO rerouting to Shenzhen EnerTech and animate Austin DOI from **3.8 days &rarr; 14.2 days**.
- **Downloadable Pitch Decks:** Direct links to download both 11-slide and 6-slide PPTX and PDF decks (< 5MB).
