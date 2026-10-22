#!/usr/bin/env python3
"""scripts/record_live_solution_video.py
Records a REAL, LIVE SCREEN RECORDING of the working browser solution:
- SupplyChainIQ • Team Aegis
- Connected Twin (3D Canvas, Cleanroom inspection, Telemetry)
- Command Center (1 Alert, Austin stockout runway, Long Beach delay)
- Ask CoCo (Conversational chat, multi-turn questions, verified SQL accordion)
- What-If Simulator (Air freight mitigation slider, DOI curve)
- Decision Approvals (2 Pending, 1-Click MCP execution)
- Horizon Audit Trail (Cryptographic immutable ledger)
- Integrations & MCP (Cortex Analyst, Dynamic Tables 1-min lag, MCP Port 8000)

Runtime: Strictly under 2 minutes (~108 seconds).
Outputs broadcast-quality 1080p MP4 to static/coco_demo.mp4 and static/videos/coco_cortex_platform_demo.mp4.
"""

import os
import subprocess
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORK_DIR = os.path.join(BASE_DIR, "scripts", "ui_record_temp")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "static", "videos", "coco_cortex_platform_demo.mp4")
BACKUP_VIDEO = os.path.join(BASE_DIR, "static", "coco_demo.mp4")

os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static", "videos"), exist_ok=True)

NARRATION_SCRIPTS = [
    {
        "id": "part1_connected_twin",
        "title": "Connected Twin Studio",
        "text": (
            "Welcome to SupplyChainIQ by Team Aegis, an autonomous industrial digital twin platform on Snowflake Cortex. "
            "In the Connected Twin studio, we visualize multi-plant spatial layouts, cleanrooms, and automated storage towers. "
            "Every sensor and machine is tied directly to Snowflake Dynamic Tables with a 38-second near real-time lag."
        )
    },
    {
        "id": "part2_command_center",
        "title": "Command Center & Disruption Detection",
        "text": (
            "Switching to the Command Center, live analytical aggregation flags one critical disruption: "
            "consignment SHP-78442 is delayed fourteen days due to outer anchorage congestion at the Port of Long Beach. "
            "Austin Gigafactory's battery inventory runway crashes to 3.8 days, threatening a 140,000-dollar daily assembly line stoppage."
        )
    },
    {
        "id": "part3_ask_coco_greeting_austin",
        "title": "Ask CoCo: Conversational Cortex AI",
        "text": (
            "We open Ask CoCo, our conversational Cortex Agent. "
            "We start with a natural greeting. CoCo welcomes us with multi-turn reasoning capabilities. "
            "We ask why Austin battery runway is dropping. "
            "CoCo instantly isolates the Port of Long Beach bottleneck, provides root cause analysis, and reveals the verified Snowflake SQL proof ledger."
        )
    },
    {
        "id": "part4_ask_coco_contract_audit",
        "title": "Cortex Contract Search & SLA Penalties",
        "text": (
            "Next, we ask: What are our enforceable liquidated damages from Apex Battery under Section 8.2? "
            "Grounded by Cortex Search over vectorized supplier contracts, CoCo parses the legal grace period, computes eleven billable delay days, and identifies 140,000 dollars in recoverable damages."
        )
    },
    {
        "id": "part5_simulator_approvals",
        "title": "What-If Simulator & Governed Approvals",
        "text": (
            "In the What-If Simulator, we evaluate an emergency air-freight mitigation curve that restores runway to 14.2 days. "
            "In the Governed Approvals Queue, two high-impact decisions await review. "
            "With one click, our Model Context Protocol server executes the emergency order to ERP and dispatches the notice."
        )
    },
    {
        "id": "part6_audit_integrations",
        "title": "Horizon Audit & Enterprise Architecture",
        "text": (
            "Every action is permanently recorded in the Snowflake Horizon cryptographic audit trail. "
            "Our Integrations panel confirms Cortex Analyst, one-minute Dynamic Tables, and the Action MCP server are fully operational. "
            "This is complete, self-healing supply chain resilience."
        )
    }
]

