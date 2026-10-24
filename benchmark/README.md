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
| rotulados / labeled | precisão / precision | revocação / recall | certos | errados | perdidos |
|---|---|---|---|---|---|
| 3 (pendentes: 14) | 92% | 85% | 34 | 3 | 6 |

| tipo / type | precisão / precision | certos | errados |
|---|---|---|---|
| audio | 100% | 1 | 0 |
| legenda | 80% | 4 | 1 |
| narracao | 89% | 8 | 1 |
| ritmo | 100% | 5 | 0 |
| visual | 94% | 16 | 1 |

_Atualizado em 2026-10-24 com `python benchmark/bench.py metricas`._
<!-- metricas:fim -->

## Defects per video / defeitos por vídeo

<!-- tabela:inicio -->
| vídeo | nota | defeitos | visual | narracao | ritmo | audio | legenda | tecnico | onde (segundo e tipo) |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-12-por-que-os-corvos-conseguem-reconhece | 5.0 | 14 | 8 | 0 | 2 | 1 | 2 | 1 | 0:49.0 visual; 0:45.0 visual; 0:55.0 visual; 0:29.5 visual; 0:38.0 visual; 0:17.5 visual; 0:04.0 visual; 0:05.0 visual; 0:00.0 legenda; 0:38.5 legenda; 0:21.5 ritmo; 0:00.0 ritmo; 0:00.0 audio; 0:00.0 tecnico |
| Como o olho humano acompanha uma bola a 200 km/h? | 5.5 | 11 | 4 | 3 | 1 | 0 | 2 | 1 | 0:02.0 visual; 0:22.0 visual; 0:05.0 legenda; 0:11.0 legenda; 0:15.5 visual; 0:45.5 ritmo; 0:52.0 narracao; 0:02.0 narracao; 0:45.5 narracao; 0:11.7 visual; 0:00.0 tecnico |
| Como o olho humano acompanha uma bola a 200 km/h? | 5.5 | 13 | 6 | 4 | 1 | 0 | 2 | 0 | 0:47.0 visual; 0:19.5 visual; 0:21.7 visual; 0:06.1 visual; 0:21.5 narracao; 0:49.0 narracao; 0:38.2 narracao; 0:45.5 narracao; 0:52.0 legenda; 0:19.5 legenda; 0:06.1 visual; 0:21.7 ritmo; 0:31.0 visual |
| Como o olho acompanha uma bola a 200 km/h? | 6.5 | 11 | 5 | 2 | 2 | 1 | 1 | 0 | 0:24.5 visual; 0:04.1 visual; 0:10.8 visual; 0:00.0 ritmo; 0:00.0 legenda; 0:00.0 audio; 0:36.5 narracao; 0:00.5 narracao; 0:24.1 visual; 0:33.0 visual; 0:23.0 ritmo |
| Por que o rio Paraná sobe e desce sem parar | 5.5 | 11 | 2 | 5 | 2 | 0 | 2 | 0 | 0:22.0 narracao; 0:08.0 narracao; 0:29.0 narracao; 0:05.2 narracao; 0:30.0 visual; 0:17.0 legenda; 0:00.0 legenda; 0:18.1 ritmo; 0:37.5 ritmo; 0:11.7 visual; 0:01.0 narracao |
| A ciência por trás da precisão do pedreiro | 5.0 | 17 | 9 | 4 | 2 | 0 | 1 | 1 | 0:42.0 visual; 0:41.8 visual; 0:34.5 visual; 0:09.0 visual; 0:08.0 visual; 0:18.0 visual; 0:52.0 visual; 0:58.7 visual; 0:03.0 visual; 0:00.0 ritmo; 0:00.0 ritmo; 0:42.0 narracao; 0:11.0 narracao; 0:01.0 narracao; 0:28.5 narracao; 0:02.0 legenda; 0:00.0 tecnico |
| Como a águia enxerga tão longe | 2.5 | 14 | 5 | 6 | 2 | 1 | 0 | 0 | 0:00.0 narracao; 0:08.5 narracao; 0:19.0 narracao; 0:38.5 narracao; 0:22.8 narracao; 0:31.0 narracao; 0:02.0 visual; 0:30.0 visual; 0:52.0 visual; 0:15.0 visual; 0:00.0 ritmo; 0:00.0 ritmo; 0:02.0 audio; 0:07.2 visual |
| Como o futebolista chuta sem olhar e acerta | 6.0 | 10 | 5 | 2 | 2 | 0 | 1 | 0 | 0:05.0 visual; 0:29.0 visual; 0:45.5 visual; 0:24.1 visual; 0:33.4 visual; 0:00.0 ritmo; 0:00.0 ritmo; 0:24.5 narracao; 0:42.0 narracao; 0:31.5 legenda |
| O segredo dos passes de costas no futebol | 5.0 | 13 | 6 | 3 | 2 | 0 | 2 | 0 | 0:30.0 visual; 0:21.5 visual; 0:20.5 visual; 0:05.4 visual; 0:00.0 ritmo; 0:20.5 ritmo; 0:00.0 narracao; 0:00.0 narracao; 0:29.5 narracao; 0:00.0 legenda; 0:41.0 legenda; 0:31.3 visual; 0:20.5 visual |
| Por que a fumaça viaja centenas de quilômetros | 5.5 | 13 | 7 | 3 | 2 | 0 | 1 | 0 | 0:26.0 visual; 0:24.5 visual; 0:22.8 visual; 0:47.0 visual; 0:31.2 narracao; ? narracao; 0:18.0 narracao; 0:07.0 visual; 0:31.0 visual; 0:08.0 visual; 0:00.0 ritmo; 0:00.0 ritmo; 0:13.5 legenda |
| The Plant That Counts Before It Snaps | 5.0 | 11 | 7 | 1 | 1 | 0 | 2 | 0 | 0:00.0 narracao; 0:12.5 visual; 0:20.5 visual; 0:20.5 visual; 0:27.1 visual; 0:35.6 visual; 0:44.3 visual; 0:00.0 ritmo; 0:00.5 legenda; 0:11.5 legenda; 0:06.0 visual |
| Five Quiet Mysteries Nature Has Never Solved | 6.0 | 8 | 3 | 1 | 2 | 2 | 0 | 0 | 0:00.0 narracao; 1:22.8 ritmo; 2:57.6 visual; 0:00.0 ritmo; 7:10.8 visual; 6:17.4 visual; 6:56.0 audio; 3:59.1 audio |
| Every Orange Hides a Flammable Secret | 5.5 | 10 | 6 | 1 | 1 | 1 | 1 | 0 | 0:00.0 narracao; 0:14.5 visual; 0:00.0 audio; 0:13.5 legenda; 0:25.5 visual; 0:00.0 visual; 0:31.5 visual; 0:18.0 visual; 0:03.7 ritmo; 0:34.0 visual |
| Why Do Hundreds of Trees in Poland Bend North? | 4.5 | 10 | 6 | 1 | 1 | 1 | 1 | 0 | 0:00.0 visual; 0:00.0 narracao; 0:29.0 visual; 0:00.0 ritmo; 0:11.5 legenda; 0:00.0 audio; 0:33.5 visual; 0:20.8 visual; 0:16.7 visual; 0:03.7 visual |
| How Do Animals Find a Home They Have Never Seen? | 6.0 | 13 | 9 | 1 | 1 | 1 | 0 | 1 | 0:00.0 narracao; 1:27.5 visual; 3:45.5 visual; 3:59.6 visual; 3:27.0 visual; 3:20.0 visual; 4:14.5 visual; 0:23.0 visual; 2:54.0 visual; 2:31.5 visual; 0:00.0 ritmo; 3:25.3 tecnico; 0:00.0 audio |
| Who Draws These Perfect Circles in the Desert? | 7.0 | 8 | 4 | 1 | 1 | 1 | 1 | 0 | 0:11.0 visual; 0:00.0 narracao; 0:04.5 legenda; 0:00.0 audio; 0:22.5 visual; 0:27.5 visual; 0:01.0 ritmo; 0:38.5 visual |
| The Rocks That Move Across Death Valley Alone | 4.5 | 9 | 7 | 1 | 0 | 1 | 0 | 0 | 0:09.0 visual; 0:06.0 narracao; 0:29.0 visual; 0:04.5 visual; 0:16.6 visual; 0:22.5 visual; 0:00.0 visual; 0:11.4 visual; 0:00.0 audio |
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
