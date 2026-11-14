#!/usr/bin/env python3
"""Build standalone dark SVG project covers. Screenshots are embedded unchanged.

Uses only the Python standard library. Source URLs are recorded in each SVG.
Reels Knowledge has a flow diagram rather than a GUI screenshot.
"""
import base64
from html import escape
from pathlib import Path
from urllib.request import urlopen

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'previews'
MONO = "'DejaVu Sans Mono',monospace"
SANS = "'DejaVu Sans',sans-serif"


def shell(title, label, subtitle, art, source='Original vector illustration'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="470" viewBox="0 0 800 470" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)} — {escape(subtitle)}</title><desc id="desc">{escape(source)}</desc>
<defs><clipPath id="image"><rect x="24" y="134" width="752" height="296" rx="5"/></clipPath></defs>
<rect x=".5" y=".5" width="799" height="469" rx="9" fill="#080f0c" stroke="#254532"/>
<path d="M24 27H43" stroke="#69d48b" stroke-width="2"/>
<text x="53" y="32" font-family="{MONO}" font-size="12" letter-spacing="1" fill="#8baa94">{escape(label)}</text>
<text x="24" y="79" font-family="{SANS}" font-size="35" font-weight="600" fill="#e0ede4">{escape(title)}</text>
<text x="26" y="108" font-family="{MONO}" font-size="14" fill="#9ab7a3">{escape(subtitle)}</text>
<rect x="24" y="134" width="752" height="296" rx="5" fill="#0d1913"/>
{art}
<text x="26" y="452" font-family="{MONO}" font-size="11" fill="#789783">alexandruraboaca00 / projects</text>
<path d="M746 447H770M762 439L770 447L762 455" fill="none" stroke="#69d48b" stroke-width="1.5"/>
</svg>'''


def screenshot(slug, title, label, subtitle, url, note):
    with urlopen(url, timeout=30) as response:
        encoded = base64.b64encode(response.read()).decode('ascii')
    art = f'<image x="24" y="134" width="752" height="296" preserveAspectRatio="xMidYMid meet" clip-path="url(#image)" href="data:image/png;base64,{encoded}"/>'
    (OUT / f'{slug}.svg').write_text(shell(title, label, subtitle, art, f'{note}. Screenshot source: {url}'),encoding='utf-8')


def reels():
    art = f'''<g font-family="{MONO}">
<path d="M133 262H210M350 262H425M565 262H641" stroke="#447456" stroke-width="2"/>
<g fill="none" stroke="#69d48b" stroke-width="2"><path d="M200 256L208 262L200 268M415 256L423 262L415 268M631 256L639 262L631 268"/></g>
<g fill="#0a120e" stroke="#30583e"><rect x="42" y="206" width="92" height="112" rx="8"/><rect x="210" y="206" width="140" height="112" rx="8"/><rect x="425" y="206" width="140" height="112" rx="8"/><rect x="641" y="206" width="116" height="112" rx="8"/></g>
<rect x="72" y="221" width="32" height="49" rx="4" fill="none" stroke="#78d997" stroke-width="2"/><path d="M83 235L95 243L83 251Z" fill="#78d997"/>
<text x="88" y="296" text-anchor="middle" font-size="15" fill="#dae8df">vídeo</text>
<path d="M232 242V255M242 233V266M252 239V260M262 227V272M272 241V258M282 235V266M292 242V256M302 233V266M312 241V260M322 237V264" stroke="#78d997" stroke-width="2"/>
<text x="280" y="296" text-anchor="middle" font-size="14" fill="#dae8df">audio + frames</text>
<text x="495" y="254" text-anchor="middle" font-size="27" fill="#78d997">IA local</text><text x="495" y="296" text-anchor="middle" font-size="12" fill="#9ab7a3">Whisper / Ollama</text>
<path d="M679 224H707L719 236V273H679Z M706 225V237H718M687 247H710M687 255H710M687 263H702" fill="none" stroke="#78d997" stroke-width="2"/>
<text x="699" y="296" text-anchor="middle" font-size="13" fill="#dae8df">Markdown</text>
<text x="400" y="175" text-anchor="middle" font-size="13" fill="#789783">de un enlace a una nota para Obsidian</text>
<text x="400" y="374" text-anchor="middle" font-size="14" fill="#9ab7a3">transcripción · análisis visual · enlaces · índices</text>
<text x="400" y="410" text-anchor="middle" font-size="11" fill="#789783">ESQUEMA DEL PROCESO</text>
</g>'''
    (OUT / 'reels.svg').write_text(shell('reels-knowledge','02 / VÍDEO → NOTAS','Python · FFmpeg · Whisper · Ollama',art,'Flow diagram based on reels-knowledge/docs/ARCHITECTURE.md. Not a GUI screenshot.'),encoding='utf-8')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    screenshot('tfg','Agentes de IA en CyberBattleSim','01 / TFG EN DESARROLLO','Agentes, simulación y ciberseguridad',
        'https://raw.githubusercontent.com/alexandruraboaca00/TFG-Agentes-IA-CyberBattleSim/main/docs/pruebas/imagenes/primer_baseline_red.png','Real capture of the first baseline; initial project stage')
    reels()
    screenshot('cvpass','CVPass','03 / APLICACIÓN DE ESCRITORIO','Currículums en local, para Linux',
        'https://raw.githubusercontent.com/alexandruraboaca00/cvpass/main/docs/screenshots/editor.png','Real editor screenshot with synthetic demo data')
    screenshot('fbi','FBI Theme','04 / SDDM · QT / QML','Mi pantalla de acceso para Linux',
        'https://raw.githubusercontent.com/alexandruraboaca00/FBI_theme_Login_GUI/main/src/theme/preview.png','Real SDDM greeter screenshot in test mode; fictional credentials')
    print('Built 4 dark project previews.')


if __name__ == '__main__':
    main()
