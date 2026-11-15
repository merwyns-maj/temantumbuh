#!/bin/sh
# One-command build: events → picture → sound → master.
# Needs the Lemo-Opuscar library (set LIB) with `setup.sh deps` done, and ffmpeg 7+ first on PATH.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
: "${LIB:?set LIB to the lemo-opuscar library folder}"
export LIB
cd "$LIB"
node core/render/events.mjs "$HERE"
node core/render/video.mjs "$HERE" --fps 24 --workers 4 --out "$HERE/out/video.mp4"
"$LIB/.venv/bin/python" "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/tunas-imunisasi-crayon.mp4" 24 0
