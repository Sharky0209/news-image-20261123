"""Build the news-image-20261123 entry: one 1024x1024 PNG.

Deterministic: no network, no randomness, no clock, no environment
input. Draws six verified stories for Monday 23 November 2026 plus an
"Also today" footer, using Pillow and the DejaVu fonts.
"""

import os

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
NAVY = (15, 42, 68)
GOLD = (212, 160, 60)
LIGHT_BLUE = (196, 214, 232)
RED = (196, 52, 40)
INK = (20, 28, 36)
BODY = (52, 62, 74)
CARD_EDGE = (214, 206, 188)
SOURCE_GREY = (150, 170, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

STORIES = [
    (
        "CLIMATE",
        "COP31 talks collapse with no deal",
        "UN climate talks in Antalya end with no deal after record "
        "overtime; fossil-fuel language is blocked and the EU rejects "
        "the final draft.",
    ),
    (
        "POLITICS",
        "Democrats clinch House majority",
        "Democrats win at least 258 House seats, their largest "
        "majority since 1992, after a North Carolina win; four races "
        "are still uncalled.",
    ),
    (
        "MIDDLE EAST",
        "Trump 'inclined' to resume Iran strikes",
        "Trump tells Fox News he is inclined to resume strikes after "
        "the New Year if no deal is reached, as talks with Tehran stall.",
    ),
    (
        "EUROPE",
        "Russian strikes hit Kyiv region",
        "An overnight drone strike collapses part of a five-storey "
        "block in Dymer as rescuers search the rubble; the region "
        "marks a day of mourning.",
    ),
    (
        "MARKETS",
        "US seeks answers on Nvidia chip sales",
        "Treasury chief Bessent says the US wants answers on Nvidia's "
        "chip sales to China and who ran compliance, after its ex-CEO "
        "resigned.",
    ),
    (
        "DISASTER",
        "24 body bags found after factory fire",
        "Rescuers recover remains in 24 body bags from a candy "
        "factory fire in Banten, Indonesia; the toll is unclear as "
        "the search resumes Monday.",
    ),
]

ALSO = [
    "Libya: drones hit Russian warship",
    "Delta delays 1,000+ Atlanta flights",
    "Alcaraz wins first ATP Finals title",
]


def load_font(name, size):
    """Load a DejaVu font from the system dir, falling back gracefully."""
    path = os.path.join(FONT_DIR, name)
    if os.path.isfile(path):
        return ImageFont.truetype(path, size)
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Greedy word wrap by measured width; returns a list of lines."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if draw.textlength(trial, font=font) <= max_width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def fit_text(draw, text, font_name, start_size, min_size, max_width, max_lines):
    """Shrink the font until the text fits in max_lines; never truncate."""
    size = start_size
    while size >= min_size:
        font = load_font(font_name, size)
        lines = wrap(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 1
    raise RuntimeError("text does not fit in %d lines even at %dpt: %r"
                       % (max_lines, min_size, text))


def draw_card(draw, base, x, y, label, title, body_text):
    card_w, card_h = 476, 232
    # Card background + red top band on a tile, clipped to rounded corners.
    tile = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=10,
                         fill=(255, 255, 255, 255),
                         outline=CARD_EDGE + (255,), width=2)
    # Red band flush with the card's top edge (visual check: the inset
    # band left a pale strip above it); the rounded mask clips the corners.
    td.rectangle([0, 0, card_w - 1, 5], fill=RED + (255,))
    mask = Image.new("L", (card_w, card_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, card_w - 1, card_h - 1], radius=10, fill=255)
    base.paste(tile, (x, y), mask)

    inner_w = card_w - 36
    label_font = load_font("DejaVuSans-Bold.ttf", 17)
    draw.text((x + 18, y + 18), label, font=label_font, fill=RED)

    title_font, title_lines = fit_text(
        draw, title, "DejaVuSans-Bold.ttf", 29, 24, inner_w, 2)
    ty = y + 48
    for line in title_lines:
        draw.text((x + 18, ty), line, font=title_font, fill=INK)
        ty += 34

    body_font, body_lines = fit_text(
        draw, body_text, "DejaVuSans.ttf", 20, 16, inner_w, 4)
    by = ty + 8
    for line in body_lines:
        draw.text((x + 18, by), line, font=body_font, fill=BODY)
        by += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Header.
    draw.rectangle([0, 0, W - 1, 171], fill=NAVY)
    draw.rectangle([0, 172, W - 1, 177], fill=GOLD)
    draw.text((36, 22), "THE WORLD IN ONE IMAGE",
              font=load_font("DejaVuSans-Bold.ttf", 20), fill=GOLD)
    draw.text((36, 48), "WORLD NEWS",
              font=load_font("DejaVuSerif-Bold.ttf", 84), fill=(255, 255, 255))
    draw.text((36, 138),
              "MONDAY 23 NOVEMBER 2026  \u2022  6 STORIES  \u2022  ONE DAY",
              font=load_font("DejaVuSans-Bold.ttf", 22), fill=LIGHT_BLUE)

    # News grid: 2 columns x 3 rows.
    gx, gy = 24, 198
    for i, (label, title, body_text) in enumerate(STORIES):
        cx = gx + (i % 2) * (476 + 24)
        cy = gy + (i // 2) * (232 + 14)
        draw_card(draw, img, cx, cy, label, title, body_text)

    # Footer.
    draw.rectangle([0, 930, W - 1, H - 1], fill=NAVY)
    draw.text((36, 938), "ALSO TODAY",
              font=load_font("DejaVuSans-Bold.ttf", 18), fill=GOLD)
    also_text = "  \u2022  ".join(ALSO)
    also_font = load_font("DejaVuSans.ttf", 16)
    assert draw.textlength(also_text, font=also_font) <= W - 72, \
        "ALSO line does not fit on one line"
    draw.text((36, 964), also_text, font=also_font, fill=(255, 255, 255))
    draw.text((36, 994),
              "Sources: CNN, Reuters, AP, Xinhua, SCMP, Al Jazeera  "
              "\u2022  23 November 2026",
              font=load_font("DejaVuSans.ttf", 15), fill=SOURCE_GREY)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img.save(OUTPUT_PATH, optimize=True)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
