"""Mix an episode's sound: voice lines, music beds (ducked under the voice) and sound effects.

    python video/tools/mix_episode.py video/tunas-e01 events.json mix.wav

events.json comes from dump_events.mjs (the page's own sound events: page turns, book open/close, flashes).
Whatever audio files are missing are skipped, so a partial set still gives a usable mix.
"""
import json, os, subprocess, sys
import numpy as np

FILM, EVP, OUTP = sys.argv[1], sys.argv[2], sys.argv[3]
S = json.load(open(f'{FILM}/script.json')); E = json.load(open(EVP))
A = f'{FILM}/audio'; SR = 48000; DUR = float(E['dur']); N = int(DUR * SR)
warn = lambda m: print(f'::warning::{m}', flush=True)

def load(path):
    if not os.path.exists(path): return None
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def track(name, sub):
    for ext in ('.own.wav', '.mp3'):
        x = load(f'{A}/{sub}/{name}{ext}')
        if x is not None: return x
    return None

def rms(x): return float(np.sqrt(np.mean(x ** 2))) + 1e-9
def fade(x, a, b):
    n = len(x); a = min(int(a * SR), n // 2); b = min(int(b * SR), n // 2)
    if a: x[:a] *= np.linspace(0, 1, a)[:, None]
    if b: x[n - b:] *= np.linspace(1, 0, b)[:, None]
    return x
def add(buf, x, t, g=1.0):
    i = int(round(t * SR))
    if i >= len(buf) or x is None: return
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), len(buf) - i); buf[i:i + n] += x[:n] * g

vo, mus, sfx = (np.zeros((N, 2), np.float32) for _ in range(3))

# —— voice: each line levelled to the same loudness, placed at its time ——
report = []
for i, l in enumerate(S.get('lines', [])):
    x = track(f'l{i}', 'vo')
    if x is None: report.append(f'l{i} missing'); continue
    x = x * (0.08 / rms(x)); add(vo, fade(x, .01, .05), l['t'])
    nxt = S['lines'][i + 1]['t'] if i + 1 < len(S['lines']) else DUR
    over = l['t'] + len(x) / SR - nxt + .15
    if over > 0: report.append(f"l{i} ({l['who']}) runs {over:.1f} s into the next line")
for r in report: warn('voice: ' + r)

# —— music: each planned bed, looped with a crossfade if it is shorter than its slot ——
cache = {}
for p in S.get('music', {}).get('plan', []):
    if p['cue'] not in cache: cache[p['cue']] = track(p['cue'], 'music')
    x = cache[p['cue']]
    if x is None: warn(f"music: {p['cue']} missing"); continue
    need = int((p['t1'] - p['t0']) * SR); off = int(p.get('offset', 0) * SR) % len(x)
    seg = x[off:]; xf = int(1.5 * SR)
    while len(seg) < need:   # loop: overlap the tail with the start
        a = seg.copy(); b = x.copy(); r = np.linspace(0, 1, xf)[:, None]
        a[-xf:] = a[-xf:] * (1 - r) + b[:xf] * r; seg = np.concatenate([a, b[xf:]])
    seg = seg[:need].copy(); seg *= 0.06 / rms(seg)
    add(mus, fade(seg, 1.0, 1.4), p['t0'], p.get('gain', .5))

# duck the music under the voice: a level follower at 100 Hz (fast attack, slow release), then back to the sample rate
H = SR // 100; lv = np.abs(vo).max(1); lv = lv[:len(lv) // H * H].reshape(-1, H).max(1)
g = np.empty_like(lv); s = 0.0
for k, v in enumerate(lv): s = v if v > s else s * 0.98 + v * 0.02; g[k] = s   # release about 0.5 s
duck = 1 - 0.6 * np.clip(np.interp(np.arange(N) / H, np.arange(len(g)), g) / 0.05, 0, 1)
mus *= duck[:, None].astype(np.float32)

# —— sound effects: the page's events, then the extra cues in script.json ——
def sound(name):
    x = track(name, 'sfx')
    if x is None: return None
    return x * (0.05 / rms(x))
fx = {}
get = lambda n: fx.setdefault(n, sound(n))
for e in E['ev']:
    n = S.get('sfx', {}).get('from_events', {}).get(e.get('type'))
    if n and get(n) is not None: add(sfx, fade(get(n).copy(), .005, .2), e['t'], .5)
for c in S.get('sfx', {}).get('extra', []):
    x = get(c['sfx'])
    if x is None: continue
    x = x.copy()
    if c.get('until'):
        need = int((c['until'] - c['t']) * SR)
        while len(x) < need: x = np.concatenate([x, x])
        x = x[:need]
    add(sfx, fade(x, .05, .4), c['t'], c.get('gain', .5))

# the series jingle (intro): the picked take, or the take named in $JINGLE, at full level from 0 s
J = S.get('jingle') or {}
jt = os.environ.get('JINGLE') or J.get('pick')
RM = J.get('remix') or {}
if jt and RM.get('take') == jt and os.path.exists(f'{A}/jingle/{jt}-vocals.mp3'):
    # rebuilt from the stems: louder vocals, and the ending replaced by the cast shouting the name over the music
    db = lambda d: 10 ** (d / 20)
    v, m = load(f'{A}/jingle/{jt}-vocals.mp3'), load(f'{A}/jingle/{jt}-instrumental.mp3'); n = min(len(v), len(m))
    cut_, xf = int(RM.get('tag_from', 16.55) * SR), int(.12 * SR)
    vg = np.ones(n, np.float32); vg[cut_:cut_ + xf] = np.linspace(1, 0, min(xf, max(0, n - cut_))); vg[cut_ + xf:] = 0
    song = m[:n] * db(RM.get('music_db', -1)) + v[:n] * db(RM.get('vocal_db', 4)) * vg[:, None]
    for k, who in enumerate((J.get('shout') or {}).get('who', [])):
        x = load(f'{A}/jingle/shout-{who}.mp3')
        if x is None: warn(f'shout {who} missing'); continue
        x = x / (np.abs(x).max() + 1e-9) * .5
        i = int((RM.get('shout_at', 16.75) + k * .025) * SR); nn = min(len(x), len(song) - i)
        if nn > 0: song[i:i + nn] += x[:nn]
    add(mus, fade(song, .005, .05), 0, 1.0)
elif jt:
    x = load(f'{A}/jingle/{jt}.mp3')
    if x is None: warn(f'jingle {jt} missing')
    else: x = x * (0.12 / rms(x)); add(mus, fade(x, .005, .3), 0, 1.0)

mix = vo + mus + sfx
peak = np.abs(mix).max() or 1
mix = np.tanh(mix * (0.89 / peak) * 1.2) / np.tanh(1.2)   # gentle limiter to about -1 dBFS
pcm = (np.clip(mix, -1, 1) * 32767).astype('<i2')
# loudness: the intro sits about 2 LU above the story (YouTube plays everything at about -14 LUFS anyway)
target = S.get('loudness', -16 if J else -18)
tmp = OUTP + '.raw.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ac', '2', '-ar', str(SR), '-i', '-', tmp], input=pcm.tobytes(), check=True)
import re as _re
meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', f'loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
mj = json.loads(meas[meas.rindex('{'):meas.rindex('}') + 1])
ln = f"loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', ln, '-ar', str(SR), OUTP], check=True); os.remove(tmp)
print(f"loudness {mj['input_i']} -> {target} LUFS")
print(f'mixed {DUR:.1f} s -> {OUTP}')
