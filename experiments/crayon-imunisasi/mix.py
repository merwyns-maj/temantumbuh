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

# —— score (C major, 90 BPM) ——
C, D_, E_, F_, G_, A_, B_ = 60, 62, 64, 65, 67, 69, 71
THEME = [(0, E_ + 12, 1), (1, G_ + 12, 1), (2, A_ + 12, 1.5), (3.5, G_ + 12, .5), (4, E_ + 12, 1), (5, D_ + 12, 1), (6, C + 12, 2)]
def put(x, at, g=1.0, pan=0.0, to=None): add(mus if to is None else to, x, at, g, pan)

# A: a few music box notes as the crayon starts
for i, m in enumerate([C + 12, E_ + 12, G_ + 12]): put(musicbox(m, v=.5), 0.3 + i * BEAT * 1.5, 0.5, -0.2 + 0.2 * i)
# B: the walk — pluck lilt on the beat, bass on 1 and 3, shaker on the off-beats
for b in range(int((10.7 - 4.1) / BEAT)):
    t = 4.1 + b * BEAT; bar = b // 4
    put(pluck([C, A_ - 12, F_ - 12, G_ - 12][bar % 4] - 12, 1.4, .9, .3), t if b % 2 == 0 else -9, 0.55)
    put(pluck([E_, G_, A_, G_, E_, D_, C, D_][b % 8], 1.0, .8, .6), t, 0.42, 0.25)
    put(shaker(.6), t + BEAT / 2, 0.12, 0.4)
# C: nerves — thin, low pluck
for b in range(0, int((17.2 - 10.7) / BEAT), 2): put(pluck([C - 12, B_ - 24, A_ - 24][(b // 2) % 3], 1.8, .7, .2), 10.7 + b * BEAT, 0.42, -0.2)
# D: the music box enters with Mama's hand
for (bt, m, ln) in THEME: put(musicbox(m, 1.6 + ln * 0.5, .8), 17.4 + bt * BEAT, 0.45, 0.1)
for b in range(0, int((22.3 - 17.2) / BEAT), 2): put(pluck([F_ - 12, C - 12][(b // 2) % 2], 1.6, .7, .3), 17.2 + b * BEAT, 0.38)
# E: silence, then a low pluck after the sting
for i, m in enumerate([A_ - 24, F_ - 24, G_ - 24]): put(pluck(m, 2.0, .7, .2), 24.0 + i * BEAT * 2, 0.4)
# F: wash — glock arpeggio rising, landing on the reveal
arp = [C + 12, E_ + 12, G_ + 12, C + 24, E_ + 24, G_ + 24, C + 36]
for i, m in enumerate(arp): put(glock(m, v=.7), 27.4 + i * 0.32, 0.3, -0.6 + i * 0.2)
for b in range(0, int((34.4 - 29.3) / BEAT), 2): put(pluck([F_ - 12, G_ - 12, C - 12][(b // 2) % 3], 1.6, .7, .4), 29.3 + b * BEAT, 0.36)
# G: the theme in full on the music box, then it winds down
for k, (bt, m, ln) in enumerate(THEME + [(8 + b, m, l) for b, m, l in THEME[:4]]):
    t = 34.6 + bt * BEAT * 1.05; dr = 0.06 if t > 38.6 else 0.0
    put(musicbox(m, 1.8 + ln * 0.5, .9, droop=dr), t, 0.5, 0.05)
put(pluck(C - 24, 3.0, .7, .2), 34.6, 0.4); put(pluck(F_ - 24, 3.0, .7, .2), 34.6 + 4 * BEAT, 0.35)

# —— foley ——
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

silences = [(e['t'], e['t'] + e['dur']) for e in EV if e['type'] == 'silence']
for e in EV:
    t, ty, pan = e['t'], e['type'], e.get('pan', 0)
    if ty == 'scratch': add(buf, scratch(e['dur']), t, 0.10, pan)
    elif ty == 'scribble': add(buf, scratch(e['dur']) * 1.0, t, 0.13, pan)
    elif ty == 'shaky': add(buf, scratch(e['dur']), t, 0.12, pan)
    elif ty == 'step': add(buf, soft_step(), t, 0.10, pan)
    elif ty == 'glint': add(buf, glock(C + 36, 1.4), t, 0.10, pan)
    elif ty == 'swish': add(buf, whoosh(.4), t, 0.07, pan)
    elif ty == 'whoosh': add(buf, whoosh(.8), t, 0.12, 0)
    elif ty == 'cus': add(buf, woodblock(1.0, 1100), t, 0.42, pan)
    elif ty == 'crinkle': add(buf, crinkle(), t, 0.10, pan)
    elif ty == 'brush':
        x = brush(e['dur'])
        for k in range(8):   # pan left → right with the brush
            seg = x[k * len(x) // 8:(k + 1) * len(x) // 8]; add(buf, seg, t + k * e['dur'] / 8, 0.16, -0.8 + k * 0.23)
    elif ty == 'reveal':
        for i, m in enumerate([G_ + 24, C + 36, E_ + 36]): add(buf, glock(m, 1.6), t + i * 0.12, 0.10, 0.2 * i)
    elif ty == 'boing': add(buf, boing(), t, 0.12, pan)
    elif ty == 'puff': add(buf, lp(noise(.4), 400) * env_exp(.4, .1), t, 0.12, 0)
    elif ty == 'page': add(buf, whoosh(1.2), t, 0.08, 0)

# ambience: birds outside, room tone inside
for k in range(14):
    t = 0.5 + k * 1.6 + rng.random() * 0.8
    if t > 21.6: break
    d = .16; tt = t_(d); f = 3000 + 1500 * np.sin(2 * np.pi * 14 * tt)
    add(buf, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 2, t, 0.025, rng.uniform(-.8, .8))
room = lp(noise(DUR + 1), 300); room = room / np.abs(room).max()
add(buf, room[: int((DUR - 22.3) * SR)], 22.3, 0.012, 0)

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
