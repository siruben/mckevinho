# Chuva de Brigadeiro

Jogo web de arcade com o MC Kevinho: apanha os brigadeiros no balde antes que caiam ao chão.
HTML + CSS + JavaScript puro, sem dependências.

## Jogar

Abre `index.html` num browser (ou serve a pasta, por exemplo `python3 -m http.server`). Adapta-se ao ecrã: telemóvel em vertical ou horizontal, tablet e computador.
No ecrã de entrada toca/clica para ativar o som.

| Ação | Teclado | Telemóvel |
|---|---|---|
| Mover | ← → ou A / D | tocar ou arrastar |
| Pausa | P ou Esc | botão ❚❚ |
| Começar / repetir | Enter ou Espaço | botão |

## Regras

- 3 vidas: perdes uma por cada brigadeiro que chega ao chão.
- +10 pontos por brigadeiro; combo ×2…×5 a cada 5 seguidos (um falhanço repõe o combo).
- Sobes de nível a cada 8 apanhados: caem mais depressa e com menos intervalo.

## Estrutura

```
index.html                 jogo completo (canvas + HUD em HTML)
assets/                    imagens redimensionadas usadas no jogo
assets/originals/          ficheiros originais aprovados (não são usados em jogo)
audio/                     intro (menu), música de jogo, game over
tools/build_single_file.py gera dist/chuva-de-brigadeiro.html (tudo num só ficheiro)
```

## Recursos gráficos

O MC Kevinho, o brigadeiro e o cenário são os recursos aprovados, sem redesenho:
apenas recortados da margem transparente e redimensionados proporcionalmente (alfa preservado).
Kevinho e brigadeiros são desenhados a 70 % do tamanho (`SIZE = 0.7` em `index.html`).

## Áudio

- `intro-cai-brigadeiro.mp3`: música do menu
- `musica-mc-kevinho.mp3`: durante o jogo (em loop)
- `game-over-brigadeiros.m4a`: fim de jogo (AAC; o original vinha em Opus, que o Safari/iOS pode não tocar)

## Ficheiro único

```
python3 tools/build_single_file.py   # → dist/chuva-de-brigadeiro.html
```
