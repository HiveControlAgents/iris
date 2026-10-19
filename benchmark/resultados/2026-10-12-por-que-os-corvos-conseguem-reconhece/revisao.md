# Revisão ÍRIS: Por que os corvos conseguem reconhecer rostos humanos

**Nota: 5,0 / 10**

Tema forte e áudio limpo, mas o modelo de vídeo enfia rostos humanos em quase todas as cenas, há deformações visíveis (bico que muda de cor, cérebros que viram rostos, texto inventado) e as legendas quebram as frases no meio.

## Cenas a refazer

| Cena | Motivo | Ajuste no prompt |
|---|---|---|
| 8 (45,2 a 53,1 s) | Cérebros duplicados que se transformam em dois homens nariz com nariz, sem relação com a narração | Cérebro de corvo ao lado de cérebro de chimpanzé, ilustração científica, câmera parada; sem pessoas, sem morph |
| 9 (53,1 a 59,6 s) | O bico do corvo muda de preto para amarelo em 55,0 s, na cena final | Corvo com bico e plumagem inteiramente pretos; o mesmo pássaro do início ao fim |
| 5 (29,4 a 37,8 s) | Gráfico com letras inventadas, silhuetas humanas no lugar de corvos e rostos em dupla exposição | Corvo observando duas pessoas de costas num parque; sem texto, gráfico ou números (o 80% fica na legenda) |

## Problemas

**Alta**
- 49,0 s, cena 8: cérebros viram dois homens de perfil quase encostados; não mostra corvo nem primata.
- 55,0 s, cena 9: bico preto vira amarelo e a cabeça muda de forma.
- 29,5 s, cena 5: infográfico com texto falso ('7A', símbolos), sem corvo; rostos humanos sobrepostos de 32 a 37,5 s.
- 38,5 s, cena 6: legenda "ELES NÃO ESQUECESSEM." com erro de português (é "esquecem"); provavelmente a voz também leu assim.

**Média**
- 4,0 s / 17,5 s / 21,5 s / 32 s / 49 s: rostos humanos não pedidos em 5 das 9 cenas (rosto no canto da cena 1, mulher que surge na cena 3, criança cortada no canto da cena 4, cenas 5 e 8). Vem do pipeline.
- 17,5 s, cena 3: mulher surge do nada, mãos entram pelas bordas e o cérebro deforma ao girar; e é um cérebro humano, embora a narração diga "deles".
- 5,0 s, cena 2: máscara quase invisível no escuro; as aves que fogem parecem andorinhas, não corvos; o "depois ele tira" não aparece; o brilho sobe ~40% ao longo da cena.
- 38,0 s, cena 6: calendário com números ilegíveis e papel deformando; cortes picotados a cada ~0,07 s entre 38,43 e 38,87 s (cena de 0,66 s).
- 45,0 s, cena 8: dois pares de cérebros iguais, que não ilustram a comparação.
- Vídeo todo: as legendas cortam a frase no meio ("RECONHECER E", "COLOCA UMA", "QUE É" / "SEGURO.", "QUEM É", "APÓS 5" / "ANOS...", "PARA") e ficam no centro, por cima do assunto.

**Baixa**
- 21,5 s, cena 4: corvos quase parados por ~8 s; ritmo de ~2,2 palavras/s, pouco abaixo do ideal.
- 0 a 2 s: o gancho é uma afirmação sobre um close parado; o experimento da máscara abriria melhor.
- Áudio em -15,3 LUFS (alvo -14); pico -1,4 dBFS e nenhum corte, ok.
- Arquivo de 47,6 MB, acima dos ~40 MB.

Sem roteiro, a narração não foi comparada com a transcrição; a voz não foi verificada.

## Para o pipeline
- Negativo padrão "sem pessoas, sem rostos humanos, sem texto na imagem" em toda cena cujo sujeito não seja uma pessoa.
- Legendas quebradas por pontuação (~32 caracteres), sem terminar em artigo/preposição, no terço inferior.
- Duração mínima de ~1,5 s por cena na montagem.
- Exportar em -14 LUFS e abaixo de ~40 MB.
