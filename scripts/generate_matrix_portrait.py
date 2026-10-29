#!/usr/bin/env python3
"""
Generate an image-derived Matrix/terminal portrait animation and terminal banner.

Pipeline:
1. Load local avatar source image (assets/avatar-source.jpg - Sukhshum2628's verified GitHub avatar).
   If missing, downloads from GitHub user endpoint.
2. Extracts pixel luminance / geometry from the actual avatar.
3. Maps luminance values across an aspect-ratio corrected character ramp:
   '@%#*+=-:. '
4. Animates a digital matrix reveal:
   - Initial state: ambient falling matrix glyphs.
   - Reveal phase: scattered characters progressively resolve and lock into the
     exact image-derived avatar pixels.
   - Final state: crisp, recognizable avatar portrait with subtle edge matrix rain.
5. Exports:
   - assets/matrix-portrait.gif (animated, lightweight < 500 KB)
   - assets/matrix-portrait.png (clean static fallback)
   - assets/terminal-banner.gif (cohesive companion banner)

Reproducible, offline-first, respects source image proportions.
"""

import math
import os
import random
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# Dimensions
PORTRAIT_WIDTH = 380
PORTRAIT_HEIGHT = 280
BANNER_WIDTH = 720
BANNER_HEIGHT = 140

# Colors (Terminal Workstation / Snake Green Theme)
COLOR_BG = (11, 15, 16)               # #0b0f10
COLOR_BG_CARD = (17, 23, 26)          # #11171a
COLOR_BORDER = (35, 75, 90)           # #234b5a
COLOR_ACCENT = (85, 230, 165)         # #55e6a5 (Snake / Terminal green)
COLOR_ACCENT_BRIGHT = (140, 255, 195) # Glowing glyph
COLOR_CYAN = (102, 217, 239)          # #66d9ef
COLOR_DIM = (35, 80, 65)              # Background rain
COLOR_DIM_CYAN = (25, 60, 75)
COLOR_TEXT_MUTED = (120, 140, 145)

