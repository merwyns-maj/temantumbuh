"""Score, foley, placeholder voice → out/mix.wav. Everything synthesised (no samples, no downloads).
Instruments from the crayon-book sound palette: nylon pluck (Karplus-Strong), music box, glockenspiel, woodblock, shaker.
Run with the library's venv: $LIB/.venv/bin/python mix.py   (needs LIB in the environment for core/audio/sfx.py)
"""
import json, os, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter, resample_poly
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ['LIB'], 'core', 'audio'))
from sfx import SR, t_, env_exp, bp, lp, hp, noise, norm, add, compress, limit, whoosh, step  # noqa: E402

E = json.load(open(os.path.join(HERE, 'events.json')))
DUR, EV = E['dur'], E['ev']
buf = np.zeros((int(DUR * SR) + SR, 2)); mus = np.zeros_like(buf); vox = np.zeros_like(buf)
rng = np.random.default_rng(5)
BPM = 90; BEAT = 60 / BPM
mf = lambda m: 440 * 2 ** ((m - 69) / 12)

# —— instruments ——
def pluck(m, d=1.6, v=1.0, bright=0.5):
    f = mf(m); N = int(SR / f); n = int(d * SR)
    x = np.zeros(n); x[:N] = lp(rng.uniform(-1, 1, N), 1500 + 4000 * bright)
    a = np.zeros(N + 2); a[0] = 1; a[N] = a[N + 1] = -0.4985
    y = lfilter([1], a, x)
    return norm(hp(y, 80)) * v * env_exp(d, d * 0.6)