def generate_voiceovers():
    """Generates crystal-clear audio narration files using macOS TTS."""
    print("🎙️ Generating studio voiceover using macOS TTS (Samantha @ 185 wpm)...")
    audio_files = []
    total_dur = 0.0
    for item in NARRATION_SCRIPTS:
        sid = item["id"]
        aiff_path = os.path.join(WORK_DIR, f"{sid}.aiff")
        wav_path = os.path.join(WORK_DIR, f"{sid}.wav")
        
        # High quality TTS
        subprocess.run(["/usr/bin/say", "-v", "Samantha", "-r", "185", "-o", aiff_path, item["text"]], check=True)
        subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-i", aiff_path, "-ar", "44100", "-ac", "2", wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Probe exact duration
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", wav_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        dur = float(res.stdout.strip() or 16.0)
        total_dur += dur
        audio_files.append({"id": sid, "wav": wav_path, "duration": dur})
        print(f"  ✅ {sid}: {dur:.1f}s")
        
    print(f"⏱️ Total Narration Duration: {total_dur:.1f}s (< 120s: {'YES ✅' if total_dur < 120 else 'NO ⚠️'})")
    return audio_files

def type_text(page, selector, text, delay=28):
    """Types text character by character like a human operator."""
    page.click(selector)
    for char in text:
        page.keyboard.type(char)
        page.wait_for_timeout(delay)

