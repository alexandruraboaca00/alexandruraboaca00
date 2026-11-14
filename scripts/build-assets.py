#!/usr/bin/env python3
"""Build original SVG artwork and a looping GIF using librsvg and FFmpeg.

Requirements: Python 3, rsvg-convert, ffmpeg. No network or Python packages.
The temporary frame directory is removed automatically. No external image service.
"""

import math
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MONO = "'DejaVu Sans Mono',monospace"
SANS = "'DejaVu Sans',sans-serif"


def header(frame=0, total=72):
    phase = frame / total
    angle = phase * 360 - 90
    cx, cy, radius = 946, 205, 132
    sweep = []
    for offset in range(0, 43, 3):
        a = math.radians(angle - offset)
        b = math.radians(angle - offset - 3)
        sweep.append(
            f'<path d="M{cx} {cy} L{cx+radius*math.cos(a):.2f} '
            f'{cy+radius*math.sin(a):.2f} A{radius} {radius} 0 0 0 '
            f'{cx+radius*math.cos(b):.2f} {cy+radius*math.sin(b):.2f} Z" '
            f'fill="#67e8c4" opacity="{0.12*(1-offset/45):.3f}"/>'
        )
    a = math.radians(angle)
    tipx, tipy = cx + radius * math.cos(a), cy + radius * math.sin(a)
    ticks = []
    for tick in range(60):
        a = math.radians(tick * 6)
        r0, r1 = (145, 154) if tick % 5 == 0 else (149, 153)
        ticks.append(
            f'<path d="M{cx+r0*math.cos(a):.2f} {cy+r0*math.sin(a):.2f} '
            f'L{cx+r1*math.cos(a):.2f} {cy+r1*math.sin(a):.2f}"/>'
        )
    nodes = []
    for j, (x, y) in enumerate([(875, 123), (1038, 174), (983, 306), (843, 250)]):
        node_phase = (phase + j * 0.23) % 1
        nodes.append(
            f'<circle cx="{x}" cy="{y}" r="{5+node_phase*19:.2f}" '
            f'fill="none" stroke="#67e8c4" opacity="{0.38*(1-node_phase):.3f}"/>'
            f'<circle cx="{x}" cy="{y}" r="3.3" fill="#67e8c4"/>'
        )
    cursor_opacity = 1 if frame % 16 < 10 else 0.2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430" role="img" aria-labelledby="title desc">
  <title id="title">Alexandru — Desarrollo, Linux y ciberseguridad</title>
  <desc id="desc">Una terminal oscura junto a un radar con un escudo. Ilustración decorativa original.</desc>
  <defs>
    <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0a111c"/><stop offset="1" stop-color="#0c1c26"/></linearGradient>
    <radialGradient id="halo"><stop stop-color="#1f635c" stop-opacity=".22"/><stop offset="1" stop-color="#1f635c" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#b1d4d9" stroke-opacity=".042"/></pattern>
    <linearGradient id="line"><stop stop-color="#67e8c4" stop-opacity="0"/><stop offset=".5" stop-color="#67e8c4"/><stop offset="1" stop-color="#67e8c4" stop-opacity="0"/></linearGradient>
    <clipPath id="bounds"><rect width="1200" height="430" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#bounds)">
    <rect width="1200" height="430" fill="url(#bg)"/>
    <rect width="1200" height="430" fill="url(#grid)"/>
    <ellipse cx="946" cy="205" rx="290" ry="250" fill="url(#halo)"/>
    <path d="M714 0V430" stroke="#b1d4d9" stroke-opacity=".07"/>
    <path d="M0 381H1200" stroke="#b1d4d9" stroke-opacity=".08"/>
    <path d="M35 58V34H59M1141 34H1165V58M35 346V369H59M1141 369H1165V346" fill="none" stroke="#67e8c4" stroke-opacity=".35"/>
    <g font-family="{MONO}" font-size="13" letter-spacing="2" fill="#8da7b3">
      <text x="65" y="57">PERSONAL LAB</text>
      <text x="1133" y="57" text-anchor="end">SYSTEMS / SECURITY</text>
    </g>
    <g font-family="{SANS}">
      <text x="64" y="161" font-size="76" font-weight="700" letter-spacing="-3" fill="#eff5f7">Alexandru<tspan fill="#67e8c4">.</tspan></text>
      <text x="67" y="205" font-family="{MONO}" font-size="17" fill="#90a5b3">@alexandruraboaca00</text>
      <text x="65" y="269" font-size="28" fill="#c5d5dc">Código, sistemas y curiosidad.</text>
    </g>
    <g font-family="{MONO}" font-size="12" letter-spacing="1.2">
      <rect x="65" y="301" width="133" height="32" rx="5" fill="#67e8c4" fill-opacity=".08" stroke="#67e8c4" stroke-opacity=".24"/>
      <text x="131.5" y="322" text-anchor="middle" fill="#8debd3">DESARROLLO</text>
      <rect x="210" y="301" width="87" height="32" rx="5" fill="#67e8c4" fill-opacity=".08" stroke="#67e8c4" stroke-opacity=".24"/>
      <text x="253.5" y="322" text-anchor="middle" fill="#8debd3">LINUX</text>
      <rect x="309" y="301" width="169" height="32" rx="5" fill="#67e8c4" fill-opacity=".08" stroke="#67e8c4" stroke-opacity=".24"/>
      <text x="393.5" y="322" text-anchor="middle" fill="#8debd3">CIBERSEGURIDAD</text>
    </g>
    <g fill="none" stroke="#67e8c4">
      <circle cx="946" cy="205" r="132" stroke-opacity=".25"/>
      <circle cx="946" cy="205" r="96" stroke-opacity=".14"/>
      <circle cx="946" cy="205" r="60" stroke-opacity=".13"/>
      <path d="M790 205H1102M946 49V361" stroke-opacity=".13"/>
      <g stroke-opacity=".3">{''.join(ticks)}</g>
    </g>
    {''.join(sweep)}
    <path d="M946 205L{tipx:.2f} {tipy:.2f}" stroke="#67e8c4" stroke-width="1.5" opacity=".75"/>
    {''.join(nodes)}
    <path d="M946 151L984 166V201C984 227 969 247 946 258C923 247 908 227 908 201V166Z" fill="#0c2029" stroke="#81f0d0" stroke-width="2"/>
    <path d="M935 198V186A11 11 0 0 1 957 186V198" fill="none" stroke="#81f0d0" stroke-width="2.5"/>
    <rect x="930" y="198" width="32" height="26" rx="4" fill="#67e8c4" fill-opacity=".12" stroke="#81f0d0" stroke-width="1.8"/>
    <circle cx="946" cy="209" r="2.5" fill="#81f0d0"/>
    <path d="M946 211V216" stroke="#81f0d0" stroke-width="2"/>
    <g font-family="{MONO}" font-size="12" fill="#8da7b3" letter-spacing="1.2">
      <text x="946" y="354" text-anchor="middle">BUILD · EXPLORE · LEARN</text>
      <text x="65" y="411"><tspan fill="#67e8c4">~ $</tspan> learning by building</text>
      <rect x="273" y="398" width="7" height="15" fill="#67e8c4" opacity="{cursor_opacity}"/>
      <text x="1133" y="411" text-anchor="end" fill="#637f8d">DEVELOPMENT / SYSTEMS / SECURITY</text>
    </g>
  </g>
  <rect x=".5" y=".5" width="1199" height="429" rx="21.5" fill="none" stroke="#b1d4d9" stroke-opacity=".13"/>
