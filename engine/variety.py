"""Visual-variety check for Field Guide-length decks (10-12 slides).

The Mosel Field Guide is the benchmark (guides/VISUAL_BENCHMARK_v10.md):
11 distinct layouts in 12 slides, none twice in a row, none more than
twice, and a third of the slides led by a data graphic, diagram or map.
This turns those rules into a build-time check, so a deck that drifts back
toward a run of text slides fails the build like any other QA failure --
the fix is a different layout, not an exemption.

Call it from a deck's build with the list of module names in slide order.
Apply it to Field Guides only; shorter formats (Quick Sips, GTR, FFFA)
have their own structures.
"""

# Modules whose slide is LED by a data graphic, diagram or map (not a
# photo band over running text). Extend when a new graphic module is added.
GRAPHIC_MODULES = {
    "atlas", "map_facsimile", "region_map", "ladder", "stair_ladder",
    "euler_nesting", "timeline", "process_map", "stat_wall",
    "chart_stack", "rail_rings",
}


def check_variety(names, min_distinct=8, max_uses=2, min_graphic=4):
    """Returns a list of human-readable problems (empty = passes)."""
    problems = []
    distinct = len(set(names))
    if distinct < min_distinct:
        problems.append(f"only {distinct} distinct layouts in {len(names)} slides "
                        f"(need {min_distinct}+)")
    for i in range(1, len(names)):
        if names[i] == names[i - 1]:
            problems.append(f"slides {i} and {i + 1} both use '{names[i]}' -- never "
                            f"the same layout twice in a row")
    for n in sorted(set(names)):
        if names.count(n) > max_uses:
            problems.append(f"'{n}' used {names.count(n)} times (max {max_uses})")
    graphic = [i + 1 for i, n in enumerate(names) if n in GRAPHIC_MODULES]
    if len(graphic) < min_graphic:
        problems.append(f"only {len(graphic)} data/diagram/map-led slides {graphic} "
                        f"(need {min_graphic}+)")
    return problems


def report(names, **kw):
    """Print a one-line summary and raise ValueError if the deck fails."""
    problems = check_variety(names, **kw)
    graphic = [i + 1 for i, n in enumerate(names) if n in GRAPHIC_MODULES]
    print(f"variety: {len(set(names))} distinct layouts / {len(names)} slides; "
          f"graphic-led slides {graphic}")
    if problems:
        raise ValueError("visual-variety check failed:\n  " + "\n  ".join(problems))
