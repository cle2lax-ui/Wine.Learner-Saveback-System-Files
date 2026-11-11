# South Africa Wine of Origin boundaries: source and license note

**What:** `za_wo_winelands.geojson` holds the Wine of Origin districts, wards and regions that fall in the Western Cape winelands window (28 districts, 92 wards), with coordinates rounded to four decimals and lightly simplified (0.0004 degrees, about 40 m). `ne_10m_sa_clip.geojson` is the coastline.

**Where it comes from**
- Boundaries: the open GitHub repository `Tolar-dio/wine-world` ("Vitis Mundi"), file `docs/data/geo/za.geojson` (148 South African features, all marked boundary quality "official"). That repository republishes the **VinPro / SAWIS Wine of Origin layer**: the statutory demarcations kept by the Wine and Spirit Board and the South African Wine Industry Information and Systems (SAWIS). Pulled with `arc5/prepare_wo_geo.py`.
- Coastline: Natural Earth 10 m land (public domain).

**How it was checked (November 2026)**
- Count: 32 districts and 102 wards in the whole file, matching Wines of South Africa's own figure ("32 districts and some 102 wards").
- Names: against the official SAWIS production-areas list (October 2023), 79 of 80 coastal, south coast and Breede district and ward names are present; the other is a spelling variant (Paardeberg/Perdeberg).
- Currency: the file also holds **Shaw's Mountain**, a newer Overberg ward (listed by Wineland with Goukou River Valley and the new Stilbaai and Nuveld-Karoo districts), so it is more recent than the 2023 list. A proposed Stanford Valley ward (a 2026 gazette notice) is not in it, and is not a ward yet.
- Not checked: the polygon edges against the gazetted farm-by-farm descriptions. The data is the industry layer as republished; for a legal question, use SAWIS.

**LICENSE CAVEAT (read before wide promotion).** The Vitis Mundi repository states that the VinPro/SAWIS layer has **no stated license** ("check before wide public promotion"). The boundaries are the public, statutory demarcations and are used here, credited, for a non-commercial educational carousel. If a post is ever promoted, sponsored or sold, ask SAWIS or Wines of South Africa for permission first. Every map slide carries the credit line "Wine of Origin boundaries: Wine and Spirit Board / SAWIS (VinPro layer)."

**Official sources for the same maps.** Wines of South Africa publishes its district maps (Cape Town, Stellenbosch, Paarl, Franschhoek, Swartland, Walker Bay, Elgin, Robertson and others) as PDF and JPG files at `wosa.co.za/multimedia/maps-links`, and SAWIS publishes the production-areas list at `sawis.co.za`. Neither site is reachable from the build sandbox; they were read through the search tool.
