#!/usr/bin/env python3
"""Gera dist/chuva-de-brigadeiro.html: o jogo num único ficheiro, com imagens e áudio embebidos."""
import base64, mimetypes, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")

files = [
    "assets/palco.jpg", "assets/kevinho.png", "assets/brigadeiro.png",
    "audio/intro-cai-brigadeiro.mp3", "audio/musica-mc-kevinho.mp3", "audio/game-over-brigadeiros.m4a",
]
mime_override = {".m4a": "audio/mp4"}
for rel in files:
    p = root / rel
    mime = mime_override.get(p.suffix) or mimetypes.guess_type(p.name)[0]
    data = base64.b64encode(p.read_bytes()).decode()
    needle = f'"{rel}"'
    assert html.count(needle) == 1, f"{rel}: esperava 1 ocorrência, encontrei {html.count(needle)}"
    html = html.replace(needle, f'"data:{mime};base64,{data}"')

out = root / "dist" / "chuva-de-brigadeiro.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"{out.relative_to(root)}  {out.stat().st_size / 1024 / 1024:.1f} MB")
