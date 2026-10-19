# Revisão ÍRIS: "Como o olho acompanha uma bola a 200 km/h?"

**Nota: 6,5 / 10**

Narração limpa e ritmo bom, mas 13 s de gavião num vídeo sobre tenistas, imagens quase todas paradas para um assunto de velocidade, sombra que pisca na cena 5, legendas quebradas no meio da frase e áudio baixo (-15,9 LUFS).

## Refazer

- **Cena 5** (24,07 a 29,53 s): uma sombra escura surge e some no chão entre quadros vizinhos durante a cena toda.
  Ajuste: câmera travada no lugar do pan, "soft even light, no moving shadows", outra semente.

## Problemas

| Seg. | Cena | Tipo | Grav. | O que se vê | Origem |
|---|---|---|---|---|---|
| 24,5 | 5 | visual | alta | Sombra escura que aparece e some no chão (24,5 a 28,5 s) | sorteio |
| 4,1 | 2 | visual | média | Close de gavião enquanto a fala trata dos olhos humanos | pipeline |
| 10,8 | 3 | visual | média | Segundo gavião seguido sobre "o cérebro antecipa onde a bola vai estar" | pipeline |
| 0,0 | 1 | ritmo | média | Gancho de "200 por hora" sobre bola parada; 5 de 7 cenas com bola ou raquete paradas | pipeline |
| 0,0 | 1 | legenda | média | Blocos terminam em artigo ou preposição ("BOLA DE TÊNIS A", "GIRAM O", "É TÃO"...); "SOZINHO. A CONCENTRAÇÃO" junta duas frases | pipeline |
| 0,0 | 1 | áudio | média | -15,9 LUFS, quase 2 LU abaixo do alvo de -14 (pico -1,6 dBFS, sem corte) | pipeline |
| 36,5 | 7 | narração | média | "por" e "quem" ouvidos com pouca certeza no fecho rápido; "NO TÊNIS" fica menos de 0,5 s na tela | sorteio |
| 0,5 | 1 | narração | baixa | "a duzentos por hora" sem "quilômetros" | pipeline |
| 24,07 | 5 | visual | baixa | Saturação sobe ~21% ao longo da cena | sorteio |
| 33,0 | 6 | visual | baixa | Aro da raquete passa de preto a azul | sorteio |
| 23,0 | 4 | ritmo | baixa | "A concentração" (cena 5) começa ainda na imagem da cena 4 | pipeline |

Sem erros de narração, cortes internos, congelamentos ou telas pretas. Ritmo de 2,4 a 3,0 palavras/s em todas as cenas. Formato 1080x1920, 24,9 MB.

## Pipeline

- **Legendas:** cortar em pontuação; nunca fechar um bloco em artigo ou preposição.
- **Áudio:** normalizar para -14 LUFS (loudnorm) depois da mixagem.
- **Prompts:** nada de metáfora animal que a narração não cite; em tema de velocidade, pedir movimento de câmera ou desfoque em vez de "ball stays still" em todas as cenas.
- **Roteiro:** falar a unidade por extenso.
