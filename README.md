# GTA 6 meme — make.fun bounty `gta6-meme-x-01`

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/sopiahusen42/gta6-meme-makefun/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard)
[![reward](https://make.fun/badge/gta6-meme-x-01/sopiahusen42/gta6-meme-makefun/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

A GTA 6 launch-week meme for the make.fun bounty
[gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01) ("Post a GTA 6 meme on X").
The judged picture is `meme.png`; the post text is in `caption.txt`.

## The meme

Vice City sunset, Leonida energy: neon pink/orange sky, sliced synthwave sun,
art-deco hotel strip with a glowing **make.fun** rooftop sign, palm silhouettes
and ocean reflection. The official make.fun ghost (from the press kit's
`mark-1024.png`) lounges large in a striped deck chair beside a retro TV stuck
at **GTA VI — INSTALLING… 99%**.

The joke: **13 YEARS OF WAITING** … **MY make.fun AGENT GOT PAID IN 13 MINUTES**.
GTA 6 took 13 years since GTA V; a make.fun bounty paid out while the game was
still installing. People and their AI agents earn real money on make.fun.

The scene is drawn with Pillow (`meme_gen.py`, vector shapes) and the official
ghost mark is composited in. Display font: Archivo Black (OFL, bundled in
`fonts/`).

## Run

Node 22.18+, stdlib only:

```sh
mkdir -p out
MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` reads `POST.json` from the repository and copies it byte-for-byte to
`$MAKEFUN_OUTPUT_DIR/POST.json` (fallback `/output/POST.json`).

To re-render the meme: `python3 meme_gen.py <path-to-mark-1024.png> meme.png`
(needs Pillow).

## The post text

`caption.txt` holds the text to post on X with `meme.png` attached (216 chars,
all required tokens included — the bounty link, `@makefunai`, and the play code
`makefun-pouch-bow-racket`):

> 13 years of waiting and GTA 6 is STILL installing 💀 my AI agent got paid in
> 13 minutes on make.fun — people + agents earn real money there 👻💸
> https://make.fun/bounty/gta6-meme-x-01 @makefunai makefun-pouch-bow-racket

## Status and remaining steps

`POST.json` currently holds `{"url": "PENDING"}` — the post on X is made after
this repository is built. Before submission:

1. Post `meme.png` + `caption.txt` from the public X account, inside the bounty
   window (opened 2026-11-19T14:00Z, deadline 2026-11-23T14:00Z).
2. Replace `PENDING` in `POST.json` with the post's URL
   (`https://x.com/<handle>/status/<id>`) and commit.
3. Run `main.ts` (above), bundle the transcripts, run the kit's `check`, then
   `submit`.

## License

MIT — see `LICENSE`. The make.fun ghost mark belongs to make.fun and is used
from its official press kit.
