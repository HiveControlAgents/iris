# Revisão ÍRIS: The Plant That Counts Before It Snaps

**Nota: 5,0 / 10**

Técnica e áudio corretos (1080x1920, 31,9 MB, -14,5 LUFS, pico -1,8 dBFS, sem cortes de áudio nem silêncios). Mas a
transcrição da narração não bate com o roteiro, 4 das 7 cenas mostram dioneias com anatomia impossível, a cena 5 rompe
o estilo e as imagens quase paradas nunca mostram a armadilha agindo.

## Refazer

- **Cena 5 (27,1–35,6 s)**: aparece fundo de parede branca de estúdio com a planta inteira num vaso, e o brilho fica
  em 129 contra cerca de 70 no resto do vídeo. A imagem também não mostra a armadilha meio fechada de que a narração
  fala. Ajuste do prompt: *"extreme close-up of ONE half-closed trap filling the frame, dark wet moss background,
  outdoor bog, no pot, no wall, no white background"*.

## Problemas

| s | cena | tipo | gravidade | o quê | origem |
|---|---|---|---|---|---|
| 0–52 | 1–7 | narração | alta | A transcrição saiu em português sem sentido para um roteiro em inglês (acerto 0,05). O mais provável é que o Whisper tenha rodado no idioma errado ("e nada mexe dentro" = "nothing moves inside"). **Ouça para confirmar.** | pipeline |
| 27,1 | 5 | visual | alta | Salto de estilo para estúdio branco, e a imagem não ilustra a narração | sorteio |
| 12,5 | 3 | visual | média | Planta em totem simétrico: uma armadilha presa embaixo do mesmo caule | pipeline |
| 20,5 | 4 | visual | média | Duas armadilhas ligadas ponta a ponta | pipeline |
| 35,6 | 6 | visual | média | Duas armadilhas fechadas empilhadas, uma na base da outra | pipeline |
| 44,3 | 7 | visual | média | Armadilha "haltere": duas armadilhas espelhadas nas pontas de um caule | pipeline |
| 0–52 | todas | ritmo | média | Imagens quase paradas: a armadilha nunca fecha nem reabre, as cenas 3, 5, 6 e 7 têm 8 s ou mais e o gancho não tem movimento | pipeline |
| 20,5 | 4 | visual | baixa | O brilho sobe 37% durante a cena | sorteio |
| 0,5 | todas | legenda | baixa | A legenda fica em cima da armadilha de baixo | pipeline |
| 11,5 | 2–6 | legenda | baixa | Blocos que atravessam frases: "HAPPENS. THE PLANT", "OPEN. HERE", "TIGHT. EVERY WASTED SNAP" | pipeline |
| 6,0 | 2 | visual | baixa | A narração fala dos pelos-gatilho, mas eles não aparecem | pipeline |

As cenas 3, 4, 6 e 7 não estão em "refazer" porque o defeito se repete: trocar a semente não resolve. O que resolve é
mudar o template de prompt (veja abaixo).

## Pipeline

- **Inspetor/Whisper**: passar o idioma do roteiro (`en`) ao transcritor.
- **Prompt das cenas**: trocar "single plant ... centered" por close de uma armadilha preenchendo o quadro, com "no
  mirrored or stacked traps".
- **Movimento**: deixar a armadilha se mover devagar nas cenas que descrevem a ação.
- **Legendas**: cortar os blocos na pontuação e tirar a legenda do centro do assunto.

## Lições

- Em formato vertical, "single X, centered" faz o modelo empilhar ou espelhar partes para preencher a altura. Peça um
  close de uma parte só.
- Se o assunto é um movimento, ao menos uma cena precisa mostrá-lo.
- Fixe o cenário com termos negativos (no studio, no white background, no pot).
- Quebre a legenda na pontuação.
