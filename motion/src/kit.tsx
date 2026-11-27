// Shared motion kit for TemanTumbuh videos: colours, fonts, word timing, captions, background.
import React from 'react';
import {AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

export const C = {
  bg: '#fbf4ea', bg2: '#f4e8d8', card: '#fffdf9', line: '#e9dccb', ink: '#4a3f35', muted: '#7a6c5f',
  sage: '#7fa98f', sageDeep: '#5f8a70', sageTint: '#e3eee6', terra: '#e07856', terraDeep: '#c46040',
  blush: '#f6cdbd', sun: '#f3c45f', ibuBg: '#f0dde9', ibuInk: '#73395f', milk: '#fff6dc', milkEdge: '#f1dfae',
};
// Safe zone: x 80..900 (right rail has the buttons), y 220..1500 (bottom has the caption).
export const SAFE = {left: 80, right: 900, top: 220, bottom: 1500};
export const CX = (SAFE.left + SAFE.right) / 2;

export const Fonts: React.FC = () => (
  <style>{`
    @font-face{font-family:'Fredoka';src:url(${staticFile('fredoka-latin-600-normal.woff')}) format('woff');font-weight:600}
    @font-face{font-family:'Nunito';src:url(${staticFile('nunito-latin-800-normal.woff')}) format('woff');font-weight:800}
    @font-face{font-family:'Nunito';src:url(${staticFile('nunito-latin-700-normal.woff')}) format('woff');font-weight:700}
  `}</style>
);
export const display: React.CSSProperties = {fontFamily: 'Fredoka', fontWeight: 600};
export const body: React.CSSProperties = {fontFamily: 'Nunito', fontWeight: 800};

export type Align = {characters: string[]; character_start_times_seconds: number[]; character_end_times_seconds: number[]};
export type Word = {text: string; start: number; end: number};

export function wordsFrom(a: Align): Word[] {
  const out: Word[] = [];
  let cur = '', s = 0, e = 0;
  a.characters.forEach((ch, i) => {
    if (/\s/.test(ch)) {
      if (cur) out.push({text: cur, start: s, end: e});
      cur = '';
    } else {
      if (!cur) s = a.character_start_times_seconds[i];
      cur += ch;
      e = a.character_end_times_seconds[i];
    }
  });
  if (cur) out.push({text: cur, start: s, end: e});
  return out;
}
// Start time of the first word that begins with `w` (case-insensitive), searching from index `from`.
export function at(words: Word[], w: string, from = 0): number {
  for (let i = from; i < words.length; i++) if (words[i].text.toLowerCase().replace(/[^a-z0-9]/g, '').startsWith(w.toLowerCase())) return words[i].start;
  throw new Error('word not found: ' + w);
}

export const usePop = (delayFrames: number, damping = 11, stiffness = 160) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: f - delayFrames, fps, config: {damping, stiffness}});
};
export const ease = (f: number, a: number, b: number, from = 0, to = 1) =>
  interpolate(f, [a, b], [from, to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});

