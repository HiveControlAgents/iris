# Revisão: tênis v3

**Nota 5,5.** A ideia é boa, mas o fim desmonta: bola aparece e some no ar, o vídeo passa de 50 s e termina numa frase truncada.

Medidas: 54,3 s · 540x960 (prévia) · LUFS -14,6 · pico -1,3 dBFS · 7 cenas · 0 congelamentos.

## Refazer (sorteio)
| Cena | Motivo | Ajuste de prompt |
|---|---|---|
| 7 (45,2 s a 54,3 s) | 0:47 uma bola surge no alto da quadra e some em meio segundo; 0:53 uma mancha amarela borrada atravessa o chão | quadra vazia e parada, "no ball, no flying objects" |

## Problemas
- **0:06 legenda** "CONSEGUE ACOMPANHÁ -LA?" com espaço antes do hífen e cruzando o corte para a cena do gavião (pipeline: divisão de palavras com hífen).
- **0:08, 0:19 legenda** blocos que aparecem meio transparentes, difíceis de ler (pipeline: transição da legenda).
- **0:31 a 0:37 ritmo** 7 s de quadra parada com a bola imóvel na linha: nada acontece enquanto a narração fala de visão periférica.
- **0:45 cor** a cena da quadra abre desbotada e meio segundo depois fica saturada (sorteio do encadeamento de clipes).
- **0:52 narração** o fecho "IMPRESSIONANTE! NÃO." soa como frase cortada.
- **Duração** 54 s para um Short de curiosidade: acima do alvo de 35 a 45 s (pipeline: roteiro longo demais).

## Lições
- esporte / geração: em cenas de quadra, pedir a quadra sem bola no ar; o modelo inventa bolas voando que somem.
- geral / roteiro: o fecho precisa ser uma frase completa que responde ao gancho, não uma exclamação solta.
- geral / montagem: nunca quebrar legenda em hífen de ênclise ("acompanhá-la").

Revisado pela ÍRIS, de Isaque Moutta: https://github.com/HiveControlAgents/iris
