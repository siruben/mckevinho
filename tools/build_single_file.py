#!/usr/bin/env python3
"""Gera dist/chuva-de-brigadeiro.html: o jogo num único ficheiro, com imagens e áudio embebidos."""
import base64, mimetypes, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")

files = [
    "assets/palco.jpg", "assets/kevinho.png", "assets/brigadeiro.png", "assets/capa-mc-kevinho-rush.jpg",
    "audio/intro-cai-brigadeiro.mp3", "audio/musica-mc-kevinho.mp3",
    "audio/game-over-brigadeiros.m4a", "audio/game-over-brigadeiros.webm",
]
mime_override = {".m4a": "audio/mp4"}
for rel in files:
    p = root / rel
    mime = mime_override.get(p.suffix) or mimetypes.guess_type(p.name)[0]
    data = base64.b64encode(p.read_bytes()).decode()
    data_uri = f"data:{mime};base64,{data}"
    # O caminho pode aparecer com aspas duplas (JS) ou simples (CSS url(...)); troca ambas.
    replaced = 0
    for quote in ('"', "'"):
        needle = f'{quote}{rel}{quote}'
        count = html.count(needle)
        if count:
            html = html.replace(needle, f'{quote}{data_uri}{quote}')
            replaced += count
    assert replaced >= 1, f"{rel}: não encontrei nenhuma ocorrência (nem com aspas simples nem duplas)"

out = root / "dist" / "chuva-de-brigadeiro.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"{out.relative_to(root)}  {out.stat().st_size / 1024 / 1024:.1f} MB")
