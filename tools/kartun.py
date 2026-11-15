#!/usr/bin/env python3
"""Cartoon kit for slow-paced Tunas episodes (YouTube, 16:9 1920x1080, 30 fps).

Puppet-style limited animation: Tunas is redrawn every frame from parts (body bob, leaf sway,
blink, mouth driven by the voice, arm swing or wave, stepping feet). Backgrounds are drawn once
as wide layers and the camera pans across them (far layer moves slower = parallax).

Usage: python tools/kartun.py <workdir>
  workdir must hold voice.wav (the line Tunas says). Writes frames check PNGs and test.mp4.

Rules kept from CLAUDE.md: own characters only, flat illustration (not photoreal), no red-cross
emblem on clinics (protected by UU 1/2018), palette from artkit.
"""
import math
import os
import subprocess
import sys

import cairosvg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import (BLUSH, BOX, BOXD, CARD, FLOOR, INK, LINE, MUTED, SAGE, SD,  # noqa: E402
                    SKY, SKYD, SUN, TERRA, TD)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1920, 1080, 30
GROUND = 900          # world y where Tunas' feet touch
S = 4.0               # Tunas scale (source viewBox units -> px)
ARM = '#eab5a1'


# ---------- Tunas rig ----------
def tunas_svg(bob=0.0, leaf=0.0, blink=0.0, mouth=0.0, look=0.0, arm_l=0.0, arm_r=0.0,
              wave=None, foot_l=0.0, foot_r=0.0, squash=0.0):
    """One frame of Tunas. Angles in degrees. wave=None keeps the right arm down, else its angle."""
    sy = 1 - squash * 0.06
    sx = 1 + squash * 0.05
    body = f'translate(60 130) scale({sx} {sy}) translate(-60 -130) translate(0 {bob})'
    leaves = (f'<g transform="rotate({leaf} 60 56)">'
              f'<path d="M60 58 V38" stroke="{SD}" stroke-width="5" stroke-linecap="round" fill="none"/>'
              f'<path d="M60 40 C50 26 36 25 26 33 C36 45 50 46 60 40 Z" fill="{SAGE}"/>'
              f'<path d="M60 40 C70 26 84 25 94 33 C84 45 70 46 60 40 Z" fill="{SD}"/>'
              f'<circle cx="60" cy="35" r="5" fill="{SUN}"/></g>')
    left = f'<path transform="rotate({arm_l} 30 96)" d="M28 97 Q18 106 22 116" stroke="{ARM}" stroke-width="9" stroke-linecap="round" fill="none"/>'
    if wave is None:
        right = f'<path transform="rotate({arm_r} 90 96)" d="M92 97 Q103 105 98 115" stroke="{ARM}" stroke-width="9" stroke-linecap="round" fill="none"/>'
    else:
        right = (f'<g transform="rotate({wave} 92 92)"><path d="M93 92 Q108 80 104 64" stroke="{ARM}" stroke-width="9" stroke-linecap="round" fill="none"/>'
                 f'<path d="M110 56 l6 -4 M112 66 l7 0" stroke="{TERRA}" stroke-width="3" stroke-linecap="round" opacity="{0.9 if wave > -2 else 0.4}"/></g>')
    # eyes: pupils squash shut on blink; glasses stay
    ry = max(0.7, 4 * (1 - blink))
    eyes = ''.join(f'<ellipse cx="{cx + look}" cy="88" rx="4" ry="{ry}" fill="{INK}"/>' for cx in (48, 72))
    if blink < 0.5:
        eyes += ''.join(f'<circle cx="{cx + look + 1.4}" cy="86.6" r="1.3" fill="#fff"/>' for cx in (48, 72))
    glasses = (''.join(f'<circle cx="{cx}" cy="88" r="10" fill="none" stroke="{INK}" stroke-width="3"/>' for cx in (48, 72))
               + f'<path d="M58 87 Q60 84 62 87 M38 86 L26 83 M82 86 L94 83" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if mouth < 0.08:
        m = f'<path d="M54 102 Q60 108 66 102" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    else:
        d = 3 + 9 * mouth
        w = 6 + 1.5 * mouth
        m = (f'<path d="M{60-w} 101 Q60 {101 + d*0.15} {60+w} 101 Q{60+w*0.8} {101+d} 60 {101+d} Q{60-w*0.8} {101+d} {60-w} 101 Z" fill="{INK}"/>'
             + (f'<ellipse cx="60" cy="{101 + d*0.78}" rx="{w*0.5}" ry="{d*0.22}" fill="{TERRA}"/>' if mouth > 0.35 else ''))
    feet = (f'<ellipse cx="46" cy="{128 - foot_l}" rx="10" ry="6" fill="{TERRA}"/>'
            f'<ellipse cx="74" cy="{128 - foot_r}" rx="10" ry="6" fill="{TERRA}"/>')
    shadow = f'<ellipse cx="60" cy="134" rx="{34 - abs(bob)*0.8}" ry="5" fill="#000" opacity="0.08"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -14 160 160">{shadow}{feet}'
            f'<g transform="{body}">{leaves}{left}{right}'
            f'<ellipse cx="60" cy="92" rx="36" ry="38" fill="{BLUSH}"/>'
            f'<ellipse cx="38" cy="102" rx="6" ry="3.5" fill="{TERRA}" opacity="0.35"/>'
            f'<ellipse cx="82" cy="102" rx="6" ry="3.5" fill="{TERRA}" opacity="0.35"/>'
            f'{eyes}{glasses}{m}</g></svg>')


