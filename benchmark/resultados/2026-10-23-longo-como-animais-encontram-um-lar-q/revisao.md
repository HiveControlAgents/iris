# Revisão ÍRIS: "How Do Animals Find a Home They Have Never Seen?"

**Nota: 6,0 / 10**

Documentário bonito e coerente com o tema, mas quase todo feito de imagens paradas com zoom lento. Três cenas estragam o vídeo, e a narração não pôde ser validada: a transcrição tratou áudio em inglês como português.

## Refazer

| Cena | Tempo | Motivo | Ajuste no prompt |
|---|---|---|---|
| 12 | 1:27–1:34 | A narração fala de milhões de monarcas nos galhos e a imagem mostra só um pinheiro, sem borboletas | Pedir milhares de monarcas agrupadas nos galhos de abeto, com os galhos vergando |
| 28 | 3:43–3:51 | O rosto do pisco deforma (máscara preta a partir de 3:45,5) | Plano médio, ave parada de perfil, outra semente |
| 30 | 3:59–4:09 | Tábuas molhadas sem relação com o clímax (cabanas blindadas, física quântica) | Mostrar a cabana com blindagem metálica à noite ou o pisco voando ao sul |

## Outros problemas

- **Narração (alta, pipeline):** taxa_acerto 0,041 porque o Whisper traduziu o inglês para o português (aparecem "butterflies", "hatchlings", "birde"). A narração ficou sem verificação e a nota vai no máximo a 6 até uma nova transcrição em inglês sair limpa.
- **Cena 27, 3:25–3:33 (média):** close do pisco com o fundo virando de verde para roxo e a plumagem mudando.
- **Ritmo (média, pipeline):** 31 cenas de 7 a 10 s, quase todas foto parada com Ken Burns. A abertura não tem gancho visual.
- **Leves:** o pisco vira a cabeça de uma vez (3:19 e 4:14,5); ovos de salmão expostos em vez de escondidos no cascalho (0:23); ovos de tartaruga em anel de coração (2:54); arrebentação que muda e mancha fixa no canto (cena 20).
- **Áudio:** -15,7 LUFS, um pouco abaixo de -14. Sem cortes, silêncios ou saltos.
- **Técnico:** o detector não marcou a troca em ~3:33, então a "cena 27" ficou com 17,5 s.

## Pipeline

1. Transcrever no idioma do roteiro (hoje sai forçado em português).
2. Misturar clipes com movimento real e variar a duração das cenas.
3. Normalizar a mixagem para -14 LUFS.
4. Inspecionar com `--roteiro` para alinhar as cenas.
