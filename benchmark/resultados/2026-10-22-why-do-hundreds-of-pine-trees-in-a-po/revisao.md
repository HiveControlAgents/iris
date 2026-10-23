# Revisão: Why Do Hundreds of Trees in Poland Bend North?

**Nota: 4.5 / 10**

O vídeo fala de pinheiros tortos, mas quase todas as cenas mostram troncos retos. A narração também não foi confirmada: o transcritor ouviu português num roteiro em inglês.

## Cenas a refazer
- **Cena 8 (29-33,5 s)**: o tronco atravessa um barco de madeira que veio da metáfora do prompt ("rib of a wooden boat"). Tire a comparação e descreva só a forma: tronco quase horizontal rente ao chão, depois sobe na vertical, vista lateral.

## Problemas principais
- **Alta, pipeline (0-29 s)**: o fenômeno não aparece. As cenas 1, 2, 3, 6 e 7 mostram troncos retos ou uma muda em pé. Por isso a cena 4 ("as outras crescem retas") fica igual às anteriores e o contraste some. Refazer com outra semente não resolve: o prompt precisa descrever a geometria ou usar uma imagem de referência.
- **Alta, pipeline (todo o vídeo)**: a narração não confere com o roteiro (acerto 2,7%, transcrição em português). Ou a voz do TTS é um modelo em português lendo inglês, ou o Whisper rodou com o idioma fixo em pt. Ouça os 4 s iniciais para saber qual é. Pelo critério, isso limita a nota a 6.
- **Média**: o gancho é fraco. A abertura mostra 3,7 s de floresta comum quase parada.
- **Média**: há legendas que juntam frases ou partem expressões: "NORTH. JUST OUTSIDE" (11,5 s), "THE STRANGE / PART:" (21-22 s), "AND ONLY" (19 s).
- **Média**: o áudio está em -15,8 LUFS, abaixo do alvo de -14.
- **Baixa**: na cena 9 a árvore está iluminada como de dia contra um fundo preto e parece recortada. Na cena 6 o céu sai azul de dia, embora o prompt peça anoitecer. O brilho cai mais de 15% dentro das cenas 1, 5 e 7. Os movimentos pedidos quase não aparecem (cenas 2 e 7).

## O que está bom
- Formato 1080x1920 e 23,7 MB.
- Ritmo entre 2,4 e 3,0 palavras por segundo.
- Sem picos cortados, silêncios, congelamentos ou telas pretas.
- A cena 4 (troncos retos) e a cena 5 (tronco inclinado com musgo) combinam com a narração.

## Pipeline
1. TTS e inspeção: usar uma voz no idioma do roteiro e passar `language='en'` ao Whisper.
2. Prompts: descrever a forma central de maneira física ou usar image-to-image a partir de uma referência, sem metáforas.
3. Montagem: quebrar as legendas por pontuação e normalizar o áudio para -14 LUFS.
