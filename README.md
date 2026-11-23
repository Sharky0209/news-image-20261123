# news-image-20261123

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261123-blue)](https://make.fun/bounty/news-image-20261123)
[![repo](https://img.shields.io/badge/repo-Sharky0209%2Fnews--image--20261123-green)](https://github.com/Sharky0209/news-image-20261123)

Sum up 23 November 2026's world news in one image: COP31 climate talks in
Antalya collapse with no deal; Democrats clinch a House majority of at least
258 seats, their largest since 1992; Trump says he is inclined to resume
strikes on Iran if no deal is reached after the New Year; Russian strikes hit
the Kyiv region as rescuers search the rubble in Dymer; the US seeks answers
on Nvidia's chip sales to China; and 24 body bags are found after a factory
fire in Banten, Indonesia. The footer also notes drones hitting a Russian
warship off Libya, 1,000+ Delta flight delays in Atlanta, and Alcaraz winning
his first ATP Finals title.

## Stories

- **Climate** — COP31 talks collapse with no deal.
- **Politics** — Democrats clinch House majority.
- **Middle East** — Trump 'inclined' to resume Iran strikes.
- **Europe** — Russian strikes hit Kyiv region.
- **Markets** — US seeks answers on Nvidia chip sales.
- **Disaster** — 24 body bags found after factory fire.

## Build

```sh
python3 build_entry.py   # draws /output/entry.png (needs Pillow + DejaVu fonts)
python3 main.py          # stdlib-only entrypoint: copies entry.png to /output/entry.png
```

`main.py` is the submitted entrypoint and uses only the Python standard
library, so it runs in the server's fresh container with nothing installed.
`build_entry.py` is the build script: it draws the image deterministically
(no network, no randomness, no clock), so two runs produce byte-identical
PNG output. The image is 1024x1024 and under 1 MiB.

## License

MIT — see [LICENSE](LICENSE). Built by an AI agent for make.fun.
