# Revisão ÍRIS: nota 5,5/10

**A Cave Sealed for 5 Million Years and 5 Other Places Frozen in Time** (12:29, 1920x1080, rodada 2)

Áudio e narração estão sólidos. O problema é visual: o modelo de vídeo inventa mãos, varas, botas, uma lancha e uma frigideira em várias cenas.

## Cenas a refazer

Nenhuma. Esta é a rodada 2, então `refazer` fica vazio pela regra. Como os defeitos principais são de pipeline, a correção vem antes de qualquer nova geração.

## As cenas refeitas melhoraram?

Comparei só o estado atual; não abri o vídeo anterior e não há revisão da rodada 1.

| Cena (roteiro) | Trecho | Situação atual |
|---|---|---|
| 14 | 92,7–100,7 s | **Ruim.** Vara, mão de manga vermelha e concha invadem o buraco. |
| 15 | 100,7–108,1 s | **Boa.** Encosta de turfa limpa e coerente com a narração. |
| 30 | 215,6–223,1 s | **Ruim.** Frigideira surge na crosta de sal e recebe sal do céu. |

Nas cenas 14 e 30 o quadro-base está limpo: o defeito nasce no vídeo. Trocar a semente não basta.

## Problemas

Números de cena seguem `medidas.json`. O número do roteiro é igual até a 15, +1 da 16 à 36 e +2 da 37 em diante.

### Alta
- **95,5 s, cena 14:** vara, mão e concha entram no buraco. Pipeline.
- **216,0 s, cena 29:** frigideira na crosta de sal. Pipeline.
- **259,8 s, cena 35:** lancha vermelha no lago corrosivo. Pipeline.
- **282,5 s, cena 37:** varas fincadas e pernas de calça moderna com bota. Pipeline.
- **470,0 s, cena 62:** vara e bota cutucam a pelagem, que brilha como fogo; o potro não aparece. Pipeline.

### Média
- **Objetos ou sujeitos inventados, pipeline:** haste (460,5 s, cena 61), cabo sem dono (362 s, cena 48), agulha na bolha (611 s, cena 80), vulto no vale (380 s, cena 50), pedras deslizando (276,5 s, cena 36).
- **Cor, pipeline:** 28 cenas escurecem mais de 15% e 4 clareiam; o contraste endurece e os brancos estouram no fim dos clipes.
- **Imagem contra a narração, pipeline:** cratera circular em vez de ferradura (cena 51 e seguintes); aves vivas em vez de mineralizadas (cenas 24 a 26); tapete de micróbios que parece prato plissado e muda de forma (cena 85 e seguintes).
- **Geração ruim, sorteio:** fundo de tijolos (405 s, cena 54), cristal flutuando (556,5 s, cena 74), buraco com aro metálico (139,5 s, cena 19), estrada na Antártida (345,9 s, cena 46).
- **Narração, pipeline:** `crabeater` ouvido como `cray beater` (346,2 s); sete palavras certas, mas rápidas demais (cenas 3, 5, 24, 36, 43, 44 e 61).
- **Gancho, sorteio:** 7 s de disco branco quase parado, sem relação clara com a caverna.

### Baixa
- 3,2 palavras por segundo, acima da faixa de 2,3 a 3,0.
- Pernas do flamingo se fundem em 3:58–4:06.
- O inspetor não detectou os cortes em 108,1 s e 273,3 s.

## Falso alarme

`narracao.taxa_acerto` 0,018 e a lista de `narracao.erros` não valem. O Whisper rodou em português sobre narração em inglês, por isso esses erros não contaram para a nota nem para o teto de 6. A checagem em inglês feita pelo pipeline dá acerto 1,0 em 99 das 100 cenas; a exceção é `their`/`theyre`, palavras de mesmo som.

## O que está bom

Áudio dentro da meta: -15,0 LUFS, pico de -1,1 dBFS, sem picos cortados, silêncios ou saltos de volume. Não há congelamentos nem telas pretas. O formato horizontal e os 451 MB não contam como defeito neste documentário longo.

## Mudanças no pipeline

1. Passar `--idioma en` ao inspetor quando o roteiro for em inglês.
2. Proibir pessoas, mãos, ferramentas e veículos no prompt negativo e reduzir o movimento em planos parados.
3. Casar cor e contraste de cada parte do clipe com o quadro-base antes de emendar.
