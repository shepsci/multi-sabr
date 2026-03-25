#!/usr/bin/env python3
"""Generate Chem-SABR benchmark logo and card images."""

import math
from PIL import Image, ImageDraw, ImageFont

# --- Color Palette (chemistry theme: green/amber hazard colors) ---
BG_DARK = "#1a1a2e"
CHEM_GREEN = "#4CAF50"
CHEM_AMBER = "#FF9800"
CHEM_RED = "#F44336"
CHEM_TEAL = "#009688"
TEXT_WHITE = "#EAEAEA"
TEXT_LIGHT = "#B0BEC5"


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 8:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_flask_symbol(draw, cx, cy, radius, color, line_width=3):
    """Draw a stylized Erlenmeyer flask / chemistry symbol."""
    r = radius
    # Flask neck (narrow top)
    neck_w = r * 0.22
    neck_top = cy - r * 0.95
    neck_bot = cy - r * 0.3
    draw.line([(cx - neck_w, neck_top), (cx - neck_w, neck_bot)], fill=color, width=line_width)
    draw.line([(cx + neck_w, neck_top), (cx + neck_w, neck_bot)], fill=color, width=line_width)
    # Neck rim
    draw.line([(cx - neck_w * 1.4, neck_top), (cx + neck_w * 1.4, neck_top)], fill=color, width=line_width)

    # Flask body (widening from neck to base)
    body_w = r * 0.75
    body_bot = cy + r * 0.7
    draw.line([(cx - neck_w, neck_bot), (cx - body_w, body_bot)], fill=color, width=line_width)
    draw.line([(cx + neck_w, neck_bot), (cx + body_w, body_bot)], fill=color, width=line_width)
    # Flat bottom
    draw.line([(cx - body_w, body_bot), (cx + body_w, body_bot)], fill=color, width=line_width)

    # Liquid level line inside flask
    liq_y = cy + r * 0.2
    liq_w_at_y = neck_w + (body_w - neck_w) * ((liq_y - neck_bot) / (body_bot - neck_bot))
    draw.line([(cx - liq_w_at_y + 3, liq_y), (cx + liq_w_at_y - 3, liq_y)], fill=color, width=max(1, line_width - 1))

    # Bubbles
    for bx, by, br in [(cx - r*0.1, cy + r*0.4, r*0.06), (cx + r*0.15, cy + r*0.3, r*0.04), (cx, cy + r*0.05, r*0.05)]:
        draw.ellipse([bx - br, by - br, bx + br, by + br], outline=color, width=max(1, line_width - 1))


def draw_hexagonal_molecule(draw, cx, cy, radius, color, line_width=2):
    """Draw a benzene ring / hexagonal molecule structure."""
    r = radius
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append((px, py))
    # Outer hexagon
    for i in range(6):
        draw.line([points[i], points[(i+1) % 6]], fill=color, width=line_width)
    # Inner circle (aromatic ring representation)
    inner_r = r * 0.55
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], outline=color, width=max(1, line_width - 1))


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


