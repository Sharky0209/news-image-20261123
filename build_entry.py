"""Draw the 23 November 2026 world-news image (1024x1024 PNG).

Deterministic: no network, no randomness, no clock, no environment
input. All six stories were verified as Monday 23 November events or
first reports before this file was written. Run: python3 build_entry.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
PAPER = (247, 243, 232)
NAVY = (15, 42, 68)
GOLD = (212, 160, 60)
PALE_BLUE = (196, 214, 232)
RED = (196, 52, 40)
INK = (20, 28, 36)
BODY = (52, 62, 74)
CARD_BORDER = (214, 206, 188)
FOOTER_NOTE = (150, 170, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    """Load a DejaVu font from the system directory, then by name."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        pass
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Greedy word wrap, measuring each candidate line for real."""
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


def fit_body(draw, text, max_width, max_lines=4):
    """Shrink the body font (20 -> 16) until it fits in max_lines."""
    for size in (20, 19, 18, 17, 16):
        font = load_font("DejaVuSans.ttf", size)
        lines = wrap(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
    raise RuntimeError("body text does not fit in %d lines: %r" % (max_lines, text))


STORIES = [
    (
        "MARKETS",
        "KOSPI dives 5% as Seoul vows to act",
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
        "Indonesia confirms 24 dead in factory fire",
        "Indonesia confirms 24 people died in a candy factory fire in "
        "Banten; rescuers search the wreckage for about 30 still missing.",
    ),
    (
        "SECURITY",
        "NATO meets over missiles in Polish airspace",
        "NATO's council meets in Brussels after Russian missiles and a "
        "drone crossed into Poland; Warsaw seeks stronger air defences "
        "on the eastern flank.",
    ),
    (
        "DIPLOMACY",
        "Nepal PM holds talks with Modi in Delhi",
        "Balendra Shah meets Narendra Modi on his first bilateral trip "
        "abroad; the leaders launch a new Ayodhya\u2013Janakpur train.",
    ),
    (
        "POLITICS",
        "Burnham defends 'landmark' EU deal",
        "The UK prime minister tells MPs the Brussels deal is a choice "
        "between 'a broken status quo or change'; opponents dispute his "
        "\u00a317bn growth claim.",
    ),
]

ALSO = [
    "Ganges: talks continue in Dhaka",
    "Seoul eases buyback limits",
    "Badenoch to attack EU deal at CBI",
]


def draw_card(draw, x, y, label, title, body_text):
    w, h = 476, 232
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill="white", outline=CARD_BORDER, width=2)
    # Top red band, 6 px high, with rounded top corners: draw a 12 px
    # tall rounded red block, then cover its lower half with card white
    # so only the top 6 px stay red (single cover rect, no inset step).
    draw.rounded_rectangle([x, y, x + w, y + 12], radius=10, fill=RED)
    draw.rectangle([x, y + 6, x + w, y + 12], fill="white")
    # Re-draw the card outline so the band sits inside the border.
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           outline=CARD_BORDER, width=2)

    label_font = load_font("DejaVuSans-Bold.ttf", 17)
    draw.text((x + 18, y + 18), label, font=label_font, fill=RED)

    title_font = load_font("DejaVuSans-Bold.ttf", 29)
    text_w = w - 36
    title_lines = wrap(draw, title, title_font, text_w)
    assert len(title_lines) <= 2, "title over 2 lines: %r" % title
    ty = y + 48
    for line in title_lines:
        draw.text((x + 18, ty), line, font=title_font, fill=INK)
        ty += 34

    body_font, body_lines = fit_body(draw, body_text, text_w)
    assert len(body_lines) <= 4, "body over 4 lines: %r" % body_text
    by = ty + 8
    for line in body_lines:
        draw.text((x + 18, by), line, font=body_font, fill=BODY)
        by += 27


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # Header.
    draw.rectangle([0, 0, WIDTH, 172], fill=NAVY)
    draw.rectangle([0, 172, WIDTH, 178], fill=GOLD)
    draw.text((36, 22), "THE WORLD IN ONE IMAGE",
              font=load_font("DejaVuSans-Bold.ttf", 20), fill=GOLD)
    draw.text((36, 48), "WORLD NEWS",
              font=load_font("DejaVuSerif-Bold.ttf", 84), fill="white")
    draw.text((36, 138), "MONDAY 23 NOVEMBER 2026  \u2022  6 STORIES  \u2022  ONE DAY",
              font=load_font("DejaVuSans-Bold.ttf", 22), fill=PALE_BLUE)

    # Story cards: 2 columns x 3 rows.
    for i, (label, title, body_text) in enumerate(STORIES):
        x = 24 + (i % 2) * (476 + 24)
        y = 198 + (i // 2) * (232 + 14)
        draw_card(draw, x, y, label, title, body_text)

    # Footer.
    draw.rectangle([0, 930, WIDTH, HEIGHT], fill=NAVY)
    draw.text((36, 938), "ALSO TODAY",
              font=load_font("DejaVuSans-Bold.ttf", 18), fill=GOLD)
    also_font = load_font("DejaVuSans.ttf", 16)
    also_line = "  \u2022  ".join(ALSO)
    assert draw.textlength(also_line, font=also_font) <= WIDTH - 72, \
        "ALSO line overflows one line"
    draw.text((36, 964), also_line, font=also_font, fill="white")
    draw.text((36, 994),
              "Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, "
              "Al Jazeera  \u2022  23 November 2026",
              font=load_font("DejaVuSans.ttf", 15), fill=FOOTER_NOTE)

    os.makedirs("/output", exist_ok=True)
    out = "/output/entry.png"
    img.save(out, optimize=True)
    print(out)


if __name__ == "__main__":
    main()
