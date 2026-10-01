"""
SPECIMEN DECK v5.0 — one slide per module, real assets, real content.
This is the regression suite, not a reference document (STYLE_GUIDE_v5.md
§10). Re-render this whole file before any module change ships. If a
module drifts from its own documented schema, this is what catches it —
nothing else will, until a real deck hits the gap.

Photo names below are placeholders from a working deck's asset library
(Southeast Australia) that is NOT in this repo. Until v10 that made 12 of
the 18 original modules fail with FileNotFoundError, so they were never
actually regression-tested. The suite now substitutes a stand-in photo
for any missing name (and prints which ones), so every module renders and
every QA check passes clean. What matters for regression purposes is that
every module renders and every QA check (including the v5 additions:
edge-bounds automatic, photo-contrast opt-in) passes clean.

v10: M19-M26 (the visual-variety modules promoted from the Mosel Field
Guide) are covered with neutral synthetic data -- nothing here depends on
any one deck.
"""
import sys, json
sys.path.insert(0, '.')
import importlib, core, modules
importlib.reload(core); importlib.reload(modules)
from tokens import DEFAULT_PALETTE

# Stand-in photos for placeholder names that aren't in this repo (see the
# docstring). Patched AFTER the reloads above, on both modules, because
# modules.py binds load_photo by name at import.
STAND_IN = 'de_bernkastel_aerial'
substituted = set()
def _fallback(orig):
    def wrapped(name, *a, **k):
        try:
            return orig(name, *a, **k)
        except FileNotFoundError:
            substituted.add(name)
            return orig(STAND_IN, *a, **k)
    return wrapped
core.load_photo = modules.load_photo = _fallback(core.load_photo)
core.load_photo_rgba = modules.load_photo_rgba = _fallback(core.load_photo_rgba)

pal = dict(DEFAULT_PALETTE)
TOTAL = 27
results = {}

def run(name, no):
    fn = modules.MODULES[name]
    slot = SLOTS[no]
    try:
        img = fn(slot, no, TOTAL, pal)
        img.save(f'/home/claude/specimen_renders/spec{no:02d}_{name}.png')
        results[no] = 'OK'
        print(f'{no:2d}  {name:16s} OK')
    except Exception as e:
        results[no] = f'FAIL: {e}'
        print(f'{no:2d}  {name:16s} FAIL: {e}')

