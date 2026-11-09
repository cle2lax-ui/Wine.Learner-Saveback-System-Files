# COMING UP: trailer Reel caption (draft)
30 s · 1080 x 1920 · American English · DRAFT for Steve's review · post it BEFORE the first of the four posts, in the order shown

---

## CAPTION: paste as-is

Coming up on the page over the next two weeks:

The Field Guide: Climate's Impact on Wine, 15 slides on what shapes every vintage.
Guess the Wine Region: same latitude, different ocean. Can you name it?
Five Fascinating Facts about climate change and wine.
What Am I Drinking? A mystery red that spent six years in barrel.

And then a new arc: Wines of South Africa.

Follow so you never miss one.

#wine #winestudy #WSETDiploma #wineeducation #winetasting

Video: South Africa tease backdrop, Franschhoek vineyard, South African Tourism (CC BY 2.0), via Wikimedia Commons.

---

## NOTES (not for the caption)

**What it shows.** The four locked Arc 4 posts, in the planned posting order (Field Guide, Guess the Wine Region, Five Facts, What Am I Drinking?), each as its real page; then a six-second tease of Arc 5. The cards are the finished pages, so nothing in the trailer is a promise the posts do not keep.

**The tease is the one thing that is not a published post.** It comes from the Arc 5 plan (`arc5/ARC5_SOUTH_AFRICA_PLAN.md`: two currents and a wind; Cape Cabernet blends; Cap Classique) and is a single scene, 22-28 s. To drop it, delete that row from `SCENE_TABLE` in `trailer_reel.py` and the two chunks of audio events that name it; the other beats keep their bars. If the plan changes (the Field Guide title, the order), the three bullets are three strings in `s_tease`.

**If the posting order changes,** reorder `SCENE_TABLE`; the progress strip and the audio follow the table.

**No dates on screen, by design.** "The next two weeks" stays true only if the posts go out in that window; change the line (`s_hook`) if the schedule moves.

**Audio.** Original and synthesized (-14.0 LUFS, -3.6 dBFS peak); every effect is placed from the scene table (the impact on each cut starts at 0.00 ms, measured by subtracting a silent-impact build). Instagram's audio library can replace it at upload.

**Hashtags: five.** `#WSETDiploma` and `#winestudy` match the rest of the page.
