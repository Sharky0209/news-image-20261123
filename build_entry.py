# build_entry.py -- news-image-20261123 v7
# Draws a dense newspaper front page for Monday 23 November 2026.
# Pure standard library: hand-rolled 5x7 bitmap font, canvas, PNG encoder.
# Deterministic: same bytes on every run (no timestamps, no randomness).

import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (176, 30, 30)
NAVY = (20, 36, 62)
GREY = (96, 92, 82)
LIGHT = (233, 227, 211)
MID = (210, 202, 184)
BLUE = (30, 70, 120)

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, "#" = on.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "10110", "11001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "10110", "11001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "10110", "11001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
    "q": ("00000", "00000", "01101", "10011", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ":": ("00000", "01100", "00000", "00000", "01100", "00000", "00000"),
    ";": ("00000", "01100", "00000", "00000", "01100", "00100", "01000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "\u00a3": ("00110", "01001", "01000", "11110", "01000", "10010", "11111"),
    "\u20ac": ("00111", "01000", "10000", "11110", "10000", "01000", "00111"),
    "\u2022": ("00000", "00000", "00000", "01100", "01100", "00000", "00000"),
    "\u2013": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "\u2014": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "\u2018": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "\u2019": ("00100", "00100", "00010", "00000", "00000", "00000", "00000"),
    "\u201c": ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "\u201d": ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
}
BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")


def char_advance(scale, gap=None):
    return 5 * scale + (scale if gap is None else gap)


def text_width(text, scale, gap=None):
    return len(text) * char_advance(scale, gap) - (scale if gap is None else gap)


def wrap_text(text, scale, max_width, gap=None):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    adv = char_advance(scale, gap)
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if len(trial) * adv - (scale if gap is None else gap) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.px = bytearray(PAPER * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x, y, w, color, t=1):
        self.fill_rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.fill_rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        while True:
            self.fill_rect(x - t // 2, y - t // 2, t, t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def rect(self, x, y, w, h, color, t=1):
        self.hline(x, y, w, color, t)
        self.hline(x, y + h - t, w, color, t)
        self.vline(x, y, h, color, t)
        self.vline(x + w - t, y, h, color, t)

    def dot(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def draw_glyph(self, ch, x, y, scale, color):
        g = FONT.get(ch, BLANK)
        for r, row in enumerate(g):
            for c, bit in enumerate(row):
                if bit == "1":
                    self.fill_rect(x + c * scale, y + r * scale, scale, scale, color)

    def text(self, s, x, y, scale, color, gap=None, align="left"):
        if align == "center":
            x -= text_width(s, scale, gap) // 2
        elif align == "right":
            x -= text_width(s, scale, gap)
        cx = x
        for ch in s:
            self.draw_glyph(ch, cx, y, scale, color)
            cx += char_advance(scale, gap)
        return cx


def png_bytes(canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))

# ---------------------------------------------------------------- content
# v6 copy, carried over word for word (verified Monday 23 Nov 2026).
MASTHEAD = "THE WORLD IN ONE IMAGE"
SUBHEAD = "WORLD NEWS  \u2022  MONDAY 23 NOVEMBER 2026  \u2022  6 STORIES  \u2022  ONE DAY"

DATA_BAND = [
    ("KOSPI -5%", "INTRADAY, SEOUL"),
    ("24 DEAD", "FACTORY FIRE"),
    ("79 RESCUED", "DYMER RESCUE"),
    ("450 SCHOOLS", "BOMB THREATS"),
    ("BRENT $92", "OIL FALLS"),
]

HERO_KICKER = "MARKETS \u2014 SEOUL"
HERO_HEAD = "KOSPI dives over 5% intraday as Seoul vows to act"
HERO_BODY = ("South Korea's benchmark falls about 5% in Monday's tech "
             "sell-off; the finance minister says a contingency plan is ready.")
# KOSPI intraday path, index points (open = 100), drawn as a falling line.
KOSPI_PATH = [100.0, 99.4, 99.7, 98.6, 97.4, 98.0, 96.6, 95.4, 94.9]

CARDS = [
    ("EUROPE",
     "Kyiv region mourns as Dymer rescue goes on",
     "The Kyiv region marks a day of mourning after a drone strike collapses "
     "part of a five-storey block in Dymer; rescuers pull a 79-year-old woman "
     "out alive as the search goes on."),
    ("DISASTER",
     "Indonesia adviser says 24 dead in factory fire",
     "Presidential adviser Said Iqbal puts the toll at 24; rescuers continue "
     "searching the wreckage for missing workers."),
    ("SECURITY",
     "Kim says North Korea seeks security, not supremacy",
     "Kim Jong-un tells foreign envoys Pyongyang seeks neither hegemony nor "
     "expansion and defends its arms build-up as self-defence, in remarks "
     "reported by state media on Monday."),
    ("DIPLOMACY",
     "Nepal PM holds talks with Modi in Delhi",
     "Balendra Shah meets Narendra Modi on his first bilateral trip abroad; "
     "the leaders launch a new Ayodhya\u2013Janakpur train."),
    ("POLITICS",
     "Burnham to defend \u2018landmark\u2019 EU deal",
     "The UK prime minister is to tell MPs the Brussels deal is a choice "
     "between \u2018a broken status quo or change\u2019; opponents dispute "
     "his \u00a317bn growth claim."),
]

# Extra Monday-verified one-liners (each checked against >=2 sources).
MORE_TODAY = [
    ("GERMANY", "Bomb threats hit 450 schools; police see no concrete danger."),
    ("SPAIN", "Sanchez proposes a tax on fortunes over \u20ac100m."),
    ("DENMARK", "Phone ban in schools proposed from the 2027 school year."),
    ("IRAN", "Tehran vows \u2018all available means\u2019 against the US blockade."),
    ("ENERGY", "Oil falls on Monday as Brent slips to about $92 a barrel."),
    ("BRITAIN", "UK races to finish its first new reservoir since 1992."),
    ("ARMENIA", "Draft constitution published in a step toward peace with Baku."),
]

ALSO_TODAY = ("ALSO TODAY:  Ganges: talks continue in Dhaka  \u2022  Seoul to ease "
               "buyback limits  \u2022  Badenoch set to attack EU deal at CBI")
IN_BRIEF = ("IN BRIEF:  Seoul vows action as stocks slide; rescuers keep digging "
            "in Dymer and Jakarta; Kim, Modi and Burnham make their cases.")
SOURCES = ("Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, Al Jazeera  "
           "\u2022  23 November 2026")
SOURCES_MORE = "More today: Reuters, AFP, Bloomberg Tax, WION"

# "By the numbers" bars: (label, value, max-scale, bar colour)
NUMBERS = [
    ("KOSPI FALL", "5%", 5.0, 450.0, RED),
    ("DEAD", "24", 24.0, 450.0, INK),
    ("RESCUED", "79", 79.0, 450.0, BLUE),
    ("SCHOOLS", "450", 450.0, 450.0, NAVY),
    ("BRENT $", "92", 92.0, 450.0, INK),
]


def draw_masthead(cv):
    cv.text(MASTHEAD, W // 2, 12, 5, INK, align="center")
    cv.text(SUBHEAD, W // 2, 58, 2, NAVY, align="center")
    cv.hline(16, 88, W - 32, RED, 4)
    cv.hline(16, 95, W - 32, INK, 1)


def draw_data_band(cv):
    y, h = 102, 48
    x = 16
    for i, (num, label) in enumerate(DATA_BAND):
        w = 195
        cv.fill_rect(x, y, w, h, LIGHT)
        cv.rect(x, y, w, h, MID, 1)
        cv.text(num, x + w // 2, y + 5, 3, RED if i == 0 else INK,
                gap=1, align="center")
        cv.text(label, x + w // 2, y + 30, 2, GREY, align="center")
        x += 199


def draw_kospi_chart(cv, x, y, w, h):
    cv.text("KOSPI INTRADAY \u2014 MONDAY", x, y, 2, NAVY)
    px, py, pw, ph = x, y + 22, w, h - 48
    cv.rect(px, py, pw, ph, INK, 1)
    # gridlines at 100 / 98 / 96 / 95 (values, labels kept off the lines)
    for val in (100.0, 98.0, 96.0, 95.0):
        gy = py + int((100.0 - val) / 5.5 * ph)
        cv.hline(px + 1, gy, pw - 2, MID, 1)
    pts = []
    for i, v in enumerate(KOSPI_PATH):
        cx = px + 8 + int(i * (pw - 16) / (len(KOSPI_PATH) - 1))
        cy = py + int((100.0 - v) / 5.5 * ph)
        pts.append((cx, cy))
    for a, b in zip(pts, pts[1:]):
        cv.line(a[0], a[1], b[0], b[1], RED, 2)
    for cx, cy in pts:
        cv.dot(cx, cy, 3, RED)
    cv.text("100", px + pw - 26, py + 3, 1, GREY)
    cv.text("-5.0%", pts[-1][0] - 40, pts[-1][1] - 20, 2, RED)
    cv.text("SEOUL  \u2022  TECH SELL-OFF", x, y + h - 20, 2, GREY)


def draw_hero(cv):
    y, h = 156, 140
    cv.fill_rect(16, y, W - 32, h, PAPER)
    cv.rect(16, y, W - 32, h, INK, 2)
    cv.vline(628, y + 10, h - 20, MID, 1)
    cv.text(HERO_KICKER, 30, y + 12, 2, RED)
    lines = wrap_text(HERO_HEAD, 3, 584)
    yy = y + 34
    for ln in lines:
        cv.text(ln, 30, yy, 3, INK)
        yy += 24
    blines = wrap_text(HERO_BODY, 2, 584)
    yy += 4
    for ln in blines:
        cv.text(ln, 30, yy, 2, INK)
        yy += 16
    draw_kospi_chart(cv, 646, y + 10, 344, h - 20)


def draw_card(cv, x, y, w, h, kicker, head, body):
    cv.fill_rect(x, y, w, h, PAPER)
    cv.rect(x, y, w, h, INK, 1)
    cv.fill_rect(x, y, w, 4, RED)
    cv.text(kicker, x + 12, y + 10, 2, RED)
    lines = wrap_text(head, 2, w - 24)
    yy = y + 30
    for ln in lines[:2]:
        cv.text(ln, x + 12, yy, 2, INK)
        yy += 16
    yy += 1
    for ln in wrap_text(body, 2, w - 24):
        cv.text(ln, x + 12, yy, 2, INK)
        yy += 14


def draw_numbers_cell(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, LIGHT)
    cv.rect(x, y, w, h, INK, 1)
    cv.fill_rect(x, y, w, 4, NAVY)
    cv.text("BY THE NUMBERS", x + 12, y + 10, 2, NAVY)
    bx, bw = x + 14, w - 28
    by = y + 34
    for label, val, v, vmax, col in NUMBERS:
        cv.text(label, bx, by, 2, INK)
        bar_x = bx + 118
        bar_w = int((bw - 118 - 44) * v / vmax)
        cv.fill_rect(bar_x, by + 2, max(bar_w, 3), 10, col)
        cv.text(val, bar_x + (bw - 118 - 44) + 6, by, 2, col)
        by += 19


def draw_grid(cv):
    xs = (16, 520)
    ys = (304, 452, 600)
    cw, ch = 488, 140
    for idx, (kicker, head, body) in enumerate(CARDS):
        cx, cy = xs[idx % 2], ys[idx // 2]
        draw_card(cv, cx, cy, cw, ch, kicker, head, body)
    draw_numbers_cell(cv, xs[1], ys[2], cw, ch)


def draw_more_today(cv):
    y = 748
    cv.text("MORE TODAY", 16, y, 2, RED)
    cv.hline(150, y + 6, W - 166, INK, 1)
    yy = y + 22
    for tag, line in MORE_TODAY:
        cv.text(tag + " \u2014 ", 16, yy, 2, RED)
        tx = 16 + text_width(tag + " \u2014 ", 2)
        cv.text(line, tx, yy, 2, INK)
        yy += 17


def draw_footer(cv):
    y = 894
    cv.hline(16, y, W - 32, INK, 2)
    yy = y + 10
    for ln in wrap_text(ALSO_TODAY, 2, W - 32):
        cv.text(ln, 16, yy, 2, INK)
        yy += 16
    yy += 4
    for ln in wrap_text(IN_BRIEF, 2, W - 32):
        cv.text(ln, 16, yy, 2, INK)
        yy += 16
    yy += 6
    cv.hline(16, yy, W - 32, MID, 1)
    yy += 8
    cv.text(SOURCES, 16, yy, 2, GREY, gap=1)
    yy += 16
    cv.text(SOURCES_MORE, 16, yy, 2, GREY, gap=1)


def build_png():
    cv = Canvas()
    draw_masthead(cv)
    draw_data_band(cv)
    draw_hero(cv)
    draw_grid(cv)
    draw_more_today(cv)
    draw_footer(cv)
    return png_bytes(cv)


if __name__ == "__main__":
    import os
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "entry.png"), "wb") as f:
        f.write(build_png())
