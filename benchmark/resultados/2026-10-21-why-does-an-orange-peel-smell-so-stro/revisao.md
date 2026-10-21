# Revisão ÍRIS: "Every Orange Hides a Flammable Secret"

**Nota: 5,5 / 10**

Imagens bonitas e coerentes na maior parte. Mas a transcrição não reconheceu quase nada da narração em inglês (4,5% de acerto). A cena 5 mostra um besouro em cima da laranja enquanto a voz diz que os insetos ficam longe. E o áudio está 2 LU abaixo do alvo.

## Refazer

- **Cena 5 (14,5 a 18,0 s):** o besouro pousado na laranja contradiz "Many insects stay away". Tire o besouro do prompt ou mostre-o voando para longe da fruta, e acrescente "no insects touching the fruit".

## Problemas

| Segundo | Cena | Tipo | Gravidade | O que acontece | Origem |
|---|---|---|---|---|---|
| 0,0 | 1 a 9 | narração | alta | A transcrição sai em português aproximado do começo ao fim ("called limonene" vira "chamando limineo"). Pode ser uma voz de outro idioma lendo inglês ou o Whisper com o idioma forçado em português. Ouça os primeiros 4 s para saber qual. | pipeline |
| 14,5 | 5 | visual | alta | O besouro fica em cima da laranja durante "Many insects stay away". | sorteio |
| todo | n/a | áudio | média | -16 LUFS (alvo -14); o pico de -1,4 dBFS está bom. | pipeline |
| 13,5 | 4 | legenda | média | "LIMONENE. THE TREE MAKES" junta duas frases e atravessa o corte das 14,53 s. | pipeline |
| 25,5 | 8 | visual | baixa | Um fio verde liga a laranja ao galho de pinheiro, como se ela pendesse dele. | sorteio |
| 0,0 | 1 | visual | baixa | Faixa clara em crescente na laranja da abertura, parecendo um gomo descascado. | sorteio |
| 31,5 | 9 | visual | baixa | A casca ganha um vinco vertical. A luz é de dia, não o pôr do sol pedido. | sorteio |
| 18,0 | 6 | visual | baixa | Em "Near a flame, it sparks", nada faísca: só uma vela com a casca encostada. | sorteio |
| 3,7 | 2 | ritmo | baixa | 3,57 palavras/s numa cena de 2,8 s. A média do vídeo (2,75) está boa. | sorteio |
| 34,0 | 9 | visual | baixa | A queda de brilho é o fade final para preto; aceitável. | pipeline |

## Pipeline

- **Narração (TTS):** use uma voz do mesmo idioma do roteiro.
- **Inspetor:** passe ao Whisper o idioma do roteiro e registre o idioma detectado.
- **Mixagem:** normalize para -14 LUFS com pico máximo de -1 dBFS.
- **Legendas:** quebre os blocos no ponto final e nos cortes de cena.

## Lições

- Narração que diz que algo está ausente não deve ter esse elemento parado no prompt.
- A voz precisa estar no mesmo idioma do roteiro.
- Um bloco de legenda não junta duas frases nem atravessa um corte.
- A frase de impacto precisa de um prompt que mostre a ação acontecendo.