def musicbox(m, d=2.2, v=1.0, droop=0.0):
    tt = t_(d); f = mf(m) * (1 - droop * tt / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(a * np.sin(k * ph) * env_exp(d, tau) for k, a, tau in [(1, 1, .9), (2.0, .35, .5), (3.0, .15, .25), (5.4, .08, .08)])
    x += hp(noise(d), 3000) * env_exp(d, .004) * .2
    return norm(x) * v

def glock(m, d=1.8, v=1.0):
    tt = t_(d); f = mf(m)
    x = sum(a * np.sin(2 * np.pi * f * k * tt) * env_exp(d, tau) for k, a, tau in [(1, 1, .7), (2.76, .4, .25), (5.4, .2, .08)])
    return norm(x) * v

def woodblock(v=1.0, f=900):
    d = .12; tt = t_(d)
    return norm(np.sin(2 * np.pi * f * tt) * env_exp(d, .018) + bp(noise(d), 600, 2500) * env_exp(d, .006) * .5) * v

def shaker(v=1.0):
    d = .09
    return norm(hp(noise(d), 5000) * np.sin(np.pi * t_(d) / d) ** 2) * v

# —— score (C major, 90 BPM): music box + pizzicato-ish pluck, toy feel ——
C, D_, E_, F_, G_, A_, B_ = 60, 62, 64, 65, 67, 69, 71
THEME = [(0, E_ + 12, 1), (1, G_ + 12, 1), (2, A_ + 12, 1.5), (3.5, G_ + 12, .5), (4, E_ + 12, 1), (5, D_ + 12, 1), (6, C + 12, 2)]
def put(x, at, g=1.0, pan=0.0, to=None): add(mus if to is None else to, x, at, g, pan)
# desk: soft music box intro
for i, m in enumerate([C + 12, E_ + 12, G_ + 12, C + 24]): put(musicbox(m, v=.5), 0.6 + i * BEAT * 1.5, 0.45, -0.2 + 0.15 * i)
# walk (6.8-13.6): pluck lilt on the beat, bass on 1 and 3, shaker
for b in range(int((14.0 - 5.0) / BEAT)):
    t = 5.0 + b * BEAT; bar = b // 4
    if b % 2 == 0: put(pluck([C, A_ - 12, F_ - 12, G_ - 12][bar % 4] - 12, 1.4, .9, .3), t, 0.5)
    put(pluck([E_, G_, A_, G_, E_, D_, C, D_][b % 8], 1.0, .8, .6), t, 0.38, 0.25)
    put(shaker(.6), t + BEAT / 2, 0.1, 0.4)
# nerves: thin low pluck
for b in range(0, int((19.5 - 14.0) / BEAT), 2): put(pluck([C - 12, B_ - 24, A_ - 24][(b // 2) % 3], 1.8, .7, .2), 14.0 + b * BEAT, 0.4, -0.2)
# hand: the theme on the music box
for (bt, m, ln) in THEME: put(musicbox(m, 1.6 + ln * 0.5, .8), 19.7 + bt * BEAT * .7, 0.42, 0.1)
# room: soft pluck pad, then silence before the shot
for b in range(0, int((27.0 - 25.2) / BEAT), 2): put(pluck([F_ - 12, C - 12][(b // 2) % 2], 1.6, .7, .3), 25.2 + b * BEAT, 0.34)
for i, m in enumerate([A_ - 24, F_ - 24, G_ - 24]): put(pluck(m, 2.0, .7, .2), 28.6 + i * BEAT * 2, 0.36)
# shield: glock arpeggio landing on the pop-up
for i, m in enumerate([C + 12, E_ + 12, G_ + 12, C + 24, E_ + 24, G_ + 24, C + 36]): put(glock(m, v=.7), 30.0 + i * 0.16, 0.28, -0.6 + i * 0.2)
for b in range(0, int((36.4 - 31.2) / BEAT), 2): put(pluck([F_ - 12, G_ - 12, C - 12][(b // 2) % 3], 1.6, .7, .4), 31.2 + b * BEAT, 0.34)
# hug + ending: theme in full, winding down
for (bt, m, ln) in THEME + [(8 + b, m, l) for b, m, l in THEME[:4]]:
    t = 36.6 + bt * BEAT * 1.05; dr = 0.06 if t > 40.4 else 0.0
    put(musicbox(m, 1.8 + ln * 0.5, .9, droop=dr), t, 0.48, 0.05)
put(pluck(C - 24, 3.0, .7, .2), 36.6, 0.38)

# —— paper foley ——

def scratch(d, v=1.0):
    tt = t_(d); slip = (np.sin(2 * np.pi * 7.5 * tt) > 0.2).astype(float) * 0.7 + 0.3
    return norm(bp(noise(d), 1800, 6500) * slip * np.minimum(1, np.minimum(tt / .05, (d - tt) / .1))) * v
def soft_step(v=1.0): d = .12; return norm(lp(noise(d), 500) * env_exp(d, .03)) * v
def boing(v=1.0):
    d = .45; tt = t_(d); f = 300 + 220 * np.sin(2 * np.pi * 6 * tt) * np.exp(-tt * 6)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, .15)) * v
def brush(d, v=1.0):
    tt = t_(d); return norm(lp(bp(noise(d), 200, 2500), 1800) * np.sin(np.pi * tt / d) ** 0.7) * v
def crinkle(v=1.0):
    d = .5; x = hp(noise(d), 2500) * (rng.random(int(d * SR)) > 0.985) * 3 + hp(noise(d), 3000) * .15
    return norm(x * env_exp(d, .2)) * v

def creak(d=1.4):
    tt = t_(d); f = 180 + 60 * np.sin(2 * np.pi * 1.3 * tt); sw = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return norm(bp(sw * (rng.random(len(tt)) * .6 + .4), 300, 2500) * np.sin(np.pi * tt / d))
def thump(): d = .3; return norm(lp(noise(d), 180) * env_exp(d, .05) + np.sin(2 * np.pi * 70 * t_(d)) * env_exp(d, .08))
def pop():
    d = .18; tt = t_(d); f = 900 - 3000 * tt
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, .04) * .7 + hp(noise(d), 3000) * env_exp(d, .02) * .5)
def page_swish(d): tt = t_(d); return norm(bp(noise(d), 600, 5000) * np.sin(np.pi * tt / d) ** 1.5)
silences = [(e['t'], e['t'] + e['dur']) for e in EV if e['type'] == 'silence']
for e in EV:
    t, ty, pan = e['t'], e['type'], e.get('pan', 0)
    if ty == 'creak': add(buf, creak(), t, 0.10, -0.2)
    elif ty == 'thump': add(buf, thump(), t, 0.22, 0)
    elif ty == 'pop': add(buf, pop(), t, 0.09, rng.uniform(-.5, .5))
    elif ty == 'page': add(buf, page_swish(e['d']), t, 0.14, 0.3)
    elif ty == 'step': add(buf, soft_step(), t, 0.08, 0)
    elif ty == 'cus': add(buf, woodblock(1.0, 1100), t, 0.42, 0.2)
    elif ty == 'crinkle': add(buf, crinkle(), t, 0.1, 0.2)
    elif ty == 'reveal':
        for i, m in enumerate([67 + 24, 72 + 24, 76 + 24]): add(buf, glock(m, 1.6), t + .25 + i * 0.12, 0.10, 0.2 * i)
    elif ty == 'boing': add(buf, boing(), t, 0.12, rng.uniform(-.4, .4))
    elif ty == 'puff': add(buf, lp(noise(.4), 400) * env_exp(.4, .1), t, 0.12, 0)
    elif ty == 'whoosh': add(buf, whoosh(1.4), t, 0.08, 0)
# room tone
room = lp(noise(DUR + 1), 260); room = room / np.abs(room).max(); add(buf, room[: int(DUR * SR)], 0, 0.01, 0)

# —— voice: placeholder lines, compressed ——
for e in EV:
    if e['type'] != 'voice': continue
    sr, v = wavfile.read(os.path.join(HERE, 'voices', e['id'] + '.wav')); v = v.astype(np.float64)
    if v.ndim > 1: v = v.mean(1)
    if sr != SR: v = resample_poly(v, SR, sr)
    v = norm(v); v = compress(v, .3, 3.0); v = norm(v)
    add(vox, v, e['t'], 0.55, 0)

# duck music under the voice and kill everything in the silence
venv = np.abs(vox[:, 0]); from scipy.ndimage import uniform_filter1d, maximum_filter1d
venv = uniform_filter1d(maximum_filter1d(venv, int(.25 * SR)), int(.2 * SR)); duck = 1 - 0.55 * np.clip(venv / (venv.max() + 1e-9) * 3, 0, 1)
mus *= duck[:, None]
for a, b in silences:
    s, e = int(a * SR), int(b * SR); mus[s:e] = 0; buf[s:e] *= 0.0
mix = buf + mus * 0.9 + vox
fade = np.ones(len(mix)); n = int(1.0 * SR); end = int(DUR * SR); fade[end - n:end] = np.linspace(1, 0, n); fade[end:] = 0
mix *= fade[:, None]
for c in range(2): mix[:, c] = limit(mix[:, c], .9)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
wavfile.write(os.path.join(HERE, 'out', 'mix.wav'), SR, (mix[: int(DUR * SR)] * 32767).astype(np.int16))
print('mix ok', DUR, 's')
