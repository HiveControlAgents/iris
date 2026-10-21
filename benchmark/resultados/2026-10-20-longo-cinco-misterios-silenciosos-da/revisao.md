# Revisão: Five Quiet Mysteries Nature Has Never Solved

**Nota: 6,0 / 10**

O vídeo longo (9:45, 1920x1080) é visualmente limpo e coerente com os cinco mistérios, e o áudio está no alvo (-13,9 LUFS, pico -1,0 dBFS, sem distorção). Pesam contra ele as imagens quase paradas por 12 s ou mais e uma narração que não pôde ser conferida.

## Cenas a refazer

- **Cena 16 (2:57.6-3:14.2):** cogumelos translúcidos e sobrepostos, com cara de dupla exposição. Ajuste no prompt: corpo sólido e opaco, brilho verde só nas lamelas e bordas, grupo pequeno e nítido, sem transparência.

## Problemas

- **Alta, narração, pipeline:** a transcrição saiu em português sobre um roteiro em inglês, e o transcritor traduziu em vez de transcrever. Por isso a taxa de acerto deu 3% e as divergências não provam erro de voz, mas a pronúncia de acacia, kudu e foxfire continua sem conferência. A nota fica limitada a 6 até a narração ser checada na língua certa.
- **Média, ritmo, pipeline:** cada imagem fica de 10 a 15 s praticamente parada, com zoom leve. A cena 23 (4:41-5:19) junta três imagens de ~13 s.
- **Média, visual, sorteio:** cena 16, cogumelos translúcidos (veja acima).
- **Baixa, ritmo:** o gancho fica 12 s numa imagem do vale com a luz parada, enquanto a narração diz que ela paira e some.
- **Baixa, visual, sorteio:** cena 33 (7:10.8): monte de pó numa mesa de estúdio. Destoa do estilo de natureza.
- **Baixa, visual, sorteio:** cena 29 (6:17.4): duna chapada e lavada.
- **Baixa, áudio:** o fundo sobe sob a voz entre 6:56 e 6:58. Não deu para confirmar pela transcrição.
- **Baixa, áudio:** pausas de 0,8 s (3:59.1) e 0,9 s (5:58.8). Provavelmente são respiro.

Nenhum objeto some ou duplica, não há tela preta nem congelamento, e as imagens batem com os temas (acácia, girafa, kudu, fungo, mofo, dunas, vale norueguês).

## Pipeline

1. **Transcrição:** usar o idioma do roteiro ou a detecção automática, não português fixo.
2. **Detecção de cenas:** cinco trocas suaves de imagem passaram (~0:12, 3:26, 4:55, 5:08, 9:08). Passe `dur_s` no roteiro ou baixe o limiar.
3. **Montagem:** no máximo ~8 s por imagem, ou um clipe com movimento real.

## Lições

- Vídeo longo e calmo: troque de imagem ou de enquadramento a cada 6 a 8 s.
- Bioluminescência: peça corpo sólido, com brilho só nas bordas.
- Close de material (areia, grãos): ponha cenário natural no prompt.
