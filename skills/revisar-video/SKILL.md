---
name: revisar-video
description: Reviews an AI-generated video (Shorts, Reels, TikTok) frame by frame, points out each defect with the exact second, says which scenes to regenerate and keeps lessons for the next videos. Use when asked to review, critique, check or score a video, or what to improve in it (also in Portuguese - revisar, criticar, dar nota).
---

# ÍRIS: revisão de vídeo gerado por IA

A ÍRIS não só olha o vídeo: ela mede, assiste quadro a quadro, separa azar de sorteio de defeito do pipeline,
manda refazer só as cenas ruins e aprende com cada vídeo. O ciclo é gerar, revisar, refazer, aprender.

## 1. Inspecionar

Rode o inspetor que está na pasta `scripts/` desta skill:

```bash
python "<pasta desta skill>/scripts/inspecionar.py" caminho/do/video.mp4 [--roteiro roteiro.json] [--referencia-voz voz.wav]
```

- `--roteiro`: JSON com `"cenas": [{"narracao": "...", "prompt": "...", "dur_s": 5.4}]`. Com ele, as cenas seguem o
  roteiro e a narração é comparada com o que foi dito (precisa de faster-whisper ou openai-whisper). Sem ele, as cenas
  vêm dos cortes bruscos. Veja `exemplos/roteiro.json` na raiz do plugin.
- `--referencia-voz`: gravação da voz aprovada. Confere se a narração ainda é a mesma voz (precisa de librosa).
- `--max-refazer N`: quantas cenas a revisão pode mandar refazer (padrão 3). Se o usuário pedir outro limite, passe aqui.
- Saída em `.iris/<nome-do-video>/`: `medidas.json` e `folha_N.jpg`.
- Se faltar ffmpeg ou Pillow, diga ao usuário o que instalar e pare.

## 2. Assistir

1. Leia `medidas.json` inteiro.
2. Abra TODAS as folhas de contato com a ferramenta de leitura de imagem. Cada folha tem 2 quadros por segundo
   (1 a cada 5 s em vídeo de mais de 3 min; o ritmo está em `medidas.json`, campo `folha`), 6 por linha, da esquerda para a direita, com o tempo em amarelo no canto. Compare quadros vizinhos: é ali que
   aparecem objetos sumindo, duplicando ou deformando.
3. Leia `.iris/historico.json` se existir (lições já aprendidas e últimos vídeos) e `.iris/regras.md` se existir
   (regras do canal, por exemplo "sem pessoas" ou "sem texto na imagem").

## 3. Analisar

Use o checklist de [criterios.md](criterios.md) e avalie gancho, virada e fecho por [retencao.md](retencao.md). Se
o vídeo é longo e horizontal (mais de 3 min), [longo.md](longo.md) substitui as regras de duração, vertical e legenda.
Se o vídeo foi gravado pelo usuário (rosto, tela, voz própria) e não gerado por IA, use também [reels.md](reels.md). Para cada problema, anote: segundo exato, cena, o que se vê, causa
provável e se é **sorteio** (aconteceu uma vez, outra semente resolve) ou **pipeline** (sistemático, ou já apareceu
em vídeos do histórico). Nunca descreva este vídeo com base no histórico: o histórico só serve para reconhecer padrões.

## 4. Entregar

Grave em `.iris/<nome-do-video>/`:

- `revisao.json`:
  ```json
  {"nota": 7.5, "resumo": "uma frase",
   "problemas": [{"segundo": 12.5, "cena": 3, "tipo": "visual|narracao|ritmo|audio|legenda|tecnico",
                  "gravidade": "alta|media|baixa", "descricao": "...", "causa": "...", "origem": "sorteio|pipeline"}],
   "refazer": [{"cena": 3, "motivo": "...", "ajuste_prompt": "o que mudar no prompt dessa cena, se algo"}],
   "licoes": [{"tipo_assunto": "esporte|animais|espaco|corpo_humano|historia|tecnologia|natureza|geral",
               "alvo": "roteiro|geracao|montagem", "regra": "regra geral, não detalhe deste vídeo"}],
   "pipeline": [{"onde": "arquivo ou etapa", "mudanca": "...", "motivo": "..."}]}
  ```
- `revisao.md`: a mesma revisão em texto curto para humanos, com a nota no topo e a lista de cenas a refazer.

Regras do `refazer`: no máximo `max_refazer` cenas (está em `medidas.json`; padrão 3), e só defeitos de sorteio que estragam o vídeo (objeto que some, duplica ou
deforma; pessoa, mão ou texto proibido pelas regras; salto brusco; imagem sem relação com a narração). Defeito leve,
de gosto ou de pipeline não entra. Se a pasta tiver `rodada: 2` (o usuário diz que é a versão refeita), `refazer`
fica vazio e a revisão diz se as cenas refeitas melhoraram.

## 5. Aprender

Atualize `.iris/historico.json` (crie se não existir):

```json
{"licoes": [{"tipo_assunto": "animais", "alvo": "geracao", "regra": "...", "vezes": 2, "ultima": "2026-10-17"}],
 "videos": [{"video": "nome", "data": "2026-10-17", "nota": 7.5, "resumo": "...", "refazer": [3]}]}
```

- Lição que repete uma existente (mesmo sentido, palavras diferentes) soma 1 em `vezes`; não duplique.
- Guarde no máximo 40 lições (descarte as de menor `vezes` e mais antigas) e os últimos 30 vídeos.

## 6. Corrigir o pipeline (só se o usuário pedir)

Se o projeto do usuário tem o código ou a config que gera os vídeos e ele pedir a correção:
- no máximo 3 edições, mínimas, preferindo config e texto de prompt a lógica;
- nunca mexa em caminhos de disco, chaves ou segredos;
- mostre o diff e rode os testes do projeto, se houver, antes de dizer que terminou.

## Resposta no chat

Nota, uma frase de resumo, as cenas a refazer com o motivo, e o caminho de `revisao.md`. Nada de repetir a revisão
inteira no chat.
