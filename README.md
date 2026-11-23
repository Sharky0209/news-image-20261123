# news-image-20261123

[![news-image-20261123](https://img.shields.io/badge/make.fun-news--image--20261123-blue)](https://github.com/Sharky0209/news-image-20261123)

Sum up 23 November's world news in one image: six verified stories from
Monday 23 November 2026, laid out as a single 1024x1024 front page.

## Stories

1. **Climate — COP31 talks collapse with no deal.** UN climate talks in
   Antalya end with no deal after record overtime; fossil-fuel language
   is blocked and the EU rejects the final draft.
2. **Politics — Democrats clinch House majority.** Democrats win at
   least 258 House seats, their largest majority since 1992, after a
   North Carolina win; four races are still uncalled.
3. **Middle East — Trump "inclined" to resume Iran strikes.** Trump
   tells Fox News he is inclined to resume strikes after the New Year
   if no deal is reached, as talks with Tehran stall.
4. **Europe — Russian strikes hit Kyiv region.** An overnight drone
   strike collapses part of a five-storey block in Dymer as rescuers
   search the rubble; the region marks a day of mourning.
5. **Markets — US seeks answers on Nvidia chip sales.** Treasury chief
   Bessent says the US wants answers on Nvidia's chip sales to China
   and who ran compliance, after its ex-CEO resigned.
6. **Disaster — 24 body bags found after factory fire.** Rescuers
   recover remains in 24 body bags from a candy factory fire in
   Banten, Indonesia; the toll is unclear as the search resumes Monday.

Also today: Libya — drones hit a Russian warship; Delta delays 1,000+
Atlanta flights; Alcaraz wins his first ATP Finals title.

Sources: CNN, Reuters, AP, Xinhua, SCMP, Al Jazeera.

## Layout

A single 1024x1024 front page on a paper background: a navy masthead
with the "WORLD NEWS" title, a gold rule, and the date line; six story
cards in a 2x3 grid (white, rounded, red top band, label + headline +
body); and a navy footer with three "Also today" items on one line and
the sources line. Body text shrinks (20pt down to 16pt) rather than
truncating when a story runs long.

## Build and run

Requires Python 3 with Pillow installed, and the DejaVu fonts
(present at `/usr/share/fonts/truetype/dejavu` on Debian/Ubuntu).

```sh
python3 build_entry.py   # renders the image to /output/entry.png
python3 main.py          # stdlib-only entry point: copies entry.png to /output/entry.png
```

`build_entry.py` is fully deterministic: no network, no randomness, no
clock, no environment input. Running it twice produces byte-identical
output. `main.py` uses only the Python standard library (`os` and
`shutil`) and verifies the copy by size.

## License

MIT. See [LICENSE](LICENSE).
