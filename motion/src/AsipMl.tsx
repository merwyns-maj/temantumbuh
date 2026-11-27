// ASIP ml: voiced motion video. Copy = the approved ASIP ml carousel (w4s-asip-ml), voice = semangat Mama.
// No bottles or teats anywhere (PP 28/2024): milk is shown in a cup and in storage bags.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {C, SAFE, CX, Fonts, display, body, wordsFrom, merge, at, Captions, LivingBg, Progress, Img, Counter, ease, Align} from './kit';
import align from './data/asip-align.json';

const FPS = 30;
const END_HOLD = 3.4; // sting + CTA after the voice
const words = merge(wordsFrom(align as Align), [
  ['sembilan puluh sampai seratus dua puluh mililiter', '90-120 ml'],
  ['satu sampai enam bulan', '1-6 bulan'],
  ['tujuh ratus lima puluh', '750 ml'],
  ['tiga puluh mililiter', '30 ml'],
  ['enam bulan', '6 bulan'],
]);
const voiceEnd = words[words.length - 1].end;
const T = {
  hook: 0,
  bayi: at(words, 'bayi') - 0.15,
  sehari: at(words, 'sehari') - 0.1,
  dan: at(words, 'dan') - 0.1,
  cara: at(words, 'cara') - 0.1,
  simpan: at(words, 'simpan') - 0.1,
  end: voiceEnd + END_HOLD,
};
export const asipDuration = () => Math.ceil(T.end * FPS);
const fr = (s: number) => Math.round(s * FPS);

const Bag: React.FC<{label?: string; fill?: number; w?: number}> = ({label = '30 ml', fill = 0.6, w = 120}) => (
  <svg width={w} height={w * 1.35} viewBox="0 0 100 135">
    <rect x="8" y="6" width="84" height="14" rx="5" fill={C.sage} />
    <path d="M10 22 H90 V118 Q90 130 78 130 H22 Q10 130 10 118 Z" fill="#fff" stroke={C.line} strokeWidth="4" />
    <path d={`M12 ${128 - 104 * fill} H88 V118 Q88 128 78 128 H22 Q12 128 12 118 Z`} fill={C.milk} />
    <text x="50" y="88" textAnchor="middle" style={{...body, fontSize: 22}} fill={C.ink}>{label}</text>
  </svg>
);

const Cup: React.FC<{level: number; w: number}> = ({level, w}) => (
  <svg width={w} height={w * 1.1} viewBox="0 0 200 220">
    <defs><clipPath id="cupc"><path d="M30 30 L170 30 L152 200 Q150 212 138 212 L62 212 Q50 212 48 200 Z" /></clipPath></defs>
    <path d="M30 30 L170 30 L152 200 Q150 212 138 212 L62 212 Q50 212 48 200 Z" fill="#fff" stroke={C.ink} strokeWidth="7" />
    <g clipPath="url(#cupc)">
      <rect x="0" y={212 - 182 * level} width="200" height="220" fill={C.milk} />
      <path d={`M0 ${212 - 182 * level} q25 -10 50 0 t50 0 t50 0 t50 0 V230 H0Z`} fill={C.milkEdge} opacity=".6" />
    </g>
    {[0.25, 0.5, 0.75].map((m) => <line key={m} x1="140" x2="160" y1={212 - 182 * m} y2={212 - 182 * m} stroke={C.muted} strokeWidth="4" />)}
  </svg>
);

// ---------- Scene 1: hook ----------
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = (d: number) => spring({frame: f - d, fps, config: {damping: 9, stiffness: 180}});
  const shake = f > 14 && f < 26 ? Math.sin(f * 2.2) * 8 : 0;
  const bags = [0, 1, 2, 3, 4, 5];
  const xIn = spring({frame: f - 40, fps, config: {damping: 8, stiffness: 200}});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: SAFE.left, top: 270, width: 820}}>
        <div style={{...display, fontSize: 112, color: C.ink, lineHeight: 1.02, transform: `scale(${p(0)})`, transformOrigin: 'left'}}>STOK ASIP</div>
        <div style={{...display, fontSize: 112, color: C.terra, lineHeight: 1.02, transform: `scale(${p(8)}) translateX(${shake}px)`, transformOrigin: 'left'}}>NGGAK PERLU</div>
        <div style={{...display, fontSize: 84, color: C.ink, lineHeight: 1.1, transform: `translateY(${(1 - p(16)) * 80}px)`, opacity: p(16)}}>ditambah tiap bulan!</div>
      </div>
      {/* bags piling up month by month, then struck out */}
      <div style={{position: 'absolute', left: 100, top: 800, width: 780, height: 460, display: 'flex', alignItems: 'flex-end', gap: 6}}>
        {bags.map((i) => {
          const s = spring({frame: f - 18 - i * 3, fps, config: {damping: 10, stiffness: 220}});
          return (
            <div key={i} style={{transform: `translateY(${(1 - s) * -500}px) rotate(${(i % 2 ? 6 : -5) * s}deg)`, opacity: s > 0.02 ? 1 : 0}}>
              <Bag w={124} fill={0.65} label={`Bln ${i + 1}`} />
              <div style={{height: i * 22}} />
            </div>
          );
        })}
      </div>
      <svg style={{position: 'absolute', left: 150, top: 830, opacity: xIn}} width="680" height="420" viewBox="0 0 680 420">
        <path d={`M40 40 L${40 + 600 * xIn} ${40 + 340 * xIn}`} stroke={C.terra} strokeWidth="34" strokeLinecap="round" />
        <path d={`M640 40 L${640 - 600 * xIn} ${40 + 340 * xIn}`} stroke={C.terra} strokeWidth="34" strokeLinecap="round" />
      </svg>
      <div style={{position: 'absolute', left: 690, top: 600, transform: `translateY(${(1 - p(30)) * 300}px) rotate(${Math.sin(f / 6) * 6}deg)`}}>
        <Img src="tunas-kaget.svg" w={190} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- Scene 2: 90-120 ml sekali minum ----------
