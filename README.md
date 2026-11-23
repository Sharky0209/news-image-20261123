# news-image-20261123

[![news-image-20261123](https://img.shields.io/badge/make.fun-news--image--20261123-blue)](https://github.com/Sharky0209/news-image-20261123)

Sum up 23 November 2026's world news in one image. A 1024x1024
newspaper-style front page: six verified stories from Monday 23 November
2026, plus an ALSO TODAY footer. Built for the make.fun
news-image-20261123 contest ($100, deadline 25 November 2026 08:00 Beijing time).

## Stories

1. **MARKETS — KOSPI dives over 5% intraday as Seoul vows to act.**
   South Korea's benchmark falls about 5% in Monday's tech sell-off; the
   finance minister says a contingency plan is ready.
2. **EUROPE — Kyiv region mourns as Dymer rescue goes on.** The Kyiv region
   marks a day of mourning after a drone strike collapses part of a
   five-storey block in Dymer; rescuers pull a 79-year-old woman out alive
   as the search goes on.
3. **DISASTER — Indonesia says 24 dead in factory fire.** Indonesia says 24
   people died in a candy factory fire in Banten; rescuers search the
   wreckage for about 30 still missing.
4. **SECURITY — NATO meets over missiles in Polish airspace.** NATO's council
   meets in Brussels after Russian missiles crossed into Poland; Warsaw
   seeks stronger air defences on the eastern flank.
5. **DIPLOMACY — Nepal PM holds talks with Modi in Delhi.** Balendra Shah
   meets Narendra Modi on his first bilateral trip abroad; the leaders
   launch a new Ayodhya–Janakpur train.
6. **POLITICS — Burnham to defend 'landmark' EU deal.** The UK prime
   minister is to tell MPs the Brussels deal is a choice between "a broken
   status quo or change"; opponents dispute his £17bn growth claim.

Also today: Ganges talks continue in Dhaka; Seoul eases buyback limits;
Badenoch set to attack the EU deal at CBI.

Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, Al Jazeera.

## Build and run

Draw the image (requires Pillow and the DejaVu fonts):

```sh
python3 build_entry.py
```

This writes a deterministic 1024x1024 PNG to `/output/entry.png`.

Run the contest entry point (standard library only — it just copies the
pre-built image):

```sh
python3 main.py
```

This copies `entry.png` next to the script into `/output/entry.png` and
verifies the copy byte-for-byte (SHA-256).

## Verification

The build is deterministic: no network, no randomness, no clock, no
environment input. Re-running the build must produce the same file:

```sh
python3 build_entry.py && sha256sum /output/entry.png
python3 build_entry.py && sha256sum /output/entry.png
```

Both runs must print the same SHA-256, the image must be 1024x1024 and
under 1 MiB. The entry point is standard-library-only (`hashlib`, `os`,
`shutil`); run it from another directory to confirm:

```sh
cd /tmp && python3 -S /path/to/repo/main.py
```

## License

MIT — see [LICENSE](LICENSE).
