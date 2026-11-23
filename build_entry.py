"""Draw the news-image-20261123 entry: one 1024x1024 PNG.

Deterministic: no network, no randomness, no clock, no environment input.
Layout is a newspaper front page: navy masthead, six story cards in a
2x3 grid, navy footer with an ALSO TODAY line and a sources line.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (247, 243, 232)
NAVY = (15, 42, 68)
GOLD = (212, 160, 60)
RED = (196, 52, 40)
INK = (20, 28, 36)
BODY = (52, 62, 74)
LIGHT_BLUE = (196, 214, 232)
CARD_BORDER = (214, 206, 188)
SOURCE_GREY = (150, 170, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

STORIES = [
    (
        "MARKETS",
        "KOSPI dives over 5% intraday as Seoul vows to act",
        "South Korea's benchmark falls about 5% in Monday's tech sell-off; "
        "the finance minister says a contingency plan is ready.",
    ),
    (
        "EUROPE",
        "Kyiv region mourns as Dymer rescue goes on",
        "The Kyiv region marks a day of mourning after a drone strike "
        "collapses part of a five-storey block in Dymer; rescuers pull a "
        "79-year-old woman out alive as the search goes on.",
    ),
    (
        "DISASTER",
        "Indonesia says 24 dead in factory fire",
        "Indonesia says 24 people died in a candy factory fire in Banten; "
        "rescuers search the wreckage for about 30 still missing.",
    ),
    (
        "SECURITY",
        "NATO meets over missiles in Polish airspace",
        "NATO's council meets in Brussels after Russian missiles crossed "
        "into Poland; Warsaw seeks stronger air defences on the eastern flank.",
    ),
    (
        "DIPLOMACY",
        "Nepal PM holds talks with Modi in Delhi",
        "Balendra Shah meets Narendra Modi on his first bilateral trip "
        "abroad; the leaders launch a new Ayodhya\u2013Janakpur train.",
    ),
    (
        "POLITICS",
        "Burnham to defend 'landmark' EU deal",
        "The UK prime minister is to tell MPs the Brussels deal is a choice "
        "between 'a broken status quo or change'; opponents dispute his "
        "\u00a317bn growth claim.",
    ),
]

ALSO_ITEMS = [
    "Ganges: talks continue in Dhaka",
    "Seoul eases buyback limits",
    "Badenoch set to attack EU deal at CBI",
]

SOURCES_LINE = (
    "Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, Al Jazeera"
    "  \u2022  23 November 2026"
)


def load_font(filename, size):
    """Load a DejaVu font from the system directory, with fallbacks."""
    path = os.path.join(FONT_DIR, filename)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        pass
    try:
        return ImageFont.truetype(filename, size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap by measured width. Returns a list of lines."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_card(draw, x, y, label, title, body, title_size):
    card_w = 476
    card_h = 232
    draw.rounded_rectangle(
        [x, y, x + card_w, y + card_h],
        radius=10,
        fill=(255, 255, 255),
        outline=CARD_BORDER,
        width=2,
    )
    # Red strip across the top of the card. Drawn as a rounded rectangle
    # whose lower half is painted back to white, so the strip is 6px tall
    # with top corners rounded to match the card (a plain rectangle's
    # square corners poked outside the card outline).
    draw.rounded_rectangle([x, y, x + card_w, y + 12], radius=10, fill=RED)
    draw.rectangle([x, y + 6, x + card_w, y + 12], fill=(255, 255, 255))
    draw.rounded_rectangle(
        [x, y, x + card_w, y + card_h],
        radius=10,
        outline=CARD_BORDER,
        width=2,
    )

    label_font = load_font("DejaVuSans-Bold.ttf", 17)
    draw.text((x + 18, y + 18), label, font=label_font, fill=RED)

    text_w = card_w - 36
    title_font = load_font("DejaVuSans-Bold.ttf", title_size)
    title_lines = wrap_text(draw, title, title_font, text_w)
    if len(title_lines) > 2:
        raise ValueError("title does not fit in 2 lines: %r" % title)
    ty = y + 48
    for line in title_lines:
        draw.text((x + 18, ty), line, font=title_font, fill=INK)
        ty += 34

    # Body: shrink 20 -> 16 until it fits in 4 lines; never truncate.
    body_font = None
    body_lines = None
    for size in (20, 19, 18, 17, 16):
        font = load_font("DejaVuSans.ttf", size)
        lines = wrap_text(draw, body, font, text_w)
        if len(lines) <= 4:
            body_font = font
            body_lines = lines
            break
    if body_font is None:
        raise ValueError("body does not fit in 4 lines even at 16pt: %r" % body)
    by = ty + 8
    for line in body_lines:
        draw.text((x + 18, by), line, font=body_font, fill=BODY)
        by += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, W, 172], fill=NAVY)
    draw.rectangle([0, 172, W, 178], fill=GOLD)
    eyebrow_font = load_font("DejaVuSans-Bold.ttf", 20)
    draw.text((36, 22), "THE WORLD IN ONE IMAGE", font=eyebrow_font, fill=GOLD)
    title_font = load_font("DejaVuSerif-Bold.ttf", 84)
    draw.text((36, 48), "WORLD NEWS", font=title_font, fill=(255, 255, 255))
    date_font = load_font("DejaVuSans-Bold.ttf", 22)
    draw.text(
        (36, 138),
        "MONDAY 23 NOVEMBER 2026  \u2022  6 STORIES  \u2022  ONE DAY",
        font=date_font,
        fill=LIGHT_BLUE,
    )

    # Story cards: 2 columns x 3 rows.
    # Title target is 29pt; the longer v5 KOSPI title only fits the 2-line
    # cap at 26pt, so use the largest size (29..26) under which every title
    # fits in 2 lines, applied uniformly so all cards match.
    title_size = 26
    for size in (29, 28, 27, 26):
        font = load_font("DejaVuSans-Bold.ttf", size)
        if all(
            len(wrap_text(draw, t, font, 476 - 36)) <= 2 for _, t, _ in STORIES
        ):
            title_size = size
            break
    origin_x, origin_y = 24, 198
    card_w, card_h = 476, 232
    gap_x, gap_y = 24, 14
    for i, (label, title, body) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = origin_x + col * (card_w + gap_x)
        y = origin_y + row * (card_h + gap_y)
        draw_card(draw, x, y, label, title, body, title_size)

    # Footer.
    draw.rectangle([0, 930, W, H], fill=NAVY)
    also_head_font = load_font("DejaVuSans-Bold.ttf", 18)
    draw.text((36, 938), "ALSO TODAY", font=also_head_font, fill=GOLD)
    also_font = load_font("DejaVuSans.ttf", 16)
    also_line = "  \u2022  ".join(ALSO_ITEMS)
    if draw.textlength(also_line, font=also_font) > W - 72:
        raise ValueError("ALSO TODAY line does not fit on one line")
    draw.text((36, 964), also_line, font=also_font, fill=(255, 255, 255))
    sources_font = load_font("DejaVuSans.ttf", 15)
    draw.text((36, 994), SOURCES_LINE, font=sources_font, fill=SOURCE_GREY)

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, optimize=True)
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
