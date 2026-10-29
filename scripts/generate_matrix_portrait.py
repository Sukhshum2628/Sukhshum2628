#!/usr/bin/env python3
"""
Generate an ultra-detailed, high-resolution Matrix ASCII portrait (animated GIF and static PNG)
directly from the user's actual profile photo (assets/avatar-source.jpg).

Key features:
1. Ultra-high character resolution (140 columns x 86 rows = 12,040 character cells).
   Preserves crisp photographic detail: eyes, pupils, eyebrows, eyelids, nose bridge,
   nostrils, moustache, lips, beard, and hairline.
2. Authentic Matrix rain stream reveal:
   - Green digital matrix rain streams fall down from the top across every column.
   - As the falling streams sweep through the grid, the characters behind the stream
     heads lock permanently and cleanly into the high-detail portrait characters.
3. Zero jitter / 100% rock-solid stable hold:
   - Once all streams pass, all characters are completely locked.
   - The hold frames are identical copies of the clean master frame with no random
     character cycling or noise on the resolved face.
   - Long stable hold (~3.5 seconds) before looping.
4. Outputs:
   - assets/matrix-portrait.png: Ultra-detail master photographic ASCII portrait.
   - assets/matrix-portrait.gif: Smooth Matrix rain animation revealing the high-detail face.
   - assets/terminal-banner.gif: Cohesive companion terminal banner.
"""

import math
import os
import random
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps

