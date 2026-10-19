# Revisão ÍRIS: Como o futebolista chuta sem olhar e acerta

**Nota: 6,0 / 10**

Áudio e técnica em ordem, mas o vídeo é uma sequência de bolas paradas com narração lenta, uma bola que duplica na cena 1 e pés a mais na cena 4.

## Cenas a refazer
- **Cena 1** (0–7,9 s): a bola duplica e se deforma em 5,0–5,5 s quando uma perna entra no quadro. Ajuste: bola sozinha, sem pessoas, ou jogador enquadrado desde o primeiro quadro.
- **Cena 4** (24,1–33,4 s): pés e chuteiras sobrando nas pernas ao fundo (27–33 s). Ajuste: campo vazio, ou um único jogador inteiro e nítido.

## Problemas
| s | cena | tipo | grav. | o quê | origem |
|---|---|---|---|---|---|
| 5,0 | 1 | visual | alta | bola duplicada/fantasma quando a perna entra | sorteio |
| 29,0 | 4 | visual | média | três pés para duas pernas; chuteira solta na borda | sorteio |
| 45,5 | 6 | visual | baixa | gomos duplicados quando a bola cai | sorteio |
| 24,1 | 4 | visual | média | brilho cai ~24% ao longo da cena | pipeline |
| 33,4 | 5 | visual | média | brilho cai ~26% e a cor desbota | pipeline |
| 0,0 | todas | ritmo | média | a mesma bola parada em 6 cenas de ~8 s; ninguém chuta; gancho imóvel | pipeline |
| 0,0 | todas | ritmo | média | de 1,6 a 2,17 palavras/s (alvo 2,3–3,0) | pipeline |
| 24,5 | 4 | narração | média | "propriocepção" ouvida como "própria acepção e" | pipeline |
| 42,0 | 6 | narração | média | "o passes saem" no roteiro (concordância), ouvido como "passe sai em"; fecha falando de passes, não de chute | pipeline |
| 31,5 | 4 | legenda | baixa | "PERFEITO. MILHARES" junta duas frases; legendas encostam na bola | pipeline |

Sem problemas: volume (-14 LUFS, pico -1,7 dBFS, sem distorção, sem silêncios), 1080x1920, 29,4 MB.

## Pipeline
- Estilo visual: trocar "sports equipment photography" por ação esportiva fotorrealista.
- Montagem: normalizar o brilho dentro de cada clipe (todas as cenas escurecem até o fim).
- Roteiro: calcular a duração das cenas pelas palavras (~2,6 palavras/s) e revisar a gramática antes da voz.
- Legendas: quebrar os blocos no fim das frases e posicioná-los longe do assunto principal.
