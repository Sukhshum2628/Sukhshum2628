#!/usr/bin/env python3
"""
Generate a unified, single-window Matrix Workstation display (animated GIF and static PNG)
combining the Matrix Brand of Sacrifice digital rain on the left and the large, readable
terminal initialization console on the right inside one single, cohesive terminal interface.

Dimensions: 1040 x 480 px
- Left pane (Matrix Emblem): 450 px wide x 480 px tall (Brand of Sacrifice in green digital rain).
- Right pane (Terminal Console): 590 px wide x 480 px tall (Large, prominent bash sequence).
- Single unified outer window border, shared title bar, and seamless division.
- Zero gap, perfectly aligned top and bottom edges, identical near-black background.
- FAST TYPEWRITER PACE: All 5 initialization lines finish completely typing by frame 16.
- EXTENDED HOLD: The 100% complete terminal console and resolved Brand of Sacrifice remain
  fully displayed and steady for 4.0 seconds (with gentle cursor blinking) before looping.

Outputs:
- assets/matrix-portrait.gif (Unified master workstation animation, < 1MB)
- assets/matrix-portrait.png (Unified static fallback)
- assets/terminal-banner.gif (Updated standalone banner fallback)
"""

import math
import os
import random
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps

# Total Canvas Dimensions
CANVAS_WIDTH = 1040
CANVAS_HEIGHT = 480

# Sub-pane division
LEFT_WIDTH = 450
RIGHT_WIDTH = CANVAS_WIDTH - LEFT_WIDTH  # 590 px
HEADER_HEIGHT = 28
FOOTER_HEIGHT = 26

# Colors (Terminal Workstation / Matrix Green Palette)
COLOR_BG = (11, 15, 16)               # Near-black #0b0f10
COLOR_BG_CARD = (17, 23, 26)          # #11171a
COLOR_BORDER = (35, 75, 90)           # #234b5a
COLOR_DIVIDER = (25, 55, 65)          # Subtle inner divider
COLOR_ACCENT = (85, 230, 165)         # Terminal green #55e6a5
COLOR_ACCENT_BRIGHT = (140, 255, 195) # Glowing highlight #8cffc3
COLOR_CYAN = (102, 217, 239)          # Muted cyan #66d9ef
COLOR_DIM = (35, 80, 65)              # Background rain glyphs
COLOR_TEXT_MUTED = (120, 140, 145)

RAMP = "@#%8&WM$B0QOZ*ahkbdpqwmXvjtLJtf1i!lI;:,\"^`'. "
MATRIX_CHARS = ["0", "1", "/", "\\", "|", "#", "@", "%", "*", "+", "-", ".", ":"]

