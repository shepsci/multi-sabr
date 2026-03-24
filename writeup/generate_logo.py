#!/usr/bin/env python3
"""Generate Multi-SABR benchmark logo and card images."""

import math
from PIL import Image, ImageDraw, ImageFont

# --- Color Palette (multi-domain: uses colors from all variants) ---
BG_DARK = "#1a1a2e"
SABR_BLUE = "#5B86E5"       # SABR (general)
BIO_YELLOW = "#F5A623"      # Bio-SABR
CHEM_GREEN = "#4CAF50"      # Chem-SABR
CYBER_CYAN = "#00BCD4"      # Cyber-SABR
TEXT_WHITE = "#EAEAEA"
TEXT_LIGHT = "#B0BEC5"
ACCENT_PURPLE = "#7C4DFF"


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 8:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_four_circles(draw, cx, cy, radius, colors, line_width=3):
    """Draw four overlapping circles representing the 4 SABR domains."""
    offsets = [
        (-0.35, -0.35),  # top-left: SABR
        (0.35, -0.35),   # top-right: Bio
        (-0.35, 0.35),   # bottom-left: Chem
        (0.35, 0.35),    # bottom-right: Cyber
    ]
    circle_r = radius * 0.55
    for (ox, oy), color in zip(offsets, colors):
        x = cx + ox * radius
        y = cy + oy * radius
        c = hex_to_rgb(color) if isinstance(color, str) else color
        draw.ellipse([x - circle_r, y - circle_r, x + circle_r, y + circle_r],
                     outline=c, width=line_width)


def draw_hex_grid(draw, width, height, hex_size=30, color="#ffffff08"):
    col = hex_to_rgb(color) if isinstance(color, str) and color.startswith("#") else color
    if len(col) == 3:
        col = col + (12,)
    h = hex_size
    w = math.sqrt(3) * h
    for row in range(-1, int(height / (h * 1.5)) + 2):
        for c in range(-1, int(width / w) + 2):
            cx = c * w + (w / 2 if row % 2 else 0)
            cy = row * h * 1.5
            points = []
            for i in range(6):
                angle = math.radians(60 * i + 30)
                px = cx + h * 0.9 * math.cos(angle)
                py = cy + h * 0.9 * math.sin(angle)
                points.append((px, py))
            if len(points) >= 3:
                draw.polygon(points, outline=col)


def draw_gradient_rect(img, x1, y1, x2, y2, color1, color2, vertical=True):
    draw = ImageDraw.Draw(img)
    c1 = hex_to_rgb(color1) if isinstance(color1, str) else color1
    c2 = hex_to_rgb(color2) if isinstance(color2, str) else color2
    if vertical:
        for y in range(int(y1), int(y2)):
            t = (y - y1) / max(1, (y2 - y1))
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            draw.line([(x1, y), (x2, y)], fill=(r, g, b))


def draw_glow_circle(img, cx, cy, radius, color, alpha_max=40):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    c = hex_to_rgb(color) if isinstance(color, str) else color
    for r in range(int(radius), 0, -2):
        t = r / radius
        a = int(alpha_max * (1 - t))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(c[0], c[1], c[2], a))
    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0, 0, 0, 0)), overlay), (0, 0), overlay)


def draw_domain_bar(draw, x, y, width, height, colors, labels, font):
    """Draw a horizontal bar with 4 colored segments representing domains."""
    seg_w = width / len(colors)
    for i, (color, label) in enumerate(zip(colors, labels)):
        c = hex_to_rgb(color) if isinstance(color, str) else color
        sx = x + i * seg_w
        draw.rounded_rectangle(
            [sx + 2, y, sx + seg_w - 2, y + height],
            radius=int(height / 2),
            fill=c + (35,), outline=c + (120,), width=1
        )
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((sx + (seg_w - tw) / 2, y + 4), label,
                  fill=c + (220,), font=font)


