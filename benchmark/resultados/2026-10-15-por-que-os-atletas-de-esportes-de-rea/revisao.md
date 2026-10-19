# Revisão ÍRIS: nota 2,5 / 10

**Resumo:** o vídeo não responde ao tema. A pauta pergunta por que atletas de tênis, badminton e squash treinam a visão periférica, mas título, roteiro e imagens tratam só de como a águia enxerga longe. Além disso, há 4 erros de narração, ritmo lento e deformações nas cenas 1, 5 e 7.

## Cenas a refazer

Nenhuma. Refazer cenas não resolve: o roteiro inteiro está em outro assunto, e o vídeo precisa ser gerado de novo a partir do tema. As deformações de sorteio abaixo (cenas 1, 5 e 7) iriam para o refazer se o roteiro estivesse certo; vale vigiar esse tipo de defeito na nova geração.

## Problemas

| s | cena | tipo | gravidade | o que acontece | origem |
|---|---|---|---|---|---|
| 0,0 | todas | narração | alta | Fora do tema: só fala da águia; não aparece atleta, raquete nem visão periférica | pipeline |
| ~8,5–14 | 2 | narração | alta | "pumoes", "fossotossensiveis" e o trecho inventado "os e sacea" | pipeline |
| ~19 | 3 | narração | alta | "águia" engolida ("a ag") | sorteio |
| 38,5 | 6 | narração | alta | "caçe" escrito errado no roteiro e na legenda; a voz diz "acasse" | pipeline |
| ~22,8 | 4 | narração | média | "fóvea" → "fovia" | pipeline |
| ~31 | 5 | narração | média | "contrai" → "contraa" | sorteio |
| 1,5–2,5 | 1 | visual | alta | A cabeça gira 180° e em 2,0 s aparecem duas cabeças/bicos fundidos, em pleno gancho | sorteio |
| 29,5–31 | 5 | visual | alta | A cabeça vira fantasma e muda de forma; o fundo troca de verde para céu azul no meio do plano | sorteio |
| 51,5–52,5 | 7 | visual | média | Um galho surge do nada; brilho laranja nos pés parece fogo | sorteio |
| 15 | 3 | visual | baixa | Águia de cabeça branca (outra espécie), rastro na cauda, quase parada por 8 s | sorteio |
| todo | 1–6 | ritmo | média | 1,67–1,85 palavras/s (o alvo é 2,3–3,0); cenas de 8–9 s com imagem parada | pipeline |
| 0–2 | 1 | ritmo | média | Gancho sem pergunta nem ação | pipeline |
| 2–4 | 1 | áudio | média | Música abafa a voz ("a mais de dois") | pipeline |
| todo | todas | visual | baixa | Todas as cenas escurecem 9–17% do início ao fim; saturação baixa | pipeline |

O que está ok: volume (-13,9 LUFS, pico -1,6 dBFS), 1080x1920, 29,8 MB, legendas curtas e sem cobrir a ave.

## Pipeline

1. **Roteiro x tema:** validar que título, narração e estilo visual citam o sujeito do tema antes de gerar.
2. **Ortografia e termos técnicos:** revisar a narração antes do TTS e da legenda ("caçe", "fotossensíveis", "fóvea").
3. **Ritmo:** duração da cena calculada pelas palavras (~2,6 palavras/s), ou mais texto por cena.
4. **Mixagem:** ducking da música sob a voz.

## Lições

- Rejeitar roteiro cuja narração não cita o sujeito do tema.
- 2,3–3,0 palavras/s: cena de ~8 s pede ~20 palavras.
- Corretor ortográfico e palavras comuns no lugar de termos técnicos.
- Gancho com pergunta ou ação nos 2 primeiros segundos.
- Animal em close: só a câmera se move; fixar a espécie em todos os prompts.
