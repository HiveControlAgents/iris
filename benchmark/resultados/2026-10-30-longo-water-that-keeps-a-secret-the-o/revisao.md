# Nota 7,0

Documentário bem medido e sem falhas de áudio, mas o tronco do Old Man muda de forma, a queda dividida nunca mostra o buraco e ainda exibe a caverna que a narração nega, e há saltos de cor nas emendas dos clipes.

## Cenas a refazer

Nenhuma. `rodada.json` indica rodada 3, então tratei o vídeo como versão refeita, o que deixa a lista vazia. Se houver outra rodada, a primeira candidata é a **cena 7** (45,9 s): o tronco reto vira dois troncos fundidos e inclinados. É o único defeito de sorteio com peso para isso.

## As cenas refeitas melhoraram?

Não dá para dizer: não há revisão nem folhas das versões anteriores. Estado atual das cenas refeitas (roteiro 1, 20, 26, 27, 28 e 34; aqui 1, 19, 24, 25, 26 e 32):

- **Só deriva de brilho:** 25 (rio).
- **Com defeito:** 1 (água sem rio), 19 (chama na frente da água), 24 (sem cortina de água) e 26 e 32 (sem buraco, com caverna).

## Principais problemas

| Segundo | Cena | Gravidade | O que se vê | Origem |
|---|---|---|---|---|
| 215,4 e 264,2 | 26 e 32 | alta | As duas quedas caem na mesma lagoa, sem o buraco, e há uma boca de caverna; a narração diz que essa rocha não forma cavernas | pipeline |
| 45,9 | 7 | media | Old Man vira dois troncos fundidos e inclinados | sorteio |
| 33,5, 36,0, 73,8, 85,0, 168,5, 258,5 | 5, 10, 11, 21, 31 | media | Saltos de cor e de forma nas emendas dos clipes | pipeline |
| 15,0 | 3, 6, 8, 10, 25, 29 | media | Brilho deriva mais de 15%; saturação sobe e os pretos esmagam | pipeline |
| 0,0 e 222,1 | 1 e 27 | media | Água cai do topo do quadro em chão plano, sem rio | pipeline |
| 150,5 | 19 | media | Chama na frente da queda, não atrás; a narração diz o contrário | pipeline |

Defeitos menores: gelo no lugar de água clara (cena 10), poça sem redemoinho (14), capim que surge e lampejo (15), rocha com cara de muro (23) e ritmo de 3,25 palavras por segundo.

## Medição da narração

Os erros do `medidas.json` não contam: a narração em inglês foi transcrita em português, então a taxa de 0,031 não mede a voz. Por isso o teto de nota 6 não foi aplicado. A conferência em inglês por cena deu acerto 1,0 em 33 das 34 cenas, e a única divergência é a grafia fonética de "Brule", que saiu certa. Essa conferência é das tomadas: a mixagem final não foi retranscrita em inglês.

## Sem problemas

Áudio em -14,8 LUFS, pico de -1,4 dBFS, sem cortes de pico, silêncios ou saltos de volume. Sem congelamentos, telas pretas, pessoas ou texto na imagem. O vídeo não tem legendas embutidas. 1920x1080 e 166,7 MB são normais para o formato longo.

## Pipeline

- Passar `--idioma en` na inspeção e `dur_s` no roteiro, porque dois cortes reais não foram detectados.
- Igualar a cor dos clipes dentro de cada cena e usar fusão curta nas emendas.
- Separar queda e buraco em dois planos e proibir caverna no prompt: a rodada 3 repetiu o defeito.
- Mostrar o rio chegando ao buraco nas cenas 1 e 29 do roteiro.
- Pôr a água entre a câmera e a chama nas cenas 20 e 26 do roteiro.

A numeração das cenas segue o `medidas.json`. Da cena 16 à 22 ela fica 1 atrás do roteiro, e da 24 em diante, 2 atrás.
