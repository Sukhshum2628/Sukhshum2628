#!/usr/bin/env python3
"""
Generate a high-detail, resolution-enhanced Matrix ASCII animation (GIF and static PNG)
of the Berserk Brand of Sacrifice symbol directly from the user's updated GitHub profile
avatar (assets/avatar-source.jpg).

Key features:
1. Genuine image-to-ASCII conversion pipeline using Pillow:
   - Loads updated avatar (Brand of Sacrifice in red/blood eclipse).
   - Sharpens and enhances contrast to delineate the Brand of Sacrifice rune,
     the inner/outer eclipse contours, and negative spaces.
   - High-density character ramp:
     '@#%8&WM$B0QOZ*ahkbdpqwmXvjtLJtf1i!lI;:,"^`\'. '
   - Aspect-ratio correction for monospace fonts.
2. Resolution:
   - Configurable character grid (150 columns x 92 rows = 13,800 character cells).
   - High-definition rendering inside a 640 x 580 px canvas.
3. Authentic Matrix Rain Animation with Progressive Symbol Reveal:
   - Matrix digital rain cascades vertically downwards with green terminal characters:
     0 1 / \ | # @ % * + . :
   - The Brand of Sacrifice emerges and resolves through the falling character field.
   - Once resolved, continuous subtle falling green characters stream in the background
     and around the emblem while keeping the Brand of Sacrifice 100% legible, sharp,
     and rock-solid without jitter.
4. Outputs:
   - assets/matrix-portrait.png: Static master ASCII rendering of the Brand of Sacrifice.
   - assets/matrix-portrait.gif: Smooth Matrix digital rain animation revealing and
     surrounding the Brand of Sacrifice.
   - assets/terminal-banner.gif: Cohesive companion terminal sequence.
"""

import math
import os
import random
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps

# Canvas Dimensions
PORTRAIT_WIDTH = 640
PORTRAIT_HEIGHT = 580
BANNER_WIDTH = 720
BANNER_HEIGHT = 140

# Colors (Terminal Workstation / Matrix Green Palette)
COLOR_BG = (11, 15, 16)               # Near-black #0b0f10
COLOR_BG_CARD = (17, 23, 26)          # #11171a
COLOR_BORDER = (35, 75, 90)           # #234b5a
COLOR_ACCENT = (85, 230, 165)         # Terminal green #55e6a5
COLOR_ACCENT_BRIGHT = (140, 255, 195) # Glowing highlight #8cffc3
COLOR_CYAN = (102, 217, 239)          # Muted cyan #66d9ef
COLOR_DIM = (35, 80, 65)              # Background rain glyphs
COLOR_DIM_CYAN = (25, 60, 75)
COLOR_TEXT_MUTED = (120, 140, 145)

RAMP = "@#%8&WM$B0QOZ*ahkbdpqwmXvjtLJtf1i!lI;:,\"^`'. "
MATRIX_CHARS = ["0", "1", "/", "\\", "|", "#", "@", "%", "*", "+", "-", ".", ":"]

def get_font(size=6, bold=False):
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

