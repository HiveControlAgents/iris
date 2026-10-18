# Critérios da ÍRIS

Valores de referência para Shorts/Reels verticais. Use as medidas de `medidas.json` e as folhas de contato.

## Visual (folhas de contato)
- Objeto que some, duplica, deforma ou surge entre quadros vizinhos.
- Ação rápida (golpe, arremesso, bola voando) que o modelo de vídeo não sustenta.
- Anatomia quebrada: mãos, dedos, olhos, membros a mais ou a menos.
- Texto ilegível ou inventado dentro da imagem.
- Imagem sem relação com a narração daquela cena.
- `cortes_internos_s`: salto dentro de uma cena, longe da fronteira.
- Brilho ou saturação que derivam do início ao fim da cena (`brilho_ini` x `brilho_fim`, diferença acima de ~15%).
- `congelamentos`: imagem parada por 2 s ou mais. `telas_pretas`: quase sempre defeito.

## Narração
- `narracao.divergencias`: roteiro x transcrição. Costuma ser pronúncia errada ou palavra engolida.
- `narracao.taxa_acerto` abaixo de 0,9 merece atenção.
- `audio.identidade_voz.confere = false`: a voz mudou em relação à referência.

## Ritmo
- `palavras_por_s` entre 2,3 e 3,0 é bom para vídeo curto.
- Gancho forte nos 2 primeiros segundos: a primeira cena precisa ter movimento ou pergunta.
- Cena de mais de ~8 s com imagem quase parada cansa.

## Áudio
- `lufs_integrado` alvo -14 (±1) para YouTube/Instagram. Abaixo de -16 fica baixo no celular.
- `pico_dbfs` até -1. Acima disso, risco de distorção depois da compressão da plataforma.

## Legendas (vistas nas folhas)
- No máximo ~32 caracteres por bloco, sem cobrir o assunto principal.
- Palavra cortada no meio de uma ideia ("BOLA DE TÊNIS A") deixa a leitura truncada.

## Técnico
- Vertical 1080x1920 é o padrão; 540x960 serve para prévia, não para publicar.
- Tamanho até ~40 MB para subir rápido pelo celular.

## Sorteio x pipeline
- **Sorteio**: aparece uma vez; trocar a semente resolve. Vai para `refazer`.
- **Pipeline**: sistemático no vídeo, ou já aparece no histórico. Vai para `pipeline` e vira lição.
- Se uma correção de pipeline já foi aplicada e o problema voltou, diga e sugira outra abordagem.