// Word-by-word captions: shows the current phrase (split at punctuation), current word in terra and slightly larger.
export const Captions: React.FC<{words: Word[]; until: number}> = ({words, until}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  if (t > until) return null;
  // group into phrases of at most 5 words, breaking after punctuation
  const groups: Word[][] = [];
  let g: Word[] = [];
  words.forEach((w) => {
    g.push(w);
    if (/[.,!?:]$/.test(w.text) || g.length >= 5) { groups.push(g); g = []; }
  });
  if (g.length) groups.push(g);
  let gi = 0;
  groups.forEach((gr, i) => { if (t >= gr[0].start - 0.05) gi = i; });
  const gr = groups[gi];
  const enter = spring({frame: f - Math.round((gr[0].start - 0.05) * fps), fps, config: {damping: 14, stiffness: 200}});
  return (
    <div style={{position: 'absolute', left: SAFE.left, width: SAFE.right - SAFE.left, top: 1300, height: 190,
      display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{background: C.ink, borderRadius: 36, padding: '18px 30px', maxWidth: 800, textAlign: 'center',
        transform: `translateY(${(1 - enter) * 30}px) scale(${0.92 + 0.08 * enter})`, boxShadow: '0 10px 0 rgba(74,63,53,.18)'}}>
        {gr.map((w, i) => {
          const on = t >= w.start - 0.03;
          const now = on && t < w.end + 0.08;
          return (
            <span key={i} style={{...body, fontSize: now ? 60 : 56, color: now ? C.sun : on ? '#fff' : 'rgba(255,255,255,.45)',
              margin: '0 9px', display: 'inline-block', transform: now ? 'translateY(-4px)' : 'none', lineHeight: 1.25}}>
              {w.text.replace(/[,]$/, '')}
            </span>
          );
        })}
      </div>
    </div>
  );
};

// Soft moving background: floating dots and two drifting blobs, so no frame is ever static.
export const LivingBg: React.FC<{tint?: string}> = ({tint = C.bg2}) => {
  const f = useCurrentFrame();
  const dots = Array.from({length: 14}, (_, i) => i);
  return (
    <AbsoluteFill style={{background: C.bg, overflow: 'hidden'}}>
      <div style={{position: 'absolute', width: 900, height: 900, borderRadius: '50%', background: tint, opacity: 0.8,
        left: -300 + Math.sin(f / 70) * 60, top: -260 + Math.cos(f / 90) * 50}} />
      <div style={{position: 'absolute', width: 700, height: 700, borderRadius: '50%', background: tint, opacity: 0.6,
        left: 600 + Math.cos(f / 80) * 50, top: 1350 + Math.sin(f / 60) * 40}} />
      {dots.map((i) => {
        const x = (i * 137) % 1000 + 40;
        const y = ((i * 263) % 1800) - ((f * (0.6 + (i % 4) * 0.25)) % 1900) + 1900;
        const col = [C.sun, C.blush, C.sageTint, C.terra][i % 4];
        return <div key={i} style={{position: 'absolute', left: x, top: y % 1950 - 30, width: 14 + (i % 3) * 8, height: 14 + (i % 3) * 8,
          borderRadius: '50%', background: col, opacity: 0.55}} />;
      })}
    </AbsoluteFill>
  );
};

// Thin progress bar at the top of the safe zone (retention cue).
export const Progress: React.FC<{total: number}> = ({total}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: SAFE.left, top: 190, width: SAFE.right - SAFE.left, height: 12, borderRadius: 6, background: C.line}}>
      <div style={{width: `${Math.min(100, (f / total) * 100)}%`, height: '100%', borderRadius: 6, background: C.terra}} />
    </div>
  );
};

export const Img: React.FC<{src: string; w: number; style?: React.CSSProperties}> = ({src, w, style}) => (
  <img src={staticFile(src)} style={{width: w, display: 'block', ...style}} />
);

// Animated number: counts from `from` to `to` between frames a..b.
export const Counter: React.FC<{from: number; to: number; a: number; b: number; style?: React.CSSProperties; suffix?: string}> =
  ({from, to, a, b, style, suffix = ''}) => {
    const f = useCurrentFrame();
    const v = Math.round(ease(f, a, b, from, to));
    return <span style={style}>{v}{suffix}</span>;
  };

// Merge spoken number phrases into one caption token ("sembilan puluh ... mililiter" -> "90-120 ml").
export function merge(words: Word[], rules: [string, string][]): Word[] {
  const out: Word[] = [];
  const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
  let i = 0;
  while (i < words.length) {
    let hit = false;
    for (const [phrase, show] of rules) {
      const ps = phrase.split(' ');
      if (ps.every((p, k) => words[i + k] && norm(words[i + k].text) === norm(p))) {
        const last = words[i + ps.length - 1];
        const trail = (last.text.match(/[.,!?:]+$/) || [''])[0];
        out.push({text: show + trail, start: words[i].start, end: last.end});
        i += ps.length; hit = true; break;
      }
    }
    if (!hit) { out.push(words[i]); i++; }
  }
  return out;
}
