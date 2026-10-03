import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    template_path = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/Prototype Submission Template _ CoCo CLI Hackathon GCC Edition.pptx"
    prs = Presentation(template_path)
    
    # Theme Colors
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_CYAN = RGBColor(41, 181, 232)      # Snowflake Cyan #29B5E8
    COLOR_BLUE = RGBColor(56, 189, 248)      # Sky Blue #38BDF8
    COLOR_DARK_CARD = RGBColor(15, 23, 42)   # Dark Slate #0F172A
    COLOR_CARD_BORDER = RGBColor(51, 65, 85) # Slate Border #334155
    COLOR_CARD_BORDER_CYAN = RGBColor(41, 181, 232)
    COLOR_CARD_BORDER_RED = RGBColor(239, 68, 68)
    COLOR_CARD_BORDER_AMBER = RGBColor(245, 158, 11)
    COLOR_CARD_BORDER_GREEN = RGBColor(16, 185, 129)
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Muted Silver #94A3B8
    COLOR_TEXT_BODY = RGBColor(226, 232, 240)  # Light Silver #E2E8F0
    COLOR_RED = RGBColor(248, 113, 113)     # Coral Red #F87171
    COLOR_AMBER = RGBColor(251, 191, 36)    # Amber Gold #FBBF24
    COLOR_GREEN = RGBColor(52, 211, 153)    # Emerald Green #34D399

    FONT_FAMILY = "Segoe UI" # Highly compatible, clean enterprise font

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    slide1 = prs.slides[0]
    # Update text fields
    for shape in slide1.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "Team Name" in txt:
                shape.text_frame.text = "Team Name :  Aegis"
            elif "Team Leader Name" in txt:
                shape.text_frame.text = "Team Leader Name :  Chirag H S"
            elif "Team Size" in txt:
                shape.text_frame.text = "Team Size :  1"
            elif "Problem Statement" in txt:
                shape.text_frame.text = "Problem Statement :  Track 5 - Supply Chain Ontology and Governed Conversational Analytics"
            
            for p in shape.text_frame.paragraphs:
                p.font.name = FONT_FAMILY
                p.font.color.rgb = COLOR_WHITE
                p.font.size = Pt(13.5)
                p.font.bold = True

    # Add Project Tagline on Cover
    tb_tagline = slide1.shapes.add_textbox(Inches(0.44), Inches(2.3), Inches(8.2), Inches(0.8))
    tf_tag = tb_tagline.text_frame
    tf_tag.word_wrap = True
    p1 = tf_tag.paragraphs[0]
    p1.text = "SupplyChainIQ"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_CYAN

    p2 = tf_tag.add_paragraph()
    p2.text = "Governed Conversational Supply Chain Analytics on Snowflake CoCo & Cortex"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # HELPER FUNCTIONS
    # =========================================================================
    def add_header(slide, tag_text, title_text, subtitle_text=None):
        # Header Box
        header_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.28), Inches(8.14), Inches(0.85))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = FONT_FAMILY
        p_tag.font.size = Pt(9.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_CYAN

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(19)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_FAMILY
            p_sub.font.size = Pt(10)
            p_sub.font.color.rgb = COLOR_TEXT_MUTED

    def add_footer(slide, current_section):
        footer_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.78), Inches(8.14), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"SupplyChainIQ  •  Track 5: Supply Chain Ontology  •  {current_section}  •  Snowflake CoCo Hackathon GCC Edition"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(8)
        p.font.color.rgb = COLOR_TEXT_MUTED

    def clear_non_background_shapes(slide):
        # Shape 0 is the background image, delete others
        shapes_to_remove = [s for idx, s in enumerate(slide.shapes) if idx > 0]
        for s in shapes_to_remove:
            sp = s._element
            sp.getparent().remove(sp)

    def create_card(slide, left, top, width, height, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_DARK_CARD
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 2: SUBMISSION OVERVIEW & EXECUTIVE SUMMARY
    # =========================================================================
    slide2 = prs.slides[1]
    clear_non_background_shapes(slide2)
    add_header(
        slide2, 
        "SUBMISSION BLUEPRINT  •  CORE PHILOSOPHY", 
        "SupplyChainIQ: Enterprise Executive Summary",
        '"The LLM understands the question; the governed ontology decides what it means and where the answer comes from."'
    )

    col_w3 = Inches(2.55)
    gap3 = Inches(0.24)
    top_pos3 = Inches(1.22)
    card_h3 = Inches(3.42)

    # Card 1: Problem Brief
    create_card(slide2, Inches(0.5), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_RED)
    tb1 = slide2.shapes.add_textbox(Inches(0.6), Inches(1.32), Inches(2.35), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "1. PROBLEM BRIEF"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_RED

    p = tf1.add_paragraph()
    p.text = "The Meaning Crisis in Supply Chain"
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_WHITE

    bullets1 = [
        ("Data, Not Meaning:", "Teams have abundant data across ERP, WMS, and TMS, but inconsistent definitions yield 3 different answers to the same question."),
        ("Crisis Scenario:", "Port of Houston bottleneck traps lithium-ion battery modules (PART_BAT_402), placing Gigafactory Texas at 3.8 days to stockout."),
        ("Personas Addressed:", "Procurement VP (liquidated damages), Logistics Director (OTIF & demurrage), Plant Manager (assembly buffer runway).")
    ]
    for b_title, b_desc in bullets1:
        p = tf1.add_paragraph()
        p.text = f"• {b_title} "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_BODY

    # Card 2: Architecture & CoCo Lifecycle
    create_card(slide2, Inches(0.5) + col_w3 + gap3, top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_CYAN)
    tb2 = slide2.shapes.add_textbox(Inches(0.6) + col_w3 + gap3, Inches(1.32), Inches(2.35), Inches(3.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "2. ARCHITECTURE & COCO"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_CYAN

    p = tf2.add_paragraph()
    p.text = "Deterministic Bottom, Intelligent Top"
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_WHITE

    bullets2 = [
        ("Pipelines (CoCo):", "3 near real-time Dynamic Tables (1m lag) on COMPUTE_WH aggregating OTIF, DOI, and active disruptions."),
        ("Governed Semantics:", "First-class METRIC_REGISTRY + semantic YAML model defining canonical metrics across personas."),
        ("Unstructured RAG:", "Cortex Search Service (SUPPLIER_CONTRACTS_SEARCH) indexing vendor MSAs for SLA penalty clauses."),
        ("Action MCP Tools:", "Registered tools for emergency air freight dispatch and formal Slack SLA breach alerts.")
    ]
    for b_title, b_desc in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {b_title} "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_BODY

    # Card 3: Impact Statement
    create_card(slide2, Inches(0.5) + 2*(col_w3 + gap3), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_GREEN)
    tb3 = slide2.shapes.add_textbox(Inches(0.6) + 2*(col_w3 + gap3), Inches(1.32), Inches(2.35), Inches(3.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "3. IMPACT STATEMENT"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_GREEN

    p = tf3.add_paragraph()
    p.text = "Measurable Outcomes & Scalability"
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_WHITE

    bullets3 = [
        ("100% Metric Consistency:", "Guarantees mathematically identical numbers for OTD, DOI, and Landed Cost across all personas."),
        ("90% Faster Recovery:", "Reduces contract breach discovery from 4 hours to seconds, recovering $22,500 in liquidated damages."),
        ("Universal Scalability:", "SCOR-compliant ontology readily adapts to Pharma, Retail, and Aerospace without changing pipelines."),
        ("Production Live:", "Deployed natively as Streamlit in Snowflake (SiS) with full automated test validation suite.")
    ]
    for b_title, b_desc in bullets3:
        p = tf3.add_paragraph()
        p.text = f"• {b_title} "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_WHITE
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_BODY

    add_footer(slide2, "Executive Blueprint")

    # =========================================================================
    # SLIDE 3: PROBLEM BRIEF & CRISIS SCENARIO
    # =========================================================================
    slide3 = prs.slides[2]
    clear_non_background_shapes(slide3)
    add_header(
        slide3,
        "SECTION 1: PROBLEM BRIEF & CRISIS CONTEXT",
        "The Enterprise 'Meaning Problem' in Global Supply Chains",
        "Disparate ERP, logistics, and supplier systems yield conflicting answers, paralyzing cross-functional crisis response."
    )

    # Card 1: The Fragmentation Trap
    create_card(slide3, Inches(0.5), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_RED)
    tb = slide3.shapes.add_textbox(Inches(0.6), Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3 CONFLICTING ANSWERS"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_RED
    p = tf.add_paragraph()
    p.text = "Metric Ambiguity & Silos"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("The 'Meaning' Breakdown:", "Procurement, Planning, and Logistics calculate delivery performance using conflicting formulas and dates."),
        ("The Discrepancy:", "When asked 'What is our on-time delivery?', Procurement gets 87%, Planning gets 82%, and Logistics gets 91%."),
        ("No Shared Ontology:", "Missing relational model connecting Supplier ➔ Part ➔ Plant ➔ Shipment ➔ Order.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    # Card 2: Crisis Scenario
    create_card(slide3, Inches(0.5) + col_w3 + gap3, top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_AMBER)
    tb = slide3.shapes.add_textbox(Inches(0.6) + col_w3 + gap3, Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3.8 DAYS RUNWAY"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_AMBER
    p = tf.add_paragraph()
    p.text = "EV Battery Assembly Crisis"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("Port Bottleneck Disruption:", "Port of Houston maritime berth congestion traps critical battery cells (PART_BAT_402) from Apex Battery Cells Ltd."),
        ("Imminent Plant Stoppage:", "Gigafactory Texas (Austin) burns 600 units/day with only 2,280 units on hand = exactly 3.8 Days of Inventory remaining!"),
        ("Accumulating Demurrage:", "Container demurrage charges at port already surge past $19,500 USD.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    # Card 3: Personas
    create_card(slide3, Inches(0.5) + 2*(col_w3 + gap3), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_CYAN)
    tb = slide3.shapes.add_textbox(Inches(0.6) + 2*(col_w3 + gap3), Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "$22,500 PENALTY RISK"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CYAN
    p = tf.add_paragraph()
    p.text = "Cross-Domain Persona Needs"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("VP of Procurement:", "Needs to calculate liquidated damages trapped in dense PDF Master Service Agreements ($1,500/day after 3-day grace)."),
        ("Logistics Director:", "Needs real-time OTIF tracking, port demurrage monitoring, and carrier accountability."),
        ("Plant Manager:", "Needs instantaneous stockout early warnings to trigger emergency air-freight re-routing.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    add_footer(slide3, "1. Problem Brief")

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & COCO LIFECYCLE
    # =========================================================================
    slide4 = prs.slides[3]
    clear_non_background_shapes(slide4)
    add_header(
        slide4,
        "SECTION 2: SYSTEM ARCHITECTURE & COCO INTEGRATION",
        "SupplyChainIQ: End-to-End Enterprise Architecture",
        "A 4-tier governed data & AI pipeline built and orchestrated entirely via Snowflake CoCo CLI."
    )

    col_w4 = Inches(1.92)
    gap4 = Inches(0.15)
    top_pos4 = Inches(1.22)
    card_h4 = Inches(3.42)

    tiers = [
        ("TIER 1: PIPELINES", "Dynamic Tables (1m Lag)", COLOR_CARD_BORDER_CYAN, [
            ("7 Core Tables:", "Seeded referentially sound data: DIM_SUPPLIERS, PARTS, PLANTS, ORDERS, SHIPMENTS, INVENTORY, CONTRACTS."),
            ("Near Real-Time DTs:", "3 Dynamic Tables continuously refreshing on 1-min lag on COMPUTE_WH."),
            ("Automated Rollups:", "DT_SUPPLIER_PERFORMANCE, DT_PLANT_STOCKOUT_RISK, DT_ACTIVE_DISRUPTIONS.")
        ]),
        ("TIER 2: SEMANTICS", "Governed Metric Registry", COLOR_CARD_BORDER_GREEN, [
            ("Metric Registry:", "First-class METRIC_REGISTRY cataloging canonical formulas, owners, and grains."),
            ("Semantic Model YAML:", "supply_chain_semantic_model.yaml staged at @SEMANTIC_MODELS_STAGE."),
            ("Canonical Truth:", "Centralized definitions for OTIF %, Days of Inventory, and Landed Cost.")
        ]),
        ("TIER 3: CORTEX AI", "Unstructured RAG Search", COLOR_CARD_BORDER_AMBER, [
            ("Cortex Search Service:", "SUPPLIER_CONTRACTS_SEARCH indexes vendor MSAs using native vector embeddings."),
            ("Semantic Contract RAG:", "Extracts Section 8.1 grace periods and Section 8.2 liquidated damages ($1,500/day)."),
            ("High Precision:", "0.68 cosine similarity and 1.24 reranker score on contract clauses.")
        ]),
        ("TIER 4: AGENT & ACTION", "CoCo & Action MCP Tools", COLOR_CARD_BORDER_RED, [
            ("Full CoCo Lifecycle:", "Planning, SQL pipeline generation, execution, and automated testing suite."),
            ("MCP Action Tools:", "expedite_purchase_order (air freight PO) & send_supplier_sla_breach_alert (Slack)."),
            ("Streamlit in Snowflake:", "Live interactive Command Center accessible directly in Snowsight.")
        ])
    ]

    for idx, (t_tag, t_title, t_border, t_bullets) in enumerate(tiers):
        c_left = Inches(0.5) + idx * (col_w4 + gap4)
        create_card(slide4, c_left, top_pos4, col_w4, card_h4, t_border)
        tb = slide4.shapes.add_textbox(c_left + Inches(0.08), Inches(1.32), col_w4 - Inches(0.16), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = t_tag
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_CYAN

        p = tf.add_paragraph()
        p.text = t_title
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_WHITE

        for bt, bd in t_bullets:
            p = tf.add_paragraph()
            p.text = f"• {bt} "
            p.font.bold = True
            p.font.size = Pt(8.2)
            p.font.color.rgb = COLOR_WHITE
            r = p.add_run()
            r.text = bd
            r.font.bold = False
            r.font.color.rgb = COLOR_TEXT_BODY

    add_footer(slide4, "2. System Architecture")

    # =========================================================================
    # SLIDE 5: GOVERNED CONVERSATIONAL DEMO & INNOVATION
    # =========================================================================
    slide5 = prs.slides[4]
    clear_non_background_shapes(slide5)
    add_header(
        slide5,
        "SECTION 3: CONVERSATIONAL AI & DEMO HIGHLIGHTS",
        "Semantic Query Plans, Root-Cause 'Why' & Trust Verification",
        "Eliminating LLM hallucinations through intermediate query compilation, mathematical decomposition, and full auditability."
    )

    create_card(slide5, Inches(0.5), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_CYAN)
    tb = slide5.shapes.add_textbox(Inches(0.6), Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ZERO HALLUCINATION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CYAN
    p = tf.add_paragraph()
    p.text = "Semantic Query Plan (JSON)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("Intermediate Representation:", "Natural language does NOT generate raw SQL directly. It compiles into a structured JSON query plan."),
        ("Entity & Path Grounding:", "Specifies intent (performance_decomposition), metric (on_time_delivery), and traverses: Supplier ➔ Part ➔ Plant ➔ Shipment."),
        ("Deterministic Boundary:", "The LLM understands the question; the semantic view determines what the math means.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    create_card(slide5, Inches(0.5) + col_w3 + gap3, top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_AMBER)
    tb = slide5.shapes.add_textbox(Inches(0.6) + col_w3 + gap3, Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MATHEMATICAL ATTRIBUTION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_AMBER
    p = tf.add_paragraph()
    p.text = "Deterministic 'Why' Engine"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("No Vague Explanations:", "Explains why OTD dropped to 33.3% with exact mathematical component contributions."),
        ("Apex Battery Cells:", "4 delayed consignments contribute -66.7 pp, generating $22,500 in accrued damages."),
        ("Port of Houston:", "Shipments SHP_9002 & SHP_9011 stuck at berth, adding $19,500 demurrage penalty fees.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    create_card(slide5, Inches(0.5) + 2*(col_w3 + gap3), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_GREEN)
    tb = slide5.shapes.add_textbox(Inches(0.6) + 2*(col_w3 + gap3), Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "AUDITABLE TRANSPARENCY"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_GREEN
    p = tf.add_paragraph()
    p.text = "The 3 Trust Buttons in SiS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("[View Governed SQL]:", "Provides immediate inspection of the verified SQL generated by the semantic layer."),
        ("[Metric Definition]:", "Exposes metric owner (Logistics), grain (Shipment), and canonical SQL formula."),
        ("[Data Lineage]:", "Traces full provenance from ERP ➔ Dynamic Tables ➔ Semantic View ➔ Answer."),
        ("Live SiS App:", "SUPPLY_CHAIN_COMMAND_CENTER deployed live in Snowsight.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    add_footer(slide5, "3. Governed Conversational Intelligence")

    # =========================================================================
    # SLIDE 6: IMPACT STATEMENT & SCALABILITY
    # =========================================================================
    slide6 = prs.slides[5]
    clear_non_background_shapes(slide6)
    add_header(
        slide6,
        "SECTION 4: MEASURABLE OUTCOMES & SCALABILITY",
        "Measurable Business Impact & Enterprise Extension",
        "Proven ROI, universal SCOR-compliant industry adaptability, and production readiness beyond the hackathon."
    )

    create_card(slide6, Inches(0.5), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_GREEN)
    tb = slide6.shapes.add_textbox(Inches(0.6), Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "QUANTIFIABLE ROI"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_GREEN
    p = tf.add_paragraph()
    p.text = "Measurable Business Outcomes"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("100% Metric Consistency:", "Eliminates cross-departmental conflicting reports across Procurement, Planning, and Logistics."),
        ("90% Faster Triage:", "Cuts contract breach investigation from 4 hours of manual legal search to 3 seconds via Cortex Search."),
        ("$22,500 Direct Recovery:", "Automates liquidated damages penalty filings and averts a multi-million-dollar plant shutdown.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    create_card(slide6, Inches(0.5) + col_w3 + gap3, top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_CYAN)
    tb = slide6.shapes.add_textbox(Inches(0.6) + col_w3 + gap3, Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SCOR COMPLIANT"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CYAN
    p = tf.add_paragraph()
    p.text = "Universal Industry Scalability"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("Plug-and-Play Ontology:", "The entity graph (Supplier ➔ Part ➔ Plant ➔ Shipment ➔ Order) is 100% industry-agnostic:"),
        ("Pharmaceuticals:", "API Suppliers ➔ Vials ➔ Formulation Plants ➔ Cold-Chain Distribution ➔ FDA SLA compliance."),
        ("Retail & E-commerce:", "Vendors ➔ SKUs ➔ Regional Fulfillment Centers ➔ Late Delivery Chargebacks."),
        ("Aerospace:", "Fasteners ➔ Aircraft Sub-assemblies ➔ Hangars ➔ FAA lead times.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    create_card(slide6, Inches(0.5) + 2*(col_w3 + gap3), top_pos3, col_w3, card_h3, COLOR_CARD_BORDER_AMBER)
    tb = slide6.shapes.add_textbox(Inches(0.6) + 2*(col_w3 + gap3), Inches(1.32), Inches(2.35), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "BEYOND THE DEMO"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_AMBER
    p = tf.add_paragraph()
    p.text = "Production Extensibility"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE

    bullets = [
        ("Packaged CoCo Skill:", "skills/supply_chain_agent_skill/SKILL.md ready for deployment across any Snowflake organization."),
        ("Unattended Automations:", "Scheduled Snowflake Task (HOURLY_SUPPLY_CHAIN_MONITOR_TASK) runs 24/7 background anomaly checks."),
        ("GitHub Open Source:", "All pipelines, tests, and documentation maintained at https://github.com/chiraghs/CoCo-Learn.")
    ]
    for bt, bd in bullets:
        p = tf.add_paragraph()
        p.text = f"• {bt} "
        p.font.bold = True
        p.font.size = Pt(8.8)
        p.font.color.rgb = COLOR_WHITE
        r = p.add_run()
        r.text = bd
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT_BODY

    add_footer(slide6, "4. Impact Statement & Scalability")

    # Save to the target presentation
    prs.save(template_path)
    print(f"Successfully generated and saved submission deck to: {template_path}")

if __name__ == "__main__":
    build_deck()
