#!/usr/bin/env python3
"""
Generate a terminal-inspired Matrix character silhouette animation (GIF and static PNG)
and a terminal banner GIF simulating a profile initialization sequence.

Output files:
- assets/matrix-portrait.gif
- assets/matrix-portrait.png
- assets/terminal-banner.gif
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

# Dimensions
PORTRAIT_WIDTH = 320
PORTRAIT_HEIGHT = 320
BANNER_WIDTH = 720
BANNER_HEIGHT = 160

# Palette
COLOR_BG = (11, 15, 16)          # Near-black charcoal #0b0f10
COLOR_BG_CARD = (17, 23, 26)     # Deep terminal #11171a
COLOR_ACCENT = (85, 230, 165)    # Terminal green #55e6a5
COLOR_ACCENT_BRIGHT = (140, 255, 195) # Glowing matrix char
COLOR_CYAN = (102, 217, 239)     # Muted cyan #66d9ef
COLOR_DIM = (40, 95, 75)         # Dim matrix green
COLOR_DIM_CYAN = (35, 75, 90)    # Dim matrix cyan
COLOR_TEXT_MUTED = (120, 140, 145)

MATRIX_CHARS = ["0", "1", "/", "\\", "|", "#", "@", "%", "*", "+", ".", ":"]

def get_font(size=12):
    # Try system monospace fonts, fallback to default
    candidates = [
        "consola.ttf", "consolab.ttf", "cour.ttf", "lucon.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Monaco.ttf"
    ]
    for font_name in candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def is_inside_silhouette(x, y, w, h):
    """
    Returns True if (x, y) falls inside an abstract developer silhouette:
    - Head & hood / headset
    - Shoulders & torso
    - Terminal workstation posture
    """
    nx = (x - w / 2) / (w / 2)  # -1.0 to 1.0
    ny = (y - h / 2) / (h / 2)  # -1.0 to 1.0

    # Head / Hoodie (centered around ny = -0.32, radius ~ 0.32)
    head_cy = -0.30
    head_dist = math.sqrt((nx * 1.05) ** 2 + ((ny - head_cy) * 0.95) ** 2)
    if head_dist < 0.30:
        # Visor / glasses cut-out highlight check
        return True, "head"

    # Headset ear cups
    left_cup = math.sqrt((nx + 0.30) ** 2 + ((ny - head_cy) * 1.5) ** 2)
    right_cup = math.sqrt((nx - 0.30) ** 2 + ((ny - head_cy) * 1.5) ** 2)
    if left_cup < 0.09 or right_cup < 0.09:
        return True, "headset"

    # Headband
    if -0.33 < nx < 0.33 and -0.63 < ny < -0.55:
        return True, "headset"

    # Neck
    if abs(nx) < 0.14 and -0.05 <= ny <= 0.12:
        return True, "torso"

    # Shoulders and torso
    if ny > 0.08:
        # Trapezoid expansion from neck to shoulders
        shoulder_width = 0.18 + (ny - 0.08) * 0.85
        if abs(nx) < shoulder_width and ny < 0.85:
            # Chest terminal emblem / core
            core_dist = math.sqrt((nx * 1.4) ** 2 + ((ny - 0.42) * 1.8) ** 2)
            if core_dist < 0.14:
                return True, "core"
            return True, "torso"

    return False, "bg"

def generate_matrix_portrait():
    font = get_font(size=13)
    grid_w = 26
    grid_h = 24
    cell_w = PORTRAIT_WIDTH // grid_w
    cell_h = PORTRAIT_HEIGHT // grid_h

    random.seed(42)

    # Pre-calculate cell categories and static matrix stream data
    cells = []
    for r in range(grid_h):
        for c in range(grid_w):
            cx = c * cell_w + cell_w // 2
            cy = r * cell_h + cell_h // 2
            inside, part = is_inside_silhouette(cx, cy, PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
            cells.append({
                "col": c,
                "row": r,
                "x": c * cell_w,
                "y": r * cell_h,
                "inside": inside,
                "part": part,
                "char": random.choice(MATRIX_CHARS),
                "reveal_delay": (r * 1.8 + abs(c - grid_w // 2) * 2.2 + random.uniform(0, 8))
            })

    # Falling matrix code streams in the background
    streams = []
    for col in range(grid_w):
        streams.append({
            "speed": random.uniform(0.8, 1.8),
            "offset": random.uniform(0, grid_h),
            "length": random.randint(4, 9)
        })

    total_frames = 28
    frames = []

    for f in range(total_frames):
        img = Image.new("RGB", (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        # Draw terminal frame border
        draw.rectangle([(2, 2), (PORTRAIT_WIDTH - 3, PORTRAIT_HEIGHT - 3)], outline=COLOR_DIM_CYAN, width=1)
        # Terminal header bar
        draw.rectangle([(2, 2), (PORTRAIT_WIDTH - 3, 20)], fill=COLOR_BG_CARD)
        draw.ellipse([(8, 7), (14, 13)], fill=(230, 85, 85))
        draw.ellipse([(18, 7), (24, 13)], fill=(230, 190, 85))
        draw.ellipse([(28, 7), (34, 13)], fill=COLOR_ACCENT)
        draw.text((45, 5), "ENGINEER // AVATAR_REVEAL", fill=COLOR_TEXT_MUTED, font=get_font(size=10))

        # Render cells
        progress = (f / float(total_frames - 1)) * 40.0  # reveal curve

        for cell in cells:
            r = cell["row"]
            c = cell["col"]

            # Background stream contribution
            st = streams[c]
            stream_pos = (st["offset"] + f * st["speed"]) % grid_h
            stream_dist = (r - stream_pos) % grid_h

            char = cell["char"]
            # occasionally mutate character
            if random.random() < 0.15:
                char = random.choice(MATRIX_CHARS)

            if cell["inside"]:
                if progress >= cell["reveal_delay"]:
                    # Revealed
                    # Just revealed leading edge effect
                    if progress - cell["reveal_delay"] < 3.0 and f < total_frames - 3:
                        char_color = COLOR_ACCENT_BRIGHT
                        char = random.choice(["#", "@", "1", "%"])
                    else:
                        if cell["part"] == "core":
                            char_color = COLOR_CYAN
                            char = random.choice(["<", ">", "/", "\\", "1", "0"])
                        elif cell["part"] == "headset":
                            char_color = COLOR_CYAN
                        else:
                            # Silhouette body
                            char_color = COLOR_ACCENT
                            if random.random() < 0.08 and f < total_frames - 2:
                                char_color = COLOR_ACCENT_BRIGHT
                    draw.text((cell["x"] + 2, cell["y"] + 1), char, fill=char_color, font=font)
                else:
                    # Not yet revealed - subtle falling background matrix
                    if stream_dist < st["length"]:
                        dim_alpha = 1.0 - (stream_dist / st["length"])
                        if stream_dist < 1:
                            draw.text((cell["x"] + 2, cell["y"] + 1), char, fill=COLOR_ACCENT_BRIGHT, font=font)
                        else:
                            color = (int(COLOR_DIM[0] * dim_alpha), int(COLOR_DIM[1] * dim_alpha), int(COLOR_DIM[2] * dim_alpha))
                            draw.text((cell["x"] + 2, cell["y"] + 1), char, fill=color, font=font)
            else:
                # Outside silhouette: gentle background matrix rain
                if stream_dist < st["length"]:
                    dim_alpha = 0.85 - (stream_dist / st["length"]) * 0.7
                    if stream_dist < 1:
                        draw.text((cell["x"] + 2, cell["y"] + 1), char, fill=COLOR_ACCENT, font=font)
                    else:
                        color = (int(COLOR_DIM[0] * dim_alpha), int(COLOR_DIM[1] * dim_alpha), int(COLOR_DIM[2] * dim_alpha))
                        draw.text((cell["x"] + 2, cell["y"] + 1), char, fill=color, font=font)

        # Status badge at bottom of portrait
        status_text = "[ SYNTHESIZING ]" if f < total_frames - 5 else "[ IDENTITY: READY ]"
        status_color = COLOR_CYAN if f >= total_frames - 5 else COLOR_ACCENT
        draw.rectangle([(6, PORTRAIT_HEIGHT - 22), (PORTRAIT_WIDTH - 6, PORTRAIT_HEIGHT - 6)], fill=COLOR_BG_CARD)
        draw.text((12, PORTRAIT_HEIGHT - 20), status_text, fill=status_color, font=get_font(size=10))

        frames.append(img)

    # Save static fallback (final clean frame)
    static_img = frames[-1]
    static_path = os.path.join("assets", "matrix-portrait.png")
    static_img.save(static_path, format="PNG")

    # Add pauses on the final completed frame so the reconstructed silhouette lingers
    final_frames = frames + [frames[-1]] * 14

    # Convert to P-mode with global web-safe palette to keep file size under 1MB
    gif_path = os.path.join("assets", "matrix-portrait.gif")
    final_frames[0].save(
        gif_path,
        save_all=True,
        append_images=final_frames[1:],
        duration=110,
        loop=0,
        optimize=True
    )
    print(f"Generated {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")
    print(f"Generated {static_path} ({os.path.getsize(static_path) / 1024:.1f} KB)")

def generate_terminal_banner():
    """Generates an animated terminal initialization banner."""
    font = get_font(size=13)
    font_bold = get_font(size=13)
    header_font = get_font(size=11)

    lines = [
        ("$ ./initialize-profile.sh --target=Sukhshum2628", COLOR_CYAN, 0),
        ("[ OK ] Loading developer identity: Sukhshum Vaishnavi", COLOR_ACCENT, 8),
        ("[ OK ] Mounting engineering modules: Distributed Systems / AI / Net", COLOR_ACCENT, 16),
        ("[ OK ] Initializing project registry: STALKER-MP [FLAGSHIP]", COLOR_ACCENT, 24),
        ("[ OK ] Workstation ready. Host authority active. Determinism locked.", COLOR_ACCENT_BRIGHT, 32),
    ]

    total_frames = 46
    frames = []

    for f in range(total_frames):
        img = Image.new("RGB", (BANNER_WIDTH, BANNER_HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        # Border
        draw.rectangle([(1, 1), (BANNER_WIDTH - 2, BANNER_HEIGHT - 2)], outline=COLOR_DIM_CYAN, width=1)
        # Header bar
        draw.rectangle([(1, 1), (BANNER_WIDTH - 2, 22)], fill=COLOR_BG_CARD)
        draw.ellipse([(8, 8), (14, 14)], fill=(230, 85, 85))
        draw.ellipse([(18, 8), (24, 14)], fill=(230, 190, 85))
        draw.ellipse([(28, 8), (34, 14)], fill=COLOR_ACCENT)
        draw.text((45, 6), "bash - 80x24 (sukhshum@workstation:~)", fill=COLOR_TEXT_MUTED, font=header_font)

        y = 32
        for line_text, color, appear_frame in lines:
            if f >= appear_frame:
                # Typewriter effect for current line
                chars_visible = min(len(line_text), int((f - appear_frame) * 4) + 1)
                text_slice = line_text[:chars_visible]

                # Highlight bracket tags
                if text_slice.startswith("[ OK ]"):
                    draw.text((16, y), "[ OK ]", fill=COLOR_ACCENT_BRIGHT, font=font_bold)
                    draw.text((64, y), text_slice[6:], fill=color, font=font)
                else:
                    draw.text((16, y), text_slice, fill=color, font=font)

                # Cursor on active line
                if chars_visible < len(line_text) or (f - appear_frame < 6 and f == appear_frame + 1):
                    cursor_x = 16 + (chars_visible * 8)
                    draw.rectangle([(cursor_x, y + 2), (cursor_x + 7, y + 15)], fill=COLOR_ACCENT)

                y += 24

        # Blinking cursor at the end after all lines
        if f >= 38 and (f // 3) % 2 == 0:
            draw.rectangle([(16, y + 2), (24, y + 15)], fill=COLOR_ACCENT)

        frames.append(img)

    # Pause on finished state
    final_frames = frames + [frames[-1]] * 18

    gif_path = os.path.join("assets", "terminal-banner.gif")
    final_frames[0].save(
        gif_path,
        save_all=True,
        append_images=final_frames[1:],
        duration=100,
        loop=0,
        optimize=True
    )
    print(f"Generated {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_matrix_portrait()
    generate_terminal_banner()

