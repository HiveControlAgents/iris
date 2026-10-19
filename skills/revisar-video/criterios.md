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
- O transcritor (Whisper) corrige sozinho muita pronúncia torta: `narracao.taxa_acerto` alta NÃO prova que a voz
  falou certo e nunca é ponto forte.
- `narracao.erros` (palavra inventada, engolida ou trocada): problema de tipo `narracao`, gravidade alta. Com
  qualquer erro, a nota fica no máximo 6. Cite a palavra e a cena.
- `narracao.suspeitas` (palavra por outra parecida, ex. "alisios"/"aliseos") e `narracao.duvidosas` (ouvidas com
  pouca certeza): gravidade media.
- Palavra difícil que erra em vídeos seguidos (termo técnico, nome estrangeiro) é problema do pipeline: lição de alvo
  `roteiro` pedindo uma palavra mais comum no lugar.
- `audio.identidade_voz.confere = false`: a voz mudou em relação à referência.

## Ritmo
- `palavras_por_s` entre 2,3 e 3,0 é bom para vídeo curto.
- Gancho forte nos 2 primeiros segundos: a primeira cena precisa ter movimento ou pergunta.
- Cena de mais de ~8 s com imagem quase parada cansa.

## Áudio
- `lufs_integrado` alvo -14 (±1) para YouTube/Instagram. Abaixo de -16 fica baixo no celular.
- `pico_dbfs` até -1. Acima disso, risco de distorção depois da compressão da plataforma.
- `picos_cortados.trechos` > 0: o áudio bateu no teto digital (distorção audível). Gravidade alta se passar de ~10.
- `silencios`: buraco de 0,7 s ou mais no meio do vídeo. Entre frases é respiro; no meio de uma frase, ou mais de
  ~1,5 s, quebra o ritmo.
- `saltos_volume`: o volume muda 6 LU ou mais em 1 s (troca de música, cena mixada em outro nível, voz que some).
- `voz_abafada`: trecho em que a música (ou ruído) preenche os vãos da fala. É heurística: confirme pela transcrição
  (palavras `duvidosas` ou erros no mesmo trecho) antes de dar gravidade alta.

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