def tunas_img(**p):
    px = int(160 * S)
    png = cairosvg.svg2png(bytestring=tunas_svg(**p).encode(), output_width=px, output_height=px)
    from io import BytesIO
    return Image.open(BytesIO(png)).convert('RGBA')


def paste_tunas(frame, img, wx, camx, zoom_ctr=None):
    # source point (60,134) sits on the ground; viewBox origin (-20,-14)
    x = int(wx - camx - (60 + 20) * S)
    y = int(GROUND - (134 + 14) * S)
    frame.alpha_composite(img, (max(x, 0), y), (max(-x, 0), 0))


# ---------- backgrounds ----------
def png(svg_body, w, h):
    from io import BytesIO
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{svg_body}</svg>'
    return Image.open(BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')


def far_layer():
    w = 2600
    hills = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in
                    [(200, 860, 520, 230, '#cfe1d4'), (900, 900, 640, 260, '#bcd6c4'), (1700, 870, 600, 240, '#cfe1d4'),
                     (2400, 900, 560, 250, '#bcd6c4')])
    body = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfdcf2"/>'
            f'<stop offset="1" stop-color="#f4f8f6"/></linearGradient></defs>'
            f'<rect width="{w}" height="{H}" fill="url(#g)"/>'
            f'<circle cx="420" cy="190" r="70" fill="{SUN}" opacity="0.9"/><circle cx="420" cy="190" r="110" fill="{SUN}" opacity="0.15"/>'
            + hills)
    return png(body, w, H)


def cloud(scale=1.0):
    b = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>' for x, y, r in [(60, 70, 40), (110, 50, 55), (165, 72, 38), (110, 85, 40)])
    return png(f'<g transform="scale({scale})" opacity="0.92">{b}</g>', int(220 * scale), int(130 * scale))


def tree(x, base, s=1.0):
    return (f'<g transform="translate({x} {base}) scale({s})">'
            f'<rect x="-14" y="-170" width="28" height="170" rx="10" fill="{BOXD}"/>'
            f'<circle cx="0" cy="-230" r="110" fill="{SAGE}"/><circle cx="-70" cy="-180" r="70" fill="{SAGE}"/>'
            f'<circle cx="70" cy="-185" r="75" fill="{SD}"/><circle cx="20" cy="-290" r="70" fill="{SD}" opacity="0.6"/></g>')


def pot(x, base):
    return (f'<g transform="translate({x} {base})"><path d="M-40 -70 L40 -70 L30 0 L-30 0 Z" fill="{TERRA}"/>'
            f'<rect x="-46" y="-80" width="92" height="16" rx="6" fill="{TD}"/>'
            + ''.join(f'<path d="M0 -78 Q{dx} -150 {dx*1.6} -175" stroke="{SD}" stroke-width="10" fill="none" stroke-linecap="round"/>' for dx in (-30, 0, 30))
            + '</g>')


