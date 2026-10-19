# Re-render adapters / Adaptadores para refazer cenas

*Português abaixo.*

ÍRIS writes `revisao.json` with a `refazer` list: the scenes worth regenerating (at most `--max-refazer`, default 3),
each with a reason and a suggested prompt change. An adapter takes that list and regenerates only those scenes.

## ComfyUI (included, local, free)

```
python -m iris.comfyui .iris/<video>/revisao.json --roteiro script.json --workflow my_workflow_api.json
```

1. In ComfyUI, build the workflow that generates one scene (text-to-video, image-to-video, whatever you use) and
   export it with **Save (API Format)**.
2. In that JSON, put the markers in the fields: `"{{prompt}}"` in the positive prompt, `"{{seed}}"` in the seed
   (it becomes a new number per scene) and, optionally, `"{{nome}}"` in the output file prefix.
3. The scene prompt comes from the script (`prompt_video`, `prompt` or `narracao`), plus the `ajuste_prompt` that
   ÍRIS suggested. The new clips land in `.iris/<video>/refeitas/` with a `manifesto.json` (scene, seed, prompt).
4. Swap the clips in your edit and run ÍRIS again on the new video (round 2).

`--servidor` points to another ComfyUI address (default `http://127.0.0.1:8188`).

## Kling and other paid APIs (optional, not included)

ÍRIS does not ship code that spends money. To plug in Kling (or Runway, Veo, Luma...), write a function with the same
contract as `iris.comfyui.refazer_cena`:

```python
def refazer_cena(prompt: str, semente: int, nome: str, destino: Path) -> list[Path]:
    """Generates one scene and returns the saved files."""
```

For Kling, that function would authenticate with your own API keys (read from environment variables, never from the
repository), submit an image-to-video or text-to-video task with `prompt`, poll the task until it finishes and
download the video to `destino`. Follow the official Kling API documentation for the endpoints and the price per
second; keep `--max-refazer` low, since each scene is a paid call.

---

## Português

A ÍRIS grava em `revisao.json` a lista `refazer`: as cenas que valem gerar de novo (no máximo `--max-refazer`,
padrão 3), com motivo e ajuste de prompt. Um adaptador pega essa lista e gera de novo só essas cenas.

- **ComfyUI (incluído, local, de graça):** `python -m iris.comfyui .iris/<video>/revisao.json --roteiro roteiro.json
  --workflow meu_workflow_api.json`. Exporte o workflow com "Save (API Format)" e use os marcadores `{{prompt}}`,
  `{{seed}}` e `{{nome}}`. As cenas novas saem em `.iris/<video>/refeitas/`.
- **Kling e outras APIs pagas (opcional, não incluído):** escreva uma função com o mesmo contrato de
  `refazer_cena`, com as suas chaves em variáveis de ambiente, seguindo a documentação oficial da API. Cada cena é
  uma chamada paga: mantenha `--max-refazer` baixo.
