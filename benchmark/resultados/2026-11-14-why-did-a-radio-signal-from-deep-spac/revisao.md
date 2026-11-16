# Revisão ÍRIS: The Signal From Space That Never Came Back

**Nota: 7,0**

Vídeo limpo e bem medido, mas visualmente repetitivo: só Via Láctea e antenas, uma nebulosa fora do estilo com
estrelas que surgem, e o clímax do "Wow" sem imagem própria.

## Refazer (1 cena)

- **Cena 5, segunda imagem (0:25 a 0:31, nebulosa vermelha)**: estrelas azuis e magenta surgem e crescem entre
  quadros (a partir de 0:29.0) e a imagem parece arte digital, não fotografia. Ajuste do prompt: astrofotografia real
  de nebulosa de hidrogênio, brilho vermelho suave, estrelas pequenas sem pontas em cruz, sem silhueta preta no
  centro, só aproximação lenta.

## Problemas

| Segundo | Cena | Tipo | Gravidade | O que se vê | Origem |
|---|---|---|---|---|---|
| 0:29.0 | 5 | visual | alta | Estrelas surgem e crescem na nebulosa; estilo de arte digital saturada | sorteio |
| 0:37.7 | 7 | visual | média | "Printout", círculo e "Wow" narrados sobre mais uma antena ao amanhecer | pipeline |
| 0:10.5 | 3 | visual | média | Narração fala de um surto que sobe e some; a imagem é céu parado | pipeline |
| 0:09.7 | 3 | visual | média | 4 imagens da mesma Via Láctea (cenas 1, 3, 5, 8) e 4 antenas (2, 4, 6, 7) | pipeline |
| 0:17.0 | 4 | legenda | média | Legenda branca sobre o prato branco (cenas 2, 4, 6) e sobre a antena (1, 7, 8) | pipeline |
| 0:00.0 | 1 | narração | média | Narração não conferida: o transcritor ouviu o inglês como português | pipeline |
| 0:14.5 | 4 | visual | baixa | O telescópio é uma antena diferente em cada cena | pipeline |
| 0:16.0 | 4 | legenda | baixa | Blocos cortados: "IT LASTED SEVENTY-TWO" / "SECONDS.", "OF SKY." sozinho | pipeline |
| 0:09.5 | 3 | visual | baixa | Primeiro quadro das cenas difere do resto (0:09.5, 0:14.5, 0:20.0, 0:37.5, 0:43.0) | pipeline |
| 0:20.2 | 5 | ritmo | baixa | Cena de 11,1 s são duas imagens em fusão; a primeira repete as cenas 1 e 3 | pipeline |
| 0:47.8 | 8 | ritmo | baixa | Cerca de 2 s de cauda sem fala, só escurecendo | pipeline |

## O que está certo

- Áudio: -15,1 LUFS, pico -1,6 dBFS, sem distorção, sem buracos, sem saltos de volume.
- Formato: 1080x1920, 30 fps, 29,4 MB, 49,7 s.
- Gancho com data e mistério nos 2 primeiros segundos, e a cena final repete a primeira ("never came back").
- Sem cortes internos, congelamentos ou telas pretas; nenhum objeto deformado nas antenas.

## Sobre a narração

A taxa de acerto de 0,007 é falha da medição: a transcrição veio em português para um áudio em inglês. Não limitei a
nota por isso, mas a pronúncia fica sem conferência até a inspeção rodar com o idioma certo.

## Lições

1. Não repetir o mesmo assunto visual em mais de duas cenas; variar assunto, distância e ângulo.
2. A cena do clímax mostra o objeto que a narração cita, nunca imagem genérica.
3. Frase que narra um acontecimento pede esse acontecimento no prompt.
4. Nebulosas: pedir astrofotografia real, estrelas pequenas, cor discreta.
5. Objeto que volta em várias cenas precisa de descrição fixa ou imagem de referência.
6. Legenda fora do assunto principal e nunca branco sobre branco.
7. Quebrar legenda no fim da ideia.
8. Passar o idioma do vídeo ao transcritor na inspeção.

## Pipeline

- Inspeção: fixar o idioma do transcritor no idioma do roteiro.
- Roteiro visual: assunto diferente da cena anterior; clímax com o objeto da narração.
- Legendas: quebrar por pontuação e dar fundo ou contorno mais grosso.
- Geração: mesma descrição ou referência do telescópio em todas as cenas.