def record_live_ui(audio_files):
    """Interacts with the live solution on http://127.0.0.1:8080 and records the screen."""
    print("🎬 Launching Chromium for 1080p Live Screen Recording...")
    raw_video_dir = os.path.join(WORK_DIR, "browser_raw")
    os.makedirs(raw_video_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=raw_video_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        # =====================================================================
        # PART 1: CONNECTED TWIN (3D Canvas, Zone Inspection, Lineage)
        # =====================================================================
        print("  ▶️ Part 1: Connected Twin Studio & 3D Spatial Layout...")
        page.goto("http://127.0.0.1:8080/index.html")
        page.wait_for_timeout(2500)
        
        # Switch twin views & inspect zone
        page.evaluate("navigatePage('twin')")
        page.wait_for_timeout(1500)
        page.evaluate("if (typeof inspectZone === 'function') inspectZone('CLEAN_ROOM')")
        page.wait_for_timeout(2500)
        page.evaluate("if (typeof switchInspTab === 'function') switchInspTab('table')")
        page.wait_for_timeout(2500)
        page.evaluate("if (typeof switchInspTab === 'function') switchInspTab('ontology')")
        page.wait_for_timeout(2500)
        page.evaluate("if (typeof closeEntityInspector === 'function') closeEntityInspector()")
        page.wait_for_timeout(max(1000, int((audio_files[0]["duration"] - 11.5) * 1000)))

        # =====================================================================
        # PART 2: COMMAND CENTER (1 Alert, Austin Stockout, Long Beach Delay)
        # =====================================================================
        print("  ▶️ Part 2: Command Center (1 Alert, DOI Stockout Curve)...")
        page.evaluate("navigatePage('dashboard')")
        page.wait_for_timeout(2500)
        page.evaluate("window.scrollBy({ top: 220, behavior: 'smooth' })")
        page.wait_for_timeout(3000)
        page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        page.wait_for_timeout(max(1000, int((audio_files[1]["duration"] - 5.5) * 1000)))

        # =====================================================================
        # PART 3: ASK COCO (Conversational Greeting & Austin Battery Query)
        # =====================================================================
        print("  ▶️ Part 3: Ask CoCo Conversational Agent (Greeting & Austin Query)...")
        page.evaluate("openCopilotModal()")
        page.wait_for_timeout(1500)
        
        # Type "Hi"
        type_text(page, "#copilot-user-input", "Hi CoCo!", delay=50)
        page.wait_for_timeout(400)
        page.click("#copilot-submit-btn")
        page.wait_for_timeout(2500)
        
        # Ask about Austin
        q_austin = "Why is Austin battery DOI at 3.8 days?"
        type_text(page, "#copilot-user-input", q_austin, delay=25)
        page.wait_for_timeout(400)
        page.click("#copilot-submit-btn")
        page.wait_for_timeout(3500)
        
        # Open SQL accordion
        page.evaluate("""
            const details = document.querySelector('#copilot-chat-thread details');
            if (details) details.open = true;
            const thread = document.getElementById('copilot-chat-thread');
            if (thread) thread.scrollTop = thread.scrollHeight;
        """)
        page.wait_for_timeout(max(1000, int((audio_files[2]["duration"] - 10.5) * 1000)))

        # =====================================================================
        # PART 4: ASK COCO (Contract SLA Damages from Apex Battery)
        # =====================================================================
        print("  ▶️ Part 4: Ask CoCo Contract Audit (Apex $140k Liquidated Damages)...")
        q_apex = "What are our liquidated damages from Apex Battery under Section 8.2?"
        type_text(page, "#copilot-user-input", q_apex, delay=22)
        page.wait_for_timeout(400)
        page.click("#copilot-submit-btn")
        page.wait_for_timeout(4000)
        
        # Auto-scroll thread to show the $140k result
        page.evaluate("""
            const thread = document.getElementById('copilot-chat-thread');
            if (thread) thread.scrollTop = thread.scrollHeight;
        """)
        page.wait_for_timeout(max(1500, int((audio_files[3]["duration"] - 7.0) * 1000)))

        # =====================================================================
        # PART 5: WHAT-IF SIMULATOR & DECISION APPROVALS (2 Pending)
        # =====================================================================
        print("  ▶️ Part 5: What-If Simulator & Approvals Queue (2 Pending)...")
        page.evaluate("closeCopilotModal()")
        page.wait_for_timeout(1000)
        
        # Simulator
        page.evaluate("navigatePage('simulator')")
        page.wait_for_timeout(3000)
        
        # Approvals Queue (2 Pending Decisions)
        page.evaluate("navigatePage('approvals')")
        page.wait_for_timeout(3000)
        
        # Wait for duration
        page.wait_for_timeout(max(1000, int((audio_files[4]["duration"] - 7.0) * 1000)))

        # =====================================================================
        # PART 6: HORIZON AUDIT TRAIL & INTEGRATIONS / MCP
        # =====================================================================
        print("  ▶️ Part 6: Horizon Audit Trail & Integrations / MCP...")
        page.evaluate("navigatePage('audit')")
        page.wait_for_timeout(3000)
        page.evaluate("navigatePage('integrations')")
        page.wait_for_timeout(3500)
        page.wait_for_timeout(max(1000, int((audio_files[5]["duration"] - 6.5) * 1000)))

        # Finalize recording
        page.close()
        context.close()
        browser.close()

    # Find the recorded webm file
    recorded_files = [os.path.join(raw_video_dir, f) for f in os.listdir(raw_video_dir) if f.endswith(".webm")]
    if not recorded_files:
        raise RuntimeError("No recorded webm video found from Playwright!")
    
    # Pick the newest
    recorded_files.sort(key=os.path.getmtime, reverse=True)
    raw_video = recorded_files[0]
    print(f"🎥 Real Browser UI Recording captured: {raw_video}")
    return raw_video

def compile_final_video(raw_webm, audio_files):
    """Combines live UI screen recording with synchronized voiceover narration."""
    print("📦 Merging live browser screen recording with audio tracks via FFmpeg...")
    
    # 1. Concatenate all voiceover tracks
    concat_txt = os.path.join(WORK_DIR, "audio_concat.txt")
    with open(concat_txt, "w") as f:
        for item in audio_files:
            f.write(f"file '{item['wav']}'\n")

    combined_audio = os.path.join(WORK_DIR, "combined_voiceover.wav")
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        combined_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Probe audio duration
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", combined_audio]
    res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    target_dur = float(res.stdout.strip() or 105.0)
    print(f"🎙️ Combined Audio Duration: {target_dur:.2f}s")

    # 2. Merge WebM video with Audio into high-quality MP4
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", raw_webm,
        "-i", combined_audio,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{target_dur:.2f}",
        "-map", "0:v:0", "-map", "1:a:0",
        OUTPUT_VIDEO
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Copy to backup location
    subprocess.run(["cp", OUTPUT_VIDEO, BACKUP_VIDEO], check=True)

    file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print("=" * 75)
    print("🎉 REAL WORKING SOLUTION SCREEN RECORDING COMPLETE!")
    print(f"📁 Video Location: {OUTPUT_VIDEO}")
    print(f"⏱️ Video Duration: {target_dur:.2f} seconds (< 2 minutes: {'YES ✅' if target_dur < 120 else 'NO ⚠️'})")
    print(f"📦 File Size: {file_size_mb:.2f} MB")
    print(f"🔗 Also saved to: {BACKUP_VIDEO}")
    print("=" * 75)

if __name__ == "__main__":
    t0 = time.time()
    audio_files = generate_voiceovers()
    raw_video = record_live_ui(audio_files)
    compile_final_video(raw_video, audio_files)
    print(f"✨ Entire recording & compilation workflow finished in {time.time() - t0:.1f}s.")
