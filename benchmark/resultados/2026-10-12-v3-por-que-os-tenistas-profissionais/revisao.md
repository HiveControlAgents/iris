# Revisão ÍRIS: Como o olho humano acompanha uma bola a 200 km/h?

**Nota: 5,5 / 10**

As imagens são bonitas e o áudio está no ponto. O problema é que um vídeo sobre uma bola a 200 km/h quase não tem movimento. Duas cenas têm defeito de sorteio, e o roteiro e as legendas têm erros de português.

## Cenas a refazer

| Cena | Motivo | Ajuste no prompt |
|---|---|---|
| 7 | Bola surge do nada no céu em 47,0 s e some em 48,0 s | Pôr no negativo: no ball, no flying objects, nothing enters the frame |
| 3 | O falcão muda de plumagem (barriga alaranjada) a partir de 19,5 s | Giro de cabeça menor; pedir same bird, consistent plumage |

## Problemas

**Visual**
- 47,0 s (cena 7, alta): bola aparece e some na quadra vazia. *Sorteio.*
- 19,5 s (cena 3, média): o falcão muda de aparência ao virar a cabeça. *Sorteio.*
- Cenas 2, 4, 5 e 6 (média): o quadro de partida trocou a ação do prompt por objeto parado (olho de falcão no lugar de olho humano; raquete no chão no lugar de golpe; bola e gota paradas). O vídeo fica quase todo natureza-morta. *Pipeline.*
- 30,97 s (cena 5, baixa): quadra dura azul entre quadras de saibro, e a imagem não ilustra "visão periférica e concentração".
- Todas as cenas escurecem de 9% a 13% e ganham saturação ao longo do clipe (baixa). *Pipeline.*

**Narração / roteiro**
- 21,5 s (média): "onde ela **é** agora" deveria ser "está". *Pipeline.*
- 49,0 s (média): "o jogador **enxergava**" deveria ser "enxerga", e a frase final fica confusa. *Pipeline.*
- 38,17 s (baixa): a explicação científica é frouxa. A retina "atualizando" não explica o tema, e o vídeo omite o essencial: antecipar a trajetória e levar o olhar até o ponto de contato.
- Palavras ouvidas com pouca certeza: "quando" (45,5 s) e "por" (2,0 s ou 41,0 s). Vale ouvir esses trechos. Nenhum erro de transcrição.

**Legendas**
- 52,0 s: "IMPRESSIONANTE! NÃO." inverte o sentido de "Impressionante, não?".
- 5,0 a 6,5 s: "ACOMPANHÁ -LA?" tem um espaço solto. 11,0 a 12,0 s: "MUSCULOS" está sem acento.
- 21,5 s: o fragmento "É AGORA." aparece sozinho sobre a cena da raquete. Em 19,5 s, o bloco "BOLA ESTARÁ" entra quase transparente.

**Ritmo**
- As cenas 2, 4 e 7 passam de 9 s com imagem quase parada. A cena 4 tem fala lenta (1,94 palavra/s). A média geral está boa (2,5 palavras/s).

**Áudio e técnico:** sem problemas. O áudio tem -14,5 LUFS e pico de -1,4 dBFS, sem cortes, silêncios ou saltos de volume. O vídeo é 1080x1920, tem 36 MB e não tem congelamentos nem telas pretas.

## Pipeline
1. **Quadro de partida:** manter o sujeito e a ação do prompt_video, com movimento lento, em vez de natureza-morta.
2. **Legendas:** usar o texto do roteiro com os tempos do Whisper (acentos, pontuação, ênclise) e não deixar fim de frase sozinho na cena seguinte.
3. **Roteiro:** revisar gramática e fatos antes de gerar a narração.
4. **Montagem:** dividir em dois planos as cenas estáticas de mais de ~7 s.
