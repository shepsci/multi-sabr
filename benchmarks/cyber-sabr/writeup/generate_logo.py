#!/usr/bin/env python3
"""Generate Cyber-SABR benchmark logo and card images."""

import math
from PIL import Image, ImageDraw, ImageFont

# --- Color Palette (cybersecurity theme: electric blue/red/green) ---
BG_DARK = "#1a1a2e"
CYBER_BLUE = "#00BCD4"
CYBER_RED = "#FF5252"
CYBER_GREEN = "#76FF03"
CYBER_PURPLE = "#7C4DFF"
TEXT_WHITE = "#EAEAEA"
TEXT_LIGHT = "#B0BEC5"


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 8:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_shield_symbol(draw, cx, cy, radius, color, line_width=3):
    """Draw a stylized shield / lock symbol for cybersecurity."""
    r = radius
    # Shield outline: rounded top, pointed bottom
    points = []
    # Top arc
    for angle_deg in range(180, 361):
        angle = math.radians(angle_deg)
        px = cx + r * 0.7 * math.cos(angle)
        py = cy - r * 0.3 + r * 0.5 * math.sin(angle)
        points.append((px, py))

    # Right side going down to point
    points.append((cx + r * 0.7, cy - r * 0.3))
    points.append((cx + r * 0.65, cy + r * 0.3))
    points.append((cx + r * 0.4, cy + r * 0.65))
    points.append((cx, cy + r * 0.85))

    # Left side going back up
    points.append((cx - r * 0.4, cy + r * 0.65))
    points.append((cx - r * 0.65, cy + r * 0.3))
    points.append((cx - r * 0.7, cy - r * 0.3))

    # Draw shield outline
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=line_width)
    draw.line([points[-1], points[0]], fill=color, width=line_width)

    # Lock keyhole inside shield
    lock_cy = cy + r * 0.05
    lock_r = r * 0.15
    draw.ellipse([cx - lock_r, lock_cy - lock_r, cx + lock_r, lock_cy + lock_r],
                 outline=color, width=line_width)
    # Keyhole slot
    slot_w = r * 0.06
    draw.line([(cx, lock_cy + lock_r * 0.5), (cx, lock_cy + lock_r * 2.2)],
              fill=color, width=max(2, line_width))


def draw_circuit_pattern(draw, x_start, y_start, width, height, color, line_width=2, nodes=12):
    """Draw a stylized circuit board pattern."""
    import random
    random.seed(42)  # Deterministic for reproducibility

    node_positions = []
    for _ in range(nodes):
        nx = x_start + random.random() * width
        ny = y_start + random.random() * height
        node_positions.append((nx, ny))

    # Draw connections (Manhattan-style routing)
    for i in range(len(node_positions) - 1):
        x1, y1 = node_positions[i]
        x2, y2 = node_positions[i + 1]
        mid_x = (x1 + x2) / 2
        draw.line([(x1, y1), (mid_x, y1)], fill=color, width=line_width)
        draw.line([(mid_x, y1), (mid_x, y2)], fill=color, width=line_width)
        draw.line([(mid_x, y2), (x2, y2)], fill=color, width=line_width)

    # Draw nodes
    node_r = max(3, int(4 * min(width, height) / 300))
    for nx, ny in node_positions:
        draw.ellipse([nx - node_r, ny - node_r, nx + node_r, ny + node_r],
                     fill=color, outline=color)


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


