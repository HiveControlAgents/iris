# Revisão ÍRIS: "The Waterfall That Turns Into Fire Every February"

**Nota: 6,0 / 10**

O visual é forte e fiel ao tema: o "fogo" da Horsetail Fall aparece já no primeiro quadro. A nota fica limitada a 6 porque a
narração não pôde ser conferida (a transcrição saiu em português), o pico de áudio bate em 0 dBFS e o roteiro corre rápido demais.

## Cenas a refazer

Nenhuma. Não há defeito de sorteio que estrague o vídeo: nada some, duplica ou deforma, e não há salto brusco nem imagem fora do tema.

## Problemas

| Segundo | Cena | Tipo | Gravidade | O que é | Origem |
|---|---|---|---|---|---|
| 0,0 | 1 | narração | alta | 9 "erros" e acerto de 7%: o roteiro está em inglês e a transcrição veio em português, mas acompanha o sentido do roteiro e deixa vazar palavras em inglês ("granite", "face"). Quase certamente é o transcritor no idioma errado, não a voz. Mesmo assim, nada foi conferido. | pipeline |
| 5,37 | 2 a 6 | ritmo | média | De 3,0 a 3,6 palavras/s em cinco das sete cenas (o ideal é de 2,3 a 3,0). | pipeline |
| 0,0 | todas | áudio | média | Pico em 0,0 dBFS (o limite é -1) e volume de -15,2 LUFS, um pouco baixo. | pipeline |
| 4,5 / 18,5 / 28,0 | 1, 4, 6 | legenda | baixa | Blocos que atravessam o fim de frase ("ONLY. IT FALLS DOWN", "RIGHT. THE WATER GLOWS", "APPEARS. NO LAVA,"). | pipeline |
| 10,0 | 3 (e 6) | visual | baixa | A narração diz "thin ribbon", "barely there" e "fragile", mas a imagem mostra uma cachoeira larga e cheia. | pipeline |
| 6,0 | 2 | visual | baixa | Pequena mancha azulada no topo da queda, estável. | sorteio |
| 28,9 | 7 | visual | baixa | O brilho cai cerca de 22% e a água laranja em close lembra lava, justo quando a narração diz "no lava". | sorteio |

## Pontos fortes

- O gancho é visual e imediato, com o firefall desde 0,0 s.
- O contraste entre luz e sombra das cenas 1, 4 e 5 conta a explicação sem precisar de texto.
- Não há congelamentos, telas pretas nem cortes internos. O vídeo está em 1080x1920 e tem 21,8 MB.

## Para o pipeline

1. Transcrever a narração no idioma do roteiro (inglês) e rodar a checagem de novo; a nota pode subir para cerca de 7,5.
2. Normalizar o áudio final em -14 LUFS, com pico máximo de -1 dBTP.
3. Quebrar as legendas na pontuação e limitar o roteiro a cerca de 2,7 palavras/s.
