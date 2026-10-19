# Revisão ÍRIS: Por que a fumaça viaja centenas de quilômetros

**Nota: 5,5 / 10**

Áudio (-13,9 LUFS, pico -1,7 dBFS) e formato (1080x1920, 55 s, 25,8 MB) estão corretos. O vídeo perde pontos por quatro motivos: na cena 4 a fumaça vira um tubo sólido; o final fala de cidades e não mostra nenhuma; a narração engole "partículas"; e o ritmo é lento do começo ao fim. A nota fica limitada a 6 por causa dos erros de narração.

## Cenas a refazer
- **Cena 4 (22,8 s a 31,2 s)**: a partir de 26,0 s a fumaça vira um tubo branco sólido que se deforma, e em 24,5 s uma mancha escura surge e some. O close no chão também não combina com "se espalha sobre regiões inteiras". Ajuste: plano aéreo aberto de fumaça difusa sobre a floresta.
- **Cena 7 (47,0 s a 55,1 s)**: a narração diz "cidades ficam cobertas por fumaça" e a imagem mostra só uma nuvem. Ajuste: pedir no prompt o horizonte de uma cidade amazônica sumindo na fumaça parda.

## Outros problemas
- 31,2 s, cena 5: "partículas" foi ouvida como "cticulas" (sílaba cortada na emenda das cenas). **Pipeline.**
- Narração: "a" foi ouvido como "as" e outro "a" sumiu (o inspetor não deu o segundo); "alísios" saiu como "aliseos".
- Cenas 2, 3 e 7: a fumaça aparece como nuvens comuns (mar de nuvens, nuvem de chuva). **Pipeline.**
- Ritmo: de 1,84 a 2,05 palavras/s em todas as cenas (alvo de 2,3 a 3,0), com cenas de cerca de 8 s quase paradas. O gancho não faz a pergunta do título. **Pipeline.**
- Cena 5: o sol muda de tamanho entre 31,0 s e 31,5 s, e um reflexo verde e vermelho cresce no rodapé até 38 s (leve).
- Legendas "HORIZONTALMENTE. ESSAS" e "ALTITUDE. CIDADES" juntam duas frases e cruzam o corte (leve).

## Pipeline
- Folga de cerca de 100 ms antes de cada trecho de narração na emenda.
- Legenda quebrando em fim de frase e em corte de cena.
- Roteiro com 18 a 22 palavras por cena de 8 s e sem termos difíceis para o TTS.
- Estilo de queimada com "brownish wildfire smoke, not clouds, fire source visible".
