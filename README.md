# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Sharky0209/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Sharky0209/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Sum up 23 November 2026's world news in one image: six verified stories
from Monday 23 November 2026, laid out as a single 1024x1024 newspaper-style
graphic. The entry is the PNG at `entry.png`.

## Stories

1. **MARKETS — KOSPI dives over 5% intraday as Seoul vows to act.**
   South Korea's benchmark falls about 5% in Monday's tech sell-off; the
   finance minister says a contingency plan is ready.
2. **EUROPE — Kyiv region mourns as Dymer rescue goes on.** The Kyiv region
   marks a day of mourning after a drone strike collapses part of a
   five-storey block in Dymer; rescuers pull a 79-year-old woman out alive
   as the search goes on.
3. **DISASTER — Indonesia adviser says 24 dead in factory fire.**
   Presidential adviser Said Iqbal puts the toll at 24; rescuers continue
   searching the wreckage for missing workers.
4. **SECURITY — Kim says North Korea seeks security, not supremacy.** Kim
   Jong-un tells foreign envoys Pyongyang seeks neither hegemony nor
   expansion and defends its arms build-up as self-defence, in remarks
   reported by state media on Monday. The credentials ceremony itself was
   held on Sunday; KCNA reported it on Monday.
5. **DIPLOMACY — Nepal PM holds talks with Modi in Delhi.** Balendra Shah
   meets Narendra Modi on his first bilateral trip abroad; the leaders
   launch a new Ayodhya–Janakpur train.
6. **POLITICS — Burnham to defend 'landmark' EU deal.** The UK prime
   minister is to tell MPs the Brussels deal is a choice between "a broken
   status quo or change"; opponents dispute his £17bn growth claim.

Also today: Ganges talks continue in Dhaka; Seoul to ease buyback limits;
Badenoch set to attack the EU deal at CBI.

Sources: Yonhap, Reuters, CNA, BBC, Kyiv Independent, Al Jazeera.

## Build / run

Requires Python 3 and Pillow for the drawing step.

```sh
python3 build_entry.py   # draws /output/entry.png (1024x1024, deterministic)
python3 main.py          # copies entry.png to /output/entry.png (stdlib only)
```

`build_entry.py` uses only Pillow and the system DejaVu fonts, with no
network, randomness, clock or environment input, so repeated runs produce
identical bytes. `main.py` uses only the Python standard library (`os`,
`shutil`): it finds the `entry.png` next to itself, checks it is a PNG,
copies it to `/output/entry.png`, and checks the copy's size matches.

## Verification

Two consecutive `python3 build_entry.py` runs produced identical bytes:
SHA-256 `949ad398557536f0a869094125cac30f2991ebacf3f534b6df0460328fac3b4c`,
144,763 bytes, 1024x1024. Running `python3 -S main.py` from another
directory reproduced the same bytes in `/output/entry.png`.

## License

MIT — see `LICENSE`.
