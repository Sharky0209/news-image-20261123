"""Build entry.png for make.fun news-image-20261123 (v7).

At-a-glance redesign: one dominant KOSPI lead story with a drawn
intraday chart, three medium secondary stories, and a compact bottom
strip (diplomacy + politics, ALSO line, sources line).

Deterministic: fixed strings, fixed geometry, no clock, no randomness,
no network, no environment input. Two runs produce byte-identical PNGs.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = 1024
H = 1024

PAPER = (247, 243, 232)
NAVY = (15, 42, 68)
GOLD = (212, 160, 60)
WHITE = (255, 255, 255)
INK = (40, 52, 64)
MUTED = (100, 110, 120)
OUTLINE = (165, 175, 185)
GRID = (215, 218, 222)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def text_w(fnt, text):
    return fnt.getlength(text)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines, each <= max_w."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if text_w(fnt, trial) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def wrap_first_narrow(text, fnt, first_w, rest_w):
    """Wrap where the first line is narrower (a bold label precedes it)."""
    words = text.split(" ")
    lines = []
    cur = ""
    limit = first_w
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(fnt, trial) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            limit = rest_w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def label(draw, x, y, text, size=20):
    """Gold square + navy bold label. Returns bottom y."""
    draw.rectangle([x, y + 2, x + 13, y + 15], fill=GOLD)
    fnt = font(True, size)
    draw.text((x + 22, y), text, font=fnt, fill=NAVY)
    return y + size + 6


def card(draw, x0, y0, x1, y1, gold_h=6):
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=OUTLINE, width=1)
    draw.rectangle([x0, y0, x1, y0 + gold_h], fill=GOLD)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.rectangle([0, 96, W, 102], fill=GOLD)
    d.text((36, 14), "SUM UP THE DAY — IN ONE IMAGE",
           font=font(True, 18), fill=GOLD)
    d.text((36, 36), "WORLD NEWS", font=font(True, 46), fill=WHITE)
    f_monday = font(True, 20)
    d.text((988 - text_w(f_monday, "MONDAY"), 14), "MONDAY",
           font=f_monday, fill=GOLD)
    f_date = font(True, 30)
    d.text((988 - text_w(f_date, "23 NOVEMBER 2026"), 42),
           "23 NOVEMBER 2026", font=f_date, fill=WHITE)

    # ---- Lead story: MARKETS / KOSPI ------------------------------------
    LX0, LY0, LX1, LY1 = 36, 112, 988, 404
    card(d, LX0, LY0, LX1, LY1, gold_h=8)
    y = label(d, 64, 134, "MARKETS — LEAD STORY", size=21)
    # Headline, two fixed lines, biggest type on the page.
    f_head = font(True, 44)
    d.text((64, y + 6), "KOSPI dives 5.8% intraday",
           font=f_head, fill=NAVY)
    d.text((64, y + 58), "as Seoul vows to act",
           font=f_head, fill=NAVY)
    d.rectangle([64, y + 116, 200, y + 120], fill=GOLD)

    split_y = y + 132
    # Body, left of the chart.
    body = ("South Korea's benchmark falls 5.8% in Monday's "
            "tech sell-off; finance minister says a contingency "
            "plan is ready.")
    f_body = font(False, 23)
    body_lines = wrap(body, f_body, 536)
    assert len(body_lines) <= 4, body_lines
    bottom = draw_lines(d, 64, split_y, body_lines, f_body, INK, 31)
    assert bottom <= 392, bottom

    # Chart, right of the body. Four verified points only, % vs the
    # previous close (4,869.96): previous close 0% (left edge) ->
    # open -2.77% at 09:00 (4,734.90) -> intraday trough -5.8%
    # mid-session (4,586.80) -> close -3.31% at 15:30 (4,708.54).
    # The trough's exact time is unverified, so it sits mid-session
    # with no time label of its own.
    cx0, cx1 = 632, 960
    d.text((cx0, split_y), "KOSPI — INTRADAY MOVE (%)",
           font=font(True, 14), fill=NAVY)
    plot_top, plot_bot = split_y + 20, split_y + 70
    plot_x0, plot_x1 = 676, 952

    def py(v):
        return plot_top + (0.5 - v) / 7.0 * (plot_bot - plot_top)

    f_grid = font(False, 13)
    for v, lab in ((0, "0%"), (-2, "−2"), (-4, "−4"), (-6, "−6")):
        gy = int(round(py(v)))
        d.line([(plot_x0, gy), (plot_x1, gy)], fill=GRID, width=1)
        d.text((668 - text_w(f_grid, lab), gy - 7), lab,
               font=f_grid, fill=MUTED)
    open_x = plot_x0 + 84  # +84 so "Previous close" and "09:00 open"
    # axis labels fit side by side, each centred under its own point.
    trough_x = (plot_x0 + plot_x1) // 2
    pts = [(plot_x0, int(round(py(0)))),
           (open_x, int(round(py(-2.77)))),
           (trough_x, int(round(py(-5.8)))),
           (plot_x1, int(round(py(-3.31))))]
    d.line(pts, fill=NAVY, width=4, joint="curve")
    for (px, pyy) in (pts[0], pts[1], pts[3]):
        d.ellipse([px - 4, pyy - 4, px + 4, pyy + 4], fill=NAVY)
    tx, ty = pts[2]
    d.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=GOLD)
    # Time axis: open/close endpoints only (KST). The time of the
    # intraday low is not marked — it is not a verified data point.
    d.line([(plot_x0, plot_bot), (plot_x1, plot_bot)],
           fill=OUTLINE, width=1)
    f_axis = font(False, 12)
    prev_lab = "Previous close"
    d.text((plot_x0 - text_w(f_axis, prev_lab) / 2, plot_bot + 4),
           prev_lab, font=f_axis, fill=MUTED)
    open_lab = "09:00 open"
    d.text((open_x - text_w(f_axis, open_lab) / 2, plot_bot + 4),
           open_lab, font=f_axis, fill=MUTED)
    close_lab = "15:30 close (KST)"
    d.text((plot_x1 - text_w(f_axis, close_lab), plot_bot + 4),
           close_lab, font=f_axis, fill=MUTED)
    d.text((cx0, plot_bot + 18),
           "Intraday low −5.8%; closed −3.31%",
           font=font(True, 14), fill=NAVY)
    assert plot_bot + 18 + 14 <= LY1 - 8

    # ---- Secondary stories: EUROPE / DISASTER / SECURITY ----------------
    SY0, SY1 = 418, 764
    secondaries = [
        ("EUROPE", "Kyiv region mourns as Dymer rescue goes on",
         "The Kyiv region marks a day of mourning after a drone strike "
         "collapsed part of a five-storey block in Dymer; rescuers pull "
         "a 79-year-old woman out alive as the search goes on."),
        ("DISASTER", "Indonesia rescuers continue search after factory fire",
         "Rescue teams searched the unstable Cikande factory site on "
         "Monday; police say DNA testing is needed because recovered "
         "remains cannot be identified visually."),
        ("SECURITY", "Kim says North Korea seeks security, not supremacy",
         "Kim Jong-un tells foreign envoys Pyongyang seeks neither "
         "hegemony nor expansion and defends its arms build-up as "
         "self-defence, in remarks reported by state media on Monday."),
    ]
    for i, (tag, headline, text) in enumerate(secondaries):
        x0 = 36 + i * 323
        x1 = x0 + 306
        card(d, x0, SY0, x1, SY1, gold_h=6)
        y = label(d, x0 + 18, SY0 + 16, tag, size=20)
        f_h = font(True, 22)
        h_lines = wrap(headline, f_h, 270)
        assert len(h_lines) <= 3, (tag, h_lines)
        y = draw_lines(d, x0 + 18, y + 6, h_lines, f_h, NAVY, 28)
        f_b = font(False, 18)
        b_lines = wrap(text, f_b, 270)
        assert len(b_lines) <= 8, (tag, b_lines)
        bottom = draw_lines(d, x0 + 18, y + 6, b_lines, f_b, INK, 24)
        assert bottom <= SY1 - 16, (tag, bottom)

    # ---- Bottom strip: DIPLOMACY + POLITICS, ALSO, sources -------------
    TX0, TY0, TX1, TY1 = 36, 778, 988, 1016
    d.rectangle([TX0, TY0, TX1, TY1], fill=WHITE, outline=OUTLINE, width=1)
    y = TY0 + 12
    f_sh = font(True, 19)
    d.text((56, y), "DIPLOMACY — Nepal PM holds talks with Modi in Delhi",
           font=f_sh, fill=NAVY)
    y += 24
    f_sb = font(False, 16)
    lines = wrap("Balendra Shah meets Narendra Modi on his first bilateral "
                 "trip abroad; the leaders flag off a new Ayodhya–Janakpur "
                 "train.", f_sb, 912)
    assert len(lines) <= 2, lines
    y = draw_lines(d, 56, y, lines, f_sb, INK, 22)
    y += 8
    d.text((56, y), "POLITICS — Burnham defends 'landmark' EU deal",
           font=f_sh, fill=NAVY)
    y += 24
    lines = wrap("Burnham told MPs the deal could add up to £17bn a year "
                 "by 2040; at the CBI, Badenoch criticised the projected "
                 "growth, then in the Commons said 'could be' was doing a "
                 "lot of heavy lifting.", f_sb, 912)
    assert len(lines) <= 2, lines
    y = draw_lines(d, 56, y, lines, f_sb, INK, 22)
    y += 8
    d.rectangle([56, y, 968, y + 2], fill=GOLD)
    y += 10
    f_al = font(True, 14)
    f_ar = font(False, 14)
    lab = "ALSO — "
    lab_w = text_w(f_al, lab)
    also_lines = wrap_first_narrow(
        "Seoul to ease buyback limits • Badenoch attacks EU deal at CBI",
        f_ar, 912 - lab_w, 912)
    assert len(also_lines) <= 1, also_lines
    d.text((56, y), lab, font=f_al, fill=NAVY)
    y = draw_lines(d, 56 + lab_w, y, also_lines, f_ar, INK, 19)
    y += 8
    d.text((56, y),
           "Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, "
           "Al Jazeera • 23 November 2026",
           font=font(False, 14), fill=MUTED)
    y += 14
    assert y <= TY1 - 6, y

    img.save(OUT)
    print("wrote %s (%dx%d)" % (OUT, W, H))


if __name__ == "__main__":
    main()