def near_layer():
    w = 3000
    g0 = GROUND - 60
    bx0, bx1, top = 1450, 2650, 330
    door_l, door_r = 1940, 2160
    win = lambda x: (f'<rect x="{x}" y="520" width="190" height="150" rx="14" fill="{SKY}"/>'
                     f'<rect x="{x}" y="520" width="190" height="150" rx="14" fill="none" stroke="{CARD}" stroke-width="10"/>'
                     f'<path d="M{x+95} 520 V670 M{x} 595 H{x+190}" stroke="{CARD}" stroke-width="8"/>'
                     f'<path d="M{x+20} 540 l40 0 M{x+20} 556 l24 0" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')
    building = (
        f'<rect x="{bx0}" y="{top+80}" width="{bx1-bx0}" height="{g0-top-80}" fill="#fbf3e6"/>'
        f'<rect x="{bx0}" y="{g0-40}" width="{bx1-bx0}" height="40" fill="{LINE}"/>'
        f'<path d="M{bx0-50} {top+100} L{bx0+60} {top-10} L{bx1-60} {top-10} L{bx1+50} {top+100} Z" fill="{TERRA}"/>'
        f'<rect x="{bx0-50}" y="{top+92}" width="{bx1-bx0+100}" height="18" rx="6" fill="{TD}"/>'
        # sign: leaf-heart icon, no red cross
        f'<rect x="1790" y="{top+140}" width="520" height="96" rx="24" fill="{SAGE}"/>'
        f'<text x="2085" y="{top+205}" font-family="Nunito, sans-serif" font-weight="800" font-size="56" fill="{CARD}" text-anchor="middle">PUSKESMAS</text>'
        f'<path d="M1850 {top+214} C1820 {top+190} 1826 {top+160} 1850 {top+170} C1874 {top+160} 1880 {top+190} 1850 {top+214} Z" fill="{CARD}"/>'
        + win(1500) + win(2360) +
        f'<rect x="{door_l-20}" y="600" width="{door_r-door_l+40}" height="{g0-600}" rx="18" fill="{SD}"/>'
        f'<rect x="{door_l}" y="620" width="{(door_r-door_l)/2-6}" height="{g0-640}" rx="8" fill="{SKY}"/>'
        f'<rect x="{door_l+(door_r-door_l)/2+6}" y="620" width="{(door_r-door_l)/2-6}" height="{g0-640}" rx="8" fill="{SKY}"/>'
        f'<path d="M{door_l+20} 650 l50 -20 M{door_r-90} 650 l50 -20" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity="0.6"/>'
        f'<rect x="{door_l+(door_r-door_l)/2-28}" y="720" width="12" height="60" rx="6" fill="{SUN}"/><rect x="{door_l+(door_r-door_l)/2+16}" y="720" width="12" height="60" rx="6" fill="{SUN}"/>'
        f'<rect x="{door_l-60}" y="{g0-14}" width="{door_r-door_l+120}" height="22" rx="8" fill="{BOX}"/>'
    )
    bench = (f'<g transform="translate(2420 {g0})"><rect x="0" y="-70" width="200" height="22" rx="8" fill="{BOX}"/>'
             f'<rect x="0" y="-120" width="200" height="18" rx="8" fill="{BOX}"/><rect x="16" y="-50" width="14" height="50" fill="{BOXD}"/>'
             f'<rect x="170" y="-50" width="14" height="50" fill="{BOXD}"/></g>')
    ground = (f'<rect x="0" y="{g0}" width="{w}" height="{H-g0}" fill="{FLOOR}"/>'
              f'<rect x="0" y="{g0-22}" width="{w}" height="30" rx="10" fill="{SAGE}"/>'
              + ''.join(f'<ellipse cx="{x}" cy="{g0+120 + (x % 3)*10}" rx="46" ry="12" fill="{LINE}"/>' for x in range(80, w, 190)))
    body = (tree(250, g0, 1.0) + tree(820, g0, 0.85) + tree(2900, g0, 1.05)
            + building + pot(2250, g0) + pot(2700, g0) + bench + ground)
    return png(body, w, H)


# ---------- timing helpers ----------
def ease(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)


def blink_at(t, times, dur=0.16):
    for b in times:
        if b <= t < b + dur:
            x = (t - b) / dur
            return 1 - abs(2 * x - 1)
    return 0.0


def envelope(wav, start, n_frames):
    sr, a = wavfile.read(wav)
    a = a.astype(np.float32)
    if a.ndim > 1:
        a = a.mean(axis=1)
    a /= (np.abs(a).max() + 1e-6)
    env = np.zeros(n_frames)
    hop = sr / FPS
    for i in range(n_frames):
        t0 = (i / FPS - start) * sr
        if t0 < 0 or t0 >= len(a):
            continue
        seg = a[int(t0):int(t0 + hop)]
        env[i] = np.sqrt((seg ** 2).mean()) if len(seg) else 0
    env = env / (env.max() + 1e-6)
    sm = np.copy(env)
    for i in range(1, n_frames):   # quick attack, slower release
        sm[i] = env[i] if env[i] > sm[i - 1] else sm[i - 1] * 0.55 + env[i] * 0.45
    return np.clip((sm - 0.08) * 1.5, 0, 1)


