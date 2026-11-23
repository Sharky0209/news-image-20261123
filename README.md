# news-image-20261123

[![news-image-20261123](https://img.shields.io/badge/make.fun-news--image--20261123-blue)](https://github.com/Sharky0209/news-image-20261123)

Sum up 23 November 2026's world news in one image — six stories from a
single Monday, drawn as a 1024x1024 newspaper front page.

## Stories

1. **MARKETS — KOSPI dives 5% as Seoul vows to act.** South Korea's
   benchmark falls about 5% in Monday's tech sell-off; the finance
   minister says a contingency plan is ready.
2. **EUROPE — Kyiv region mourns as Dymer rescue goes on.** The Kyiv
   region marks a day of mourning after a drone strike collapses part of
   a five-storey block in Dymer; rescuers pull a 79-year-old woman out
   alive as the search goes on.
3. **DISASTER — Indonesia confirms 24 dead in factory fire.** Indonesia
   confirms 24 people died in a candy factory fire in Banten; rescuers
   search the wreckage for about 30 still missing.
4. **SECURITY — NATO meets over missiles in Polish airspace.** NATO's
   council meets in Brussels after Russian missiles and a drone crossed
   into Poland; Warsaw seeks stronger air defences on the eastern flank.
5. **DIPLOMACY — Nepal PM holds talks with Modi in Delhi.** Balendra
   Shah meets Narendra Modi on his first bilateral trip abroad; the
   leaders launch a new Ayodhya–Janakpur train.
6. **POLITICS — Burnham defends 'landmark' EU deal.** The UK prime
   minister tells MPs the Brussels deal is a choice between "a broken
   status quo or change"; opponents dispute his £17bn growth claim.

Also today: Ganges talks continue in Dhaka; Seoul eases buyback limits;
Badenoch to attack the EU deal at CBI.

Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, Al Jazeera.
Every story was checked against reporting dated Monday 23 November 2026:
each one is an event that happened that day, or was first reported that
day — not a reprint of a 22 November story.

## Build and run

```sh
python3 build_entry.py   # draws /output/entry.png (1024x1024 PNG)
python3 main.py          # copies entry.png to /output/entry.png
```

`build_entry.py` uses Pillow and the system DejaVu fonts and is fully
deterministic — no network, no randomness, no clock. `main.py` is the
submission entry point and uses only the Python standard library
(`os` and `shutil`): it copies the pre-built `entry.png` next to it
into `/output/entry.png` and verifies the copy by size.

## Verification

Each story was checked against reporting dated Monday 23 November 2026
before drawing: the KOSPI's Monday ~5% fall and the finance minister's
Monday press conference (CNA/Yonhap); the Kyiv region's Monday day of
mourning and the 79-year-old woman pulled out alive early Monday
(UNN/Kyiv Independent/CNA); Indonesia's Monday confirmation of 24 dead
in the Banten factory fire (Reuters/CNA); the North Atlantic Council's
Monday meeting in Brussels over the 20 November Polish airspace
incursion (New Voice of Ukraine/Kyiv Post/EU Today); Balendra Shah's
Monday talks with Narendra Modi at Hyderabad House and the joint
Ayodhya–Janakpur train launch (ETV Bharat/Himalayan Times); and Andy
Burnham's Monday statement to MPs on the Friday EU deal, with his
£17bn claim disputed by opponents (BBC/London24News).

Determinism check: run `python3 build_entry.py` twice — both runs
produce the same sha256 for `/output/entry.png` (1024x1024, under
1 MiB). Entry-point check: from another directory run
`python3 -S repo/main.py` and confirm `/output/entry.png` is
byte-identical to `repo/entry.png`.

## License

MIT — see `LICENSE`.
