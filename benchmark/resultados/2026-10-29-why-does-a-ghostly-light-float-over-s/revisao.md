# Nota 6,5 — The Swamp Light Science Still Can't Explain

Roteiro, ritmo e áudio funcionam, mas as bolhas da cena 7 viram olhos, uma lua surge na cena 5 e toda cena dá um salto de contraste na emenda das duas partes do clipe.

Os números de cena seguem as 9 cenas do roteiro.

## Cenas a refazer

- **Cena 7 (31,5 a 36,5 s):** as bolhas viram olhos abertos entre as folhas, pior a partir de 35,0 s. Manter a foto, trocar a semente do vídeo, pedir bolhas minúsculas, transparentes e sem cor, e tirar "no eyes, no faces" do texto.
- **Cena 5 (21,0 a 25,5 s):** uma lua surge no céu e cresce, contra o que o quadro pede. Refazer a foto sem o ponto claro no céu e descrever um céu todo coberto por nuvens, em vez de "no moon, no stars".

## Problemas

**Alta**
- 35,0 s, cena 7: bolhas azuis opacas que parecem olhos (sorteio).
- 21,0 s, cena 5: lua que surge no céu (sorteio).

**Média**
- 3,5 / 14,0 / 18,5 / 34,5 / 40,0 / 45,5 s: salto de contraste e saturação na emenda das partes, cerca de 3 s depois do início da cena (pipeline).
- 0,0 s e cenas 8 e 9: a luz é uma labareda grande presa à água, não uma luz pálida que flutua (pipeline).
- 15,5 s, cena 4: chama laranja em vez de azul, com pedaço aceso que se solta (sorteio).
- 30,5 s, cena 6: o fogo-fátuo vira fumaça rosa e queimada na margem (sorteio).
- 12,0 s, cena 3, e 27,4 s, cena 6: "will-o'-the-wisp" e "jack-o'-lantern" com pronúncia a conferir de ouvido (sorteio).
- 21,0 a 31,0 s: a legenda cobre a boca da abóbora; a altura é fixa no vídeo todo (pipeline).
- Inspeção: 9 erros de narração falsos, porque o Whisper rodou em português numa narração em inglês (pipeline).

**Baixa**
- 14,0 / 15,5 / 24,0 s: legendas cortadas no meio da ideia; aos 20,5 s a legenda anterior ainda aparece sobre a abóbora (pipeline).
- 45,5 s, cena 9: o reflexo fica quase parado e a chama estoura para branco (sorteio).
- Loudness de -15,2 LUFS, um pouco abaixo da faixa de -14 ±1 (pipeline).

## Limites desta revisão

- O teto de nota 6 por erro de narração não foi aplicado, porque esses erros são falsos: a transcrição em inglês da produção bate com o roteiro. Ela foi feita na narração antes da mixagem, não no vídeo final, e a voz não foi ouvida.
- A produção registra rodada 4, mas nem a pasta da revisão nem o pedido marcam esta versão como refeita, então vale a regra normal do refazer. Sem revisões anteriores nem acesso às versões antigas, não dá para dizer se as cenas melhoraram.

## Pipeline

- Inspeção: usar `--idioma en` em vídeos em inglês, ou o idioma do roteiro.
- Quadro-ponte: igualar cor e contraste aos da foto da cena antes de gerar a parte 2.
- Legendas: altura por cena e quebra por sentido.
- Mixagem: subir o alvo em cerca de 1 dB.
