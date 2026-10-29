#!/usr/bin/env python3
"""
Generate a unified, single-window Matrix Workstation display (animated GIF and static PNG)
combining the Matrix Brand of Sacrifice digital rain on the left and the large, readable
terminal initialization console on the right inside one single, cohesive terminal interface.

Dimensions: 1040 x 480 px
- Left pane (Matrix Emblem): 440 px wide x 480 px tall (Brand of Sacrifice in green digital rain).
- Right pane (Terminal Console): 600 px wide x 480 px tall (Large, prominent bash sequence).
- Single unified outer window border, shared title bar, and seamless division.
- Zero gap, perfectly aligned top and bottom edges, identical near-black background.
- Zero jitter / rock-solid stability during hold frames.

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
        start_frame = random.uniform(0.0, 5.0)
        speed = random.uniform(4.5, 6.5)
        stream_len = random.randint(8, 16)
        ambient_speed = random.uniform(2.2, 4.0)
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
    term_font = get_font(size=16)          # Large readable terminal text (1.7x size)
    term_bold = get_font(size=16, bold=True)

    # Right pane terminal lines:
    terminal_lines = [
        ("$ ./initialize-profile.sh --target=Sukhshum2628", COLOR_CYAN, 0),
        ("[ OK ] Loading profile emblem: Brand of Sacrifice", COLOR_ACCENT, 6),
        ("[ OK ] Initializing Matrix renderer: Digital rain active", COLOR_ACCENT, 12),
        ("[ OK ] Mounting engineering modules: STALKER-MP [FLAGSHIP]", COLOR_ACCENT, 18),
        ("[ OK ] Systems online // Host authority active", COLOR_ACCENT_BRIGHT, 24),
    ]

    reveal_frames = 20
    ambient_frames = 14
    total_frames = reveal_frames + ambient_frames

    frames = []

    # Pre-render master static fallback frame (100% resolved, zero noise on symbol)
    master_img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), COLOR_BG)
    m_draw = ImageDraw.Draw(master_img)

    # Outer border
    m_draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, CANVAS_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
    # Unified Title bar
    m_draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, HEADER_HEIGHT)], fill=COLOR_BG_CARD)
    m_draw.ellipse([(10, 9), (18, 17)], fill=(230, 85, 85))
    m_draw.ellipse([(22, 9), (30, 17)], fill=(230, 190, 85))
    m_draw.ellipse([(34, 9), (42, 17)], fill=COLOR_ACCENT)
    m_draw.text((56, 7), "sukhshum@workstation: ~/brand-of-sacrifice.asc", fill=COLOR_TEXT_MUTED, font=header_font)
    m_draw.text((CANVAS_WIDTH - 180, 7), "bash - 80x24 (online)", fill=COLOR_CYAN, font=header_font)

    # Subtle vertical divider separating left & right pane
    m_draw.line([(LEFT_WIDTH, HEADER_HEIGHT), (LEFT_WIDTH, CANVAS_HEIGHT - FOOTER_HEIGHT)], fill=COLOR_DIVIDER, width=1)

    # Left: Master Brand of Sacrifice
    for cell in cells:
        if cell["target_char"] != " ":
            m_draw.text((cell["x"], cell["y"]), cell["target_char"], fill=cell["color"], font=matrix_font)

    # Right: Fully typed terminal lines
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

    # Blinking cursor at end of last line
    last_y = term_start_y + (len(terminal_lines) - 1) * term_line_gap
    last_x = term_start_x + len(terminal_lines[-1][0]) * 10
    m_draw.rectangle([(term_start_x, term_start_y + len(terminal_lines) * term_line_gap), (term_start_x + 10, term_start_y + len(terminal_lines) * term_line_gap + 16)], fill=COLOR_ACCENT)

    # Unified footer bar
    m_draw.rectangle([(4, CANVAS_HEIGHT - FOOTER_HEIGHT), (CANVAS_WIDTH - 4, CANVAS_HEIGHT - 4)], fill=COLOR_BG_CARD)
    m_draw.text((12, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ EMBLEM: BRAND OF SACRIFICE // BERSERK MATRIX TELEMETRY ]", fill=COLOR_CYAN, font=footer_font)
    m_draw.text((CANVAS_WIDTH - 300, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ WORKSTATION READY // DETERMINISM LOCKED ]", fill=COLOR_ACCENT, font=footer_font)

    # Save static fallback PNG
    static_path = os.path.join("assets", "matrix-portrait.png")
    master_img.save(static_path, format="PNG")
    print(f"Generated static fallback: {static_path} ({os.path.getsize(static_path) / 1024:.1f} KB)")

    # Render animation frames
    for f in range(total_frames):
        img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        # Single outer border
        draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, CANVAS_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
        # Shared Title bar
        draw.rectangle([(1, 1), (CANVAS_WIDTH - 2, HEADER_HEIGHT)], fill=COLOR_BG_CARD)
        draw.ellipse([(10, 9), (18, 17)], fill=(230, 85, 85))
        draw.ellipse([(22, 9), (30, 17)], fill=(230, 190, 85))
        draw.ellipse([(34, 9), (42, 17)], fill=COLOR_ACCENT)
        draw.text((56, 7), "sukhshum@workstation: ~/brand-of-sacrifice.asc", fill=COLOR_TEXT_MUTED, font=header_font)
        draw.text((CANVAS_WIDTH - 180, 7), "bash - 80x24 (online)", fill=COLOR_CYAN, font=header_font)

        # Vertical divider line
        draw.line([(LEFT_WIDTH, HEADER_HEIGHT), (LEFT_WIDTH, CANVAS_HEIGHT - FOOTER_HEIGHT)], fill=COLOR_DIVIDER, width=1)

        # Shared Footer bar
        draw.rectangle([(4, CANVAS_HEIGHT - FOOTER_HEIGHT), (CANVAS_WIDTH - 4, CANVAS_HEIGHT - 4)], fill=COLOR_BG_CARD)
        if f < reveal_frames:
            draw.text((12, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ INITIALIZING: RECONSTRUCTING NEURAL MATRIX TELEMETRY ]", fill=COLOR_TEXT_MUTED, font=footer_font)
            draw.text((CANVAS_WIDTH - 250, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ STATUS: LOADING MODULES... ]", fill=COLOR_TEXT_MUTED, font=footer_font)
        else:
            draw.text((12, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ EMBLEM: BRAND OF SACRIFICE // DIGITAL RAIN ACTIVE ]", fill=COLOR_CYAN, font=footer_font)
            draw.text((CANVAS_WIDTH - 300, CANVAS_HEIGHT - FOOTER_HEIGHT + 5), "[ WORKSTATION READY // DETERMINISM LOCKED ]", fill=COLOR_ACCENT, font=footer_font)

        # Calculate stream heads for left pane
        stream_heads = {}
        for c in range(cols):
            st = streams[c]
            if f < reveal_frames:
                if f >= st["start_frame"]:
                    head = (f - st["start_frame"]) * st["speed"]
                else:
                    head = -1.0
            else:
                head = (st["ambient_offset"] + (f - reveal_frames) * st["ambient_speed"]) % rows
            stream_heads[c] = head

        # Render Left Pane (Matrix Digital Rain + Brand of Sacrifice)
        for cell in cells:
            c = cell["col"]
            r = cell["row"]
            head = stream_heads[c]
            st = streams[c]

            if f < reveal_frames:
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

        # Render Right Pane (Large Synchronized Terminal)
        for idx, (line_text, color, appear_frame) in enumerate(terminal_lines):
            y = term_start_y + idx * term_line_gap
            if f >= appear_frame:
                chars_visible = min(len(line_text), int((f - appear_frame) * 4) + 1)
                text_slice = line_text[:chars_visible]

                if text_slice.startswith("[ OK ]"):
                    draw.text((term_start_x, y), "[ OK ]", fill=COLOR_ACCENT_BRIGHT, font=term_bold)
                    draw.text((term_start_x + 65, y), text_slice[6:], fill=color, font=term_font)
                else:
                    draw.text((term_start_x, y), text_slice, fill=color, font=term_font)

                # Cursor on actively typing line
                if chars_visible < len(line_text):
                    cursor_x = term_start_x + (chars_visible * 9.5)
                    draw.rectangle([(cursor_x, y + 2), (cursor_x + 9, y + 18)], fill=COLOR_ACCENT)

        # Blinking cursor after all lines complete
        if f >= 26 and (f // 2) % 2 == 0:
            cursor_y = term_start_y + len(terminal_lines) * term_line_gap
            draw.rectangle([(term_start_x, cursor_y), (term_start_x + 9, cursor_y + 18)], fill=COLOR_ACCENT)

        frames.append(img)

    # Frame durations: 90ms for reveal; 110ms during ambient; final frame hold for 2.5s
    durations = [90] * reveal_frames + [110] * (ambient_frames - 1) + [2500]

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

    # Also generate the standalone terminal banner for backward compatibility
    generate_terminal_banner()

def generate_terminal_banner():
    BANNER_WIDTH = 720
    BANNER_HEIGHT = 160
    font = get_font(size=14)
    font_bold = get_font(size=14, bold=True)
    header_font = get_font(size=11)

    lines = [
        ("$ ./initialize-profile.sh", COLOR_CYAN, 0),
        ("[ OK ] Loading profile emblem: Brand of Sacrifice", COLOR_ACCENT_BRIGHT, 6),
        ("[ OK ] Initializing Matrix renderer: Digital rain active", COLOR_ACCENT, 14),
        ("[ OK ] Systems online // Host authority active", COLOR_ACCENT_BRIGHT, 22),
    ]

    total_frames = 34
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
                chars_visible = min(len(line_text), int((f - appear_frame) * 4) + 1)
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

        if f >= 28 and (f // 3) % 2 == 0:
            draw.rectangle([(16, y + 2), (24, y + 16)], fill=COLOR_ACCENT)

        frames.append(img)

    final_frames = frames + [frames[-1]] * 14
    gif_path = os.path.join("assets", "terminal-banner.gif")
    final_frames[0].save(
        gif_path,
        save_all=True,
        append_images=final_frames[1:],
        duration=100,
        loop=0,
        optimize=True
    )
    print(f"Generated standalone terminal banner: {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_unified_workstation()
