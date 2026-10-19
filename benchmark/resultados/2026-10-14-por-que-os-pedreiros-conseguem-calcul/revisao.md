# Revisão: A ciência por trás da precisão do pedreiro

**Nota: 5,0 / 10**

Áudio limpo e tema bem amarrado no fim, mas em 5 de 8 cenas o modelo de vídeo faz surgir ferramentas, mãos ou água do
nada, a imagem das cenas sobre o cérebro não tem relação com a fala e o ritmo é lento (1,7 a 2,1 palavras/s).

## Cenas a refazer

1. **Cena 6 (41,8–50,6 s)**: aos 42 s uma mão com ferramenta entra e cutuca a bolha do nível; a ferramenta muda de
   forma entre quadros. Prompt: nível parado, a bolha assenta no centro, "no hands, no tools, nothing enters the frame".
2. **Cena 5 (33,1–41,8 s)**: aos 34,5 s surge uma faca que corta o concreto e a quina muda de forma; a fala é sobre
   mãos. Prompt: dedos de uma mão calejada deslizando na aresta áspera.
3. **Cena 2 (8,0–17,5 s)**: fio de água cai do nada (9–11 s) e a pedra troca de cor e de forma (11,5–12 s); pedra de
   rio não tem relação com o córtex parietal. Prompt: o olhar do pedreiro mirando a fiada de tijolos.

A cena 3 (ferramenta e pedaços de mão surgindo a partir de 18 s) seria a próxima da fila; ficou de fora pelo limite de 3.

## Problemas

| s | Cena | Tipo | Grav. | O que se vê | Origem |
|---|---|---|---|---|---|
| 42,0 | 6 | visual | alta | Mão com ferramenta cutuca a bolha; ferramenta muda de forma; brilho cai ~20% | sorteio |
| 34,5 | 5 | visual | alta | Faca surge e corta o concreto; quina deforma | sorteio |
| 9,0 | 2 | visual | alta | Jato de água surge e some; pedra troca de cor e forma | sorteio |
| 8,0 | 2 | visual | média | Pedra de rio para falar de córtex parietal | pipeline |
| 18,0 | 3 | visual | média | Ferramenta de rejunte surge; pedaços de mão na borda | sorteio |
| 52,0 | 7 | visual | baixa | Sombra de pessoa e mão com talhadeira não pedidas | pipeline |
| 58,7 | 8 | visual | baixa | Pá de jardim em vez de colher de pedreiro; lâmina varia | sorteio |
| 3,0 | 1 | visual | baixa | Bolhas do nível e borda mudam; cabo azul aparece | sorteio |
| 0,0 | 1 | ritmo | média | Gancho fraco: 8 s de nível parado, sem pergunta | pipeline |
| — | todas | ritmo | média | 1,72 a 2,07 palavras/s; cenas de 7 a 9,5 s quase paradas | pipeline |
| 42,0 | 6 | narração | média | "cerebelo" ouvido como "cérebro"; "ajusta" como "ajuste a" | pipeline |
| 11,0 | 2 | narração | média | "córtex parietal" ouvido como "cortexpareetal" | pipeline |
| 1,0 | 1 | narração | média | "parede" como "pareda"; "tato" duvidoso | sorteio |
| 28,5 | 4 | narração | média | "captam" como "capta uma" | sorteio |
| 2,0 | 1 | legenda | baixa | Blocos cruzam frases ("OBSERVANDO. NENHUMA", "POSIÇÃO. REPETIÇÃO"); legenda sobre o nível | pipeline |
| — | — | técnico | baixa | 40,1 MB, no limite para subir pelo celular | pipeline |

Áudio sem problemas: -14,4 LUFS, pico -1,8 dBFS, sem cortes, silêncios ou saltos. 1080x1920, 30 fps.

## Pipeline

- **Prompt de movimento**: terminar com "only the described motion; nothing enters the frame; no hands, no tools
  unless described". Em 5 de 8 cenas surgiram objetos não pedidos.
- **Roteiro**: quando a fala for abstrata (cérebro), mostrar o pedreiro usando a capacidade, não texturas soltas.
- **Montagem**: duração pela fala (alvo 2,5 palavras/s) ou voz ~20% mais rápida.
- **Legendas**: quebrar na pontuação e no terço inferior.
- **Exportação**: bitrate um pouco menor para ficar abaixo de 40 MB.

## Lições

- Prompt de objeto parado faz o modelo inventar ação; dê um movimento simples e proíba objetos entrando no quadro.
- Fala sobre o corpo ou o cérebro: mostre a pessoa usando a capacidade, não textura genérica.
- Termos anatômicos parecidos com palavras comuns (cerebelo/cérebro) saem trocados na voz; simplifique.
- Abaixo de 2,3 palavras/s, encurte a cena em vez de esticar a imagem.
- Legenda quebra na pontuação e não cobre o objeto principal.
