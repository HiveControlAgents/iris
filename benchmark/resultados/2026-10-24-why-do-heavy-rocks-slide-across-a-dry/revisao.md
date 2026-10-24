# Revisão: The Rocks That Move Across Death Valley Alone

**Nota: 4,5 / 10**

O roteiro é claro e bem ritmado (2,5 a 3,0 palavras/s, 41 s, 1080x1920). Mas uma mão humana invade a cena 2, o "gelo" da cena 6 parece um prato de plástico, os rastros viram trincheiras e a transcrição da narração não bate com o roteiro.

## Refazer

| Cena | Motivo | Ajuste no prompt |
|---|---|---|
| 2 | Braço e mão com uma vara entram no quadro de 9,0 s a 11,0 s | "no people, no hands, no tools, no objects entering the frame"; câmera estática com leve deriva no lugar do pan |
| 6 | O gelo é um disco branco tipo prato e a pedra está num lago fundo (29 s a 34 s) | "wide thin sheet of cracked clear ice, like a broken window pane, on a film of water a few millimetres deep over flat cracked mud; no lake, no shore" |
| 1 | Mancha vermelha surge e pousa na pedra de 4,5 s a 6,0 s (gancho) | "faint shallow track a few centimetres deep, smooth-edged"; "no debris, no particles" |

## Problemas

- **6 s a 23 s, cenas 2 a 5, narração (alta, pipeline):** o transcritor ouviu português sem sentido onde o roteiro está em inglês (2,5% de acerto). O mais provável é o Whisper ter rodado em português. **Ouça esse trecho para confirmar** que a voz está certa. Pela regra, enquanto houver erro de narração a nota fica em no máximo 6.
- **4,5 s, cena 1 (média, sorteio):** mancha vermelha sobre a pedra. O sulco parece uma trincheira serrilhada.
- **16,6 s, cena 4 (média, sorteio):** era para ser noite estrelada e saiu dia. A pedra parece flutuar.
- **22,5 s, cena 5 (média, pipeline):** lago alpino com casas na margem, nada parecido com o Racetrack Playa.
- **Cenas 1, 3, 4 e 7 (média, pipeline):** os rastros saem como trincheira, fenda ou cordão, nunca como o rastro raso e liso real.
- **Todas as cenas (baixa, pipeline):** a pedra muda de forma entre as cenas, embora o roteiro diga "the same boulder".
- **Áudio (baixa, pipeline):** -15,8 LUFS, abaixo do alvo de -14.

Sem cortes internos, congelamentos ou telas pretas. O fade final da cena 7 é intencional.

## Pipeline

1. Inspetor: rodar o Whisper no idioma do roteiro (inglês), ou com detecção automática.
2. Prompts: trocar "groove" por "faint shallow track a few centimetres deep". Para água, usar "film of water a few millimetres deep… no lake, no shore".
3. Consistência: usar a imagem da cena 1 como referência nas cenas com "the same boulder".
4. Mixagem: normalizar para -14 LUFS.
