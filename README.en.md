# ÍRIS: the reviewer for AI-generated videos

*[Leia em português](README.md)*

AI video tools generate. ÍRIS **reviews**: it watches the video frame by frame, points out each defect with the
exact second, asks to regenerate only the bad scenes, and keeps what it learned so the next video comes out better.

It was born inside a YouTube Shorts factory that runs on its own every night. There, every video goes through ÍRIS
before it is published. This repository is ÍRIS packaged as a Claude Code plugin, so it can review videos from any
pipeline (Wan, Veo, Kling, Runway, CapCut, manual editing, it does not matter).

```
generate  ->  inspect  ->  review  ->  redo only the bad scenes  ->  learn
```

## Before and after

The same trivia Short, before and after going through ÍRIS:

![The same Short before and after ÍRIS](demo/antes-depois.png)

| | Before (v3) | After (v4) |
|---|---|---|
| Score | 5.5 | 7.5 |
| Length | 54 s | 42 s |
| Object appearing or vanishing | ball appears mid-air and vanishes (0:47) | none |
| Ending | sentence cut off | closes the idea from the hook |

Full reviews (in Portuguese): [v3](demo/tenis-v3/revisao.md) and [v4](demo/tenis-v4/revisao.md). ÍRIS also pointed
out what is still missing in v4 (audio 2 dB too low, a semi-transparent subtitle that repeats), because reviewing is
not only praising.

## What it delivers

- A **score** from 0 to 10 and a one-sentence summary.
- **Defects with the exact second**: an object that vanishes or duplicates, a deformed hand, made-up text in the
  image, an abrupt jump, a frozen scene, a voice that changed, a swallowed word, low audio, a subtitle that is too long.
- **Bad luck or pipeline bug**: it separates the bad luck of one generation (another seed fixes it) from a defect
  that will keep coming back.
- A **list of scenes to redo** (3 at most), each with a suggested prompt change.
- **Lessons** collected in `.iris/historico.json`. A lesson that repeats moves up in priority.

It runs inside Claude Code: **no API key needed**, because the one who looks at the contact sheets is the Claude of
your own session.

## Install

Requirements: [Claude Code](https://claude.com/claude-code), Python 3.10+, `ffmpeg` on the PATH and `pip install Pillow`.

```
/plugin marketplace add HiveControlAgents/iris
/plugin install iris@iris
```

Optional: `pip install faster-whisper` (compares the narration with the script and lists invented, swallowed or doubtful words) and `pip install librosa` (checks
that the voice matches the reference recording).

## Use

```
/iris my_video.mp4
/iris my_video.mp4 script.json
```

Or just ask: "review this video". The review is saved to `.iris/<video-name>/revisao.md` and `revisao.json`.

- Script format: [exemplos/roteiro.json](exemplos/roteiro.json). Without a script, scenes are detected from the cuts.
- Your channel's rules (for example "no people", "no text in the image"): copy
  [exemplos/regras.md](exemplos/regras.md) to `.iris/regras.md`.
- The inspector also runs on its own, without Claude:
  `python skills/revisar-video/scripts/inspecionar.py video.mp4` writes `medidas.json` and the contact sheets.

The reviews and prompts are written in Brazilian Portuguese for now. To get the review in another language, just
ask Claude, for example: "review this video and write the review in English".

## How it works

1. `inspecionar.py` measures with ffmpeg: length, resolution, loudness (LUFS) and peak, abrupt cuts, freezes, black
   screens, and brightness and saturation per scene. With a script, it compares the text with what was said.
2. It builds **contact sheets**: 2 frames per second, 6 per row, with the timestamp in yellow in the corner. This is
   how Claude sees an object vanishing between two neighboring frames.
3. Claude reads the measurements, the sheets, the channel rules and the history, and writes the review following the
   [criteria](skills/revisar-video/criterios.md).
4. The history is updated. On the next video, repeated patterns become a pipeline fix instead of bad luck.

## What about existing tools?

- [claude-video](https://github.com/bradautomates/claude-video), [claude-video-vision](https://github.com/jordanrendric/claude-video-vision)
  and similar skills make Claude **watch** a video to answer questions or summarize it. ÍRIS **judges** an
  AI-generated video: it measures, points out each defect with the exact second, decides what to redo and learns
  across videos.
- [VISTA](https://g-vista.github.io/) (Google research) improves video prompts in critique loops. ÍRIS belongs to the
  same family of ideas, but it is a practical tool for people who publish Shorts: it runs in Claude Code, with no API
  key, on top of the pipeline you already have.

## Credits

Created by **Isaque Moutta** ([@IsaqueMoutta](https://github.com/IsaqueMoutta)), inside Colmeia, the agent team of
[HiveControlAgents](https://github.com/HiveControlAgents).

If ÍRIS helped your videos, please give credit: write "Reviewed by ÍRIS, by Isaque Moutta" with a link to this
repository in the video description, in your project's README or in your post. If you copy or adapt the code, the
MIT license requires keeping the copyright notice from the [LICENSE](LICENSE) file.

## License

MIT. Copyright (c) 2026 Isaque Moutta. See [LICENSE](LICENSE).