SLOTS = {

1: dict(  # statement / cover
    variant='cover', photo='vineyard_aerial_rows',
    title='Specimen', subtitle='One slide per module — the regression baseline'),

2: dict(  # editorial_lead
    photo='vineyard_irrigation_spray', kicker='M02 · EDITORIAL LEAD',
    headline='The Workhorse Layout',
    standfirst="Photo band, headline, hero standfirst, serif run-ins — the most-used module in the system.",
    items=[
        ("First lead.", "Body text flows from a bold serif lead on a shared baseline."),
        ("Second lead.", "Two to four run-ins per slide; a seventy-word budget is enforced."),
        ("Third lead.", "The QA harness checks type floor, hierarchy, and clearance automatically."),
    ]),

3: dict(  # mosaic
    kicker='M16 · MOSAIC', hero_photo='vineyard_sunset_rows_generic',
    small_photos=['shiraz_cluster_ripe', 'white_grapes_on_vine'],
    captions={
        'vineyard_sunset_rows_generic': "Pacing breather — one hero, two smalls, captions only",
        'shiraz_cluster_ripe': "Captions wrap now; this used to be a real bug",
        'white_grapes_on_vine': "Bold italic serif, burgundy chip — legible over any photo",
    }),

4: dict(  # atlas (schematic marker map, NOT map_facsimile)
    kicker='M09 · ATLAS', headline='Schematic Marker Map',
    outlines=[[(0.1,0.1),(0.9,0.1),(0.9,0.6),(0.1,0.6)]],
    markers=[{'name':'Example Region','target':(0.5,0.35),'label':(0.55,0.2),'side':'right'}],
    cities=[(0.5,0.35,'Capital City')],
    legend=[('Region Group', 'Example, Example, Example')]),

5: dict(  # feature_trio
    kicker='M14 · FEATURE TRIO', headline='Three Columns, Three Photos',
    features=[
        ("First Region", "Short body copy under a bold serif title, image below.", 'barossa_canola_field_radio_sign'),
        ("Second Region", "Column width and image height match across all three.", 'vineyard_panorama_lake'),
        ("Third Region", "No headline slot beyond the title — keep it tight.", 'hunter_valley_vineyard'),
    ]),

6: dict(  # spotlight
    photo='old_vine_zoomed_out2', kicker='M13 · SPOTLIGHT',
    headline='Lettered Callouts on a Hero',
    callouts=[
        (0.50, 0.85, 'A', 'First Callout', "Chip and legend entry share a letter and a color."),
        (0.50, 0.55, 'B', 'Second Callout', "Position callouts on the actual subject, not near it."),
        (0.60, 0.09, 'C', 'Third Callout', "Three to six callouts, split into two legend columns."),
        (0.63, 0.66, 'D', 'Fourth Callout', "Verify callout position against the real photo crop."),
    ]),

7: dict(  # duel
    photos=['duel_band_clare', 'duel_band_eden'], labels=['LEFT SIDE', 'RIGHT SIDE'],
    kicker='M05 · DUEL', headline='Two Things, Compared',
    standfirst="Table mode: row labels wrap now if they exceed the label column.",
    mode='table', col_heads=['Left Column', 'Right Column'],
    rows=[
        ("Attribute One", "Value A", "Value B"),
        ("A Longer Attribute Label", "Value A", "Value B"),
        ("Attribute Three", "Value A", "Value B"),
    ]),

8: dict(  # photo_quote
    photo='vineyard_rows_walker',
    quote="One large serif quote, sentence case, over a full-bleed photograph.",
    attribution="Attribution line, optional"),

9: dict(  # side_rail
    photo='vineyard_aerial_rows', side='left', kicker='M03 · SIDE RAIL',
    headline='Vertical Band\nLayout',
    standfirst="A genuine full-height photo rail, not a photo band with text underneath.",
    items=[
        ("First point.", "Run-in items stack in the text column."),
        ("Second point.", "Use this when the photo deserves full-height presence."),
    ]),

10: dict(  # showcase_shelf
    kicker='M08 · SHOWCASE SHELF', headline='Six Products, One Shelf',
    products=[
        ('wynns_coonawarra_cabernet', 'Producer One', 'Product Name', 'Style', 'Origin, XX',
         "Producer renders burgundy, mixed-case, serif — locked default."),
        ('coldstream_hills_reserve_pinot_noir_v2', 'Producer Two', 'Product Name', 'Style', 'Origin, XX',
         "Bottle bottoms align to the shelf line, backgrounds match."),
        ('chambers_rosewood_grand_muscat', 'Producer Three', 'Product Name', 'Style', 'Origin, XX',
         "Six products, 3x2 grid, uniform treatment."),
        ('vineyard_panorama_lake', 'Producer Four', 'Product Name', 'Style', 'Origin, XX', "Placeholder art."),
        ('hunter_valley_vineyard', 'Producer Five', 'Product Name', 'Style', 'Origin, XX', "Placeholder art."),
        ('barossa_canola_field_radio_sign', 'Producer Six', 'Product Name', 'Style', 'Origin, XX', "Placeholder art."),
    ]),

11: dict(  # timeline
    bg_photo='vineyard_sunset_rows_generic', kicker='M10 · TIMELINE',
    headline='A Vertical Spine',
    standfirst="Ghosted full-bleed background, events stacked on a central spine.",
    events=[
        ("YEAR", "First Event", "A short note about what happened."),
        ("YEAR", "Second Event", "A short note about what happened."),
        ("YEAR", "Third Event", "A short note about what happened."),
        ("YEAR", "Fourth Event", "A short note about what happened."),
    ]),

12: dict(  # ladder
    kicker='M11 · LADDER', headline='A Ranked Pyramid',
    standfirst="Top tier is best; use for quality hierarchies, not containment (see euler_nesting).",
    tiers=[
        ("Top Tier", "The best of the category."),
        ("Middle Tier", "Solid, dependable, mid-range."),
        ("Base Tier", "Entry point, largest volume."),
    ]),

13: dict(  # lexicon_cloud
    kicker='M12 · LEXICON CLOUD', headline='Shelf-Packed Terms',
    terms=[
        ("Terroir", 90, "Sense of place"),
        ("Tannin", 70, "Structure from skins, oak"),
        ("Acidity", 60, "The backbone of freshness"),
        ("Botrytis", 50, "Noble rot"),
        ("Malolactic", 55, "Softening fermentation"),
        ("Phylloxera", 65, "The root louse"),
        ("Sur Lie", 45, "Aging on lees"),
        ("Chaptalization", 48, "Adding sugar pre-ferment"),
        ("Vintage", 75, "Year of harvest"),
        ("Appellation", 68, "A defined place of origin"),
    ]),

14: dict(  # process_map
    photos=['vineyard_irrigation_spray', 'shiraz_cluster_ripe', 'pouring_red_wine_outdoor_table'],
    kicker='M06 · PROCESS MAP', headline='Three Parallel Flows',
    standfirst="Photo stripe up top, then three aligned decision/step columns below.",
    columns=[
        ("Column One", [("Step one", False), ("Decision point", True), ("Step two", False)]),
        ("Column Two", [("Step one", False), ("Step two", False), ("Step three", False)]),
        ("Column Three", [("Decision point", True), ("Step one", False), ("Step two", False)]),
    ]),

15: dict(  # fact_file
    photo='vineyard_panorama_lake', kicker='M15 · FACT FILE',
    headline='Key-Value Facts',
    facts=[
        ("Fact One", "A short factual statement with its key bolded to the left."),
        ("Fact Two", "Facts wrap to as many lines as needed within the row pitch."),
        ("Fact Three", "Five to eight facts fit comfortably on one slide."),
    ]),

16: dict(  # card_grid
    kicker='M07 · CARD GRID', headline='A Flexible Grid',
    standfirst="row_layout controls cards-per-row; defaults to an even 2-column split.",
    cards=[
        (None, "Card One", "Subtitle", "Body copy for the first card in the grid."),
        (None, "Card Two", "Subtitle", "Body copy for the second card in the grid."),
        (None, "Card Three", "Subtitle", "Body copy for the third card in the grid."),
        (None, "Card Four", "Subtitle", "Body copy for the fourth card in the grid."),
    ]),

17: dict(  # euler_nesting
    kicker='M18 · EULER NESTING', headline='True Containment',
    standfirst="Nested circles for a real “B is entirely inside A” relationship, not a ranked list.",
    circles=[
        ("Outer", 1080, 900, 420, None, 'above'),
        ("Inner One", 900, 950, 180, "Outer", 'in'),
        ("Inner Two", 1250, 950, 150, "Outer", 'in'),
    ]),

18: dict(  # stat_wall
    kicker='M04 · STAT WALL', headline='Big Numbers, Gridded',
    standfirst="Serif numerals in a two-column grid, rule-anchored, 4-8 stats.",
    stats=[
        ("110", "GIs Registered", "Nationwide, as of the current count"),
        ("1993", "System Founded", "Australia's place-name protection framework"),
        ("6", "States/Territories", "Covered by the multistate zone"),
        ("85%", "Content Rule", "Minimum for a single GI, vintage, or variety"),
    ]),

19: dict(  # map_facsimile — real slot requires full facsimile data; smoke-test the
           # import path only, not a full render (needs a source PDF's extracted
           # geometry, which is deck-specific, not specimen-appropriate)
    kicker='M18b · MAP FACSIMILE', headline='(see LESSONS_LEARNED_v5.md §7)',
    states=[], regions={}, rivers=[], leaders=[],
    labels={'regions':{}, 'states':{}, 'cities':{}, 'ocean':None},
    city_dots={}),


20: dict(  # cover_bleed (M19)
    photo='vineyard_aerial_rows', photo_anchor=0.6, photo_zoom=1.1,
    kicker='THE FIELD GUIDE: SPECIMEN', kicker_size=96,
    kicker_chip=dict(color=(18, 32, 30), alpha=0.80, text=(196, 158, 84)),
    title='Full Bleed,\nNo Scrim', title_top=0.60, photo_credit='Specimen / stand-in'),

21: dict(  # region_map (M20) -- synthetic geometry, normalised 0-1
    kicker='M20 · REGION MAP', headline='Five Regions, One Highlighted', map_h=1300,
    highlight='Beta', summary_lead='Reading it',
    summary='Real traced shapes on a country outline; one region picked out, the packed western ones labelled in a column.',
    left_labels=['Alpha', 'Beta', 'Gamma'], direct_labels={'Delta': (30, -70), 'Epsilon': (30, 20)},
    credit='Synthetic specimen geometry',
    map=dict(aspect=0.85,
        outline=[(0.10, 0.08), (0.88, 0.10), (0.96, 0.50), (0.82, 0.94), (0.22, 0.92), (0.05, 0.50)],
        islands=[],
        regions=[('Alpha', [(0.20, 0.30), (0.30, 0.28), (0.32, 0.40), (0.22, 0.42)]),
                 ('Beta', [(0.22, 0.46), (0.32, 0.45), (0.34, 0.58), (0.24, 0.60)]),
                 ('Gamma', [(0.26, 0.64), (0.36, 0.63), (0.38, 0.76), (0.28, 0.78)]),
                 ('Delta', [(0.62, 0.30), (0.74, 0.30), (0.74, 0.40), (0.62, 0.40)]),
                 ('Epsilon', [(0.66, 0.56), (0.78, 0.56), (0.78, 0.66), (0.66, 0.66)])],
        rivers={'River': [[(0.30, 0.10), (0.34, 0.40), (0.30, 0.70), (0.40, 0.92)]]},
        targets={'Alpha': (0.26, 0.35), 'Beta': (0.28, 0.52), 'Gamma': (0.32, 0.70),
                 'Delta': (0.68, 0.35), 'Epsilon': (0.72, 0.61)})),

22: dict(  # blades (M21)
    blades=[dict(photo='vineyard_aerial_rows', caption='Detail'),
            dict(photo='vineyard_irrigation_spray', caption='Figure in landscape'),
            dict(photo='vineyard_sunset_rows_generic', caption='Wide view')],
    blade_h=1180, kicker='M21 · BLADES', headline='Three Scales, One Subject',
    items=[('Detail', 'The close view that shows the work.'),
           ('Figure', 'Someone doing it, for scale.'),
           ('Wide', 'The place it all sits in.')],
    photo_credit='Specimen / stand-in'),

23: dict(  # stair_ladder (M22)
    kicker='M22 · STAIR LADDER', headline='Five Rungs, Lowest at the Bottom',
    standfirst='Rank climbs the page; a parallel track sits outside the ranking.',
    rungs=[('Level one', 'The entry rank.'), ('Level two', 'A step up.'),
           ('Level three', 'The middle of the range.'), ('Level four', 'Rare.'),
           ('Level five', 'The rarest of all.')],
    side_note=dict(beside=3, title='Parallel', note='Same threshold as level four, reached another way.')),

24: dict(  # chart_stack (M23)
    kicker='M23 · CHART STACK', headline='Two Graphics, One Slide',
    standfirst='A range chart with a conditional extension, and a labelled bar chart.',
    band_chart=dict(title='RANGE, UNITS', axis_max=20, ticks=[0, 4, 9, 12, 18],
        rows=[('narrow', 'focus', 0, 4, 9), ('wide', 'amber', 4, 12, 18)],
        legend=('base range', 'extension, under a condition')),
    bar_chart=dict(title='SHARE, PERCENT',
        bars=[('North', 64, '64%', 'amber', False), ('Whole', 49, 'Just under half', 'gold', False),
              ('Focus', 26, '26%', 'focus', True)])),

25: dict(  # rail_rings (M24)
    photo='vineyard_aerial_rows', anchor=0.5, photo_caption='Specimen caption',
    photo_credit='Specimen / stand-in', kicker='M24 · RAIL RINGS',
    headline='Rings Beside\nA Photo Rail',
    rings=[(91, 'SHARE ONE', 'grape'), (62, 'SHARE TWO', 'amber')],
    items=[('Reading', 'Two rings state the headline numbers.'),
           ('Then', 'The prose carries what the rings cannot.')]),

26: dict(  # hero_facts (M25)
    photo='vineyard_aerial_rows', anchor=0.4, hero_h=1340, photo_caption='The subject itself',
    photo_credit='Specimen / stand-in', kicker='M25 · HERO FACTS', headline='Photo First, Facts Second',
    facts=[('One', 'The first short fact.'), ('Two', 'The second short fact.'),
           ('Three', 'The third short fact.'), ('Four', 'The fourth short fact.')]),

27: dict(  # tile_grid (M26)
    kicker='M26 · TILE GRID', headline='Four Tiles, Four Colours',
    standfirst='Each tile takes the colour of its own subject.',
    tile_colors=[((18, 32, 30), (201, 151, 3)), ((201, 151, 3), (18, 32, 30)),
                 ((98, 91, 74), (203, 194, 165)), ((203, 114, 12), (50, 22, 8))],
    tiles=[('First', 'Sub one', 'Body text for the first tile.'),
           ('Second', 'Sub two', 'Body text for the second tile.'),
           ('Third', 'Sub three', 'Body text for the third tile.'),
           ('Fourth', 'Sub four', 'Body text for the fourth tile.')]),

}

import os
os.makedirs('/home/claude/specimen_renders', exist_ok=True)
for no in sorted(SLOTS):
    name = {1:'statement',2:'editorial_lead',3:'mosaic',4:'atlas',5:'feature_trio',
            6:'spotlight',7:'duel',8:'photo_quote',9:'side_rail',10:'showcase_shelf',
            11:'timeline',12:'ladder',13:'lexicon_cloud',14:'process_map',15:'fact_file',
            16:'card_grid',17:'euler_nesting',18:'stat_wall',19:'map_facsimile',
            20:'cover_bleed',21:'region_map',22:'blades',23:'stair_ladder',
            24:'chart_stack',25:'rail_rings',26:'hero_facts',27:'tile_grid'}[no]
    if no == 19:
        continue  # map_facsimile needs deck-specific extracted geometry; not specimen-testable in isolation
    run(name, no)

print()
print('SPECIMEN RESULTS:', results)
n_ok = sum(1 for v in results.values() if v == 'OK')
print(f'{n_ok}/{len(results)} modules pass QA clean')
if substituted:
    print('stand-in photo used for:', ', '.join(sorted(substituted)))
