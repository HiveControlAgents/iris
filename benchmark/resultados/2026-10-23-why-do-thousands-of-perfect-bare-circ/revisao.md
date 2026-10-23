# Revisão: Who Draws These Perfect Circles in the Desert?

**Nota: 7.0 / 10**

O visual é coerente e bonito na maior parte. A cena 3 mostra círculos cinza de pedra em duas fileiras retas no lugar de areia vermelha em favo de mel. As legendas quebram no meio das ideias, o áudio está baixo e a narração não pôde ser conferida porque a transcrição saiu em português.

## Refazer

- **Cena 3 (11.0–16.6 s)**: os círculos aparecem cinza, como discos de pedra, em duas fileiras retas até as dunas. Isso não combina com o "giant honeycomb" da narração nem com os círculos de areia vermelha das cenas 1 e 2.
  Ajuste: pedir vista aérea de cima ("top-down"), círculos de areia vermelha cercados de capim dourado, "honeycomb-like hexagonal pattern filling the frame, no rows, no paths, no stones".

## Problemas

| s | Cena | Tipo | Gravidade | O quê | Origem |
|---|---|---|---|---|---|
| 11.0 | 3 | visual | média | Círculos cinza de pedra em fileiras, em vez de favo de mel de areia vermelha | sorteio |
| — | todas | narração | média | Não verificada: o Whisper transcreveu em português, e os 5 "erros" são artefato do idioma | pipeline |
| 4.5 / 10.0 / 16.5 / 23.0 / 30.5 | 1–6 | legenda | média | Blocos misturam frases ("THEM. THEY ARE CALLED"), atravessam corte e partem termos ("SAND" / "TERMITES") | pipeline |
| — | todas | áudio | média | -15,9 LUFS (alvo -14) | pipeline |
| 22.5 | 5 | visual | baixa | Círculos do fundo parecem buracos escuros | sorteio |
| 27.5 | 6 | visual | baixa | Sem as gotas d'água pedidas; tufo em leque artificial; montinho surge em 31.0 s | sorteio |
| 1.0 | 1 | ritmo | baixa | 3,14 palavras/s no gancho | sorteio |
| 38.5 | 7 | visual | baixa | Fade-out deixa o sol esverdeado em 39.0 s | pipeline |

Sem congelamentos, telas pretas, cortes internos, silêncios ou clipping. O vídeo está em 1080x1920 e tem 24,4 MB.

**Sobre a nota:** as regras limitam a nota a 6 quando `narracao.erros` não está vazio. Esse limite não foi aplicado aqui porque o texto "ouvido" é uma tradução para o português que acompanha o roteiro frase a frase ("circulos feris", "deserto namib", "termites de sand"). Ou seja, os erros vêm do transcritor, não da voz. Mesmo assim, a pronúncia não foi checada.

## Pipeline

- **Transcrição (inspecionar.py)**: forçar o idioma do roteiro (`language="en"`).
- **Legendas**: quebrar os blocos por frase (até ~32 caracteres) e fechar cada bloco no corte de cena.
- **Mixagem**: normalizar para -14 LUFS.

## Lições

- (natureza/geração) Quando várias cenas mostram o mesmo objeto, repita no prompt de cada uma a cor, o material e a borda.
- (geral/geração) Para padrão espalhado pelo terreno, peça vista de cima. Em perspectiva, o padrão vira fileiras.
- (geral/montagem) Legenda termina em pausa natural, não atravessa corte e não parte termo composto.
