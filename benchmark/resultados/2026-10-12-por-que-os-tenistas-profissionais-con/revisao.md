# Revisão ÍRIS: "Como o olho humano acompanha uma bola a 200 km/h?"

**Nota: 5,5 / 10**

Áudio e ritmo bons, mas a bola de tênis duplica e deforma no gancho e na cena do saibro, as legendas cortam as frases no
meio e o estilo "documentário de natureza" troca o tênis por falcão e gota d'água.

## Cenas a refazer

Nenhuma só com troca de semente. A bola duplicou nas **duas** cenas com ação rápida (1 e 4), então o defeito é do
pipeline: primeiro corrija o prompt (veja abaixo) e depois regenere as cenas 1 e 4.

## Problemas

| Seg. | Cena | Tipo | Grav. | O que se vê | Origem |
|---|---|---|---|---|---|
| 2,0 | 1 | visual | alta | A bola vira duas no gancho (2,0 / 3,0 / 4,0-4,5 s) e aparece borrada em 5,5 s | pipeline |
| 22,0 | 4 | visual | alta | Duas bolas no saibro; bola parada na linha enquanto a raquete passa (25,5-27 s), depois na raquete e de volta ao chão | pipeline |
| 5,0 | 1 | legenda | média | "ACOMPANHÁ -LA?" separado, em cima da bola e do olho | pipeline |
| 11,0 | 1 | legenda | média | Blocos truncados ("CÉREBRO ANTECIPA ONDE A", "SUA RETINA ATUALIZA A"...) e "MUSCULOS" sem acento | pipeline |
| 15,5 | 3 | visual | média | Falcão na moita sem relação com "cérebro antecipa onde a bola estará"; a gota dourada da cena 7 também fica longe do assunto | pipeline |
| 45,5 | 8 | ritmo | média | 9 s finais de rede vazia, imagem parada | sorteio |
| 2,0 / 45,5 | 1, 8 | narração | média | "por" e "quando" ouvidos com pouca certeza: confirme ouvindo | sorteio |
| 52,0 | 8 | narração | baixa | "enxergava" (deveria ser "enxerga") e "Impressionante! Não." no lugar de "Impressionante, não?" | pipeline |
| 11,7 | 2 | visual | baixa | O brilho sobe 32% na cena 2 (e 29% na cena 7) | sorteio |
| — | — | técnico | baixa | 45 MB, acima de ~40 MB | pipeline |

Pontos fortes: -14,5 LUFS, pico -1,4 dBFS, sem distorção nem silêncios; 2,5 palavras/s; 1080x1920; o close do olho
(6-15 s) está limpo.

## Pipeline

1. **Prompts com bola (cenas 1 e 4):** pedir uma única bola em câmera lenta extrema, ou o olhar do tenista, em vez de bola a 200 km/h e impacto de raquete.
2. **Legendas:** cortar pelas pausas e pela pontuação (até ~32 caracteres), manter "acompanhá-la" junto, preservar os acentos e usar o terço inferior.
3. **Estilo visual:** escolher pelo tema (esporte → transmissão esportiva em câmera lenta), não "nature documentary" fixo.
4. **Codificação:** ~5,5 Mbps para ficar abaixo de 40 MB.

## Lições

- Esporte/geração: nada de bola em voo ou impacto rápido; uma única bola em câmera lenta ou o rosto do atleta.
- Esporte/geração: o estilo visual deve combinar com o tema.
- Geral/montagem: legenda por unidade de sentido, no terço inferior.
- Geral/roteiro: feche com uma imagem em ação e confira a pontuação da pergunta final.