def main(work):
    T = 21.0
    N = int(T * FPS)
    TALK = 10.5
    voice = os.path.join(work, 'voice.wav')
    mouth = envelope(voice, TALK, N)
    talk_end = TALK + float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', voice]))
    far, near = far_layer(), near_layer()
    clouds = [(cloud(1.0), 300, 120, 14), (cloud(0.7), 1100, 210, 9), (cloud(1.2), 1900, 90, 18)]
    font = ImageFont.truetype(os.path.join(ROOT, 'fonts/nunito-latin-800-normal.woff'), 52)
    subs = [(TALK, TALK + 1.6, 'Halo, aku Tunas!'), (TALK + 1.6, TALK + 4.7, 'Hari ini aku mau imunisasi di puskesmas.'),
            (TALK + 4.7, talk_end + 0.3, 'Agak deg-degan, nggak apa-apa.')]
    WALK0, WALK1, X0, X1 = 0.8, 9.5, -300, 1790
    blinks = [3.1, 6.4, 9.9, 13.1, 16.2, 19.2]

    def state(t):
        p = dict(look=2.5)
        if t < WALK1:
            u = (t - WALK0) / (WALK1 - WALK0)
            x = X0 + (X1 - X0) * (u if 0 <= u else 0)
            x = X0 + (X1 - X0) * min(max(u, 0), 1)
            if u > 0.92:   # ease into the stop
                x = X0 + (X1 - X0) * (0.92 + 0.08 * ease((u - 0.92) / 0.08))
            ph = (t - WALK0) * 2 * math.pi * 1.9
            walking = 0 <= u < 1
            k = 1 if walking and u < 0.97 else 0
            p.update(bob=-abs(math.sin(ph)) * 5 * k, leaf=math.sin(ph) * 7 * k, arm_l=math.sin(ph) * 14 * k,
                     arm_r=-math.sin(ph) * 14 * k, foot_l=max(0, math.sin(ph)) * 6 * k, foot_r=max(0, -math.sin(ph)) * 6 * k)
        else:
            x = X1
            settle = max(0, 1 - (t - WALK1) / 0.5)
            breath = math.sin(t * 2.2)
            p.update(bob=breath * 0.8, leaf=math.sin(t * 1.3) * 4, squash=settle * math.sin((t - WALK1) * 14) * 0.6,
                     look=2.5 * max(0, 1 - (t - WALK1) / 0.6), arm_l=breath * 2, arm_r=-breath * 2)
            if t > talk_end + 0.25:
                w = min(1, (t - talk_end - 0.25) / 0.35)
                p['wave'] = -28 * (1 - w) + w * math.sin((t - talk_end) * 9) * 13
        p['blink'] = blink_at(t, blinks)
        return x, p

    os.makedirs(os.path.join(work, 'check'), exist_ok=True)
    checks = {int(s * FPS) for s in (0.5, 5.0, 9.8, 12.5, 16.0, 19.0)}
    tmp = os.path.join(work, 'video.tmp.mp4')
    CHECK = os.environ.get('CHECK') == '1'
    ff = None if CHECK else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                           '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    camx_s = 0.0
    for i in range(N):
        t = i / FPS
        x, p = state(t)
        p['mouth'] = float(mouth[i]) if TALK <= t <= talk_end else 0.0
        target = min(max(x - 700, 0), 1060)
        camx_s = target if i == 0 else camx_s + (target - camx_s) * 0.06
        camx = camx_s
        if CHECK and i not in checks:
            continue
        fr = far.crop((int(camx * 0.35), 0, int(camx * 0.35) + W, H)).copy()
        for img, cx0, cy, spd in clouds:
            cx = int((cx0 + t * spd - camx * 0.2) % (W + 600) - 300)
            fr.alpha_composite(img, (max(cx, 0), cy), (max(-cx, 0), 0))
        fr.alpha_composite(near.crop((int(camx), 0, int(camx) + W, H)))
        paste_tunas(fr, tunas_img(**p), x, camx)
        # slow push-in while Tunas talks
        z = 1 + 0.12 * ease((t - TALK + 0.6) / 4.0) if t > TALK - 0.6 else 1.0
        if z > 1.001:
            fx, fy = x - camx, GROUND - 260
            cw, ch = W / z, H / z
            l = min(max(fx - cw / 2, 0), W - cw)
            tp = min(max(fy - ch / 2, 0), H - ch)
            fr = fr.crop((int(l), int(tp), int(l + cw), int(tp + ch))).resize((W, H), Image.LANCZOS)
        for a, b, s in subs:
            if a <= t < b:
                d = ImageDraw.Draw(fr)
                tw = d.textlength(s, font=font)
                d.rounded_rectangle((W / 2 - tw / 2 - 40, 948, W / 2 + tw / 2 + 40, 1040), 40, fill=CARD)
                d.text((W / 2, 994), s, font=font, fill=INK, anchor='mm')
        if t > T - 0.6:
            a = (t - (T - 0.6)) / 0.6
            fr = Image.blend(fr, Image.new('RGBA', (W, H), '#fbf4ea'), a)
        rgb = fr.convert('RGB')
        if i in checks:
            rgb.save(os.path.join(work, 'check', f'f{i:04d}.png'))
        if ff:
            ff.stdin.write(rgb.tobytes())
    if ff is None:
        return print('checks written')
    ff.stdin.close()
    if ff.wait() == 0:
        os.replace(tmp, os.path.join(work, 'video.mp4'))
    print('ok', N, 'frames')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
