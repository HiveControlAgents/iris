# Revisão: Why Is This Antarctic Glacier Bleeding Red?

**Nota: 7,0** (provisória)

Visual bonito e fiel à história de Blood Falls, com áudio limpo. Faltam três coisas: verificar a narração, manter a mesma geleira entre as cenas e cortar melhor as legendas.

## Cenas a refazer
Nenhuma. Não há defeito de sorteio que estrague o vídeo. Os problemas principais vêm do pipeline.

## Problemas
- **0,0 s, narração (média, pipeline):** a narração não foi verificada. O inspetor rodou o Whisper em `pt` (padrão) sobre uma voz em inglês, e o texto ouvido sai traduzido ("eles não vivem com nenhuma luz…"). Os 4 "erros" são falso alarme, mas a voz real não foi conferida. Rode de novo com `--idioma en`. Se aparecerem erros reais, a nota cai para no máximo 6.
- **5,0 s, cena 2, visual (média, pipeline):** o prompt diz "the same cliff", mas a cena 2 mostra um pico pontudo de gelo e a cena 7 (33,1 s) outro bloco. São três geleiras diferentes.
- **37,5 s, cena 7, visual (baixa, sorteio):** no push-in, a faixa fina da mancha se funde à principal e some, e a borda do bloco muda.
- **16,0 s, cena 4, visual (baixa, sorteio):** poço a céu aberto numa planície, sem a parede de gelo pedida. A imagem contradiz "sunlight has not touched it", e o quadro fica quase parado por 5,8 s.
- **8,5 s, legenda (baixa, pipeline):** "AND THE NAME BLOOD" / "FALLS STUCK." separa o nome. Em 14,0 s e 17,5 s os blocos misturam duas frases, e "WATER. THAT WATER" atravessa o corte das 16,0 s.
- **0,0 s, legenda (baixa, pipeline):** no gancho, a legenda no centro cobre a mancha vermelha. Na cena 5, cobre a base da cascata.
- **21,8 s, cena 5, ritmo (baixa, pipeline):** 3,42 palavras/s. As cenas 1, 3 e 4 também passam de 3,0.
- **39,3 s, ritmo (baixa, pipeline):** o fade para preto no fim quebra o loop do Shorts.
- **Áudio (baixa, pipeline):** -15,5 LUFS, abaixo do alvo de -14. O pico de -1,3 dBFS está ok, sem cortes nem silêncios.

## O que está bom
Formato 1080x1920 com 24,4 MB. O gancho mostra a mancha já no quadro 0. As cenas 5 e 6 ilustram bem "sai clara e fica vermelha". Não há congelamentos nem telas pretas no meio.

## Pipeline
1. `scripts/inspecionar.py`: passar `--idioma` conforme o roteiro (ou detectar o idioma), em vez de fixar `pt`.
2. Geração: nas cenas que dizem "the same", usar a imagem da cena 1 como referência.
3. Legendas: cortar na pontuação, manter os nomes próprios juntos, não atravessar cortes de cena e colocar no terço inferior.
4. Mixagem: normalizar para -14 LUFS e tirar o fade para preto do final.
