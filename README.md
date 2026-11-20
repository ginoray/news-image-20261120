[![make.fun bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ginoray/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ginoray/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World Today — 20 November 2026

Entry for the make.fun bounty [news-image-20261120](https://make.fun/bounty/news-image-20261120):
sum up the world news of Friday 20 November 2026 in one image.

The poster — "THE WORLD TODAY" — is painted ahead of time by
`tools/build_image.py` driving `render.py` (Pillow), and the finished PNG
is sealed into `assets/entry.png.b64`. `main.py` itself uses only the
Python standard library: it decodes the sealed image, verifies the PNG
(signature, chunk checksums, dimensions, size), and writes it to
`/output/entry.png` (1024×1024, deterministic: two runs, same bytes).
The lead is Anthropic's record $81.3B IPO; a feature band
covers GTA VI passing $2 billion in 24 hours; six cards and five briefs
cover the ICJ's Rohingya genocide ruling, the Shenzhen trilateral's peace
declaration, the Houthi strikes on Saudi Arabia, the Hormuz tanker fire,
the Kyiv missile strikes, Taiwan's market rout, and more. Every story was
reported on the day and cross-checked against at least two independent
reports.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Requires Python 3 (standard library only) to run. Pillow is needed only
to repaint the poster with `tools/build_image.py`. No network access is
used.

## License

MIT — see `LICENSE`.
