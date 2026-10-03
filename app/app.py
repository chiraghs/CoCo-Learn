import streamlit as st
import pandas as pd
from datetime import datetime, timezone
import json

# Set Page Config
st.set_page_config(
    page_title="Snowflake CoCo - Supply Chain Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .alert-banner {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 12px 18px;
        border-radius: 6px;
        margin-bottom: 20px;
        color: #991B1B;
        font-weight: 500;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .critical-badge {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .governed-box {
        background-color: #F0FDF4;
        border: 1px solid #86EFAC;
        border-radius: 8px;
        padding: 16px;
    }
    .ungoverned-box {
        background-color: #FFFBEB;
        border: 1px solid #FCD34D;
        border-radius: 8px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to get Snowflake session or mock fallback
@st.cache_resource
def get_session():
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:
        return None

session = get_session()

# Load Data function
def load_data(table_name):
    if session:
        try:
            return session.table(f"SUPPLY_CHAIN_DB.CORE.{table_name}").to_pandas()
        except Exception:
            pass
            
    # Realistic Seed Data fallback for standalone/local mode
    if table_name == "DT_SUPPLIER_PERFORMANCE":
        return pd.DataFrame([
            {"SUPPLIER_ID": "SUP_001", "SUPPLIER_NAME": "Apex Battery Cells Ltd", "SUPPLIER_COUNTRY": "South Korea", "SUPPLIER_TIER": "Tier 1", "TOTAL_ORDERS": 6, "TOTAL_SHIPMENTS": 6, "ON_TIME_SHIPMENTS": 2, "DELAYED_SHIPMENTS": 4, "OTIF_RATE_PCT": 33.3, "TOTAL_DELAY_DAYS": 21, "TOTAL_PENALTY_LIABILITY_USD": 18000.0, "TOTAL_DEMURRAGE_USD": 20000.0},
            {"SUPPLIER_ID": "SUP_002", "SUPPLIER_NAME": "MicroSilicon Dynamics", "SUPPLIER_COUNTRY": "Taiwan", "SUPPLIER_TIER": "Tier 1", "TOTAL_ORDERS": 3, "TOTAL_SHIPMENTS": 3, "ON_TIME_SHIPMENTS": 3, "DELAYED_SHIPMENTS": 0, "OTIF_RATE_PCT": 100.0, "TOTAL_DELAY_DAYS": 0, "TOTAL_PENALTY_LIABILITY_USD": 0.0, "TOTAL_DEMURRAGE_USD": 0.0},
            {"SUPPLIER_ID": "SUP_003", "SUPPLIER_NAME": "Nordic Precision Metals", "SUPPLIER_COUNTRY": "Sweden", "SUPPLIER_TIER": "Tier 2", "TOTAL_ORDERS": 2, "TOTAL_SHIPMENTS": 2, "ON_TIME_SHIPMENTS": 2, "DELAYED_SHIPMENTS": 0, "OTIF_RATE_PCT": 100.0, "TOTAL_DELAY_DAYS": 0, "TOTAL_PENALTY_LIABILITY_USD": 0.0, "TOTAL_DEMURRAGE_USD": 0.0},
            {"SUPPLIER_ID": "SUP_004", "SUPPLIER_NAME": "VoltStorage Chem Inc", "SUPPLIER_COUNTRY": "Japan", "SUPPLIER_TIER": "Tier 1", "TOTAL_ORDERS": 2, "TOTAL_SHIPMENTS": 2, "ON_TIME_SHIPMENTS": 2, "DELAYED_SHIPMENTS": 0, "OTIF_RATE_PCT": 100.0, "TOTAL_DELAY_DAYS": 0, "TOTAL_PENALTY_LIABILITY_USD": 0.0, "TOTAL_DEMURRAGE_USD": 0.0},
            {"SUPPLIER_ID": "SUP_005", "SUPPLIER_NAME": "Pacific Wiring & Harness", "SUPPLIER_COUNTRY": "Vietnam", "SUPPLIER_TIER": "Tier 2", "TOTAL_ORDERS": 2, "TOTAL_SHIPMENTS": 2, "ON_TIME_SHIPMENTS": 2, "DELAYED_SHIPMENTS": 0, "OTIF_RATE_PCT": 100.0, "TOTAL_DELAY_DAYS": 0, "TOTAL_PENALTY_LIABILITY_USD": 0.0, "TOTAL_DEMURRAGE_USD": 0.0},
        ])
    elif table_name == "DT_PLANT_STOCKOUT_RISK":
        return pd.DataFrame([
            {"PLANT_ID": "PLANT_02", "PLANT_NAME": "Gigafactory Texas", "PLANT_LOCATION": "Austin", "PART_ID": "PART_BAT_402", "PART_NUMBER": "BAT-MOD-402", "PART_NAME": "High-Density Lithium Battery Module", "PART_CRITICALITY": "CRITICAL", "ON_HAND_QTY": 2280, "SAFETY_STOCK_QTY": 5000, "IN_TRANSIT_QTY": 13500, "PLANT_DAILY_BURN_RATE": 600, "DAYS_OF_INVENTORY": 3.8, "STOCKOUT_RISK_LEVEL": "CRITICAL_STOCKOUT_RISK", "SAFETY_STOCK_DEFICIT_UNITS": 2720},
            {"PLANT_ID": "PLANT_01", "PLANT_NAME": "Gigafactory California", "PLANT_LOCATION": "Fremont", "PART_ID": "PART_BAT_402", "PART_NUMBER": "BAT-MOD-402", "PART_NAME": "High-Density Lithium Battery Module", "PART_CRITICALITY": "CRITICAL", "ON_HAND_QTY": 6800, "SAFETY_STOCK_QTY": 4500, "IN_TRANSIT_QTY": 4000, "PLANT_DAILY_BURN_RATE": 450, "DAYS_OF_INVENTORY": 15.1, "STOCKOUT_RISK_LEVEL": "HEALTHY_BUFFER", "SAFETY_STOCK_DEFICIT_UNITS": 0},
            {"PLANT_ID": "PLANT_03", "PLANT_NAME": "Gigafactory Europe", "PLANT_LOCATION": "Berlin", "PART_ID": "PART_BAT_402", "PART_NUMBER": "BAT-MOD-402", "PART_NAME": "High-Density Lithium Battery Module", "PART_CRITICALITY": "CRITICAL", "ON_HAND_QTY": 5200, "SAFETY_STOCK_QTY": 3500, "IN_TRANSIT_QTY": 5500, "PLANT_DAILY_BURN_RATE": 400, "DAYS_OF_INVENTORY": 13.0, "STOCKOUT_RISK_LEVEL": "HEALTHY_BUFFER", "SAFETY_STOCK_DEFICIT_UNITS": 0},
            {"PLANT_ID": "PLANT_02", "PLANT_NAME": "Gigafactory Texas", "PLANT_LOCATION": "Austin", "PART_ID": "PART_MCU_901", "PART_NUMBER": "MCU-901-AUTO", "PART_NAME": "Automotive Multi-Core Microcontroller", "PART_CRITICALITY": "CRITICAL", "ON_HAND_QTY": 18500, "SAFETY_STOCK_QTY": 10000, "IN_TRANSIT_QTY": 15000, "PLANT_DAILY_BURN_RATE": 600, "DAYS_OF_INVENTORY": 30.8, "STOCKOUT_RISK_LEVEL": "HEALTHY_BUFFER", "SAFETY_STOCK_DEFICIT_UNITS": 0},
        ])
    elif table_name == "DT_ACTIVE_DISRUPTIONS":
        return pd.DataFrame([
            {"SHIPMENT_ID": "SHP_9002", "PO_ID": "PO_2026_002", "CARRIER": "Pacific Freight Lines", "TRANSPORT_MODE": "Ocean", "ORIGIN_PORT": "Busan, KR", "DEST_PORT": "Houston, US", "SHIPMENT_STATUS": "HELD_AT_PORT", "QTY_SHIPPED": 6000, "DEMURRAGE_USD": 7500.0, "PART_NAME": "High-Density Lithium Battery Module", "SUPPLIER_NAME": "Apex Battery Cells Ltd", "DESTINATION_PLANT": "Gigafactory Texas", "DAYS_PAST_PROMISED": 8},
            {"SHIPMENT_ID": "SHP_9011", "PO_ID": "PO_2026_011", "CARRIER": "Pacific Freight Lines", "TRANSPORT_MODE": "Ocean", "ORIGIN_PORT": "Busan, KR", "DEST_PORT": "Houston, US", "SHIPMENT_STATUS": "PORT_BOTTLENECK", "QTY_SHIPPED": 7500, "DEMURRAGE_USD": 12000.0, "PART_NAME": "High-Density Lithium Battery Module", "SUPPLIER_NAME": "Apex Battery Cells Ltd", "DESTINATION_PLANT": "Gigafactory Texas", "DAYS_PAST_PROMISED": 2},
            {"SHIPMENT_ID": "SHP_9001", "PO_ID": "PO_2026_001", "CARRIER": "OceanBridge Logistics", "TRANSPORT_MODE": "Ocean", "ORIGIN_PORT": "Busan, KR", "DEST_PORT": "Houston, US", "SHIPMENT_STATUS": "ARRIVED_LATE", "QTY_SHIPPED": 5000, "DEMURRAGE_USD": 4800.0, "PART_NAME": "High-Density Lithium Battery Module", "SUPPLIER_NAME": "Apex Battery Cells Ltd", "DESTINATION_PLANT": "Gigafactory Texas", "DAYS_PAST_PROMISED": 9},
        ])
    return pd.DataFrame()

# Sidebar Setup
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/ff/Snowflake_Logo.svg", width=160)
    st.markdown("### **Operational Persona**")
    persona = st.radio(
        "Select your active persona:",
        ["💼 VP of Procurement", "🏭 Plant Operations Manager", "🚢 Logistics & Freight Director"],
        index=1
    )
    st.markdown("---")
    st.markdown("### **System Status**")
    st.success("● Snowflake Connected: `SUPPLY_CHAIN_DB.CORE`")
    st.info("● Dynamic Tables: **Live (1m lag)**")
    st.info("● Cortex Search: **Active**")
    st.markdown("---")
    st.caption("Powered by **Snowflake CoCo CLI** full-lifecycle agentic framework.")

# Main Header
st.markdown('<div class="main-header">⚡ Snowflake CoCo Supply Chain Command Center</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Industry Ontology & Governed Conversational Intelligence Engine</div>', unsafe_allow_html=True)

# Incident Alert Banner
st.markdown("""
<div class="alert-banner">
    ⚠️ <strong>ACTIVE CRISIS DETECTED:</strong> Port of Houston congestion holding battery cell shipments (PART_BAT_402) from Apex Battery Cells. 
    <strong>Gigafactory Texas (Austin) has only 3.8 Days of Inventory remaining before assembly line shutdown.</strong>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Persona Intelligence Dashboard", 
    "⚖️ Governed vs Ungoverned Truth", 
    "📑 Cortex Contract Clause Investigator", 
    "🚀 MCP Action Center"
])

# TAB 1: PERSONA DASHBOARD
with tab1:
    df_perf = load_data("DT_SUPPLIER_PERFORMANCE")
    df_stock = load_data("DT_PLANT_STOCKOUT_RISK")
    df_disrupt = load_data("DT_ACTIVE_DISRUPTIONS")

    if "Procurement" in persona:
        st.subheader("💼 Procurement Intelligence — Vendor Reliability & SLA Penalties")
        col1, col2, col3, col4 = st.columns(4)
        total_penalties = df_perf["TOTAL_PENALTY_LIABILITY_USD"].sum()
        delayed_orders = df_perf["DELAYED_SHIPMENTS"].sum()
        worst_vendor = df_perf.sort_values(by="TOTAL_PENALTY_LIABILITY_USD", ascending=False).iloc[0]["SUPPLIER_NAME"]
        
        col1.metric("Active Suppliers", len(df_perf))
        col2.metric("Delayed Shipments", int(delayed_orders), delta="-4 breached", delta_color="inverse")
        col3.metric("Liquidated Damages Claim", f"${total_penalties:,.2f}", delta="+$18,000 claim", delta_color="inverse")
        col4.metric("Highest Risk Vendor", worst_vendor)
        
        st.markdown("#### **Supplier Performance & Liquidated Damages (Dynamic Table)**")
        st.dataframe(df_perf, use_container_width=True)

    elif "Plant Operations" in persona:
        st.subheader("🏭 Plant Operations Intelligence — Assembly Line Stockout Risk")
        austin_row = df_stock[(df_stock["PLANT_ID"] == "PLANT_02") & (df_stock["PART_ID"] == "PART_BAT_402")].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Austin Battery Stock", f"{austin_row['ON_HAND_QTY']:,} units")
        col2.metric("Daily Burn Rate", f"{austin_row['PLANT_DAILY_BURN_RATE']} units/day")
        col3.metric("Days of Inventory (DOI)", f"{austin_row['DAYS_OF_INVENTORY']} Days", delta="-6.2 vs buffer", delta_color="inverse")
        col4.metric("Risk Status", "CRITICAL RISK", delta="Assembly stoppage", delta_color="inverse")
        
        st.markdown("#### **Plant Inventory & Runways (Dynamic Table)**")
        st.dataframe(df_stock, use_container_width=True)

    else:
        st.subheader("🚢 Logistics Intelligence — Port Disruption & Demurrage Exposure")
        total_demurrage = df_disrupt["DEMURRAGE_USD"].sum()
        st.metric("Total Demurrage Incurred", f"${total_demurrage:,.2f}", delta="Port of Houston fees", delta_color="inverse")
        
        st.markdown("#### **Active Ocean & Port Disruptions (Dynamic Table)**")
        st.dataframe(df_disrupt, use_container_width=True)

# TAB 2: SINGLE SOURCE OF TRUTH COMPARISON
with tab2:
    st.subheader("⚖️ The Core Hackathon Problem: Single Source of Truth")
    st.write("Demonstrating how different personas get conflicting answers with naive LLMs, but mathematically identical answers with Snowflake CoCo's Governed Ontology.")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("""
        <div class="ungoverned-box">
            <h4 style="color: #B45309;">❌ Ungoverned Generic LLM (Conflicting / Hallucinated)</h4>
            <p><strong>Query:</strong> <em>"What is our supplier delivery performance?"</em></p>
            <ul>
                <li><strong>Procurement Chatbot:</strong> "Delivery rate is <strong>94%</strong> (calculated purely on initial purchase order promise dates without checking arrival)."</li>
                <li><strong>Logistics Chatbot:</strong> "Delivery rate is <strong>66%</strong> (calculated based on carrier bill of lading dock scans)."</li>
                <li><strong>Plant Chatbot:</strong> "Inventory is sufficient for <strong>8 days</strong> (failed to account for Austin's 600/day line ramp)."</li>
            </ul>
            <p style="color: #DC2626;"><strong>Result:</strong> Disconnected data definitions, erroneous decisions, and plant shutdown.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="governed-box">
            <h4 style="color: #15803D;">✅ Governed CoCo Semantic Ontology (Single Source of Truth)</h4>
            <p><strong>Query:</strong> <em>"What is our delivery performance and stockout runway?"</em></p>
            <ul>
                <li><strong>Procurement Persona:</strong> OTIF resolves to strictly <strong>33.3% for Apex Cells</strong>, with <strong>$18,000</strong> liquidated damages.</li>
                <li><strong>Logistics Persona:</strong> Identical <strong>33.3% OTIF</strong> with exact citation of 2 shipments held at Port of Houston.</li>
                <li><strong>Plant Persona:</strong> Resolves canonical formula <code>ON_HAND / BURN_RATE</code> = <strong>3.8 Days of Inventory</strong>.</li>
            </ul>
            <p style="color: #16A34A;"><strong>Result:</strong> 100% mathematical consistency across all executive personas.</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: CORTEX SEARCH CONTRACT INVESTIGATION
with tab3:
    st.subheader("📑 Unstructured Contract Intelligence with Snowflake Cortex")
    st.write("Querying supplier Master Service Agreements (MSAs) using Cortex Search to extract penalty clauses and grace periods.")
    
    sample_q = st.selectbox(
        "Select a contract investigation question:",
        [
            "What are the liquidated damages penalties and grace period for Apex Battery Cells?",
            "What are the air freight commitments and delay clauses for MicroSilicon Dynamics?",
            "Does port terminal congestion qualify as Force Majeure under the Apex contract?"
        ]
    )
    
    if st.button("🔍 Run Cortex Contract Search"):
        with st.spinner("Executing Cortex Search over RAW_SUPPLIER_CONTRACTS..."):
            if "Apex" in sample_q or "Force Majeure" in sample_q:
                st.success("Found matching clause in **`RAW_SUPPLIER_CONTRACTS` (CTR_APEX_2025)**:")
                st.markdown("""
                > **SECTION 8: SERVICE LEVEL AGREEMENTS & DELAY PENALTIES**
                > * **8.1 Grace Period:** Buyer agrees to a 3-calendar-day grace period for port congestion beyond promised delivery date.
                > * **8.2 Liquidated Damages:** If shipment delivery exceeds the promised delivery date plus grace period, Supplier shall incur liquidated damages of **USD $1,500.00 per calendar day per delayed shipment** until actual receipt.
                > * **8.3 Force Majeure:** Routine port terminal berth congestion **does not qualify as Force Majeure**.
                """)
                st.info("💡 **Governed Intelligence Insight:** Apex Battery Cells' current delay of 8 days minus 3-day grace = 5 penalized days × $1,500/day = **$7,500 penalty for Shipment SHP_9002**.")
            else:
                st.success("Found matching clause in **`RAW_SUPPLIER_CONTRACTS` (CTR_MICRO_2025)**:")
                st.markdown("""
                > **SECTION 7: PENALTY CLAUSES**
                > * **7.1:** Liquidated damages for unapproved delivery delays are assessed at **USD $2,000.00 per day** after a 48-hour grace window.
                """)

# TAB 4: MCP ACTIONS
with tab4:
    st.subheader("🚀 Model Context Protocol (MCP) — Closing the Action Loop")
    st.write("Rather than merely returning text, CoCo invokes registered MCP tools to take real-world action.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### Action 1: Emergency PO Re-route")
        st.write("Dispatches an emergency air-cargo shipment of 2,000 battery units directly to Gigafactory Texas.")
        if st.button("✈️ Trigger Emergency Air-Freight PO via MCP"):
            now_iso = datetime.now(timezone.utc).isoformat()
            payload = {
                "action": "EXPEDITE_PURCHASE_ORDER",
                "status": "EXECUTED",
                "timestamp": now_iso,
                "details": {
                    "original_po_id": "PO_2026_002",
                    "emergency_po_id": "EXP_2026_002",
                    "part_id": "PART_BAT_402",
                    "transport_mode": "Air Freight",
                    "expedited_carrier": "Global Aero Air Cargo",
                    "expedited_cost_usd": 12500.0,
                    "estimated_delivery_hours": 36,
                    "impact": "Averts Plant 2 (Austin) assembly line shutdown. Arrival within 36 hours."
                }
            }
            st.success("✅ Emergency Air-Freight Order Executed!")
            st.json(payload)

    with col_b:
        st.markdown("### Action 2: Contractual SLA Breach Notice")
        st.write("Dispatches a legally grounded breach notice citing contract terms to the Slack supplier incident channel.")
        if st.button("📢 Dispatch Formal Breach Notice to Slack"):
            now_iso = datetime.now(timezone.utc).isoformat()
            st.success("✅ SLA Breach Notice dispatched to `#supply-chain-crisis` on Slack!")
            st.markdown("""
            **Slack Preview:**
            > 🚨 **FORMAL CONTRACTUAL SLA BREACH NOTICE: Apex Battery Cells Ltd**  
            > **Supplier ID:** SUP_001 | **Purchase Order:** PO_2026_002  
            > **Delay Duration:** 5 days beyond contract grace period  
            > **Liquidated Damages Claim:** $7,500.00 USD  
            > **Contract Citation:** *Section 8.2 — Liquidated damages of USD $1,500.00/day after 3-day grace.*  
            > *Dispatched by Snowflake CoCo Supply Chain Agent*
            """)