</svg>'''


def project_card(kind):
    cv = kind == "cvpass"
    accent = "#83baff" if cv else "#67e8c4"
    title = "CVPass" if cv else "FBI Theme"
    index = "01 / DESKTOP APP" if cv else "02 / LINUX CUSTOMIZATION"
    label = "TUS DATOS, EN TU EQUIPO" if cv else "UN LOGIN CON PERSONALIDAD"
    if cv:
        art = '''<rect x="347" y="52" width="171" height="114" rx="7" fill="#101f32" stroke="#83baff" stroke-opacity=".45"/>
        <path d="M347 74H518M393 74V166" stroke="#83baff" stroke-opacity=".22"/>
        <circle cx="360" cy="63" r="2.5" fill="#83baff"/><circle cx="369" cy="63" r="2.5" fill="#83baff" opacity=".4"/>
        <path d="M359 91H381M359 104H376M359 117H380" stroke="#83baff" stroke-opacity=".35" stroke-width="3"/>
        <rect x="412" y="86" width="75" height="92" rx="3" fill="#d3e5f8"/>
        <circle cx="430" cy="103" r="7" fill="#3c608b"/>
        <path d="M444 100H475M444 106H464M423 121H475M423 129H475M423 141H461M423 149H475M423 157H470" stroke="#536f90" stroke-width="2.5"/>
        <circle cx="504" cy="159" r="20" fill="#112e40" stroke="#83baff" stroke-opacity=".4"/>
        <path d="M495 159L501 165L513 153" fill="none" stroke="#83baff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>'''
    else:
        art = '''<rect x="347" y="52" width="171" height="114" rx="7" fill="#0c2328" stroke="#67e8c4" stroke-opacity=".45"/>
        <path d="M347 74H518" stroke="#67e8c4" stroke-opacity=".22"/>
        <circle cx="360" cy="63" r="2.5" fill="#67e8c4"/><circle cx="369" cy="63" r="2.5" fill="#67e8c4" opacity=".4"/>
        <g fill="none" stroke="#67e8c4" stroke-opacity=".18"><circle cx="433" cy="120" r="34"/><ellipse cx="433" cy="120" rx="16" ry="34"/><path d="M399 120H467M404 104H462M404 136H462"/></g>
        <path d="M403 141L429 115L452 123L476 96" fill="none" stroke="#67e8c4" stroke-opacity=".55"/>
        <g fill="#67e8c4"><circle cx="403" cy="141" r="3"/><circle cx="429" cy="115" r="3"/><circle cx="452" cy="123" r="3"/><circle cx="476" cy="96" r="3"/></g>
        <rect x="387" y="150" width="92" height="29" rx="4" fill="#0b1b24" stroke="#67e8c4" stroke-opacity=".5"/>
        <path d="M399 160L404 164L399 168M411 168H423" fill="none" stroke="#67e8c4" stroke-width="2"/>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="215" viewBox="0 0 560 215" role="img" aria-labelledby="title">
  <title id="title">{title} — {label.lower()}</title>
  <defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0c1521"/><stop offset="1" stop-color="#101f2c"/></linearGradient></defs>
  <rect x=".5" y=".5" width="559" height="214" rx="12" fill="url(#bg)" stroke="#28404d"/>
  <path d="M26 34H44" stroke="{accent}" stroke-width="2"/>
  <text x="54" y="38" font-family="{MONO}" font-size="10" letter-spacing="1.3" fill="#a1b4be">{index}</text>
  <text x="27" y="110" font-family="{SANS}" font-size="42" font-weight="700" letter-spacing="-1.5" fill="#eff5f7">{title}</text>
  <text x="29" y="151" font-family="{MONO}" font-size="10.5" letter-spacing=".8" fill="{accent}">{label}</text>
  <path d="M29 184H316" stroke="#28404d"/>
  {art}
</svg>'''


