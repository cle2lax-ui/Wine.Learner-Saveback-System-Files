"""
FIELD GUIDE STYLE SYSTEM — TOKENS
Single source of truth for BOTH series built on this system: Field Guide
(modules.py) and Quick Sips (quick_sips.py). Modules import from here;
nothing is hardcoded downstream. All pixel values are at build scale
2160x2700 (export 1080x1350 @0.5x) — shared canvas, shared safe zones,
shared QA harness, distinct visual languages per series.
"""

# ---------- Canvas ----------
W, H = 2160, 2700                 # 4:5 portrait, built @2x
EXPORT = (1080, 1350)
M = 120                           # side/top margin (60px @1080 — published safe zone)
FOOTER_Y = H - 150                # footer baseline zone (inside caption-overlay risk band, by design)
CONTENT_BOTTOM = H - 200          # no CONTENT below this (Instagram caption preview zone) -- updated from H-400 per standing preference; exceptions still use "!" prefix
GRID_SQUARE = (H - W) // 2        # 270px top/bottom hidden in profile-grid 1:1 crop

# ---------- Type ramp (locked, Field Guide) ----------
# Quick Sips uses its own sizes chosen per-element in quick_sips.py (a
# denser infographic/brochure format doesn't fit one shared ramp), but
# obeys the same FLOOR and the same QA harness.
TYPE = dict(
    display_xl=220,     # cover title
    display_lg=168,     # statement words / big page titles
    display_md=112,     # standard page headline
    standfirst_hero=92, # hero standfirst
    standfirst=74,      # standard standfirst
    lead=74,            # serif run-in lead
    body=64,            # body text
    caption=60,         # captions, footer, micro-labels (FLOOR)
)
FLOOR = 60              # absolute type floor
HIERARCHY_GAP = 30      # headline must exceed largest other type by this

# ---------- Fixed neutrals (never change per deck) ----------
PAPER  = (251, 249, 244)
INK    = (38, 33, 38)
MUTED  = (110, 96, 104)
LINE   = (231, 222, 207)

# ---------- Quick Sips series constants ----------
# Fixed across every Quick Sips deck regardless of topic, unlike
# SIGNATURE/ACCENT/LEAD below which flex per deck. This is the series'
# own identity accent (stat-strip hairlines, eyebrow labels, producer
# names on the benchmark-bottle caption) — closer to the Cigar
# Aficionado/Rolex register than DEFAULT_PALETTE's ACCENT gold.
QUICKSIPS_GOLD = (168, 130, 60)

# ---------- Per-deck palette slots (override in manifest) ----------
# Rand filter (adopted system-wide, save-back v7): bold flat red and
# gold, not the earlier dusty claret/muted brass. Headlines read as
# black typography with a colored underline accent (see core.headline);
# SIGNATURE now drives flat color blocks (cover/closing panels) rather
# than headline fill directly in most decks -- see core.py's Rand notes.
DEFAULT_PALETTE = dict(
    SIGNATURE=(196, 30, 30),      # deck signature (Rand filter: bold flat red)
    ACCENT=(232, 165, 22),        # secondary accent (Rand filter: bold flat gold)
    LEAD=(140, 92, 24),           # serif run-in lead color
)

# ---------- Photography ----------
BAND_TALL = 720                   # standard photo band height
BAND_MIN = 550                    # never crop a band below this
SCRIM = (20, 16, 18)

# ---------- Content discipline ----------
MAX_BODY_WORDS = 105              # Field Guide per-slide body budget (QA-enforced) -- raised from 70 (+50%) per standing preference
                                   # Quick Sips overrides via qa.max_words = 130 (denser format)
MAX_HOOK_WORDS = 12               # cover headline budget
SLIDES_MIN, SLIDES_MAX = 8, 12    # Field Guide deck length; Quick Sips is always exactly 2

# ---------- Contrast (WCAG) ----------
CONTRAST_BODY = 4.5
CONTRAST_LARGE = 3.0

# ---------- Fonts (role -> file) ----------
FONT_DIR = "/home/claude/styleguide/fonts"
FONT_FILES = {
    "display_black": "Playfair-Black.ttf",
    "display_xbold": "Playfair-XBold.ttf",
    "display_bold": "Playfair-Bold.ttf",
    "display_light": "Playfair-Regular.ttf",   # Quick Sips: benchmark-bottle caption note
    "italbold": "Playfair-BoldItalic.ttf",
    "standfirst_italic": "Playfair-MediumItalic.ttf",
    "caption_italic": "Cormorant-Italic.ttf",
    "body": "Archivo-Medium.ttf",
    "body_light": "Archivo-Light.ttf",         # Quick Sips: main body text (thin, magazine-column feel)
    "body_regular": "Archivo-VF.ttf",          # true Regular weight (400) -- no static Regular file ships,
                                                # so this loads the variable font pinned to its "Regular"
                                                # named instance (see core.font(), which special-cases it)
    "body_bold": "Archivo-Bold.ttf",
    "kicker": "ArchivoCond-SemiBold.ttf",
    "kicker_bold": "ArchivoCond-Bold.ttf",
    # Added for the "Five Fascinating Facts About..." series (v1) --
    # Vignelli-grid treatment leans on grotesque sans as the dominant
    # display face (not Playfair) specifically to read as visually
    # distinct from Field Guide/Quick Sips at a glance.
    "sans_black": "Archivo-Black.ttf",
    "sans_cond_black": "ArchivoCond-Black.ttf",
}

# ---------- "Five Fascinating Facts About..." series constants ----------
# Fixed across every FFFA deck regardless of topic. Deliberately NOT
# Field Guide's red (DEFAULT_PALETTE SIGNATURE) and NOT Quick Sips' gold
# -- a flat cobalt blue + ink + paper is the whole palette, so FFFA never
# gets mistaken for either sibling series at a glance. No gradients, no
# scrims-as-default, hard-edged flat color only (Vignelli grid
# discipline).
FFFA_ACCENT = (28, 74, 172)        # flat cobalt -- series signature color
FFFA_YELLOW = (255, 197, 47)       # Brewers-gold-adjacent middle ground --
                                    # cover subject + every page headline,
                                    # set apart from body/kicker/numeral
                                    # which stay paper/cobalt
FFFA_SLIDE_COUNT = 6               # cover + 5 facts, fixed, not a range
PHOTO_DIR = "/home/claude/styleguide/photos"

# Showcase-shelf rule: light grey, deliberately softer than INK so the
# bottles read as the subject and the shelf as a quiet baseline.
SHELF_RULE = (196, 190, 182)
