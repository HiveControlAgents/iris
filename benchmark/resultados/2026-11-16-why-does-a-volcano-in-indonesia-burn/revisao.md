# Nota 7.0 — The Volcano That Burns Blue Fire Every Night

Vídeo bonito e coerente, com gancho forte, mas várias cenas noturnas mostram brilho laranja de lava enquanto a
narração diz que não é lava, o ritmo da fala passa de 3 palavras/s e a narração não pôde ser conferida.

## Refazer (2 cenas)

- **Cena 5 (19.7–24.2 s)**: rachaduras incandescentes laranja em primeiro plano parecem lava, logo depois de
  "not molten rock". Ajuste: chão e rachaduras frios e escuros, única luz é a chama azul.
- **Cena 6 (24.2–28.9 s)**: massa laranja cresce no pé do riacho (27.0–28.5 s) e a cena clareia 36%. Ajuste:
  riacho só com chama azul de cima a baixo, exposição estável, sem labareda.

## Problemas

| Segundo | Cena | Tipo | Gravidade | O que se vê | Origem |
|---|---|---|---|---|---|
| 20.5 | 5 | visual | alta | Rachaduras laranja incandescentes e chama laranja à direita | sorteio |
| 27.5 | 6 | visual | média | Massa laranja cresce, fumaça rosa, brilho 64.9 → 88.4 | sorteio |
| 3.0 | 1 | visual | média | Chama laranja e brasas sob a legenda "BUT IT IS NOT LAVA" | pipeline |
| 7.5 | 2 | visual | média | Pedra única quase parada por 6.4 s; "run downhill like rivers" sem imagem; fundo escurece 25% | pipeline |
| 31.0 | 7 | ritmo | média | 3.78 palavras/s; 6 de 9 cenas acima de 3.0 (média 3.17) | pipeline |
| 0.0 | — | técnico | média | Transcrição rodou em português num vídeo em inglês: narração não verificada | pipeline |
| 39.0 | 9 | visual | baixa | Hastes que parecem postes de cerca no horizonte, base da chama magenta, fios amarelos no chão | sorteio |
| 39.5 | 9 | legenda | baixa | "WITH BLUE FIRE ALL" / "DAY LONG." corta a expressão | pipeline |
| 0.0 | — | áudio | baixa | -15.0 LUFS (alvo -14) e pico -0.9 dBFS (teto -1) | pipeline |

## O que funciona

- Gancho: fogo azul em movimento já no primeiro quadro.
- Cenas 3, 4, 7 e 8 limpas, sem deformação, e casadas com a narração.
- Sem cortes internos, congelamentos, telas pretas, silêncios ou saltos de volume. 1080x1920, 27.2 MB.

## Sobre a narração

A taxa de acerto de 0.007 e os "erros" de `medidas.json` são artefato: o transcritor ouviu inglês como português.
Por isso o teto de nota 6 por erro de narração não foi aplicado, mas a fala também não foi confirmada. Vale
reinspecionar com o idioma certo antes de publicar.

## Pipeline

1. Prompts das cenas de fogo: trava de cor (chamas só azuis, rocha fria e escura), sem listar o objeto indesejado.
2. Inspeção: transcrever no idioma do roteiro.
3. Roteiro: até ~3.0 palavras/s por cena.
4. Mixagem: -14 LUFS com teto de pico em -1 dBFS.

## Lições

- Quando a tese nega algo visual ("não é lava"), o prompt descreve positivamente o oposto em toda cena.
- Até 3.0 palavras por segundo por cena.
- Frase da narração sem imagem correspondente: mostrar a mais forte ou dividir a cena.
- Conferir a narração no idioma do roteiro; taxa perto de zero em outro idioma é falha de medição.