const PerFeed: React.FC<{len: number}> = ({len}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const chip = spring({frame: f, fps, config: {damping: 12}});
  const cupIn = spring({frame: f - 6, fps, config: {damping: 10, stiffness: 140}});
  const level = ease(f, 25, 95, 0, 0.78) + Math.sin(f / 5) * 0.01;
  const ml = Math.round(ease(f, 25, 95, 0, 120));
  const range = ease(f, 95, 110);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: SAFE.left, top: 270, transform: `translateX(${(1 - chip) * -600}px)`,
        background: C.ibuBg, color: C.ibuInk, ...body, fontSize: 44, padding: '14px 30px', borderRadius: 40}}>BAYI 1-6 BULAN</div>
      <div style={{position: 'absolute', left: SAFE.left, top: 370, ...display, fontSize: 70, color: C.ink, opacity: ease(f, 8, 20)}}>sekali minum cuma</div>
      <div style={{position: 'absolute', left: 90, top: 560, transform: `scale(${cupIn}) rotate(${Math.sin(f / 14) * 2}deg)`, transformOrigin: 'bottom center'}}>
        <Cup level={level} w={470} />
      </div>
      <div style={{position: 'absolute', left: 560, top: 700, textAlign: 'left'}}>
        <div style={{...display, fontSize: 150, color: C.terra, lineHeight: 1, whiteSpace: 'nowrap'}}>
          {range > 0.5 ? <span style={{display: 'inline-block', transform: `scale(${1 + 0.15 * Math.sin(range * Math.PI)})`}}>90-120</span> : ml}
        </div>
        <div style={{...display, fontSize: 90, color: C.ink, marginTop: -10}}>ml</div>
      </div>
      {/* little sparkles when the number lands */}
      {[0, 1, 2, 3, 4].map((i) => {
        const s = ease(f, 98 + i * 2, 120 + i * 2);
        const ang = (i / 5) * Math.PI * 2;
        return <div key={i} style={{position: 'absolute', left: 700 + Math.cos(ang) * 230 * s, top: 700 + Math.sin(ang) * 180 * s,
          width: 26, height: 26, borderRadius: 13, background: [C.sun, C.sage, C.blush][i % 3], opacity: s > 0 && s < 1 ? 1 - s * 0.6 : 0}} />;
      })}
    </AbsoluteFill>
  );
};

// ---------- Scene 3: sehari 750 ml ----------
const PerDay: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const r = 250, circ = 2 * Math.PI * r;
  const p = ease(f, 6, 70);
  const pop = spring({frame: f, fps, config: {damping: 11}});
  const marks = Array.from({length: 24}, (_, i) => i);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: SAFE.left, top: 270, ...display, fontSize: 96, color: C.ink, transform: `scale(${pop})`, transformOrigin: 'left'}}>
        Sehari<span style={{color: C.terra}}>?</span>
      </div>
      <svg style={{position: 'absolute', left: CX - 300, top: 440, transform: `scale(${pop}) rotate(${f * 0.3}deg)`}} width="600" height="600" viewBox="0 0 600 600">
        <circle cx="300" cy="300" r={r} fill={C.card} stroke={C.line} strokeWidth="40" />
        <circle cx="300" cy="300" r={r} fill="none" stroke={C.sage} strokeWidth="40" strokeLinecap="round"
          strokeDasharray={`${circ * p} ${circ}`} transform="rotate(-90 300 300)" />
        {marks.map((i) => (
          <circle key={i} cx={300 + Math.cos((i / 24) * 2 * Math.PI - Math.PI / 2) * 205} cy={300 + Math.sin((i / 24) * 2 * Math.PI - Math.PI / 2) * 205}
            r={i / 24 <= p ? 9 : 6} fill={i / 24 <= p ? C.sun : C.line} />
        ))}
      </svg>
      <div style={{position: 'absolute', left: CX - 300, top: 440, width: 600, height: 600, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center'}}>
        <Counter from={0} to={750} a={6} b={70} style={{...display, fontSize: 150, color: C.terra, lineHeight: 1}} />
        <div style={{...display, fontSize: 60, color: C.ink}}>ml / 24 jam</div>
      </div>
      <div style={{position: 'absolute', left: SAFE.left, top: 1110, width: 820, textAlign: 'center', ...body, fontSize: 44, color: C.muted, opacity: ease(f, 50, 65)}}>
        sekitar, kira-kira
      </div>
    </AbsoluteFill>
  );
};