def create_logo(width=800, height=450, output_path="cyber_sabr_logo.png"):
    """Create the Cyber-SABR benchmark logo."""
    img = Image.new("RGBA", (width, height), hex_to_rgb(BG_DARK))
    draw_gradient_rect(img, 0, 0, width, height, "#1a1a2e", "#0f0f23")
    draw = ImageDraw.Draw(img)

    # Subtle hex grid overlay
    hex_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    hex_draw = ImageDraw.Draw(hex_overlay)
    hex_s = max(20, int(30 * width / 800))
    draw_hex_grid(hex_draw, width, height, hex_size=hex_s, color="#00BCD4")
    img = Image.alpha_composite(img, hex_overlay)
    draw = ImageDraw.Draw(img)

    sx = width / 800
    sy = height / 450

    # Glow behind shield
    shield_cx = int(160 * sx)
    shield_cy = int(200 * sy)
    shield_r = int(90 * min(sx, sy))
    draw_glow_circle(img, shield_cx, shield_cy, int(shield_r * 2.2), CYBER_BLUE, alpha_max=25)
    draw = ImageDraw.Draw(img)

    # Draw shield symbol
    draw_shield_symbol(draw, shield_cx, shield_cy, shield_r,
                       hex_to_rgb(CYBER_BLUE), line_width=max(2, int(3 * min(sx, sy))))

    # Circuit pattern on right side
    circuit_x = int(620 * sx)
    circuit_y = int(40 * sy)
    circuit_w = int(120 * sx)
    circuit_h = int(370 * sy)
    draw_glow_circle(img, int(circuit_x + circuit_w/2), int(height/2),
                     int(circuit_h * 0.4), CYBER_PURPLE, alpha_max=15)
    draw = ImageDraw.Draw(img)
    draw_circuit_pattern(draw, circuit_x, circuit_y, circuit_w, circuit_h,
                         hex_to_rgb(CYBER_GREEN) + (140,),
                         line_width=max(1, int(2 * min(sx, sy))))

    # --- Typography ---
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(72 * min(sx, sy)))
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(22 * min(sx, sy)))
        font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(16 * min(sx, sy)))
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    title_text = "Cyber-SABR"
    title_x = int(270 * sx)
    title_y = int(120 * sy)

    for offset in [(2, 2), (-1, -1), (1, 0), (0, 1)]:
        draw.text((title_x + offset[0], title_y + offset[1]), title_text,
                  fill=hex_to_rgb(CYBER_BLUE) + (60,), font=font_title)
    draw.text((title_x, title_y), title_text, fill=hex_to_rgb(CYBER_BLUE), font=font_title)

    sub_text = "Cybersecurity Selective Attention Benchmark"
    sub_x = int(272 * sx)
    sub_y = int(210 * sy)
    draw.text((sub_x, sub_y), sub_text, fill=hex_to_rgb(TEXT_LIGHT), font=font_sub)

    # Decorative line
    line_y = int(245 * sy)
    line_x1 = int(272 * sx)
    line_x2 = int(620 * sx)
    for x in range(int(line_x1), int(line_x2)):
        t = (x - line_x1) / max(1, (line_x2 - line_x1))
        c1 = hex_to_rgb(CYBER_BLUE)
        c2 = hex_to_rgb(CYBER_PURPLE)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        a = int(200 * (1 - abs(2*t - 1) * 0.5))
        draw.line([(x, line_y), (x, line_y + max(1, int(2 * sy)))], fill=(r, g, b, a))

    tag_text = "AI Reasoning  |  Threat Analysis  |  Selective Attention"
    tag_x = int(272 * sx)
    tag_y = int(265 * sy)
    draw.text((tag_x, tag_y), tag_text, fill=hex_to_rgb(CYBER_GREEN) + (180,), font=font_tag)

    # Category pills
    pill_y = int(340 * sy)
    pill_h = int(28 * sy)
    pills = [
        ("Security", CYBER_BLUE),
        ("Attention", CYBER_GREEN),
        ("Reasoning", CYBER_PURPLE),
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
        c1 = hex_to_rgb(CYBER_RED)
        c2 = hex_to_rgb(CYBER_BLUE)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(x, bottom_y), (x, height)], fill=(r, g, b, 180))

    # Top edge accent
    for x in range(width):
        t = x / width
        c1 = hex_to_rgb(CYBER_PURPLE)
        c2 = hex_to_rgb(CYBER_BLUE)
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
    create_logo(800, 450, "/Users/smallmacmini/cyber-sabr/writeup/cyber_sabr_logo.png")
    create_logo(560, 280, "/Users/smallmacmini/cyber-sabr/writeup/cyber_sabr_card.png")
    print("Done!")