def create_logo(width=800, height=450, output_path="multi_sabr_logo.png"):
    """Create the Multi-SABR benchmark logo."""
    img = Image.new("RGBA", (width, height), hex_to_rgb(BG_DARK))
    draw_gradient_rect(img, 0, 0, width, height, "#1a1a2e", "#0f0f23")
    draw = ImageDraw.Draw(img)

    # Subtle hex grid
    hex_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    hex_draw = ImageDraw.Draw(hex_overlay)
    hex_s = max(20, int(30 * width / 800))
    draw_hex_grid(hex_draw, width, height, hex_size=hex_s, color="#7C4DFF")
    img = Image.alpha_composite(img, hex_overlay)
    draw = ImageDraw.Draw(img)

    sx = width / 800
    sy = height / 450

    # Four overlapping circles (Venn-like) for 4 domains
    venn_cx = int(160 * sx)
    venn_cy = int(200 * sy)
    venn_r = int(95 * min(sx, sy))
    draw_glow_circle(img, venn_cx, venn_cy, int(venn_r * 2.0), ACCENT_PURPLE, alpha_max=20)
    draw = ImageDraw.Draw(img)
    draw_four_circles(draw, venn_cx, venn_cy, venn_r,
                      [SABR_BLUE, BIO_YELLOW, CHEM_GREEN, CYBER_CYAN],
                      line_width=max(2, int(3 * min(sx, sy))))

    # "4x" badge in center of circles
    try:
        font_badge = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(20 * min(sx, sy)))
    except Exception:
        font_badge = ImageFont.load_default()
    badge_text = "4x"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    draw.text((venn_cx - bw/2, venn_cy - bh/2), badge_text,
              fill=hex_to_rgb(TEXT_WHITE), font=font_badge)

    # Right side: stacked domain indicators
    right_x = int(640 * sx)
    domain_colors = [SABR_BLUE, BIO_YELLOW, CHEM_GREEN, CYBER_CYAN]
    domain_labels = ["SABR", "Bio", "Chem", "Cyber"]
    bar_h = int(18 * sy)
    bar_w = int(100 * sx)

    try:
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", max(8, int(12 * min(sx, sy))))
    except Exception:
        font_small = ImageFont.load_default()

    for i, (color, label) in enumerate(zip(domain_colors, domain_labels)):
        c = hex_to_rgb(color)
        by = int((100 + i * 70) * sy)
        # Colored line
        draw.rounded_rectangle(
            [right_x, by, right_x + bar_w, by + bar_h],
            radius=int(bar_h / 2),
            fill=c + (50,), outline=c + (140,), width=1
        )
        bbox = draw.textbbox((0, 0), label, font=font_small)
        tw = bbox[2] - bbox[0]
        draw.text((right_x + (bar_w - tw) / 2, by + 2), label,
                  fill=c + (220,), font=font_small)
        # "280" count
        count_text = "280"
        draw.text((right_x + bar_w + int(8 * sx), by + 1), count_text,
                  fill=hex_to_rgb(TEXT_LIGHT) + (160,), font=font_small)

    # --- Typography ---
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(68 * min(sx, sy)))
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(20 * min(sx, sy)))
        font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(16 * min(sx, sy)))
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    title_text = "Multi-SABR"
    title_x = int(270 * sx)
    title_y = int(105 * sy)

    for offset in [(2, 2), (-1, -1), (1, 0), (0, 1)]:
        draw.text((title_x + offset[0], title_y + offset[1]), title_text,
                  fill=hex_to_rgb(ACCENT_PURPLE) + (60,), font=font_title)
    draw.text((title_x, title_y), title_text, fill=hex_to_rgb(TEXT_WHITE), font=font_title)

    sub_text = "Cross-Domain Selective Attention Benchmark"
    sub_x = int(272 * sx)
    sub_y = int(195 * sy)
    draw.text((sub_x, sub_y), sub_text, fill=hex_to_rgb(TEXT_LIGHT), font=font_sub)

    # Stats line
    stats_text = "1,120 evaluations  |  4 domains  |  520 unique items"
    stats_x = int(272 * sx)
    stats_y = int(230 * sy)
    draw.text((stats_x, stats_y), stats_text,
              fill=hex_to_rgb(ACCENT_PURPLE) + (180,), font=font_tag)

    # Decorative line
    line_y = int(260 * sy)
    line_x1 = int(272 * sx)
    line_x2 = int(600 * sx)
    for x in range(int(line_x1), int(line_x2)):
        t = (x - line_x1) / max(1, (line_x2 - line_x1))
        # Four-color gradient
        if t < 0.25:
            t2 = t / 0.25
            c1 = hex_to_rgb(SABR_BLUE)
            c2 = hex_to_rgb(BIO_YELLOW)
        elif t < 0.5:
            t2 = (t - 0.25) / 0.25
            c1 = hex_to_rgb(BIO_YELLOW)
            c2 = hex_to_rgb(CHEM_GREEN)
        elif t < 0.75:
            t2 = (t - 0.5) / 0.25
            c1 = hex_to_rgb(CHEM_GREEN)
            c2 = hex_to_rgb(CYBER_CYAN)
        else:
            t2 = (t - 0.75) / 0.25
            c1 = hex_to_rgb(CYBER_CYAN)
            c2 = hex_to_rgb(ACCENT_PURPLE)
        r = int(c1[0] + (c2[0] - c1[0]) * t2)
        g = int(c1[1] + (c2[1] - c1[1]) * t2)
        b = int(c1[2] + (c2[2] - c1[2]) * t2)
        draw.line([(x, line_y), (x, line_y + max(1, int(2 * sy)))], fill=(r, g, b, 200))

    # Category pills
    pill_y = int(340 * sy)
    pill_h = int(28 * sy)
    pills = [
        ("General", SABR_BLUE),
        ("Biosafety", BIO_YELLOW),
        ("Chemistry", CHEM_GREEN),
        ("Cyber", CYBER_CYAN),
    ]
    pill_x = int(160 * sx)

    try:
        font_pill = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(13 * min(sx, sy)))
    except Exception:
        font_pill = font_tag

    for label, color in pills:
        c = hex_to_rgb(color)
        bbox = draw.textbbox((0, 0), label, font=font_pill)
        tw = bbox[2] - bbox[0]
        pill_w = tw + int(20 * sx)
        pill_shape = [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h]
        draw.rounded_rectangle(pill_shape, radius=int(pill_h / 2),
                               fill=c + (35,), outline=c + (120,), width=1)
        draw.text((pill_x + int(10 * sx), pill_y + int(5 * sy)), label,
                  fill=c + (220,), font=font_pill)
        pill_x += pill_w + int(12 * sx)

    # Bottom edge: four-color accent
    bottom_y = height - int(4 * sy)
    for x in range(width):
        t = x / width
        if t < 0.25:
            c = hex_to_rgb(SABR_BLUE)
        elif t < 0.5:
            c = hex_to_rgb(BIO_YELLOW)
        elif t < 0.75:
            c = hex_to_rgb(CHEM_GREEN)
        else:
            c = hex_to_rgb(CYBER_CYAN)
        draw.line([(x, bottom_y), (x, height)], fill=c + (180,))

    # Top edge
    for x in range(width):
        t = x / width
        c1 = hex_to_rgb(ACCENT_PURPLE)
        c2 = hex_to_rgb(SABR_BLUE)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(x, 0), (x, int(2 * sy))], fill=(r, g, b, 120))

    final = Image.new("RGB", (width, height), hex_to_rgb(BG_DARK))
    final.paste(img, (0, 0), img)
    final.save(output_path, "PNG", quality=95)
    print(f"Saved {output_path} ({width}x{height})")
    return output_path


if __name__ == "__main__":
    create_logo(800, 450, "/tmp/multi-sabr/writeup/multi_sabr_logo.png")
    create_logo(560, 280, "/tmp/multi-sabr/writeup/multi_sabr_card.png")
    print("Done!")
