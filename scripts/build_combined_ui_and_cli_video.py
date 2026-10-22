#!/usr/bin/env python3
"""
Combines UI video and CLI in VS Code video into:
1. master_supplychain_ui_and_cli.mp4: Strictly under 2 minutes (110s) - First UI (55s) then CLI (55s)
2. full_extended_ui_then_cli.mp4: Full uncut version (196s) - First full UI (105s) then full CLI (91s)
Mirrors master video to static/coco_demo.mp4 and updates index.
"""

import subprocess
import os

BASE_DIR = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI"
VIDEOS_DIR = os.path.join(BASE_DIR, "static", "videos")
UI_VIDEO = os.path.join(VIDEOS_DIR, "coco_cortex_platform_demo.mp4")
CLI_VIDEO = os.path.join(VIDEOS_DIR, "coco_cli_vscode_demo.mp4")
STATIC_DIR = os.path.join(BASE_DIR, "static")

TMP_DIR = os.path.join(BASE_DIR, "scripts", "combine_temp")
os.makedirs(TMP_DIR, exist_ok=True)

print("🎬 Processing video combinations...")

# 1. First: Full uncut concat (105s UI + 91s CLI = 196s)
concat_list_file = os.path.join(TMP_DIR, "concat_list.txt")
with open(concat_list_file, "w") as f:
    f.write(f"file '{UI_VIDEO}'\n")
    f.write(f"file '{CLI_VIDEO}'\n")

FULL_OUTPUT = os.path.join(VIDEOS_DIR, "full_extended_ui_then_cli.mp4")
cmd_full = [
    "/opt/homebrew/bin/ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_list_file,
    "-c", "copy",
    FULL_OUTPUT
]
print("📦 Generating full uncut version (First UI, Then CLI)...")
subprocess.run(cmd_full, check=True)

# 2. Master < 2 Minute Version: First UI (56s) then CLI (54s) = 110s (< 120s)
# Cut UI video from 0 to 56s with smooth audio fade out
ui_trimmed = os.path.join(TMP_DIR, "ui_trimmed.mp4")
cmd_trim_ui = [
    "/opt/homebrew/bin/ffmpeg", "-y",
    "-ss", "00:00:00", "-to", "00:00:56",
    "-i", UI_VIDEO,
    "-af", "afade=t=out:st=54:d=2",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-c:a", "aac", "-b:a", "192k",
    ui_trimmed
]
print("✂️ Trimming UI segment for under-2-minute master...")
subprocess.run(cmd_trim_ui, check=True)

# Cut CLI video (starting from VS Code launch & schema query to end) - 54s
cli_trimmed = os.path.join(TMP_DIR, "cli_trimmed.mp4")
cmd_trim_cli = [
    "/opt/homebrew/bin/ffmpeg", "-y",
    "-ss", "00:00:18", "-to", "00:01:14",
    "-i", CLI_VIDEO,
    "-af", "afade=t=in:st=0:d=1,afade=t=out:st=54:d=2",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-c:a", "aac", "-b:a", "192k",
    cli_trimmed
]
print("✂️ Trimming CLI segment for under-2-minute master...")
subprocess.run(cmd_trim_cli, check=True)

# Stitch master 110s version
trim_concat_list = os.path.join(TMP_DIR, "trim_concat_list.txt")
with open(trim_concat_list, "w") as f:
    f.write(f"file '{ui_trimmed}'\n")
    f.write(f"file '{cli_trimmed}'\n")

MASTER_OUTPUT = os.path.join(VIDEOS_DIR, "master_supplychain_ui_and_cli.mp4")
cmd_master = [
    "/opt/homebrew/bin/ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", trim_concat_list,
    "-c", "copy",
    MASTER_OUTPUT
]
print("🚀 Assembling Master Video (< 2 min: First UI, Then CLI)...")
subprocess.run(cmd_master, check=True)

# Also mirror MASTER_OUTPUT to static/coco_demo.mp4
import shutil
shutil.copy2(MASTER_OUTPUT, os.path.join(STATIC_DIR, "coco_demo.mp4"))

# Clean up temp
shutil.rmtree(TMP_DIR, ignore_errors=True)

print("✅ SUCCESS! Generated:")
print(f"1. Master (< 2 min): {MASTER_OUTPUT}")
print(f"2. Extended Full: {FULL_OUTPUT}")
print(f"3. Root Mirror: {os.path.join(STATIC_DIR, 'coco_demo.mp4')}")
