# Revisão: The Ghost Plant That Never Uses the Sun

**Nota: 5,0 / 10**

O roteiro é bom e a imagem é limpa, mas a narração não pôde ser conferida, a planta não parece uma ghost pipe, as cenas ficam quase paradas e a cena 5 contradiz o que a voz diz.

## Cenas a refazer
- **Cena 5 (19,7 s a 25,2 s)**: a planta tem folhas palmadas e uma flor solta na base, logo depois de "This one has none". Novo prompt: caule curto, grosso e carnudo, com escamas, **sem folhas**, a ponta curvada formando uma flor. No negativo: leaves, green.

## Problemas
| s | cena | gravidade | o quê | origem |
|---|---|---|---|---|
| 0,0 | todas | alta | A transcrição saiu em português ("posmato", "oldes foras", "fangus") contra um roteiro em inglês. Não dá para garantir a pronúncia; precisa de uma escuta humana | pipeline |
| 0,0 | 1,2,3,4,8,9 | alta | A planta parece um galanto (haste longa e fina, flor de sino), e não uma ghost pipe (caule grosso e escamoso) | pipeline |
| 19,7 | 5 | alta | Planta com folhas, contradizendo a narração | sorteio |
| 0,0 | todas | media | Cenas quase paradas: os movimentos de câmera pedidos não aparecem | pipeline |
| 25,2 | 6 | media | 3,57 palavras/s; 7 de 9 cenas passam de 3,0 | pipeline |
| 25,2 | 6 | baixa | A teia de fungos virou uma "árvore de coral" branca e grossa | sorteio |
| 29,9 | 7 | baixa | O cogumelo saiu como uma amanita de desenho, com fundo parecendo cerca | sorteio |
| 0,1 | 1 | baixa | Pico de +0,2 dBFS com 1 trecho cortado; -15,5 LUFS (alvo -14) | pipeline |
| — | 1,8,9 | baixa | Legenda no centro, em cima das hastes | pipeline |

## Mudanças no pipeline
1. Fixar o idioma `en` na voz e no transcritor, e escutar uma amostra.
2. Reescrever a descrição da planta: caule curto, grosso e carnudo, com escamas; no negativo, "snowdrop, long thin stalk, leaves".
3. Aumentar a força de movimento do vídeo; limitador em -1 dBTP e alvo de -14 LUFS.