RAMP = " .:-=+*#%@"
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

    # Download from verified avatar endpoint for Sukhshum2628
    url = "https://avatars.githubusercontent.com/u/124433987?v=4"
    print(f"Downloading avatar source from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(source_path, "wb") as f:
        f.write(resp.read())
    return source_path

def generate_matrix_portrait():
    source_path = ensure_avatar_source()
    src_img = Image.open(source_path).convert("L")

    # Grid configuration:
    # Character cells are roughly 8x12 pixels in monospace font.
    # We want a 40 cols x 22 rows grid inside the terminal window.
    cols = 40
    rows = 22

    # Invert/threshold so the avatar's signature pattern corresponds to foreground luminance
    # In GitHub identicons: pattern = green (lum ~ 195), background = light gray (lum ~ 240)
    # Binary contrast extraction:
    im_bin = src_img.point(lambda p: 255 if p < 220 else 0)

    # Scale to grid with lanczos resampling for smooth edges
    im_grid = im_bin.resize((cols, rows), Image.Resampling.LANCZOS)

    # Calculate target character & brightness for each cell directly from avatar pixels
    cells = []
    char_w = 8.5
    char_h = 11.5
    start_x = (PORTRAIT_WIDTH - (cols * char_w)) / 2
    start_y = 28 + ((PORTRAIT_HEIGHT - 34 - (rows * char_h)) / 2)

    random.seed(1337)

    for r in range(rows):
        for c in range(cols):
            lum = im_grid.getpixel((c, r))
            # Map lum to ramp character
            ramp_idx = int((lum / 255.0) * (len(RAMP) - 1))
            target_char = RAMP[ramp_idx]
            is_pattern = lum > 100

            # Staggered reveal delay: center outward + scanline wave
            dist_center = math.sqrt(((c - cols / 2) / 1.5) ** 2 + (r - rows / 2) ** 2)
            reveal_time = r * 0.9 + dist_center * 1.1 + random.uniform(0, 3.5)

            cells.append({
                "col": c,
                "row": r,
                "x": start_x + c * char_w,
                "y": start_y + r * char_h,
                "lum": lum,
                "target_char": target_char,
                "is_pattern": is_pattern,
                "reveal_time": reveal_time
            })

    # Falling background streams
    streams = []
    for c in range(cols):
        streams.append({
            "speed": random.uniform(0.6, 1.4),
            "offset": random.uniform(0, rows),
            "length": random.randint(4, 8)
        })

    font = get_font(size=11)
    header_font = get_font(size=10)
    total_frames = 28
    frames = []

    for f in range(total_frames):
        img = Image.new("RGB", (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        # Window border and header
        draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, PORTRAIT_HEIGHT - 2)], outline=COLOR_BORDER, width=1)
        draw.rectangle([(1, 1), (PORTRAIT_WIDTH - 2, 22)], fill=COLOR_BG_CARD)

        # Terminal dot controls
        draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
        draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
        draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)

        draw.text((45, 6), "avatar.sh --reconstruct Sukhshum2628", fill=COLOR_TEXT_MUTED, font=header_font)

        progress = (f / float(total_frames - 1)) * 32.0

        for cell in cells:
            r = cell["row"]
            c = cell["col"]

            st = streams[c]
            stream_pos = (st["offset"] + f * st["speed"]) % rows
            stream_dist = (r - stream_pos) % rows

            if cell["is_pattern"]:
                if progress >= cell["reveal_time"]:
                    # Cell has resolved into actual avatar
                    char = cell["target_char"]
                    # If target_char is blank or space in ramp, render '#'
                    if char.strip() == "":
                        char = "#"

                    # Edge flash on recent reveal
                    if progress - cell["reveal_time"] < 2.5 and f < total_frames - 2:
                        color = COLOR_ACCENT_BRIGHT
                        char = random.choice(["#", "@", "%", "1"])
                    else:
                        # Fully locked avatar pixel
                        color = COLOR_ACCENT
                    draw.text((cell["x"], cell["y"]), char, fill=color, font=font)
                else:
                    # Still resolving - scattered matrix rain in place
                    char = random.choice(MATRIX_CHARS)
                    if stream_dist < st["length"]:
                        color = COLOR_ACCENT if stream_dist < 1 else COLOR_DIM
                        draw.text((cell["x"], cell["y"]), char, fill=color, font=font)
            else:
                # Outside pattern / background of avatar
                if stream_dist < st["length"]:
                    dim_factor = max(0.0, 1.0 - (stream_dist / st["length"]))
                    color = (int(COLOR_DIM[0] * dim_factor), int(COLOR_DIM[1] * dim_factor), int(COLOR_DIM[2] * dim_factor))
                    char = random.choice([".", ":", "`", " "])
                    if char != " ":
                        draw.text((cell["x"], cell["y"]), char, fill=color, font=font)

        # Footer status bar
        status_text = "[ SYNTHESIZING AVATAR LUMINANCE ]" if f < total_frames - 5 else "[ AVATAR: RECONSTRUCTED OK ]"
        status_color = COLOR_CYAN if f >= total_frames - 5 else COLOR_TEXT_MUTED
        draw.rectangle([(4, PORTRAIT_HEIGHT - 20), (PORTRAIT_WIDTH - 4, PORTRAIT_HEIGHT - 4)], fill=COLOR_BG_CARD)
        draw.text((12, PORTRAIT_HEIGHT - 18), status_text, fill=status_color, font=header_font)

        frames.append(img)

    # Save clean static fallback from final frame
    static_path = os.path.join("assets", "matrix-portrait.png")
    frames[-1].save(static_path, format="PNG")
    print(f"Generated static fallback: {static_path} ({os.path.getsize(static_path) / 1024:.1f} KB)")

    # Extend final frame pause for clean looping
    final_frames = frames + [frames[-1]] * 14
    gif_path = os.path.join("assets", "matrix-portrait.gif")
    final_frames[0].save(
        gif_path,
        save_all=True,
        append_images=final_frames[1:],
        duration=110,
        loop=0,
        optimize=True
    )
    print(f"Generated animated portrait: {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

def generate_terminal_banner():
    font = get_font(size=13)
    header_font = get_font(size=10)

    # Short, restrained sequence complementing the portrait
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

        # Window border and header
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

        # Blinking cursor when all lines displayed
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
