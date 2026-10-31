# Nota: 6,0

Áudio e formato estão bons, mas a lampreia quase nunca parece uma lampreia: ganha cabeça de enguia e barbilhos, vira um anel fechado na cena 8 e cria espinhos na cena 9.

**Narração sem verificação.** O Whisper rodou em português sobre uma narração em inglês, então os erros em `medidas.json` não valem. Nenhuma palavra errada foi confirmada, e a pronúncia precisa ser conferida com `--idioma en`. A nota 6,0 vem dos defeitos visuais e respeita o teto de 6 caso surja algum erro real.

## Cenas a refazer

- **Cena 9 (41,2 s a 47,4 s):** espinhos surgem no corpo a partir de 41,5 s e ficam até o fim. Enquadrar de perto um trecho liso do corpo, de borda a borda.
- **Cena 8 (35,7 s a 41,2 s):** o corpo vira um anel fechado, como uma câmara de ar. Pedir uma curva em S que entra por uma borda e sai pela outra.
- **Cena 3 (8,6 s a 14,8 s):** a cauda da truta se desfaz em respingos entre 12,5 s e 13,5 s, e o ferimento parece um adesivo. Fechar no flanco e descrever uma lesão irregular.

## Outros problemas

| Segundo | Cena | Gravidade | Origem | Problema |
|---|---|---|---|---|
| 0,0 | 1, 3, 6, 9 | média | pipeline | A cabeça aparece mesmo com "no head visible"; nas cenas 1 e 9 há barbilhos durante "no jaws", e na cena 6 há nadadeiras peitorais |
| 4,0 | 2 | média | sorteio | Só um anel de dentes para "rings of teeth", disco solto na água e imagem quase parada; não entrou no limite de 3 cenas |
| 20,2 | 5 | média | pipeline | Saturação sobe 17% a 33% em 8 de 9 cenas; brilho deriva 20% na cena 5 e 16% na cena 6 |
| 25,0 | 6 | baixa | pipeline | "Eyes appear, teeth grow" sem olhos ou dentes em destaque |
| 36,0 | 8 | baixa | pipeline | Legendas truncadas ("THEIR SKELETON IS NOT" / "BONE.") e legenda sobre os dentes na cena 2 |
| 20,2 | 5 | baixa | pipeline | 3,48 palavras por segundo na cena 5; cenas 1, 2 e 4 também passam de 3,0 |
| 0,0 | 1 | baixa | pipeline | -15,3 LUFS, um pouco abaixo da faixa de -14 ±1 |

Sem problemas nas medidas de picos cortados, silêncios, saltos de volume, congelamentos e telas pretas. Formato 1080x1920 e 29,3 MB dentro do padrão.

## Mudanças no pipeline

1. Passar `--idioma en` na inspeção de vídeos em inglês.
2. Trocar as negações dos prompts por enquadramento fechado, com o corpo cortado pelas bordas.
3. Investigar a subida de saturação ao longo dos clipes.
4. Normalizar para -14 LUFS com limitador em -1 dBFS.
5. Dividir as legendas por unidade de sentido.