def get_font(size=12, bold=False):
    candidates = [
        "consola.ttf" if not bold else "consolab.ttf",
        "cour.ttf" if not bold else "courbd.ttf",
        "lucon.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Monaco.ttf"
    ]
    for font_name in candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def ensure_avatar_source():
    source_path = os.path.join("assets", "avatar-source.jpg")
    if os.path.exists(source_path):
        return source_path

    url = "https://avatars.githubusercontent.com/u/124433987?v=4"
    print(f"Downloading avatar source from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(source_path, "wb") as f:
        f.write(resp.read())
    return source_path

def generate_unified_workstation():
    source_path = ensure_avatar_source()
    src_img = Image.open(source_path).convert("RGB")
    print(f"Loaded source avatar: {src_img.size}")

    # Process Brand of Sacrifice avatar
    gray = src_img.convert("L")
    eq = ImageOps.autocontrast(gray, cutoff=1)
    sharp = eq.filter(ImageFilter.UnsharpMask(radius=2, percent=190, threshold=2))
    sharp = ImageEnhance.Sharpness(sharp).enhance(2.0)

    # Left pane grid: 104 columns x 68 rows inside 450x426 px active area
    cols = 104
    rows = 68
    resized = sharp.resize((cols, rows), Image.Resampling.LANCZOS)

    char_w = 4.10
    char_h = 6.10
    active_h = CANVAS_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT
    start_x = (LEFT_WIDTH - (cols * char_w)) / 2
    start_y = HEADER_HEIGHT + ((active_h - (rows * char_h)) / 2)

    random.seed(42)

    cells = []
    ramp_len = len(RAMP)

    for r in range(rows):
        for c in range(cols):
            lum = resized.getpixel((c, r))

            if lum < 18:
                is_symbol = False
                target_char = " "
                char_color = (15, 35, 25)
            else:
                is_symbol = True
                norm_lum = lum / 255.0
                ramp_idx = int((1.0 - norm_lum) * (ramp_len - 1))
                target_char = RAMP[ramp_idx]

                if norm_lum > 0.65:
                    char_color = COLOR_ACCENT_BRIGHT
                elif norm_lum > 0.35:
                    char_color = COLOR_ACCENT
                else:
                    char_color = (55, 145, 105)

            cells.append({
                "col": c,
                "row": r,
                "x": start_x + c * char_w,
                "y": start_y + r * char_h,
                "lum": lum,
                "is_symbol": is_symbol,
                "target_char": target_char,
                "color": char_color
            })

    # Left pane rain streams
    streams = []
    for c in range(cols):
        start_frame = random.uniform(0.0, 4.0)
        speed = random.uniform(5.0, 7.5)
        stream_len = random.randint(8, 16)
        ambient_speed = random.uniform(2.5, 4.5)
        ambient_offset = random.uniform(0.0, float(rows))
        streams.append({
            "start_frame": start_frame,
            "speed": speed,
            "stream_len": stream_len,
            "ambient_speed": ambient_speed,
            "ambient_offset": ambient_offset
        })

    # Fonts
    matrix_font = get_font(size=6)
    header_font = get_font(size=11, bold=True)
    footer_font = get_font(size=10)
    term_font = get_font(size=16)
    term_bold = get_font(size=16, bold=True)

    # Right pane terminal lines with fast staggered start frames
    # Line 0 starts at f=0, finishes by f=5
    # Line 1 starts at f=3, finishes by f=8
    # Line 2 starts at f=6, finishes by f=11
    # Line 3 starts at f=9, finishes by f=14
    # Line 4 starts at f=12, finishes by f=16
    # By frame 16, ALL lines are 100% typed out and visible!
    terminal_lines = [
        ("$ ./initialize-profile.sh --target=Sukhshum2628", COLOR_CYAN, 0),
        ("[ OK ] Loading profile emblem: Brand of Sacrifice", COLOR_ACCENT, 3),
        ("[ OK ] Initializing Matrix renderer: Digital rain active", COLOR_ACCENT, 6),
        ("[ OK ] Mounting engineering modules: STALKER-MP [FLAGSHIP]", COLOR_ACCENT, 9),
        ("[ OK ] Systems online // Host authority active", COLOR_ACCENT_BRIGHT, 12),
    ]

    typing_frames = 18    # By frame 18, all lines are 100% typed
    ambient_frames = 14   # Continuous ambient rain while terminal remains 100% full
    total_anim_frames = typing_frames + ambient_frames  # 32 animation frames

    # Pre-render master static fallback frame (100% complete)
    master_img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), COLOR_BG)
    m_draw = ImageDraw.Draw(master_img)

    m_draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, CANVAS_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
    m_draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, HEADER_HEIGHT)], fill=COLOR_BG_CARD)
    m_draw.ellipse([(10, 9), (18, 17)], fill=(230, 85, 85))
    m_draw.ellipse([(22, 9), (30, 17)], fill=(230, 190, 85))
    m_draw.ellipse([(34, 9), (42, 17)], fill=COLOR_ACCENT)
    m_draw.text((56, 7), "sukhshum@workstation: ~/brand-of-sacrifice.asc", fill=COLOR_TEXT_MUTED, font=header_font)
    m_draw.text((CANVAS_WIDTH - 180, 7), "bash - 80x24 (online)", fill=COLOR_CYAN, font=header_font)

    m_draw.line([(LEFT_WIDTH, HEADER_HEIGHT), (LEFT_WIDTH, CANVAS_HEIGHT - FOOTER_HEIGHT)], fill=COLOR_DIVIDER, width=1)

    for cell in cells:
        if cell["target_char"] != " ":
            m_draw.text((cell["x"], cell["y"]), cell["target_char"], fill=cell["color"], font=matrix_font)

    term_start_x = LEFT_WIDTH + 28
    term_start_y = HEADER_HEIGHT + 36
    term_line_gap = 46

    for idx, (line_text, color, _) in enumerate(terminal_lines):
        y = term_start_y + idx * term_line_gap
        if line_text.startswith("[ OK ]"):
            m_draw.text((term_start_x, y), "[ OK ]", fill=COLOR_ACCENT_BRIGHT, font=term_bold)
            m_draw.text((term_start_x + 65, y), line_text[6:], fill=color, font=term_font)
        else:
            m_draw.text((term_start_x, y), line_text, fill=color, font=term_font)

    # Cursor
    cursor_y = term_start_y + len(terminal_lines) * term_line_gap
    m_draw.rectangle([(term_start_x, cursor_y), (term_start_x + 10, cursor_y + 18)], fill=COLOR_ACCENT)

    m_draw.rectangle([(4, CANVAS_HEIGHT - FOOTER_HEIGHT), (CANVAS_WIDTH - 4, CANVAS_HEIGHT - 4)], fill=COLOR_BG_CARD)
    m_draw.text((12, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ EMBLEM: BRAND OF SACRIFICE // BERSERK MATRIX TELEMETRY ]", fill=COLOR_CYAN, font=footer_font)
    m_draw.text((CANVAS_WIDTH - 300, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ WORKSTATION READY // DETERMINISM LOCKED ]", fill=COLOR_ACCENT, font=footer_font)

    static_path = os.path.join("assets", "matrix-portrait.png")
    master_img.save(static_path, format="PNG")
    print(f"Generated static fallback: {static_path} ({os.path.getsize(static_path) / 1024:.1f} KB)")

    frames = []

    for f in range(total_anim_frames):
        img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, CANVAS_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
        draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, HEADER_HEIGHT)], fill=COLOR_BG_CARD)
        draw.ellipse([(10, 9), (18, 17)], fill=(230, 85, 85))
        draw.ellipse([(22, 9), (30, 17)], fill=(230, 190, 85))
        draw.ellipse([(34, 9), (42, 17)], fill=COLOR_ACCENT)
        draw.text((56, 7), "sukhshum@workstation: ~/brand-of-sacrifice.asc", fill=COLOR_TEXT_MUTED, font=header_font)
        draw.text((CANVAS_WIDTH - 180, 7), "bash - 80x24 (online)", fill=COLOR_CYAN, font=header_font)

        draw.line([(LEFT_WIDTH, HEADER_HEIGHT), (LEFT_WIDTH, CANVAS_HEIGHT - FOOTER_HEIGHT)], fill=COLOR_DIVIDER, width=1)

        draw.rectangle([(4, CANVAS_HEIGHT - FOOTER_HEIGHT), (CANVAS_WIDTH - 4, CANVAS_HEIGHT - 4)], fill=COLOR_BG_CARD)
        if f < typing_frames:
            draw.text((12, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ INITIALIZING: RECONSTRUCTING NEURAL MATRIX TELEMETRY ]", fill=COLOR_TEXT_MUTED, font=footer_font)
            draw.text((CANVAS_WIDTH - 250, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ STATUS: LOADING MODULES... ]", fill=COLOR_TEXT_MUTED, font=footer_font)
        else:
            draw.text((12, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ EMBLEM: BRAND OF SACRIFICE // DIGITAL RAIN ACTIVE ]", fill=COLOR_CYAN, font=footer_font)
            draw.text((CANVAS_WIDTH - 300, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ WORKSTATION READY // DETERMINISM LOCKED ]", fill=COLOR_ACCENT, font=footer_font)

        # Calculate stream heads for left pane
        stream_heads = {}
        for c in range(cols):
            st = streams[c]
            if f < typing_frames:
                if f >= st["start_frame"]:
                    head = (f - st["start_frame"]) * st["speed"]
                else:
                    head = -1.0
            else:
                head = (st["ambient_offset"] + (f - typing_frames) * st["ambient_speed"]) % rows
            stream_heads[c] = head

        # Render Left Pane
        for cell in cells:
            c = cell["col"]
            r = cell["row"]
            head = stream_heads[c]
            st = streams[c]

            if f < typing_frames:
                if head >= (r + 1.0):
                    char = cell["target_char"]
                    if char != " ":
                        draw.text((cell["x"], cell["y"]), char, fill=cell["color"], font=matrix_font)
                elif head >= (r - st["stream_len"]):
                    dist_from_head = head - r
                    if dist_from_head < 1.2:
                        char = random.choice(MATRIX_CHARS)
                        draw.text((cell["x"], cell["y"]), char, fill=COLOR_ACCENT_BRIGHT, font=matrix_font)
                    else:
                        char = random.choice(MATRIX_CHARS)
                        dim_factor = max(0.15, 1.0 - (dist_from_head / st["stream_len"]))
                        color = (int(COLOR_ACCENT[0] * dim_factor), int(COLOR_ACCENT[1] * dim_factor), int(COLOR_ACCENT[2] * dim_factor))
                        draw.text((cell["x"], cell["y"]), char, fill=color, font=matrix_font)
            else:
                dist = (head - r) % rows
                if cell["is_symbol"] and cell["target_char"] != " ":
                    char = cell["target_char"]
                    color = COLOR_ACCENT_BRIGHT if dist < 1.4 else cell["color"]
                    draw.text((cell["x"], cell["y"]), char, fill=color, font=matrix_font)
                else:
                    if dist < 1.4:
                        char = random.choice(MATRIX_CHARS)
                        draw.text((cell["x"], cell["y"]), char, fill=COLOR_ACCENT, font=matrix_font)
                    elif dist < st["stream_len"] * 0.6:
                        trail_factor = max(0.1, 1.0 - (dist / (st["stream_len"] * 0.6)))
                        color = (int(COLOR_DIM[0] * trail_factor), int(COLOR_DIM[1] * trail_factor), int(COLOR_DIM[2] * trail_factor))
                        char = random.choice([".", ":", "|", "/"])
                        draw.text((cell["x"], cell["y"]), char, fill=color, font=matrix_font)

        # Render Right Pane:
        # High speed multiplier (9 characters per frame) so lines finish promptly
        active_cursor = None
        for idx, (line_text, color, appear_frame) in enumerate(terminal_lines):
            y = term_start_y + idx * term_line_gap
            if f >= appear_frame:
                chars_visible = min(len(line_text), int((f - appear_frame) * 9) + 1)
                text_slice = line_text[:chars_visible]

                if text_slice.startswith("[ OK ]"):
                    draw.text((term_start_x, y), "[ OK ]", fill=COLOR_ACCENT_BRIGHT, font=term_bold)
                    draw.text((term_start_x + 65, y), text_slice[6:], fill=color, font=term_font)
                else:
                    draw.text((term_start_x, y), text_slice, fill=color, font=term_font)

                # Cursor following actively typing line
                if chars_visible < len(line_text):
                    cursor_x = term_start_x + (chars_visible * 9.5)
                    active_cursor = (cursor_x, y + 2, cursor_x + 9, y + 18)

        if active_cursor:
            draw.rectangle(active_cursor, fill=COLOR_ACCENT)
        elif (f // 2) % 2 == 0:
            # All lines finished: blinking cursor on bottom prompt
            bottom_cursor_y = term_start_y + len(terminal_lines) * term_line_gap
            draw.rectangle([(term_start_x, bottom_cursor_y), (term_start_x + 9, bottom_cursor_y + 18)], fill=COLOR_ACCENT)

        frames.append(img)

    # Frame timings:
    # 90ms per frame for smooth 32-frame animation
    # Final frame gets a 4.0-second hold (4000ms) with ALL data 100% visible
    durations = [90] * (total_anim_frames - 1) + [4000]

    gif_path = os.path.join("assets", "matrix-portrait.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"Generated unified workstation animated GIF: {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

    generate_terminal_banner()

def generate_terminal_banner():
    BANNER_WIDTH = 720
    BANNER_HEIGHT = 160
    font = get_font(size=14)
    font_bold = get_font(size=14, bold=True)
    header_font = get_font(size=11)

    lines = [
        ("$ ./initialize-profile.sh", COLOR_CYAN, 0),
        ("[ OK ] Loading profile emblem: Brand of Sacrifice", COLOR_ACCENT_BRIGHT, 3),
        ("[ OK ] Initializing Matrix renderer: Digital rain active", COLOR_ACCENT, 6),
        ("[ OK ] Systems online // Host authority active", COLOR_ACCENT_BRIGHT, 9),
    ]

    total_frames = 24
    frames = []

    for f in range(total_frames):
        img = Image.new("RGB", (BANNER_WIDTH, BANNER_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        draw.rectangle([(1, 1), (BANNER_WIDTH - 2, BANNER_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
        draw.rectangle([(1, 1), (BANNER_WIDTH - 2, 24)], fill=COLOR_BG_CARD)
        draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
        draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
        draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)
        draw.text((45, 6), "bash - 80x24 (sukhshum@workstation:~)", fill=COLOR_TEXT_MUTED, font=header_font)

        y = 36
        for line_text, color, appear_frame in lines:
            if f >= appear_frame:
                chars_visible = min(len(line_text), int((f - appear_frame) * 9) + 1)
                text_slice = line_text[:chars_visible]

                if text_slice.startswith("[ OK ]"):
                    draw.text((16, y), "[ OK ]", fill=COLOR_ACCENT_BRIGHT, font=font_bold)
                    draw.text((70, y), text_slice[6:], fill=color, font=font)
                else:
                    draw.text((16, y), text_slice, fill=color, font=font)

                if chars_visible < len(line_text):
                    cursor_x = 16 + (chars_visible * 8.5)
                    draw.rectangle([(cursor_x, y + 2), (cursor_x + 8, y + 16)], fill=COLOR_ACCENT)

                y += 28

        if f >= 16 and (f // 2) % 2 == 0:
            draw.rectangle([(16, y + 2), (24, y + 16)], fill=COLOR_ACCENT)

        frames.append(img)

    durations = [90] * (total_frames - 1) + [3000]
    gif_path = os.path.join("assets", "terminal-banner.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"Generated standalone terminal banner: {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_unified_workstation()
