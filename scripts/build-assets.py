#!/usr/bin/env python3
"""Render the terminal/code-rain banner. Requires rsvg-convert and ffmpeg.

Only Python's standard library is used. Frames are generated in a temporary
directory and removed automatically. Run from any directory.
"""

import random
import subprocess
import tempfile
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
FRAMES = 64
FPS = 8
MONO = "'DejaVu Sans Mono',monospace"


def header(frame=0):
    rng = random.Random(666)
    rain = []
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ<>/{}[]:;=+-"
    shades = ["#075020", "#08752b", "#0a9c37", "#16ca4c", "#a0fcb5"]
    for col in range(56):
        start = rng.randrange(16)
        speed = rng.choice([1, 1, 2])
        length = rng.randrange(5, 12)
        letters = [rng.choice(alphabet) for _ in range(16)]
        head = (start + frame * speed / 4) % 16
        for offset in range(length):
            row = (head - offset) % 16
            y = 54 + row * 17
            shade = 4 if offset == 0 else max(0, 3 - offset // 2)
            char = letters[(int(head) - offset) % 16]
            rain.append(f'<text x="{9+col*16}" y="{y:.2f}" fill="{shades[shade]}">{escape(char)}</text>')
    cursor = '<rect x="303" y="235" width="9" height="18" fill="#7aef96"/>' if frame % 8 < 5 else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="320" viewBox="0 0 900 320" role="img" aria-labelledby="title desc">
<title id="title">Alexandru — ciberseguridad, Linux e IA</title>
<desc id="desc">Terminal negra con columnas de caracteres verdes cayendo al estilo Matrix.</desc>
<defs><clipPath id="screen"><rect x="1" y="39" width="898" height="280"/></clipPath></defs>
<rect x=".5" y=".5" width="899" height="319" rx="5" fill="#020704" stroke="#1b3e25"/>
<path d="M1 38H899" stroke="#1b3e25"/>
<g font-family="{MONO}" font-size="12" fill="#71937a">
<text x="19" y="24">~/projects</text><text x="880" y="24" text-anchor="end">alexandruraboaca00</text>
</g>
<g clip-path="url(#screen)" font-family="{MONO}" font-size="13">{''.join(rain)}</g>
<rect x="24" y="80" width="493" height="203" fill="#020704" fill-opacity=".96"/>
<path d="M24 80H517M24 283H517" stroke="#14381e"/>
<g font-family="{MONO}">
<text x="43" y="116" font-size="15" fill="#4cbd6b">alexandru@linux:~$ whoami</text>
<text x="40" y="175" font-size="43" fill="#b4f7c5">Alexandru</text>
<text x="43" y="211" font-size="16" fill="#78d28e">ciberseguridad / linux / IA</text>
<text x="43" y="249" font-size="13" fill="#4cbd6b">&gt; TFG / reels-knowledge / CVPass</text>
</g>
{cursor}
</svg>'''


def main():
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "header-static.svg").write_text(header(12), encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="alexandru-matrix-") as tmp:
        frames = Path(tmp)
        for i in range(FRAMES):
            svg = frames / "frame.svg"
            svg.write_text(header(i), encoding="utf-8")
            subprocess.run(["rsvg-convert", "-o", str(frames / f"{i:03d}.png"), str(svg)], check=True)
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(FPS),
            "-i", str(frames / "%03d.png"), "-filter_complex",
            "[0:v]split[a][b];[a]palettegen=max_colors=48[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
            "-gifflags", "+transdiff", "-loop", "0", str(ASSETS / "header.gif"),
        ], check=True)
    print("Built terminal banner: 64 frames, 8 seconds, seamless code-rain loop.")


if __name__ == "__main__":
    main()
