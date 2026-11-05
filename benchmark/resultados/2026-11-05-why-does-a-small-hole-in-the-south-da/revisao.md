# Revisão: This Hole in the Ground Breathes

**Nota: 6,5 / 10**

O visual é bonito e o gancho é forte (fumaça saindo do buraco já em 0 s). Mas a cena 3 não mostra o buraco que a narração aponta, o teto da caverna (cena 6) parece uma grade artificial e o "buraco" muda de forma em cada cena. A narração **não foi conferida**: a transcrição saiu traduzida para português.

## Cenas a refazer

| Cena | Tempo | Motivo | Ajuste no prompt |
|---|---|---|---|
| 3 | 8,4-13,1 s | A narração diz "that hole" e não aparece buraco nenhum (plano aberto) | Plano médio baixo, com a abertura escura visível e centralizada; pradaria ao fundo |
| 6 | 22,4-27,2 s | O teto é uma grade regular de quadrados e parece treliça, não rocha | Tirar "grid/square/diamond"; pedir "irregular honeycomb-like boxwork, uneven cells, no straight lines" |

## Problemas

- **0 s, técnico (alta, pipeline):** o Whisper transcreveu em português (taxa_acerto 0,029). O conteúdo segue o roteiro, então não parece erro da voz, mas a pronúncia ficou sem checagem. A nota não leva o teto de 6 por erro de narração; refaça a inspeção com `language=en` para confirmar.
- **8,5 s, cena 3, visual (média, sorteio):** buraco ausente; imagem quase parada.
- **22,5 s, cena 6, visual (média, sorteio):** teto em grade artificial, com túnel de luz azul.
- **Cenas 1, 2, 4, 7, 8 e 9, visual (média, pipeline):** o buraco tem uma forma diferente em cada cena (fenda, toca, arco, portal retangular).
- **4,5 s / 27,2 s, cenas 2 e 7, visual (baixa, pipeline):** fala-se de vento forte, mas a grama não se dobra.
- **Legenda (média, pipeline):** fixa a ~70% da altura, cobre o buraco nas cenas 2, 7 e 9.
- **Legenda (baixa, pipeline):** palavras soltas: "PUSH.", "IT.", "IN.", "IN, THE AIR PRESSURE".
- **Ritmo (baixa):** 3,0-3,5 palavras/s em todas as cenas, acima de 3,0.
- **Áudio (baixa):** -15,1 LUFS (alvo -14). Pico em -1,6 dBFS, sem cortes nem silêncios.

## Pipeline

1. Whisper: passar o idioma do roteiro (`en`) e usar `transcribe`, não `translate`.
2. Imagem-âncora do buraco como referência para todas as cenas em que ele aparece.
3. Legenda mais alta (~20-25%) e quebra por pontuação, sem palavra solta.
4. Roteiro com no máximo ~2,8 palavras/s; mixagem final em -14 LUFS.
