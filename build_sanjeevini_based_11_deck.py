import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    base_template = "/Volumes/DiskD/HACKATHONS/smart-health/Pitch-DECK/Sanjeevini-Pitch-Deck.pptx"
    out_path = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/deck/SupplyChainIQ-Pitch-Deck.pptx"
    
    prs = Presentation(base_template)
    
    COLOR_BG = RGBColor(255, 255, 255)
    COLOR_DARK_TEXT = RGBColor(15, 23, 42)
    COLOR_MUTED_TEXT = RGBColor(100, 116, 139)
    COLOR_BODY_TEXT = RGBColor(30, 41, 59)
    COLOR_EMERALD = RGBColor(5, 150, 105)
    COLOR_BLUE = RGBColor(30, 64, 175)
    COLOR_SNOWFLAKE_CYAN = RGBColor(2, 132, 199)
    COLOR_RED = RGBColor(220, 38, 38)
    COLOR_AMBER = RGBColor(217, 119, 6)
    COLOR_PURPLE = RGBColor(124, 58, 237)
    
    COLOR_CARD_FILL = RGBColor(248, 250, 252)
    COLOR_CARD_BORDER = RGBColor(226, 232, 240)
    COLOR_BORDER_RED = RGBColor(254, 202, 202)
    COLOR_BORDER_AMBER = RGBColor(254, 215, 170)
    COLOR_BORDER_BLUE = RGBColor(191, 219, 254)
    COLOR_BORDER_GREEN = RGBColor(167, 243, 208)

    FONT_NAME = "Segoe UI"

    def clear_slide(slide):
        shapes_to_remove = [s for s in slide.shapes]
        for s in shapes_to_remove:
            sp = s._element
            sp.getparent().remove(sp)

    def add_header(slide, tag_text, title_text, tag_color=COLOR_EMERALD):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.73), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = FONT_NAME
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = tag_color

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = FONT_NAME
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_DARK_TEXT

    def add_footer(slide, current_slide, total_slides=11):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.73), Inches(0.35))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"SupplyChainIQ | Governed Conversational Analytics on Snowflake CoCo   •   Slide {current_slide} of {total_slides}"
        p.font.name = FONT_NAME
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_MUTED_TEXT

    def create_card(slide, left, top, width, height, border_color=COLOR_CARD_BORDER, fill_color=COLOR_CARD_FILL):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    card_w3 = Inches(3.64)
    card_gap3 = Inches(0.4)
    card_top3 = Inches(1.5)
    card_h3 = Inches(5.1)

    # -------------------------------------------------------------------------
    # SLIDE 1: COVER
    # -------------------------------------------------------------------------
    s1 = prs.slides[0]
    clear_slide(s1)
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TRACK 5: SUPPLY CHAIN ONTOLOGY & GOVERNED ANALYTICS  •  SNOWFLAKE COCO HACKATHON"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_SNOWFLAKE_CYAN

    p = tf1.add_paragraph()
    p.text = "SupplyChainIQ"
    p.font.name = FONT_NAME
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_TEXT

    p = tf1.add_paragraph()
    p.text = "Governed Conversational Supply Chain Intelligence & Disruption Mitigation"
    p.font.name = FONT_NAME
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    p = tf1.add_paragraph()
    p.text = "Connecting ERP, WMS, and Carrier TMS into a Unified Ontology • Canonical Single Source of Truth • Real-Time Action via MCP"
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BODY_TEXT

    p = tf1.add_paragraph()
    p.text = "\nSNOWFLAKE ARCHITECTURE & COCO LIFECYCLE:"
    p.font.name = FONT_NAME
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_MUTED_TEXT

    p = tf1.add_paragraph()
    p.text = "• Snowflake Dynamic Tables (1m Lag)  |  • Governed Semantic Views (YAML)  |  • Cortex Search Unstructured RAG  |  • Action MCP Tools  |  • Streamlit in Snowflake (SiS)"
    p.font.name = FONT_NAME
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    p = tf1.add_paragraph()
    p.text = "\nTeam: SupplyChainIQ  |  Lead: Chirag H S  |  Track 5 Prototype Submission  |  Snowflake GCC Edition"
    p.font.name = FONT_NAME
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED_TEXT
    add_footer(s1, 1, 11)

    # -------------------------------------------------------------------------
    # SLIDE 2: CHALLENGE
    # -------------------------------------------------------------------------
    s2 = prs.slides[1]
    clear_slide(s2)
    add_header(s2, "THE CHALLENGE & ENTERPRISE MEANING CRISIS", "The Supply Chain Emergency: 3 Conflicting Answers to 1 Question", COLOR_RED)

    cards_s2 = [
        ("3 CONFLICTING ANSWERS", "Metric Ambiguity & Silos", COLOR_RED, COLOR_BORDER_RED, [
            ("The Meaning Breakdown:", "Supply chain teams do not have a data problem; they have a meaning problem. Disconnected ERP, WMS, and TMS systems use incompatible business definitions."),
            ("The Discrepancy:", "When asked 'What is our supplier on-time delivery?', Procurement gets 87%, Planning gets 82%, and Logistics gets 91%."),
            ("Cost of Disconnection:", "Decisions are delayed by days as executives argue over whose spreadsheet has the 'correct' formula.")
        ]),
        ("3.8 DAYS TO SHUTDOWN", "EV Battery Stockout Crisis", COLOR_AMBER, COLOR_BORDER_AMBER, [
            ("Port Bottleneck Event:", "Port of Houston maritime congestion traps critical lithium-ion battery modules (PART_BAT_402) from Tier-1 vendor Apex Battery Cells Ltd."),
            ("Imminent Factory Halt:", "Gigafactory Texas (Austin) consumes 600 units/day with only 2,280 on hand = exactly 3.8 Days of Inventory remaining."),
            ("Surging Demurrage:", "Container demurrage holding charges at berth surge past $19,500 USD, completely unmonitored.")
        ]),
        ("$22,500 UNCLAIMED DAMAGES", "Contractual Blindspots", COLOR_BLUE, COLOR_BORDER_BLUE, [
            ("Trapped in PDF Contracts:", "Suppliers breach delivery dates, but legal penalties remain buried in dense 40-page Master Service Agreement (MSA) documents."),
            ("Manual Audit Lag:", "Procurement teams spend 4+ hours per delayed shipment manually calculating grace periods and liquidated damages."),
            ("The Need:", "Automated unstructured contract intelligence that turns contract text into enforceable penalty claims.")
        ])
    ]

    for idx, (tag, title, tag_c, border_c, bullets) in enumerate(cards_s2):
        c_left = Inches(0.8) + idx * (card_w3 + card_gap3)
        create_card(s2, c_left, card_top3, card_w3, card_h3, border_c)
        tb = s2.shapes.add_textbox(c_left + Inches(0.25), card_top3 + Inches(0.25), card_w3 - Inches(0.5), card_h3 - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = tag_c

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_NAME
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

        for bt, bd in bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK_TEXT
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s2, 2, 11)

    # -------------------------------------------------------------------------
    # SLIDE 3: STRATEGY (4 PILLARS)
    # -------------------------------------------------------------------------
    s3 = prs.slides[2]
    clear_slide(s3)
    add_header(s3, "HOLISTIC PLATFORM STRATEGY", "The SupplyChainIQ Ecosystem: 4 Pillars of Governed Resilience", COLOR_EMERALD)

    card_w4 = Inches(2.68)
    card_gap4 = Inches(0.34)

    pillars = [
        ("PILLAR 1", "Governed Ontology", COLOR_EMERALD, COLOR_BORDER_GREEN, [
            ("Unified Business Entity Graph:", "Maps Supplier ➔ Part ➔ Plant ➔ Shipment ➔ Order ➔ Customer into a canonical relational ontology."),
            ("First-Class Metric Registry:", "Centralized definitions for OTIF %, Days of Inventory, and Landed Cost. The AI never defines what a metric means."),
            ("Cross-Persona Grounding:", "Guarantees Procurement, Planning, and Logistics receive mathematically identical results.")
        ]),
        ("PILLAR 2", "Dynamic Telemetry", COLOR_BLUE, COLOR_BORDER_BLUE, [
            ("Sub-Minute Streaming Pipelines:", "Snowflake Dynamic Tables continuously materialize supplier reliability, plant stockout risk, and active disruptions with 1-min lag."),
            ("Continuous State Awareness:", "Monitors burn-rate deficits and container port bottlenecks automatically on COMPUTE_WH."),
            ("Zero Batch Delays:", "Replaces 24-hour overnight ERP ETL jobs with near real-time operational state.")
        ]),
        ("PILLAR 3", "Contract Intelligence", COLOR_AMBER, COLOR_BORDER_AMBER, [
            ("Snowflake Cortex Search RAG:", "Vector search service (SUPPLIER_CONTRACTS_SEARCH) indexing legal Master Service Agreements (MSAs)."),
            ("Automated SLA Auditing:", "Extracts Section 8.1 grace periods and Section 8.2 liquidated damages ($1,500/day) with 0.68 cosine similarity and 1.24 reranker score."),
            ("Force Majeure Verification:", "Automatically validates whether port congestion qualifies for legal penalty exemption.")
        ]),
        ("PILLAR 4", "Action MCP Engine", COLOR_PURPLE, COLOR_CARD_BORDER, [
            ("Closing the Loop via MCP:", "Rather than merely returning text, CoCo invokes registered Model Context Protocol tools to take real-world action."),
            ("Emergency PO Re-route:", "Automatically triggers 36-hour air freight consignments in ERP to avert factory stoppages."),
            ("Automated Slack Alerts:", "Dispatches legally grounded SLA breach notices directly to the #supply-chain-crisis channel.")
        ])
    ]

    for idx, (p_tag, p_title, p_color, p_border, p_bullets) in enumerate(pillars):
        c_left = Inches(0.8) + idx * (card_w4 + card_gap4)
        create_card(s3, c_left, card_top3, card_w4, card_h3, p_border)
        tb = s3.shapes.add_textbox(c_left + Inches(0.2), card_top3 + Inches(0.25), card_w4 - Inches(0.4), card_h3 - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = p_tag
        p.font.name = FONT_NAME
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = p_color

        p = tf.add_paragraph()
        p.text = p_title
        p.font.name = FONT_NAME
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

        for bt, bd in p_bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.name = FONT_NAME
            p.font.size = Pt(9.2)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK_TEXT
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s3, 3, 11)

    # -------------------------------------------------------------------------
    # SLIDE 4: 5-TIER INFRASTRUCTURE
    # -------------------------------------------------------------------------
    s4 = prs.slides[3]
    clear_slide(s4)
    add_header(s4, "5-TIER CLOUD & AGENTIC ARCHITECTURE", "System Architecture: End-to-End Enterprise Design", COLOR_BLUE)

    tier_h5 = Inches(0.9)
    tier_gap5 = Inches(0.12)
    tier_top5 = Inches(1.5)
    tier_w5 = Inches(11.73)

    tiers_s4 = [
        ("1. INGESTION & PIPELINE TIER", COLOR_EMERALD, [
            ("7 Core Relational Tables:", "DIM_SUPPLIERS, DIM_PARTS, DIM_PLANTS, FACT_PURCHASE_ORDERS, FACT_SHIPMENTS, FACT_INVENTORY, RAW_SUPPLIER_CONTRACTS."),
            ("Snowflake Dynamic Tables:", "DT_SUPPLIER_PERFORMANCE, DT_PLANT_STOCKOUT_RISK, DT_ACTIVE_DISRUPTIONS (Target Lag: 1 Minute on COMPUTE_WH).")
        ]),
        ("2. GOVERNED ONTOLOGY & SEMANTIC REGISTRY", COLOR_BLUE, [
            ("Metric Registry Table:", "METRIC_REGISTRY cataloging canonical formulas, owners, and grains (OTIF %, Days of Inventory, Landed Cost)."),
            ("Semantic Model YAML:", "supply_chain_semantic_model.yaml staged at @SEMANTIC_MODELS_STAGE with verified queries for Cortex Analyst.")
        ]),
        ("3. CORTEX AI & UNSTRUCTURED SEARCH ENGINE", COLOR_AMBER, [
            ("Cortex Search Service:", "SUPPLIER_CONTRACTS_SEARCH indexing unstructured MSAs with high-dimensional vector embeddings."),
            ("Automated Legal Retrieval:", "Retrieves Section 8 grace periods & liquidated damages ($1,500/day) with 0.68 cosine similarity and 1.24 reranker score.")
        ]),
        ("4. COCO AGENT & MCP ACTION ORCHESTRATION", COLOR_PURPLE, [
            ("Full-Lifecycle CoCo CLI:", "Planning, automated pipeline generation, execution, and validation test suite (test_ontology_accuracy.sql)."),
            ("Model Context Protocol (MCP):", "supply_chain_mcp.py executing real-world ERP PO expediting and Slack contractual breach alerts.")
        ]),
        ("5. PRESENTATION & OPERATIONAL COMMAND CENTER", COLOR_SNOWFLAKE_CYAN, [
            ("Streamlit in Snowflake (SiS):", "Live deployed native application (SUPPLY_CHAIN_COMMAND_CENTER) running inside Snowsight."),
            ("Multi-Persona Interface:", "Dedicated operational views for VP Procurement, Plant Operations Manager, and Logistics Director.")
        ])
    ]

    for idx, (t_tag, t_color, t_bullets) in enumerate(tiers_s4):
        curr_top = tier_top5 + idx * (tier_h5 + tier_gap5)
        create_card(s4, Inches(0.8), curr_top, tier_w5, tier_h5, COLOR_CARD_BORDER)
        tb = s4.shapes.add_textbox(Inches(1.0), curr_top + Inches(0.1), tier_w5 - Inches(0.4), tier_h5 - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = t_tag
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = t_color

        p = tf.add_paragraph()
        for b_idx, (bt, bd) in enumerate(t_bullets):
            r1 = p.add_run()
            r1.text = ("  • " if b_idx > 0 else "• ") + bt + " "
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = COLOR_DARK_TEXT

            r2 = p.add_run()
            r2.text = bd + ("   " if b_idx == 0 else "")
            r2.font.bold = False
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s4, 4, 11)

    # -------------------------------------------------------------------------
    # SLIDE 5: BLOCK DIAGRAM & DATA TELEMETRY
    # -------------------------------------------------------------------------
    s5 = prs.slides[4]
    clear_slide(s5)
    add_header(s5, "ENTERPRISE BLOCK DIAGRAM & DATA TELEMETRY", "System Architecture Flow: End-to-End Pipeline & Integrations", COLOR_SNOWFLAKE_CYAN)

    card_top5 = Inches(1.5)
    create_card(s5, Inches(0.8), card_top5, Inches(11.73), Inches(5.1), COLOR_BORDER_BLUE)
    tb = s5.shapes.add_textbox(Inches(1.1), card_top5 + Inches(0.3), Inches(11.13), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    flow_sections = [
        ("1. UNIFIED INGESTION LAYER (TRANSACTIONAL & UNSTRUCTURED)", COLOR_BLUE,
         "Ingests raw ERP Purchase Orders, WMS Inventory counts, Carrier AIS/GPS telematics, and PDF Master Service Agreements. Automatically partitions and stages in SUPPLY_CHAIN_DB.CORE."),
        ("2. STREAMING PIPELINE TIER (SNOWFLAKE DYNAMIC TABLES)", COLOR_EMERALD,
         "Three near real-time Dynamic Tables compute 1-minute rolling aggregates on COMPUTE_WH: DT_SUPPLIER_PERFORMANCE (OTIF & delay days), DT_PLANT_STOCKOUT_RISK (burn rates & runway), and DT_ACTIVE_DISRUPTIONS (port demurrage)."),
        ("3. GOVERNED SEMANTIC ONTOLOGY & METRIC REGISTRY", COLOR_SNOWFLAKE_CYAN,
         "Centrally registers canonical business metrics in METRIC_REGISTRY. Maps natural language to governed semantic YAML views. Guarantees that the LLM never invents or alters mathematical formulas."),
        ("4. CORTEX SEARCH & INTELLIGENCE ENGINE", COLOR_AMBER,
         "High-performance vector RAG (SUPPLIER_CONTRACTS_SEARCH) parses legal clauses from vendor MSAs. Resolves grace periods and penalty rates in sub-seconds with cosine similarity scores."),
        ("5. PRESENTATION & ACTIONABLE MCP WORKFLOW", COLOR_PURPLE,
         "Streamlit in Snowflake presents live persona dashboards with full auditability ([View SQL], [Metric Definition], [Data Lineage]). Dispatches automated emergency air-freight POs and Slack alerts via MCP.")
    ]

    for idx, (sec_title, sec_color, sec_desc) in enumerate(flow_sections):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = sec_title
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = sec_color

        p2 = tf.add_paragraph()
        p2.text = sec_desc + "\n"
        p2.font.name = FONT_NAME
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s5, 5, 11)

    # -------------------------------------------------------------------------
    # SLIDE 6: REAL-TIME OPERATIONAL INTELLIGENCE
    # -------------------------------------------------------------------------
    s6 = prs.slides[5]
    clear_slide(s6)
    add_header(s6, "REAL-TIME OPERATIONAL INTELLIGENCE", "Persona Consistency: One Single Source of Truth Across Teams", COLOR_EMERALD)

    persona_cards = [
        ("VP OF PROCUREMENT", "Supplier Reliability & Damages", COLOR_BLUE, COLOR_BORDER_BLUE, [
            ("Governed Metric:", "On-Time In-Full (OTIF %): Exactly 33.3% for Apex Battery Cells."),
            ("Liquidated Damages:", "Calculates $22,500 in accrued delay penalties based on 21 delay days minus 3-day contract grace."),
            ("Action Trigger:", "Dispatches formal contractual breach escalation notice to vendor leadership.")
        ]),
        ("LOGISTICS DIRECTOR", "Port Congestion & Demurrage", COLOR_SNOWFLAKE_CYAN, COLOR_BORDER_BLUE, [
            ("Governed Metric:", "Identical 33.3% OTIF rate with exact shipment citation (SHP_9002 & SHP_9011)."),
            ("Demurrage Incurred:", "Identifies $19,500 in port holding fees accrued at Port of Houston berth."),
            ("Action Trigger:", "Re-routes delayed ocean containers and authorizes air freight substitution.")
        ]),
        ("PLANT OPERATIONS MANAGER", "Assembly Buffer Runway", COLOR_RED, COLOR_BORDER_RED, [
            ("Governed Metric:", "Days of Inventory (DOI) = exactly 3.8 Days for Battery Module PART_BAT_402."),
            ("Stockout Severity:", "CRITICAL_STOCKOUT_RISK: On-hand 2,280 units against 600 units/day burn rate."),
            ("Action Trigger:", "Triggers emergency 36-hour air freight PO via MCP to prevent plant shutdown.")
        ])
    ]

    for idx, (p_tag, p_title, p_color, p_border, p_bullets) in enumerate(persona_cards):
        c_left = Inches(0.8) + idx * (card_w3 + card_gap3)
        create_card(s6, c_left, card_top3, card_w3, card_h3, p_border)
        tb = s6.shapes.add_textbox(c_left + Inches(0.25), card_top3 + Inches(0.25), card_w3 - Inches(0.5), card_h3 - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = p_tag
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = p_color

        p = tf.add_paragraph()
        p.text = p_title
        p.font.name = FONT_NAME
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

        for bt, bd in p_bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK_TEXT
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s6, 6, 11)

    # -------------------------------------------------------------------------
    # SLIDE 7: CONTRACT INTELLIGENCE WITH CORTEX
    # -------------------------------------------------------------------------
    s7 = prs.slides[6]
    clear_slide(s7)
    add_header(s7, "UNSTRUCTURED CONTRACT INTELLIGENCE WITH CORTEX", "Zero Legal Blindspots: Turning Legal MSAs into Enforceable Claims", COLOR_AMBER)

    c_top7 = Inches(1.5)
    create_card(s7, Inches(0.8), c_top7, Inches(11.73), Inches(5.1), COLOR_BORDER_AMBER)
    tb = s7.shapes.add_textbox(Inches(1.1), c_top7 + Inches(0.3), Inches(11.13), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CORTEX SEARCH SERVICE: SUPPLIER_CONTRACTS_SEARCH"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    p = tf.add_paragraph()
    p.text = "Automated Extraction of SLA Penalty Terms from RAW_SUPPLIER_CONTRACTS\n"
    p.font.name = FONT_NAME
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_TEXT

    cortex_clauses = [
        ("SECTION 8.1 GRACE PERIOD CLAUSE", COLOR_BLUE,
         "Buyer agrees to a 3-calendar-day grace period for port congestion beyond promised delivery date. Delays within this window are toll-free."),
        ("SECTION 8.2 LIQUIDATED DAMAGES CLAUSE", COLOR_RED,
         "If shipment delivery exceeds promised delivery date plus grace period, Supplier shall incur liquidated damages of USD $1,500.00 per calendar day per delayed shipment until actual receipt at designated facility."),
        ("SECTION 8.3 FORCE MAJEURE EXCLUSION", COLOR_AMBER,
         "Delays resulting from certified government embargoes qualify as Force Majeure. Routine port terminal berth congestion expressly does NOT qualify as Force Majeure."),
        ("RETRIEVAL PRECISION METRICS", COLOR_EMERALD,
         "Cortex Search returns CTR_APEX_2025 with Cosine Similarity Score = 0.6814 and Reranker Score = 1.24, proving high semantic grounding.")
    ]

    for c_title, c_color, c_text in cortex_clauses:
        p = tf.add_paragraph()
        p.text = c_title
        p.font.name = FONT_NAME
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = c_color

        p2 = tf.add_paragraph()
        p2.text = c_text + "\n"
        p2.font.name = FONT_NAME
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s7, 7, 11)

    # -------------------------------------------------------------------------
    # SLIDE 8: DETERMINISTIC 'WHY' DECOMPOSITION
    # -------------------------------------------------------------------------
    s8 = prs.slides[7]
    clear_slide(s8)
    add_header(s8, "DETERMINISTIC 'WHY' DECOMPOSITION & ROOT CAUSE", "Mathematical Attribution: Decomposing KPI Drops without LLM Guesswork", COLOR_RED)

    cards_s8 = [
        ("PRIMARY OFFENDER", "Apex Battery Cells Ltd", COLOR_RED, COLOR_BORDER_RED, [
            ("OTD Collapse:", "On-time delivery dropped from 100% baseline to 33.3%."),
            ("Mathematical Contribution:", "Apex Battery consignments contribute -66.7 percentage points to overall powertrain delivery failure."),
            ("Liquidated Damages:", "Accrued penalty of $22,500 across 21 delayed shipment-days.")
        ]),
        ("LOGISTICS CHOKEPOINT", "Port of Houston Congestion", COLOR_AMBER, COLOR_BORDER_AMBER, [
            ("Trapped Ocean Shipments:", "Consignments SHP_9002 (6,000 units) and SHP_9011 (7,500 units) stuck at container terminal berth."),
            ("Carrier Demurrage:", "Accumulating port holding penalties reach $19,500 USD."),
            ("Carrier Accountability:", "Pacific Freight Lines flagged for failure to provide 48-hour advance notice.")
        ]),
        ("FACTORY VULNERABILITY", "Gigafactory Texas (Austin)", COLOR_BLUE, COLOR_BORDER_BLUE, [
            ("Inventory Deficit:", "Physical on-hand inventory is 2,280 units against target buffer of 5,000 units."),
            ("Runway Depletion:", "Runway stands at 3.8 days. Assembly line will stall on day 4 without immediate intervention."),
            ("Action Recommendation:", "Trigger emergency air freight dispatch of 2,000 units to bridge the 36-hour gap.")
        ])
    ]

    for idx, (tag, title, tag_c, border_c, bullets) in enumerate(cards_s8):
        c_left = Inches(0.8) + idx * (card_w3 + card_gap3)
        create_card(s8, c_left, card_top3, card_w3, card_h3, border_c)
        tb = s8.shapes.add_textbox(c_left + Inches(0.25), card_top3 + Inches(0.25), card_w3 - Inches(0.5), card_h3 - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = tag_c

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_NAME
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

        for bt, bd in bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK_TEXT
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s8, 8, 11)

    # -------------------------------------------------------------------------
    # SLIDE 9: AUDITABLE TRANSPARENCY & THE 3 TRUST BUTTONS
    # -------------------------------------------------------------------------
    s9 = prs.slides[8]
    clear_slide(s9)
    add_header(s9, "AUDITABLE TRANSPARENCY & THE 3 TRUST BUTTONS", "Eliminating the Black Box: Explainability, Lineage & Verified SQL", COLOR_BLUE)

    cards_s9 = [
        ("ZERO HALLUCINATION", "Semantic Query Plan (JSON)", COLOR_BLUE, COLOR_BORDER_BLUE, [
            ("Intermediate Representation:", "Natural language does NOT generate raw SQL directly. It first compiles into a deterministic JSON query plan."),
            ("Entity Grounding:", "Specifies intent (performance_decomposition), metric (on_time_delivery), and target part (PART_BAT_402)."),
            ("Ontology Path:", "Supplier ➔ Part ➔ Plant ➔ Shipment ➔ Port.")
        ]),
        ("AUDITABLE REASONING", "The 3 Trust Buttons in SiS", COLOR_EMERALD, COLOR_BORDER_GREEN, [
            ("[View Governed SQL]:", "Inspects the exact verified SQL query generated by the semantic model."),
            ("[Metric Definition]:", "Exposes metric owner (Logistics), grain (Shipment), and canonical SQL formula."),
            ("[Data Lineage]:", "Traces full provenance from ERP ➔ Dynamic Tables ➔ Semantic View ➔ Answer.")
        ]),
        ("LIVE PRODUCTION UI", "Streamlit in Snowflake (SiS)", COLOR_SNOWFLAKE_CYAN, COLOR_BORDER_BLUE, [
            ("Native Deployment:", "SUPPLY_CHAIN_COMMAND_CENTER deployed live inside Snowflake Snowsight."),
            ("Multi-Persona Switcher:", "Instant toggle between VP Procurement, Plant Manager, and Logistics Director."),
            ("Live Interactive URL:", "Directly accessible on Snowflake account ZJXLXUZ.JV50315.")
        ])
    ]

    for idx, (tag, title, tag_c, border_c, bullets) in enumerate(cards_s9):
        c_left = Inches(0.8) + idx * (card_w3 + card_gap3)
        create_card(s9, c_left, card_top3, card_w3, card_h3, border_c)
        tb = s9.shapes.add_textbox(c_left + Inches(0.25), card_top3 + Inches(0.25), card_w3 - Inches(0.5), card_h3 - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = tag_c

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_NAME
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

        for bt, bd in bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK_TEXT
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s9, 9, 11)

    # -------------------------------------------------------------------------
    # SLIDE 10: ACTION MCP
    # -------------------------------------------------------------------------
    s10 = prs.slides[9]
    clear_slide(s10)
    add_header(s10, "CLOSED-LOOP AGENTIC ACTION (MCP)", "Beyond Chatbots: Executing Real-World Business Actions via MCP", COLOR_PURPLE)

    card_w2 = Inches(5.66)
    card_gap2 = Inches(0.4)

    cards_s10 = [
        ("ACTION TOOL 1: ERP RE-ORDER", "expedite_purchase_order", COLOR_EMERALD, COLOR_BORDER_GREEN, [
            ("Autonomous PO Generation:", "Dispatches emergency air freight consignment EXP_2026_002 for 2,000 battery modules directly to Gigafactory Texas."),
            ("Carrier Coordination:", "Assigns Global Aero Air Cargo with guaranteed 36-hour transit window."),
            ("Factory Impact:", "Averts assembly line shutdown, restoring Days of Inventory from 3.8 days to safe 7.1 days buffer."),
            ("Execution Status:", "EXECUTED with full JSON payload audit trail.")
        ]),
        ("ACTION TOOL 2: SLACK ESCALATION", "send_supplier_sla_breach_alert", COLOR_RED, COLOR_BORDER_RED, [
            ("Legally Grounded Alert:", "Dispatches formal contractual breach notice to #supply-chain-crisis channel."),
            ("Contract Grounding:", "Directly quotes Section 8.2 liquidated damages clause ($1,500/day after 3-day grace)."),
            ("Damages Claimed:", "Itemizes $7,500 penalty for shipment SHP_9002 and $22,500 total vendor liability."),
            ("Execution Status:", "DISPATCHED with formatted rich Slack attachment payload.")
        ])
    ]

    for idx, (tag, title, tag_c, border_c, bullets) in enumerate(cards_s10):
        c_left = Inches(0.8) + idx * (card_w2 + card_gap2)
        create_card(s10, c_left, card_top3, card_w2, card_h3, border_c)
        tb = s10.shapes.add_textbox(c_left + Inches(0.3), card_top3 + Inches(0.3), card_w2 - Inches(0.6), card_h3 - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = tag_c

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_NAME
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

        for bt, bd in bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.name = FONT_NAME
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK_TEXT
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s10, 10, 11)

    # -------------------------------------------------------------------------
    # SLIDE 11: OUTCOMES & SCALABILITY
    # -------------------------------------------------------------------------
    s11 = prs.slides[10]
    clear_slide(s11)
    add_header(s11, "MEASURABLE OUTCOMES & SCALING ROADMAP", "Enterprise ROI, SCOR Compliance & Future Production Scalability", COLOR_EMERALD)

    cards_s11 = [
        ("QUANTIFIABLE ROI", "Measurable Business Outcomes", COLOR_EMERALD, COLOR_BORDER_GREEN, [
            ("100% Metric Consistency:", "Eliminated metric disputes across Procurement, Planning, and Logistics by centralizing canonical formulas in Snowflake."),
            ("90% Faster Triage:", "Cuts contract breach discovery from 4 hours of manual legal search to 3 seconds via Cortex Search."),
            ("$22,500 Recovered:", "Automated filing of liquidated damages claims and prevented a multi-million-dollar factory shutdown.")
        ]),
        ("SCOR COMPLIANT", "Universal Industry Adaptability", COLOR_SNOWFLAKE_CYAN, COLOR_BORDER_BLUE, [
            ("Industry-Agnostic Ontology:", "The core entity graph (Supplier ➔ Part ➔ Plant ➔ Shipment ➔ Order) readily adapts to:"),
            ("Pharmaceuticals:", "API Suppliers ➔ Vials ➔ Formulation Plants ➔ Cold-Chain FDA SLA compliance."),
            ("Retail & E-commerce:", "Vendors ➔ SKUs ➔ Regional Fulfillment Centers ➔ Late Delivery Chargebacks."),
            ("Aerospace:", "Fasteners ➔ Sub-assemblies ➔ Assembly Hangars ➔ FAA lead times.")
        ]),
        ("PRODUCTION READY", "Full CoCo Lifecycle Evidence", COLOR_PURPLE, COLOR_CARD_BORDER, [
            ("Reusable CoCo Skill:", "Packaged in skills/supply_chain_agent_skill/SKILL.md, ready for deployment in any Snowflake environment."),
            ("Unattended Automations:", "Scheduled Snowflake Task (HOURLY_SUPPLY_CHAIN_MONITOR_TASK) runs 24/7 background anomaly checks."),
            ("Open Source Codebase:", "All pipelines, tests, and documentation maintained at https://github.com/chiraghs/CoCo-Learn.")
        ])
    ]

    for idx, (tag, title, tag_c, border_c, bullets) in enumerate(cards_s11):
        c_left = Inches(0.8) + idx * (card_w3 + card_gap3)
        create_card(s11, c_left, card_top3, card_w3, card_h3, border_c)
        tb = s11.shapes.add_textbox(c_left + Inches(0.25), card_top3 + Inches(0.25), card_w3 - Inches(0.5), card_h3 - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = tag_c

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_NAME
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

        for bt, bd in bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK_TEXT
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_BODY_TEXT
    add_footer(s11, 11, 11)

    prs.save(out_path)
    print("Successfully built Sanjeevini-based 11-slide pitch deck at:", out_path)

if __name__ == "__main__":
    build_deck()
