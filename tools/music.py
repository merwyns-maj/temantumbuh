#!/usr/bin/env python3
"""Original background music for TemanTumbuh videos, synthesised from scratch (no samples, no licences).

Usage: python tools/music.py <seconds> out.wav [--sparkle 21.2]

A light, happy loop in C major at 100 BPM: plucked melody (Karplus-Strong), round bass, soft pad,
shaker and a gentle kick. --sparkle adds a rising glitter arpeggio at that second (the 'wow' moment).
Mixed quiet enough to sit under voice or on-screen text.
"""
import sys

import numpy as np
from scipy.io import wavfile

SR = 44100
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(11)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def pluck(freq, dur, bright=0.5, decay=0.996):
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, period)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = decay * (bright * buf[i % period] + (1 - bright) * buf[(i + 1) % period])
    return out


def sine(freq, dur, attack=0.01, release=0.2):
    t = np.arange(int(SR * dur)) / SR
    env = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / release).clip(0)
    return np.sin(2 * np.pi * freq * t) * env


def add(track, sig, at, gain):
    i = int(at * SR)
    if i >= len(track):
        return
    j = min(len(track), i + len(sig))
    track[i:j] += sig[: j - i] * gain


def lowpass(x, a=0.15):
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc)
        y[i] = acc
    return y


def build(seconds, sparkle=None):
    track = np.zeros(int(SR * (seconds + 1)))
    chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]  # C G Am F
    roots = [48, 43, 45, 41]
    melody = [  # (beat offset in the 4-bar phrase, midi, length in beats)
        (0, 72, 1), (1, 76, 1), (2, 79, 1.5), (3.5, 76, 0.5),
        (4, 74, 1), (5, 71, 1), (6, 74, 2),
        (8, 72, 1), (9, 76, 1), (10, 81, 1.5), (11.5, 79, 0.5),
        (12, 77, 1), (13, 76, 1), (14, 74, 0.5), (14.5, 72, 1.5),
    ]
    shaker = lowpass(rng.uniform(-1, 1, int(SR * 0.06)), 0.6) * np.exp(-np.linspace(0, 6, int(SR * 0.06)))
    kick = sine(55, 0.25, 0.002, 0.2) * np.exp(-np.linspace(0, 8, int(SR * 0.25)))
    bar = 4 * BEAT
    phrase = 4 * bar
    t0 = 0.0
    k = 0
    while t0 < seconds:
        for b in range(4):
            tb = t0 + b * bar
            ch = chords[b]
            for n in ch:  # soft pad
                add(track, sine(midi(n), bar, 0.4, 0.6), tb, 0.035)
            add(track, pluck(midi(roots[b]), bar * 0.9, 0.6, 0.997), tb, 0.30)
            add(track, pluck(midi(roots[b] + 7), bar * 0.45, 0.6, 0.997), tb + 2 * BEAT, 0.18)
            for beat in range(4):
                add(track, kick, tb + beat * BEAT, 0.22 if beat % 2 == 0 else 0.10)
                for half in (0, 0.5):
                    add(track, shaker, tb + (beat + half) * BEAT, 0.05)
        if k >= 1 or t0 > 2:  # melody enters after the first phrase starts
            for off, n, ln in melody:
                add(track, pluck(midi(n), ln * BEAT + 0.3, 0.45, 0.995), t0 + off * BEAT, 0.20)
        t0 += phrase
        k += 1
    if sparkle is not None:
        for i, n in enumerate([84, 88, 91, 96, 100, 103]):
            add(track, sine(midi(n), 0.5, 0.005, 0.4) * np.exp(-np.linspace(0, 5, int(SR * 0.5))), sparkle + i * 0.07, 0.10)
        whoosh = lowpass(rng.uniform(-1, 1, int(SR * 0.9)), 0.08) * np.hanning(int(SR * 0.9))
        add(track, whoosh, sparkle - 0.3, 0.6)
    track = track[: int(SR * seconds)]
    fade_in = np.minimum(1, np.arange(len(track)) / (0.6 * SR))
    fade_out = np.minimum(1, (len(track) - np.arange(len(track))) / (1.8 * SR))
    track *= fade_in * fade_out
    track /= np.max(np.abs(track)) + 1e-9
    track *= 0.6
    stereo = np.stack([track, np.roll(track, 120) * 0.97], 1)
    return (stereo * 32767).astype(np.int16)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sparkle = float(sys.argv[sys.argv.index("--sparkle") + 1]) if "--sparkle" in sys.argv else None
    seconds, out = float(args[0]), args[1]
    wavfile.write(out, SR, build(seconds, sparkle))
    print(out)


if __name__ == "__main__":
    main()