def create_logo(width=800, height=450, output_path="chem_sabr_logo.png"):
    """Create the Chem-SABR benchmark logo."""
    img = Image.new("RGBA", (width, height), hex_to_rgb(BG_DARK))
    draw_gradient_rect(img, 0, 0, width, height, "#1a1a2e", "#0f0f23")
    draw = ImageDraw.Draw(img)

    # Subtle hex grid overlay
    hex_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    hex_draw = ImageDraw.Draw(hex_overlay)
    hex_s = max(20, int(30 * width / 800))
    draw_hex_grid(hex_draw, width, height, hex_size=hex_s, color="#4CAF50")
    img = Image.alpha_composite(img, hex_overlay)
    draw = ImageDraw.Draw(img)

    sx = width / 800
    sy = height / 450

    # Glow behind flask
    flask_cx = int(160 * sx)
    flask_cy = int(200 * sy)
    flask_r = int(90 * min(sx, sy))
    draw_glow_circle(img, flask_cx, flask_cy, int(flask_r * 2.2), CHEM_GREEN, alpha_max=25)
    draw = ImageDraw.Draw(img)

    # Draw flask symbol
    draw_flask_symbol(draw, flask_cx, flask_cy, flask_r, hex_to_rgb(CHEM_AMBER), line_width=max(2, int(3 * min(sx, sy))))

    # Molecule on right side
    mol_cx = int(680 * sx)
    mol_cy = int(height / 2)
    mol_r = int(50 * min(sx, sy))
    draw_glow_circle(img, mol_cx, mol_cy, int(mol_r * 2.5), CHEM_TEAL, alpha_max=15)
    draw = ImageDraw.Draw(img)

    # Draw molecule rings stacked
    for offset_y in [-70, 0, 70]:
        draw_hexagonal_molecule(draw, mol_cx, int(mol_cy + offset_y * sy),
                                int(mol_r * 0.7), hex_to_rgb(CHEM_GREEN),
                                line_width=max(2, int(2 * min(sx, sy))))

    # Bond lines connecting rings
    for offset_y in [-35, 35]:
        y = int(mol_cy + offset_y * sy)
        draw.line([(mol_cx, y - int(10*sy)), (mol_cx, y + int(10*sy))],
                  fill=hex_to_rgb(CHEM_TEAL), width=max(1, int(2 * min(sx, sy))))

    # --- Typography ---
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(72 * min(sx, sy)))
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(22 * min(sx, sy)))
        font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(16 * min(sx, sy)))
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    title_text = "Chem-SABR"
    title_x = int(270 * sx)
    title_y = int(120 * sy)

    for offset in [(2, 2), (-1, -1), (1, 0), (0, 1)]:
        draw.text((title_x + offset[0], title_y + offset[1]), title_text,
                  fill=hex_to_rgb(CHEM_AMBER) + (60,), font=font_title)
    draw.text((title_x, title_y), title_text, fill=hex_to_rgb(CHEM_AMBER), font=font_title)

    sub_text = "Chemical Safety Selective Attention Benchmark"
    sub_x = int(272 * sx)
    sub_y = int(210 * sy)
    draw.text((sub_x, sub_y), sub_text, fill=hex_to_rgb(TEXT_LIGHT), font=font_sub)

    # Decorative line
    line_y = int(245 * sy)
    line_x1 = int(272 * sx)
    line_x2 = int(620 * sx)
    for x in range(int(line_x1), int(line_x2)):
        t = (x - line_x1) / max(1, (line_x2 - line_x1))
        c1 = hex_to_rgb(CHEM_AMBER)
        c2 = hex_to_rgb(CHEM_TEAL)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        a = int(200 * (1 - abs(2*t - 1) * 0.5))
        draw.line([(x, line_y), (x, line_y + max(1, int(2 * sy)))], fill=(r, g, b, a))

    tag_text = "AI Reasoning  |  Chemical Safety  |  Selective Attention"
    tag_x = int(272 * sx)
    tag_y = int(265 * sy)
    draw.text((tag_x, tag_y), tag_text, fill=hex_to_rgb(CHEM_GREEN) + (180,), font=font_tag)

    # Category pills
    pill_y = int(340 * sy)
    pill_h = int(28 * sy)
    pills = [
        ("Chemistry", CHEM_AMBER),
        ("Attention", CHEM_GREEN),
        ("Reasoning", CHEM_TEAL),
    ]
    pill_x = int(272 * sx)

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

    # Bottom edge accent line
    bottom_y = height - int(4 * sy)
    for x in range(width):
        t = x / width
        c1 = hex_to_rgb(CHEM_AMBER)
        c2 = hex_to_rgb(CHEM_GREEN)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(x, bottom_y), (x, height)], fill=(r, g, b, 180))

    # Top edge accent
    for x in range(width):
        t = x / width
        c1 = hex_to_rgb(CHEM_TEAL)
        c2 = hex_to_rgb(CHEM_AMBER)
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
    create_logo(800, 450, "/Users/smallmacmini/chem-sabr/writeup/chem_sabr_logo.png")
    create_logo(560, 280, "/Users/smallmacmini/chem-sabr/writeup/chem_sabr_card.png")
    print("Done!")
