"""Draw the 23 November 2026 world-news image (1024x1024 PNG).

Deterministic: no network, no randomness, no clock, no environment input.
Run: python3 build_entry.py  ->  writes /output/entry.png
"""

import os

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

PAPER = (247, 243, 232)
NAVY = (15, 42, 68)
GOLD = (212, 160, 60)
LIGHT_BLUE = (196, 214, 232)
RED = (196, 52, 40)
INK = (20, 28, 36)
BODY = (52, 62, 74)
CARD_BORDER = (214, 206, 188)
FOOTER_GREY = (150, 170, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    """Load a DejaVu font from the system directory, then by name."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            return ImageFont.load_default(size=size)


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
        "Indonesia adviser says 24 dead in factory fire",
        "Presidential adviser Said Iqbal puts the toll at 24; rescuers "
        "continue searching the wreckage for missing workers.",
    ),
    (
        "SECURITY",
        "Kim says North Korea seeks security, not supremacy",
        "Kim Jong-un tells foreign envoys Pyongyang seeks neither hegemony "
        "nor expansion and defends its arms build-up as self-defence, in "
        "remarks reported by state media on Monday.",
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
    "Seoul to ease buyback limits",
    "Badenoch set to attack EU deal at CBI",
]


def draw_card(draw, x, y, label, title, body_text):
    w, h = 476, 232
    # White card with rounded corners and a thin border.
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=(255, 255, 255), outline=CARD_BORDER, width=2)
    # Red band, 6 px high. Visual check of the first render showed the
    # rounded-band trick left tiny white notches at the card's top
    # corners, so draw it as a straight band inset inside the border
    # instead: clean ends, no corner artefacts.
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 8], fill=RED)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           outline=CARD_BORDER, width=2)

    label_font = load_font("DejaVuSans-Bold.ttf", 17)
    draw.text((x + 18, y + 18), label, font=label_font, fill=RED)

    # Title: DejaVuSans-Bold 26, adaptive down if it needs more than 2 lines.
    text_w = w - 36
    title_size = 26
    while title_size > 18:
        title_font = load_font("DejaVuSans-Bold.ttf", title_size)
        title_lines = wrap(draw, title, title_font, text_w)
        if len(title_lines) <= 2:
            break
        title_size -= 1
    title_font = load_font("DejaVuSans-Bold.ttf", title_size)
    title_lines = wrap(draw, title, title_font, text_w)
    assert len(title_lines) <= 2, "title needs more than 2 lines: %r" % title
    title_y = y + 48
    for i, line in enumerate(title_lines):
        draw.text((x + 18, title_y + i * 34), line, font=title_font, fill=INK)

    # Body: P2 fix -- start 6 px (not 8) below the title block and use a
    # 26 px line height (not 27), so the last line keeps clear space
    # above the bottom edge of the card.
    title_block = len(title_lines) * 34
    body_y = title_y + title_block + 6
    body_size = 20
    while body_size >= 16:
        body_font = load_font("DejaVuSans.ttf", body_size)
        body_lines = wrap(draw, body_text, body_font, text_w)
        if len(body_lines) <= 4:
            break
        body_size -= 1
    body_font = load_font("DejaVuSans.ttf", body_size)
    body_lines = wrap(draw, body_text, body_font, text_w)
    assert len(body_lines) <= 4, "body needs more than 4 lines: %r" % body_text
    for i, line in enumerate(body_lines):
        draw.text((x + 18, body_y + i * 26), line, font=body_font, fill=BODY)


def main():
    img = Image.new("RGB", (1024, 1024), PAPER)
    draw = ImageDraw.Draw(img)

    # Top bar.
    draw.rectangle([0, 0, 1024, 172], fill=NAVY)
    draw.rectangle([0, 172, 1024, 178], fill=GOLD)
    draw.text((36, 22), "THE WORLD IN ONE IMAGE",
              font=load_font("DejaVuSans-Bold.ttf", 20), fill=GOLD)
    draw.text((36, 48), "WORLD NEWS",
              font=load_font("DejaVuSerif-Bold.ttf", 84), fill=(255, 255, 255))
    draw.text((36, 138), "MONDAY 23 NOVEMBER 2026  \u2022  6 STORIES  \u2022  ONE DAY",
              font=load_font("DejaVuSans-Bold.ttf", 22), fill=LIGHT_BLUE)

    # News grid: 2 columns x 3 rows, cards 476x232, gaps 24 / 14.
    for idx, (label, title, body_text) in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        x = 24 + col * (476 + 24)
        y = 198 + row * (232 + 14)
        draw_card(draw, x, y, label, title, body_text)

    # Footer.
    draw.rectangle([0, 930, 1024, 1024], fill=NAVY)
    draw.text((36, 938), "ALSO TODAY",
              font=load_font("DejaVuSans-Bold.ttf", 18), fill=GOLD)
    also_text = "  \u2022  ".join(ALSO_ITEMS)
    also_font = load_font("DejaVuSans.ttf", 16)
    also_width = draw.textlength(also_text, font=also_font)
    assert also_width <= 1024 - 72, "ALSO line too wide: %d px" % also_width
    draw.text((36, 964), also_text, font=also_font, fill=(255, 255, 255))
    draw.text((36, 994),
              "Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, "
              "Al Jazeera  \u2022  23 November 2026",
              font=load_font("DejaVuSans.ttf", 15), fill=FOOTER_GREY)

    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT_PATH, optimize=True)
    print(OUT_PATH)


if __name__ == "__main__":
    main()