def generate_matrix_portrait():
    source_path = ensure_avatar_source()
    src_img = Image.open(source_path).convert("RGB")
    print(f"Loaded source image from {source_path}: {src_img.size}")

    # Convert to grayscale
    gray = src_img.convert("L")

    # High-detail preprocessing:
    # Auto-contrast & sharpness enhancement to delineate Brand rune contours and eclipse aura
    eq = ImageOps.autocontrast(gray, cutoff=1)
    sharp = eq.filter(ImageFilter.UnsharpMask(radius=2, percent=190, threshold=2))
    sharp = ImageEnhance.Sharpness(sharp).enhance(2.0)

    # Resolution grid:
    # 150 columns x 92 rows = 13,800 character cells inside a 640 x 580 canvas
    cols = 150
    rows = 92
    resized = sharp.resize((cols, rows), Image.Resampling.LANCZOS)

    char_w = 4.10
    char_h = 5.65
    start_x = (PORTRAIT_WIDTH - (cols * char_w)) / 2
    start_y = 26 + ((PORTRAIT_HEIGHT - 48 - (rows * char_h)) / 2)

    random.seed(42)

    # Build character cell map from actual image pixels
    cells = []
    ramp_len = len(RAMP)

    for r in range(rows):
        for c in range(cols):
            lum = resized.getpixel((c, r))

            # Segment empty outer boundary vs Brand of Sacrifice emblem
            if lum < 18:
                is_symbol = False
                target_char = " "
                char_color = (15, 35, 25)
            else:
                is_symbol = True
                norm_lum = lum / 255.0
                # Invert density so bright rune lines and glowing eclipse receive dense/bright glyphs
                ramp_idx = int((1.0 - norm_lum) * (ramp_len - 1))
                target_char = RAMP[ramp_idx]

                # Matrix color grading based on luminance:
                # Core bright rune lines: Glowing bright highlight green #8cffc3 & cyan #66d9ef
                # Midtone eclipse aura: Terminal green #55e6a5
                # Outer shadow: Dim matrix emerald
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

    font = get_font(size=6)
    header_font = get_font(size=10)

    # Render static master image (clean Brand of Sacrifice ASCII fallback)
    static_img = Image.new("RGB", (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), COLOR_BG)
    s_draw = ImageDraw.Draw(static_img)
    s_draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, PORTRAIT_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
    s_draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, 22)], fill=COLOR_BG_CARD)
    s_draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
    s_draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
    s_draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)
    s_draw.text((46, 6), f"sukhshum@workstation: ~/brand-of-sacrifice.asc [HI-RES {cols}x{rows}]", fill=COLOR_TEXT_MUTED, font=header_font)

    for cell in cells:
        if cell["target_char"] != " ":
            s_draw.text((cell["x"], cell["y"]), cell["target_char"], fill=cell["color"], font=font)

    s_draw.rectangle([(4, PORTRAIT_HEIGHT - 20), (PORTRAIT_WIDTH - 4, PORTRAIT_HEIGHT - 4)], fill=COLOR_BG_CARD)
    s_draw.text((12, PORTRAIT_HEIGHT - 18), "[ BRAND OF SACRIFICE // BERSERK MATRIX TELEMETRY ]", fill=COLOR_CYAN, font=header_font)

    static_path = os.path.join("assets", "matrix-portrait.png")
    static_img.save(static_path, format="PNG")
    print(f"Generated static fallback: {static_path} ({os.path.getsize(static_path) / 1024:.1f} KB)")

    # Matrix Digital Rain Animation Sequence:
    # Phase 1: Digital rain sweeps down from the top (frames 0 to 18).
    # Phase 2: Brand of Sacrifice resolves fully into crisp ASCII.
    # Phase 3: Brand remains locked and 100% visible while subtle green characters continue
    #          raining smoothly around and behind it.
    reveal_frames = 18
    ambient_rain_frames = 16
    total_frames = reveal_frames + ambient_rain_frames

    # Rain streams for each column
    streams = []
    for c in range(cols):
        start_frame = random.uniform(0.0, 5.0)
        speed = random.uniform(4.8, 6.8)  # cells per frame downward
        stream_len = random.randint(8, 18)
        # Background ambient cycle period
        ambient_speed = random.uniform(2.5, 4.5)
        ambient_offset = random.uniform(0.0, float(rows))
        streams.append({
            "start_frame": start_frame,
            "speed": speed,
            "stream_len": stream_len,
            "ambient_speed": ambient_speed,
            "ambient_offset": ambient_offset
        })

    frames = []

    for f in range(total_frames):
        img = Image.new("RGB", (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        # Header bar
        draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, PORTRAIT_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
        draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, 22)], fill=COLOR_BG_CARD)
        draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
        draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
        draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)
        draw.text((46, 6), f"sukhshum@workstation: ~/brand-of-sacrifice.asc [MATRIX RAIN STREAM]", fill=COLOR_TEXT_MUTED, font=header_font)

        # Footer bar
        status_text = "[ MATRIX RAIN: RECONSTRUCTING SACRIFICE EMBLEM ]" if f < reveal_frames else "[ BRAND OF SACRIFICE // DIGITAL RAIN ACTIVE // ONLINE ]"
        status_color = COLOR_TEXT_MUTED if f < reveal_frames else COLOR_CYAN
        draw.rectangle([(4, PORTRAIT_HEIGHT - 20), (PORTRAIT_WIDTH - 4, PORTRAIT_HEIGHT - 4)], fill=COLOR_BG_CARD)
        draw.text((12, PORTRAIT_HEIGHT - 18), status_text, fill=status_color, font=header_font)

        # Calculate stream heads for frame f
        stream_heads = {}
        for c in range(cols):
            st = streams[c]
            if f < reveal_frames:
                if f >= st["start_frame"]:
                    head = (f - st["start_frame"]) * st["speed"]
                else:
                    head = -1.0
            else:
                # Ambient rain streaming around the symbol
                head = (st["ambient_offset"] + (f - reveal_frames) * st["ambient_speed"]) % rows
            stream_heads[c] = head

        for cell in cells:
            c = cell["col"]
            r = cell["row"]
            head = stream_heads[c]
            st = streams[c]

            if f < reveal_frames:
                # Reveal phase:
                if head >= (r + 1.0):
                    # Rain passed this cell -> locks into the Brand character
                    char = cell["target_char"]
                    if char != " ":
                        draw.text((cell["x"], cell["y"]), char, fill=cell["color"], font=font)
                elif head >= (r - st["stream_len"]):
                    # Falling rain stream head / trail over this cell
                    dist_from_head = head - r
                    if dist_from_head < 1.2:
                        char = random.choice(MATRIX_CHARS)
                        draw.text((cell["x"], cell["y"]), char, fill=COLOR_ACCENT_BRIGHT, font=font)
                    else:
                        char = random.choice(MATRIX_CHARS)
                        dim_factor = max(0.15, 1.0 - (dist_from_head / st["stream_len"]))
                        color = (int(COLOR_ACCENT[0] * dim_factor), int(COLOR_ACCENT[1] * dim_factor), int(COLOR_ACCENT[2] * dim_factor))
                        draw.text((cell["x"], cell["y"]), char, fill=color, font=font)
                else:
                    # Not yet reached
                    pass
            else:
                # Ambient rain phase (Brand of Sacrifice is 100% resolved and legible):
                dist = (head - r) % rows

                if cell["is_symbol"] and cell["target_char"] != " ":
                    # The Brand symbol is permanently locked into its photo character
                    char = cell["target_char"]
                    # If an ambient rain pulse passes through, gently illuminate it
                    if dist < 1.4:
                        color = COLOR_ACCENT_BRIGHT
                    else:
                        color = cell["color"]
                    draw.text((cell["x"], cell["y"]), char, fill=color, font=font)
                else:
                    # In the negative / background space around the emblem: subtle falling matrix glyphs
                    if dist < 1.4:
                        char = random.choice(MATRIX_CHARS)
                        draw.text((cell["x"], cell["y"]), char, fill=COLOR_ACCENT, font=font)
                    elif dist < st["stream_len"] * 0.6:
                        trail_factor = max(0.1, 1.0 - (dist / (st["stream_len"] * 0.6)))
                        color = (int(COLOR_DIM[0] * trail_factor), int(COLOR_DIM[1] * trail_factor), int(COLOR_DIM[2] * trail_factor))
                        char = random.choice([".", ":", "|", "/"])
                        draw.text((cell["x"], cell["y"]), char, fill=color, font=font)

        frames.append(img)

    # Frame durations: 90ms for reveal; 120ms during ambient streaming; final frame hold for 2.0s
    durations = [90] * reveal_frames + [110] * (ambient_rain_frames - 1) + [2000]

    gif_path = os.path.join("assets", "matrix-portrait.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"Generated Brand of Sacrifice animated portrait: {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

def generate_terminal_banner():
    font = get_font(size=13)
    header_font = get_font(size=10)

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

        # Window border
        draw.rectangle([(1, 1), (BANNER_WIDTH - 2, BANNER_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
        draw.rectangle([(1, 1), (BANNER_WIDTH - 2, 22)], fill=COLOR_BG_CARD)

        # Window controls
        draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
        draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
        draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)
        draw.text((45, 6), "bash - 80x24 (sukhshum@workstation:~)", fill=COLOR_TEXT_MUTED, font=header_font)

        y = 32
        for line_text, color, appear_frame in lines:
            if f >= appear_frame:
                chars_visible = min(len(line_text), int((f - appear_frame) * 4) + 1)
                text_slice = line_text[:chars_visible]

                if text_slice.startswith("[ OK ]"):
                    draw.text((16, y), "[ OK ]", fill=COLOR_ACCENT_BRIGHT, font=font)
                    draw.text((64, y), text_slice[6:], fill=color, font=font)
                else:
                    draw.text((16, y), text_slice, fill=color, font=font)

                if chars_visible < len(line_text):
                    cursor_x = 16 + (chars_visible * 8)
                    draw.rectangle([(cursor_x, y + 2), (cursor_x + 7, y + 14)], fill=COLOR_ACCENT)

                y += 24

        # Blinking cursor
        if f >= 28 and (f // 3) % 2 == 0:
            draw.rectangle([(16, y + 2), (23, y + 14)], fill=COLOR_ACCENT)

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
    print(f"Generated terminal banner: {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_matrix_portrait()
    generate_terminal_banner()
