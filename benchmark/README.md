# ÍRIS benchmark / benchmark da ÍRIS

*Português abaixo.*

A public test of ÍRIS on real AI-generated videos: what it finds in each video (by type, with the exact second), and,
once a human has labeled the findings, how often it is right (**precision**) and how much it misses (**recall**).

- `resultados/<id>/`: the inspector measurements (`medidas.json`) and the ÍRIS review (`revisao.json`, `revisao.md`)
  of each video. Every review runs alone, with no history from other videos.
- `rotulos/<id>.md`: the labeling checklist. A human watches the video, marks each finding as right or wrong and
  lists the defects ÍRIS missed.
- `defeitos.csv`: every finding, one per line (video, second, type, severity, description).
- `videos.json`: the dataset (title, source, license, link). **Video files are not in the repository**: our own
  videos (the *Faísca de Saber* Shorts, generated with Wan 2.2 and Z-Image) are listed with their reviews; third-party
  samples (Veo, Kling, Sora...) only with a link and the review.

```
python benchmark/bench.py adicionar video.mp4 --id my-video --roteiro script.json
python benchmark/bench.py adicionar sample.mp4 --id veo-sample --fonte terceiro --link https://... --licenca "..."
python benchmark/bench.py pasta my_videos/ --padrao "*/video.mp4"   # every video not yet in the benchmark
python benchmark/bench.py metricas                                  # after labeling
python benchmark/rotular.py --videos my_videos/                    # labeling page on 127.0.0.1
```

## Precision and recall / precisão e revocação

<!-- metricas:inicio -->
No video labeled yet. / Nenhum vídeo rotulado ainda.
<!-- metricas:fim -->

## Defects per video / defeitos por vídeo

<!-- tabela:inicio -->
| vídeo | nota | defeitos | visual | narracao | ritmo | audio | legenda | tecnico | onde (segundo e tipo) |
|---|---|---|---|---|---|---|---|---|---|
| Como o olho humano acompanha uma bola a 200 km/h? | 5.5 | 13 | 6 | 4 | 1 | 0 | 2 | 0 | 0:47.0 visual; 0:19.5 visual; 0:21.7 visual; 0:06.1 visual; 0:21.5 narracao; 0:49.0 narracao; 0:38.2 narracao; 0:45.5 narracao; 0:52.0 legenda; 0:19.5 legenda; 0:06.1 visual; 0:21.7 ritmo; 0:31.0 visual |
| Como o olho acompanha uma bola a 200 km/h? | 6.5 | 11 | 5 | 2 | 2 | 1 | 1 | 0 | 0:24.5 visual; 0:04.1 visual; 0:10.8 visual; 0:00.0 ritmo; 0:00.0 legenda; 0:00.0 audio; 0:36.5 narracao; 0:00.5 narracao; 0:24.1 visual; 0:33.0 visual; 0:23.0 ritmo |
| O segredo dos passes de costas no futebol | 5.0 | 13 | 6 | 3 | 2 | 0 | 2 | 0 | 0:30.0 visual; 0:21.5 visual; 0:20.5 visual; 0:05.4 visual; 0:00.0 ritmo; 0:20.5 ritmo; 0:00.0 narracao; 0:00.0 narracao; 0:29.5 narracao; 0:00.0 legenda; 0:41.0 legenda; 0:31.3 visual; 0:20.5 visual |
<!-- tabela:fim -->

---

## Português

Um teste público da ÍRIS em vídeos reais gerados por IA: o que ela acha em cada vídeo (por tipo, com o segundo
exato) e, depois que um humano rotula os achados, quantas vezes ela acerta (**precisão**) e quanto deixa passar
(**revocação**).

Para rotular, o jeito fácil é a página local: `python benchmark/rotular.py --videos PASTA_DOS_VIDEOS` abre o
navegador; em cada achado, ▶ toca o trecho a partir de 2 s antes, e Certo / Errado já grava no arquivo. Ou, à mão: abra `rotulos/<id>.md`, assista ao vídeo, marque `[x] certo` ou `[x] errado` em cada achado e escreva,
um por linha, os defeitos que a ÍRIS não viu. Depois rode `python benchmark/bench.py metricas`, que atualiza a seção
acima. Só entram na conta os vídeos com todos os achados marcados.
