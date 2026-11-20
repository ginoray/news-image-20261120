"""The 20 November 2026 poster: content and drawing.

A one-page broadsheet, "THE WORLD TODAY", that sums up Friday 20 November
2026 in a single 1024x1024 image. Every story below was reported on the day
and cross-checked against at least two independent reports before it was
set in type; figures that rest on estimates say so on the page.

The drawing is plain PIL: a masthead, a lead story with a stat strip, a
dark feature band, a two-row grid of news cards, an in-brief column set
and an also-today footer. Nothing here reads the clock, the network or
any random source, so the same code always paints the same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 22, 26)
FAINT = (92, 90, 84)
ACCENT = (166, 30, 40)
GOLD = (176, 141, 62)
BAND = (24, 26, 34)
BAND_INK = (240, 238, 230)
BAND_SUB = (205, 205, 198)

_font_cache = {}


def font(kind, size):
    """Serif for headlines, sans for body; first available file wins."""
    key = (kind, size)
    if key in _font_cache:
        return _font_cache[key]
    serif = ["/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSerif-%s.ttf"]
    sans = ["/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-%s.ttf"]
    paths = serif if kind.startswith("serif") else sans
    style = "Bold" if kind.endswith("bold") else "Regular"
    chosen = None
    for pat in paths:
        try:
            chosen = ImageFont.truetype(pat % style, size)
            break
        except OSError:
            continue
    if chosen is None:
        chosen = ImageFont.load_default()
    _font_cache[key] = chosen
    return chosen


def wrap(draw, text, fnt, width):
    """Greedy word wrap against pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories

LEAD = {
    "kicker": "ARTIFICIAL INTELLIGENCE  •  MARKETS",
    "headline": "ANTHROPIC'S $81.3 BILLION IPO IS THE LARGEST IN HISTORY",
    "body": ("The AI company behind Claude raised $81.3 billion in the biggest IPO ever recorded and "
             "jumped 17% on its Nasdaq debut — the first purely AI listing, read as a verdict on "
             "the industry."),
    "stats": "RAISED $81.3B   •   DEBUT +17%   •   FIRST PURE-PLAY AI LISTING",
}

FEATURE = {
    "kicker": "VICE CITY ECONOMY",
    "headline": "GTA VI TOPS $2 BILLION IN 24 HOURS",
    "body": ("Day two of the biggest entertainment launch ever: Sensor Tower estimates put sales above "
             "$1.8 billion net, three quarters of them on PlayStation. Take-Two has yet to publish "
             "official figures."),
}

CARDS = [
    ("THE HAGUE",
     "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
     "The International Court of Justice rules 9-6, in The Gambia's case, that Myanmar committed "
     "genocide against the Rohingya in the 2016-17 clearance operations in Rakhine State."),
    ("SHENZHEN",
     "SUMMIT DAY TWO: A 'PEACE DECLARATION'",
     "Trump, Xi and Putin's trilateral ends in a joint peace declaration, with differing accounts "
     "of the Trump-Xi talks. Ukraine was 'a priority', says envoy Witkoff."),
    ("RIYADH",
     "HOUTHIS STRIKE FOUR SAUDI TARGETS",
     "Yemen's Houthis claim drone and missile strikes on four targets in Saudi Arabia. Saudi "
     "authorities confirm a Riyadh landmark tower was damaged in the attack."),
    ("HORMUZ",
     "TANKER BURNS AFTER STRIKING A MINE",
     "A tanker catches fire east of the Strait of Hormuz after hitting a mine, and an ADNOC vessel "
     "is attacked with one crew member missing. Oil holds flat."),
    ("KYIV",
     "FOUR BALLISTIC MISSILES HIT THE CAPITAL",
     "Kyiv is struck by four ballistic missiles and a projectile lands near the Dutch embassy. "
     "European leaders say they are ready for talks with Russia on ending the war."),
    ("TAIPEI",
     "TAIWAN ACTS AS MARKET ROUT DEEPENS",
     "The Taiex has shed 5,248 points in three days. Short-selling curbs take effect today and a "
     "$15B stabilisation fund is deployed, as AI jitters spread after Nvidia chief Jensen Huang's "
     "resignation."),
]