def stack():
    labels = [("TypeScript", "#83baff", 192), ("React", "#70c9de", 144),
              ("Electron", "#93ced1", 176), ("SQLite", "#83baff", 152),
              ("Qt / QML", "#91d5a0", 176), ("Linux", "#e0c285", 144),
              ("Git", "#dc9d8d", 144)]
    x, parts = 0, []
    for label, color, width in labels:
        parts.append(f'<rect x="{x+.5}" y=".5" width="{width-12}" height="53" rx="7" fill="#0d1822" stroke="#253946"/>')
        parts.append(f'<circle cx="{x+21}" cy="27" r="3.5" fill="{color}"/>')
        parts.append(f'<text x="{x+35}" y="33" font-family="{MONO}" font-size="17" fill="#cddbe2">{label}</text>')
        x += width
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1117" height="55" viewBox="0 0 1117 55" role="img" aria-label="TypeScript, React, Electron, SQLite, Qt y QML, Linux, Git">{"".join(parts)}</svg>\n'


def main():
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "header-static.svg").write_text(header(9), encoding="utf-8")
    (ASSETS / "cvpass.svg").write_text(project_card("cvpass"), encoding="utf-8")
    (ASSETS / "fbi-theme.svg").write_text(project_card("fbi"), encoding="utf-8")
    (ASSETS / "stack.svg").write_text(stack(), encoding="utf-8")
    for slug, label, color in [
        ("typescript", "TypeScript", "#83baff"), ("react", "React", "#70c9de"),
        ("electron", "Electron", "#93ced1"), ("sqlite", "SQLite", "#83baff"),
        ("qt-qml", "Qt / QML", "#91d5a0"), ("linux", "Linux", "#e0c285"),
        ("git", "Git", "#dc9d8d"),
    ]:
        width = len(label) * 7.3 + 34
        badge = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="30" viewBox="0 0 {width} 30" role="img" aria-label="{label}"><rect x=".5" y=".5" width="{width-1}" height="29" rx="5" fill="#0d1822" stroke="#253946"/><circle cx="14" cy="15" r="2.5" fill="{color}"/><text x="24" y="19" font-family="{MONO}" font-size="12" fill="#cddbe2">{label}</text></svg>\n'
        (ASSETS / f"tech-{slug}.svg").write_text(badge, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="alexandru-profile-") as temp:
        frame_dir = Path(temp)
        for i in range(72):
            svg = frame_dir / "frame.svg"
            svg.write_text(header(i), encoding="utf-8")
            subprocess.run(["rsvg-convert", "-o", str(frame_dir / f"{i:03d}.png"), str(svg)], check=True)
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", "12",
            "-i", str(frame_dir / "%03d.png"), "-filter_complex",
            "[0:v]fps=10,scale=1000:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=full[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
            "-gifflags", "+transdiff", "-loop", "0", str(ASSETS / "header.gif"),
        ], check=True)
    print("Built original SVG artwork and a 6-second looping GIF.")


if __name__ == "__main__":
    main()
