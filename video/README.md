# Video (pop-up book episodes)

Each folder is one episode for the Pentol YouTube series, built on the Lemo-Opuscar paper pop-up engine (MIT). See `CREDITS` inside each film.

**Render in the cloud (free):** GitHub, then Actions, then "Render video", then Run workflow. Type the folder name (default `pentol-e01`). About 20 machines each render one slice in parallel, then a last job joins them. Download `<film>-video` from the finished run. A push that changes anything under `video/` also starts a render.

`render/video.mjs` is the engine's render script with one addition: `--shard i/n` renders only slice i of n.
