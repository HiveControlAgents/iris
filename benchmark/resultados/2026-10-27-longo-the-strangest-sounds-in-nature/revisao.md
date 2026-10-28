# Revisão ÍRIS: The Strangest Sounds on Earth, and the Whale No One Has Seen

**Nota: 6,5 / 10**

Documentário horizontal (4:01, 1920x1080) bonito, com áudio no padrão (-14,9 LUFS, pico -1,0, sem cortes, silêncios ou saltos). Três clipes de geração estragam a primeira metade, e a narração **não pôde ser conferida**: a transcrição saiu em português sobre um roteiro em inglês.

## Cenas a refazer

| Cena | Trecho | Motivo | Ajuste no prompt |
|---|---|---|---|
| 5 | 0:56,5–1:03,5 | Figura de roupa vermelha e azul (estilo super-herói) surge e corre sobre rachaduras em teia | "long straight cracks racing across clear black lake ice, empty, no people, no legs"; nada de forma radial ou em teia |
| 3 | 0:37,5–0:41,5 | Pernas de tênis entram no quadro e andam no gelo, com o corpo cortado no joelho | Só o lugar: "clear black ice with frozen bubbles, empty, no people, no shoes"; sem "skaters" |
| 6 | 1:11,5–1:19,5 | Coruja-das-neves por 8 s, sem relação com o roteiro | "empty moonlit shoreline of a frozen lake, slow push-in, no animals, no people" |

## Outros problemas

- **Narração sem verificação (técnico, alta, pipeline):** os 29 "erros" e a taxa de 0,055 vêm do idioma errado na inspeção. O texto ouvido é uma tradução fiel do roteiro, então a voz provavelmente leu certo, mas falta checar a pronúncia. Rode a inspeção de novo em inglês antes de publicar.
- **Cauda de baleia vertical** (0:05,5 e 3:56–3:59,5): anatomia de peixe. Baixa.
- **Mesmo plano de jubarte seis vezes**, e duas baleias juntas em 3:33,5–3:39,5 justo na história da baleia solitária. Baixa.
- **Clipes de 6 a 8 s quase parados** no meio (aurora, iceberg, píer); 3,15 palavras/s. Baixa.
- **Céu quase preto** em 3:27,5–3:33. Baixa.
- **Detector de cortes não pega as fusões:** as cenas 1, 3, 5, 6 e 23 juntam vários clipes; a deriva de brilho nelas é troca de clipe, não defeito.

## Pipeline

1. Na inspeção, transcrever no idioma do roteiro (ou com detecção automática).
2. Passar sempre `--roteiro` na inspeção.
3. Acrescentar "no people, no human figures, no costumes" ao estilo visual do canal.
