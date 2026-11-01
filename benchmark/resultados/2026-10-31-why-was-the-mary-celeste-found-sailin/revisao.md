# Revisão: The Ship Found Sailing With Nobody on Board

**Nota: 5,5/10**

Áudio e formato estão bons, mas a cena 5 refeita ainda mostra uma mão tocando o casaco enquanto a narração diz que nada foi tocado, e o navio não corresponde ao roteiro nem entre as próprias cenas.

## Cenas a refazer

Nenhuma. Esta é a rodada 2 (cena 5 já refeita), então a lista fica vazia.

**A cena 5 refeita não foi aprovada:** mantém a mão, a deformação do casaco e o erro de narração registrado em "Their". Não dá para dizer se melhorou, porque nem o vídeo anterior nem a primeira revisão estavam disponíveis para comparar.

## Problemas

Tempos vistos nas folhas de contato são aproximados.

| Segundo | Cena | Gravidade | Problema | Origem |
|---|---|---|---|---|
| 23,0 | 5 | alta | Mão pousa no casaco, que deforma, durante "have not been touched" | sorteio |
| 22,4 | 5 | alta | "Their" marcado como erro nas 4 tomadas; não confirmado de ouvido | pipeline |
| 0,0 | 1, 2, 9 | média | Navio de três mastros, velas inteiras e de frente; pedido: dois mastros, velas rasgadas, de lado. Parece navegar quando a narração diz "drifting" | pipeline |
| 3,9 | 1, 2, 9 | média | Navio muda de aparência entre as cenas; céu pêssego na cena 2 | pipeline |
| 15,1 | 4 | média | Lampião aceso (pedido: apagado), objeto branco moderno ao fundo, feixe azul saturado | sorteio |
| 35,7 | 8 | média | Barril fechado soltando vapor denso (pedido: aberto, vapor fino) | sorteio |
| 20,7 | 5 | média | Salto de enquadramento dentro da cena | sorteio |
| 25,2 | 6, 3, 4 | média | Narração acima de 3,0 palavras/s (até 3,62) | pipeline |
| 2,0 | várias | média | Legendas quebram ideias no meio ("AND TEN PEOPLE HAD") | pipeline |
| 32,9 | 7 | baixa | Perspectiva dos barris muda na emenda dos clipes | sorteio |
| 10,3 | 3 | baixa | Blocos de legenda de menos de 0,4 s ("HER NAME", "THEY WATCH") | pipeline |
| 0,1 | várias | baixa | Legenda cobre casco, lampião e baú | pipeline |
| 14,5 | 3, 6 | baixa | Brilho cai cerca de 17% dentro da cena | pipeline |

## Narração: medida inválida

Os `erros` e a `taxa_acerto` de 0,042 em `medidas.json` não valem: o Whisper rodou em português sobre narração em inglês. A nota não usou esses erros. O teto de 6 vale pelo "Their", que foi a única palavra marcada pela checagem em inglês do pipeline.

## O que está bom

Volume em -14,6 LUFS, pico de -1,6 dBFS, sem cortes, silêncios ou saltos de volume. Vídeo em 1080x1920 com 28,7 MB, sem congelamentos nem telas pretas.

## Pipeline

- **Inspeção:** usar `--idioma en` em vídeos em inglês.
- **Imagem:** gerar o navio uma vez e usar como referência nas demais cenas.
- **Narração:** com erro repetido na mesma palavra, trocar o texto da frase.
- **Legendas:** quebrar por sentido, com duração mínima por bloco.

## Fora do vídeo

A hashtag `#marycleste` no roteiro está com erro de grafia; o certo é `#maryceleste`.
