#!/usr/bin/env python3
"""Bake rounded corners into README images.

GitHub strips CSS from READMEs, so border-radius has to live in the pixels.
Still images and animations (GIF in, animated WebP out) both come out as WebP
with an anti-aliased alpha mask. Requires Pillow.

    python3 scripts/round_corners.py banner.png assets/images/welcome-banner.webp --radius 36
    python3 scripts/round_corners.py demo.gif assets/images/hydranet-demo.webp --radius 11

Radius is in source pixels: the README column is ~850px wide, so scale the
on-screen radius (12px) by source_width / 850.
"""
import argparse

from PIL import Image, ImageDraw, ImageSequence


def rounded_mask(size, radius, supersample=4):
    w, h = size
    s = supersample
    mask = Image.new("L", (w * s, h * s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * s - 1, h * s - 1), radius * s, fill=255)
    return mask.resize(size, Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("out", help="output path, .webp")
    ap.add_argument("--radius", type=int, required=True, help="corner radius in source pixels")
    ap.add_argument("--quality", type=int, default=82)
    args = ap.parse_args()

    src = Image.open(args.src)
    mask = rounded_mask(src.size, args.radius)

    frames, durations = [], []
    for frame in ImageSequence.Iterator(src):
        durations.append(frame.info.get("duration", 100))
        rgba = frame.convert("RGBA")
        rgba.putalpha(mask)
        frames.append(rgba)

    if len(frames) == 1:
        frames[0].save(args.out, quality=args.quality, method=6)
    else:
        frames[0].save(args.out, save_all=True, append_images=frames[1:], duration=durations,
                       loop=0, quality=args.quality, method=4, minimize_size=True)
    print(f"{args.out}: {len(frames)} frame(s), radius {args.radius}px")


if __name__ == "__main__":
    main()
