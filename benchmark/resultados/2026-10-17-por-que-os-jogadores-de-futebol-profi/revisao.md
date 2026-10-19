# Revisão ÍRIS: O segredo dos passes de costas no futebol

**Nota: 5,0 / 10**

Áudio e formato estão corretos (-14 LUFS, pico -1,5 dBFS, 1080x1920). Mas as 6 cenas mostram a mesma bola parada
enquanto a narração fala de visão periférica e cérebro. A cena 4 tem pernas e uma mão que surgem do nada, o ritmo é
lento e há um erro de narração (nota limitada a 6).

## Refazer

- **Cena 4 (20,5 s a 31,3 s):** pernas entram e saem do quadro e a chuteira muda de branca para azul. Aos 30 s uma mão
  sem corpo desce e toca a bola. Ajuste no prompt: "no people, no legs, no feet, no hands". Melhor ainda: mostrar o que
  a narração diz, por exemplo um jogador de costas olhando o campo.

## Problemas

| Segundo | Cena | Tipo | Gravidade | O quê | Origem |
|---|---|---|---|---|---|
| 30,0 | 4 | visual | alta | Mão sem corpo toca a bola | sorteio |
| 21,5 | 4 | visual | alta | Pernas aparecem e somem; chuteira muda de cor | sorteio |
| 5,4 | todas | visual | alta | Mesma bola parada nas 6 cenas, sem relação com a narração | pipeline |
| 0,0 | 1/2 | narração | alta | Um "o" a mais ouvido (provável "Como o jogador" ou "como um mapa"); confira de ouvido | sorteio |
| 0,0 | 1/3 | narração | média | Um "a" engolido ("passar a bola" ou "para a frente") | sorteio |
| 29,5 | 4 | narração | média | "milissegundos" ouvido como "milisegundos" | sorteio |
| 20,5 | 3-5 | ritmo | média | 1,5 a 1,9 palavras/s; cenas 3 e 4 com mais de 9 s quase paradas | pipeline |
| 0,0 | 1 | ritmo | média | Gancho sem ação: só uma bola parada | pipeline |
| todo | todas | legenda | média | Legenda em cima da bola, o assunto principal | pipeline |
| 41,0 | 6 | legenda | baixa | Bloco "PRECISAMENTE, MESMO" corta a ideia | pipeline |
| 20,5 | 4 | visual | baixa | Bola salta de posição no primeiro meio segundo | sorteio |
| 31,3 | 5 | visual | baixa | Bola com gomos quadrados | sorteio |
| todo | todas | visual | baixa | Todas as cenas escurecem 12-15% do início ao fim | pipeline |

## Pipeline

- **estilo_visual e prompts:** trocar "sports equipment photography" por cenas esportivas com ação, uma imagem por ideia.
- **Duração das cenas e velocidade da voz:** chegar a cerca de 2,5 palavras/s e no máximo ~8 s por cena.
- **Legendas:** colocar no terço inferior e quebrar o bloco na pontuação.