BRIEFS = [
    ("WASHINGTON", "Trump defers the Iran decision to 2027: 'see what happens' after January 1."),
    ("DEEP SPACE", "Voyager 1 is now a full light-day from Earth, NASA confirms."),
    ("ODISHA", "Cyclone Akvan nears Gopalpur: 300,000 evacuated, landfall expected today."),
    ("GAZA", "Winter floods destroy shelters; four nations demand Israel open aid access."),
    ("SPACE", "Japan's Hayabusa2 abandons its asteroid landing after engine trouble."),
]

ALSO = "ALSO TODAY — Genoa airport shut 4 hours by mystery drones  •  Fiona the hippo dies in Cincinnati"
CREDIT = "Every story cross-checked at least twice."


# ---------------------------------------------------------------- drawing

def draw_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40                      # page margin
    right = W - M

    # masthead
    d.line([(M, 34), (right, 34)], fill=INK, width=3)
    title = "THE WORLD TODAY"
    tf = font("serif-bold", 74)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 44), title, font=tf, fill=INK)
    d.line([(M, 138), (right, 138)], fill=INK, width=1)
    df = font("sans-bold", 21)
    d.text((M, 148), "Friday, 20 November 2026", font=df, fill=ACCENT)
    sub = "The whole day in one image"
    sf = font("serif-regular", 20)
    sw = d.textlength(sub, font=sf)
    d.text((right - sw, 148), sub, font=sf, fill=FAINT)
    d.line([(M, 182), (right, 182)], fill=GOLD, width=3)

    # lead story
    y = 198
    d.text((M, y), LEAD["kicker"], font=font("sans-bold", 17), fill=ACCENT)
    y += 26
    y = text_block(d, (M, y), LEAD["headline"], font("serif-bold", 40), INK, right - M, 46)
    y += 4
    y = text_block(d, (M, y), LEAD["body"], font("serif-regular", 20), INK, right - M, 25)
    y += 8
    d.text((M, y), LEAD["stats"], font=font("sans-bold", 18), fill=ACCENT)
    y += 30
    d.line([(M, y), (right, y)], fill=INK, width=1)
    y += 14

    # feature band
    band_h = 112
    d.rectangle([(M, y), (right, y + band_h)], fill=BAND)
    bx = M + 22
    by = y + 12
    d.text((bx, by), FEATURE["kicker"], font=font("sans-bold", 15), fill=(232, 197, 110))
    by += 22
    d.text((bx, by), FEATURE["headline"], font=font("serif-bold", 30), fill=BAND_INK)
    by += 39
    text_block(d, (bx, by), FEATURE["body"], font("sans-regular", 16), BAND_SUB,
               right - bx - 22, 20)
    y += band_h + 12

    # cards: three columns, two rows
    cols = 3
    gap = 18
    cw = (right - M - gap * (cols - 1)) // cols
    card_h = 146
    for i, (tag, head, body) in enumerate(CARDS):
        cx = M + (i % cols) * (cw + gap)
        cy = y + (i // cols) * (card_h + 14)
        d.line([(cx, cy), (cx + cw, cy)], fill=ACCENT, width=2)
        d.text((cx, cy + 7), tag, font=font("sans-bold", 13), fill=FAINT)
        hy = text_block(d, (cx, cy + 27), head, font("sans-bold", 17), INK, cw, 21)
        text_block(d, (cx, hy + 3), body, font("sans-regular", 14), INK, cw, 18)
    y += 2 * (card_h + 14) + 2

    # in brief: two columns of one-liners
    d.line([(M, y), (right, y)], fill=INK, width=1)
    y += 10
    d.text((M, y), "AROUND THE WORLD IN BRIEF", font=font("sans-bold", 15), fill=INK)
    y += 25
    half = (right - M - gap) // 2
    for i, (tag, body) in enumerate(BRIEFS):
        bx = M + (i % 2) * (half + gap)
        by = y + (i // 2) * 29
        d.text((bx, by), tag, font=font("sans-bold", 13), fill=ACCENT)
        tw2 = d.textlength(tag + "  ", font=font("sans-bold", 13))
        text_block(d, (bx + tw2, by), body, font("sans-regular", 13), INK, half - tw2, 16)
    y += 3 * 29 + 10

    # footer: also-today on the left, the cross-check credit on the right
    d.line([(M, y), (right, y)], fill=GOLD, width=2)
    y += 11
    d.text((M, y), ALSO, font=font("sans-regular", 13), fill=FAINT)
    cf = font("serif-regular", 13)
    cw2 = d.textlength(CREDIT, font=cf)
    d.text((right - cw2, y), CREDIT, font=cf, fill=FAINT)
    return img