# Canvas Dimensions
PORTRAIT_WIDTH = 640
PORTRAIT_HEIGHT = 560
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

    # Precise photographic crop around face & hair
    w, h = src_img.size
    crop_box = (
        int(w * 0.14),
        int(h * 0.03),
        int(w * 0.86),
        int(h * 0.83)
    )
    cropped = src_img.crop(crop_box).convert("L")

    # High-detail preprocessing:
    eq = ImageOps.autocontrast(cropped, cutoff=1)
    sharp = eq.filter(ImageFilter.UnsharpMask(radius=2, percent=180, threshold=2))
    sharp = ImageEnhance.Sharpness(sharp).enhance(2.0)

    # Ultra-high resolution character grid:
    # 140 columns x 86 rows = 12,040 character cells!
    cols = 140
    rows = 86
    resized = sharp.resize((cols, rows), Image.Resampling.LANCZOS)

    char_w = 4.35
    char_h = 5.85
    start_x = (PORTRAIT_WIDTH - (cols * char_w)) / 2
    start_y = 26 + ((PORTRAIT_HEIGHT - 48 - (rows * char_h)) / 2)

    random.seed(42)

    # Build ultra-detailed cell map
    cells = []
    ramp_len = len(RAMP)

    for r in range(rows):
        for c in range(cols):
            lum = resized.getpixel((c, r))

            # Segment background vs face/hair
            if lum > 185:
                is_subject = False
                target_char = " "
                char_color = (20, 45, 35)
            else:
                is_subject = True
                norm_lum = lum / 185.0
                ramp_idx = int(norm_lum * (ramp_len - 1))
                target_char = RAMP[ramp_idx]

                # Luminance color grading:
                if norm_lum < 0.30:
                    char_color = COLOR_ACCENT
                elif norm_lum < 0.65:
                    char_color = COLOR_ACCENT_BRIGHT
                else:
                    char_color = COLOR_CYAN

            cells.append({
                "col": c,
                "row": r,
                "x": start_x + c * char_w,
                "y": start_y + r * char_h,
                "lum": lum,
                "is_subject": is_subject,
                "target_char": target_char,
                "color": char_color
            })

    # Falling matrix rain streams:
    # Each column has a falling stream falling at speed (cells per frame)
    # The head of the stream moves down from y < 0 to y >= rows
    # Once the head passes a cell row, that cell locks into the photo character!
    streams = []
    for c in range(cols):
        # Staggered entry from top
        start_frame = random.uniform(0.0, 7.0)
        speed = random.uniform(3.8, 5.4)  # cells per frame
        stream_len = random.randint(8, 16)
        streams.append({
            "start_frame": start_frame,
            "speed": speed,
            "stream_len": stream_len
        })

    font = get_font(size=6)
    header_font = get_font(size=10)

    # Reveal takes 24 frames; total animation = 24 reveal frames + 30 stable hold frames
    reveal_frames = 24
    hold_frames = 30
    total_frames = reveal_frames + hold_frames
    frames = []

    # Pre-render the final 100% resolved master frame once to guarantee ZERO jitter during hold
    master_img = Image.new("RGB", (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), COLOR_BG)
    master_draw = ImageDraw.Draw(master_img)
    master_draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, PORTRAIT_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
    master_draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, 22)], fill=COLOR_BG_CARD)
    master_draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
    master_draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
    master_draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)
    master_draw.text((46, 6), f"sukhshum@workstation: ~/avatar.asc [ULTRA-RES {cols}x{rows}]", fill=COLOR_TEXT_MUTED, font=header_font)

    for cell in cells:
        if cell["target_char"] != " ":
            master_draw.text((cell["x"], cell["y"]), cell["target_char"], fill=cell["color"], font=font)

    master_draw.rectangle([(4, PORTRAIT_HEIGHT - 20), (PORTRAIT_WIDTH - 4, PORTRAIT_HEIGHT - 4)], fill=COLOR_BG_CARD)
    master_draw.text((12, PORTRAIT_HEIGHT - 18), "[ SUKHSHUM VAISHNAVI // HIGH-RESOLUTION ASCII REVEALED OK ]", fill=COLOR_CYAN, font=header_font)

    # Save static fallback PNG directly from the rock-solid master frame
    static_path = os.path.join("assets", "matrix-portrait.png")
    master_img.save(static_path, format="PNG")
    print(f"Generated ultra-detail static portrait: {static_path} ({os.path.getsize(static_path) / 1024:.1f} KB)")

    # Render reveal frames (0 to reveal_frames - 1)
    for f in range(reveal_frames):
        img = Image.new("RGB", (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        # Window header
        draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, PORTRAIT_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
        draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, 22)], fill=COLOR_BG_CARD)
        draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
        draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
        draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)
        draw.text((46, 6), f"sukhshum@workstation: ~/avatar.asc [ULTRA-RES {cols}x{rows}]", fill=COLOR_TEXT_MUTED, font=header_font)

        # Status footer bar
        draw.rectangle([(4, PORTRAIT_HEIGHT - 20), (PORTRAIT_WIDTH - 4, PORTRAIT_HEIGHT - 4)], fill=COLOR_BG_CARD)
        draw.text((12, PORTRAIT_HEIGHT - 18), "[ MATRIX RAIN: RECONSTRUCTING NEURAL PROFILE ]", fill=COLOR_TEXT_MUTED, font=header_font)

        # Precalculate stream heads for frame f
        stream_heads = {}
        for c in range(cols):
            st = streams[c]
            if f >= st["start_frame"]:
                head_r = (f - st["start_frame"]) * st["speed"]
            else:
                head_r = -1.0
            stream_heads[c] = head_r

        for cell in cells:
            c = cell["col"]
            r = cell["row"]
            head_r = stream_heads[c]
            st = streams[c]

            if head_r >= (r + 1.0):
                # The falling matrix stream has already passed this cell!
                # It is locked into the final photo character with zero noise.
                char = cell["target_char"]
                if char != " ":
                    draw.text((cell["x"], cell["y"]), char, fill=cell["color"], font=font)
            elif head_r >= (r - st["stream_len"]):
                # The falling matrix stream is currently passing over this cell!
                dist_from_head = head_r - r
                if dist_from_head < 1.2:
                    # Bright leading head glyph of the matrix rain
                    char = random.choice(MATRIX_CHARS)
                    draw.text((cell["x"], cell["y"]), char, fill=COLOR_ACCENT_BRIGHT, font=font)
                else:
                    # Trailing stream glyph fading down
                    char = random.choice(MATRIX_CHARS)
                    dim_factor = max(0.15, 1.0 - (dist_from_head / st["stream_len"]))
                    color = (int(COLOR_ACCENT[0] * dim_factor), int(COLOR_ACCENT[1] * dim_factor), int(COLOR_ACCENT[2] * dim_factor))
                    draw.text((cell["x"], cell["y"]), char, fill=color, font=font)
            else:
                # The falling matrix stream has not reached here yet; remains dark/empty
                pass

        frames.append(img)

    # Frame 24 onwards: The final master frame repeated cleanly (ZERO JITTER)
    # 35 hold frames at 100ms = 3.5 seconds of perfectly calm, rock-solid display
    frames.extend([master_img] * hold_frames)

    # Save animated GIF
    gif_path = os.path.join("assets", "matrix-portrait.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=True
    )
    print(f"Generated ultra-detail animated portrait: {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

def generate_terminal_banner():
    font = get_font(size=13)
    header_font = get_font(size=10)

    lines = [
        ("$ whoami", COLOR_CYAN, 0),
        ("Sukhshum Vaishnavi", COLOR_ACCENT_BRIGHT, 6),
        ("$ loading engineering modules...", COLOR_CYAN, 14),
        ("[ OK ] Systems online // Host authority active", COLOR_ACCENT, 22),
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
