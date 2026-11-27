# Video (pop-up book episodes)

Each folder is one episode for the Pentol YouTube series, built on the Lemo-Opuscar paper pop-up engine (MIT). See `CREDITS` inside each film.

**Render in the cloud (free):** GitHub, then Actions, then "Render video", then Run workflow. Type the folder name (default `pentol-e01`). About 20 machines each render one slice in parallel, then a last job joins them. Download `<film>-video` from the finished run. A push that changes anything under `video/` also starts a render.

`render/video.mjs` is the engine's render script with one addition: `--shard i/n` renders only slice i of n.

## Sound (ElevenLabs)

`<film>/script.json` holds who says each line, the music plan and the sound effects. Push a change to it and the **Make audio** workflow makes whatever is new with ElevenLabs (repo secret `ELEVENLABS_API_KEY`), saves it under `<film>/audio/`, then renders the episode with sound. Unchanged files are never made twice.

- **Pentol's voice:** in the ElevenLabs app, make an Instant Voice Clone from the voice sample and name it exactly `Pentol`. The next Make audio run finds it and remakes Pentol's lines with it. Until then a designed child voice stands in.
- **Your own music:** put a WAV at `<film>/audio/music/<cue>.own.wav` (for example `pagi.own.wav`). It replaces the generated cue in the next render.
- **Voice previews:** `<film>/audio/previews/` has a short sample of each designed voice, to judge them before watching the episode.
- The line texts in `script.json` must match `LINES` in `main.js` (the subtitles); the audio step stops if they differ.