// ---------- Scene 4: stays the same to 6 months ----------
const Flat: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const months = [1, 2, 3, 4, 5, 6];
  const line = ease(f, 40, 70);
  const nod = spring({frame: f - 55, fps, config: {damping: 7}});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: SAFE.left, top: 270, width: 820, ...display, fontSize: 78, color: C.ink, lineHeight: 1.1, opacity: ease(f, 0, 10)}}>
        Bulan 1 sampai 6:<br /><span style={{color: C.sageDeep}}>hampir sama!</span>
      </div>
      <div style={{position: 'absolute', left: 120, top: 540, width: 760, height: 660, display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between'}}>
        {months.map((m, i) => {
          const h = spring({frame: f - 6 - i * 5, fps, config: {damping: 12, stiffness: 120}});
          return (
            <div key={m} style={{width: 96, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
              <div style={{...body, fontSize: 30, color: C.ink, opacity: h}}>750</div>
              <div style={{width: 96, height: 500 * h, background: i % 2 ? C.sage : C.sageDeep, borderRadius: '20px 20px 6px 6px'}} />
              <div style={{...body, fontSize: 34, color: C.muted, marginTop: 10}}>Bln {m}</div>
            </div>
          );
        })}
      </div>
      <svg style={{position: 'absolute', left: 120, top: 640}} width="760" height="40">
        <line x1="0" y1="20" x2={760 * line} y2="20" stroke={C.terra} strokeWidth="10" strokeDasharray="22 14" strokeLinecap="round" />
      </svg>
      <div style={{position: 'absolute', left: 690, top: 300, transform: `scale(${nod}) translateY(${Math.sin(f / 4) * 6 * (f > 55 ? 1 : 0)}px)`}}>
        <Img src="tunas-mikir.svg" w={190} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- Scene 5: 30 ml per hour away ----------
const PerHour: React.FC<{len: number}> = ({len}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const hours = Math.min(10, Math.floor(ease(f, 20, len - 10, 0, 10.99)));
  const hand = ease(f, 20, len - 10, 0, 300);
  const formula = spring({frame: f, fps, config: {damping: 12}});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: SAFE.left, top: 260, transform: `scale(${formula})`, transformOrigin: 'left',
        background: C.ink, color: '#fff', ...display, fontSize: 68, padding: '18px 34px', borderRadius: 30}}>
        30 ml <span style={{color: C.sun}}>×</span> jam pergi
      </div>
      <svg style={{position: 'absolute', left: 110, top: 430}} width="300" height="300" viewBox="0 0 300 300">
        <circle cx="150" cy="150" r="130" fill={C.card} stroke={C.ink} strokeWidth="10" />
        {Array.from({length: 12}, (_, i) => (
          <line key={i} x1={150 + Math.cos((i / 12) * 2 * Math.PI) * 108} y1={150 + Math.sin((i / 12) * 2 * Math.PI) * 108}
            x2={150 + Math.cos((i / 12) * 2 * Math.PI) * 122} y2={150 + Math.sin((i / 12) * 2 * Math.PI) * 122} stroke={C.ink} strokeWidth="6" />
        ))}
        <line x1="150" y1="150" x2="150" y2="62" stroke={C.terra} strokeWidth="12" strokeLinecap="round" transform={`rotate(${hand} 150 150)`} />
        <line x1="150" y1="150" x2="150" y2="40" stroke={C.ink} strokeWidth="6" strokeLinecap="round" transform={`rotate(${hand * 12} 150 150)`} />
        <circle cx="150" cy="150" r="14" fill={C.ink} />
      </svg>
      <div style={{position: 'absolute', left: 450, top: 470}}>
        <div style={{...display, fontSize: 64, color: C.ink}}>Pergi <span style={{color: C.terra}}>{hours}</span> jam</div>
        <div style={{...display, fontSize: 120, color: C.terra, lineHeight: 1.05}}>{hours * 30} ml</div>
      </div>
      <div style={{position: 'absolute', left: 90, top: 790, width: 820, display: 'flex', flexWrap: 'wrap', gap: 14}}>
        {Array.from({length: hours}, (_, i) => {
          const at0 = 20 + ((len - 30) / 10.99) * (i + 0.001);
          const s = spring({frame: f - at0, fps, config: {damping: 9, stiffness: 240}});
          return <div key={i} style={{transform: `translateY(${(1 - s) * -200}px) scale(${s})`}}><Bag w={140} fill={0.5} /></div>;
        })}
      </div>
    </AbsoluteFill>
  );
};

// ---------- Scene 6: CTA ----------
const Cta: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const jump = spring({frame: f, fps, config: {damping: 6, stiffness: 160}});
  const pulse = 1 + Math.sin(f / 4) * 0.05;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: CX - 150, top: 300 - Math.abs(Math.sin(f / 7)) * 40, transform: `scale(${jump})`}}>
        <Img src="tunas-hore.svg" w={300} />
      </div>
      <div style={{position: 'absolute', left: SAFE.left, top: 700, width: 820, textAlign: 'center', ...display, fontSize: 130, color: C.terra, transform: `scale(${jump * pulse})`}}>
        SIMPAN YA!
      </div>
      <svg style={{position: 'absolute', left: CX - 60, top: 880, transform: `scale(${pulse}) rotate(${Math.sin(f / 5) * 8}deg)`}} width="120" height="150" viewBox="0 0 120 150">
        <path d="M10 10 H110 V140 L60 105 L10 140 Z" fill={C.sun} stroke={C.ink} strokeWidth="8" strokeLinejoin="round" />
      </svg>
      <div style={{position: 'absolute', left: SAFE.left, top: 1080, width: 820, textAlign: 'center', ...body, fontSize: 40, color: C.ink, opacity: ease(f, 10, 25)}}>
        Nggak harus habis, ikuti lapar dan kenyangnya.
      </div>
      <div style={{position: 'absolute', left: SAFE.left, top: 1250, width: 820, textAlign: 'center', fontFamily: 'Nunito', fontWeight: 700, fontSize: 28, color: C.muted, opacity: ease(f, 15, 30)}}>
        Sumber: HSE Irlandia, La Leche League GB, Australian Breastfeeding Association, CDC.<br />
        Konten edukasi umum. Untuk kondisi khusus, konsultasikan dengan dokter anak.
      </div>
    </AbsoluteFill>
  );
};

// Scene wrapper: zoom-pop in, quick scale-out at the end.
const Scene: React.FC<{from: number; to: number; children: React.ReactNode}> = ({from, to, children}) => {
  const len = fr(to) - fr(from);
  return (
    <Sequence from={fr(from)} durationInFrames={len}>
      <SceneIO len={len}>{children}</SceneIO>
    </Sequence>
  );
};
const SceneIO: React.FC<{len: number; children: React.ReactNode}> = ({len, children}) => {
  const f = useCurrentFrame();
  const out = interpolate(f, [len - 6, len], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const inn = interpolate(f, [0, 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{opacity: Math.min(out, inn), transform: `scale(${0.96 + 0.04 * inn + (1 - out) * 0.06})`}}>{children}</AbsoluteFill>;
};

export const AsipMl: React.FC = () => {
  const total = asipDuration();
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <Fonts />
      <LivingBg />
      <Scene from={T.hook} to={T.bayi}><Hook /></Scene>
      <Scene from={T.bayi} to={T.sehari}><PerFeed len={fr(T.sehari - T.bayi)} /></Scene>
      <Scene from={T.sehari} to={T.dan}><PerDay /></Scene>
      <Scene from={T.dan} to={T.cara}><Flat /></Scene>
      <Scene from={T.cara} to={T.simpan}><PerHour len={fr(T.simpan - T.cara)} /></Scene>
      <Scene from={T.simpan} to={T.end}><Cta /></Scene>
      <Progress total={total} />
      <Captions words={words} until={voiceEnd + 0.3} />
      <Audio src={staticFile('voice.mp3')} />
      <Sequence from={fr(voiceEnd + 0.15)}><Audio src={staticFile('sting.mp3')} volume={0.9} /></Sequence>
      {HAS_BED && <Audio src={staticFile('bed.mp3')} volume={(f) => interpolate(f, [0, 15, total - 30, total], [0, 0.1, 0.1, 0], {extrapolateRight: 'clamp'})} />}
    </AbsoluteFill>
  );
};
const HAS_BED = true;
