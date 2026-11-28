"""Make (only what changed of) an episode's voices, voice lines, music and sound effects with ElevenLabs.

    ELEVENLABS_API_KEY=... python video/tools/eleven_audio.py video/tunas-e01

Reads <film>/script.json and writes into <film>/audio/:
  voices.json            voice id per character (designed once, then reused)
  vo/l<i>.mp3            one file per line in script.json
  music/<cue>.mp3        one file per music cue
  sfx/<name>.mp3         one file per sound effect
  manifest.json          what each file was made from, so an unchanged file is never paid for twice

A character with clone_name (Tunas): if a voice of that name exists in the account (an instant clone made in the ElevenLabs app),
it is used; until then a designed child voice stands in, and that character's lines are remade once the clone exists.
Never prints the key. If credits run out, it keeps what it made, reports, and exits 0 so the render still runs.
"""
import hashlib, json, os, re, sys, time
from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError

FILM = sys.argv[1].rstrip('/')
S = json.load(open(f'{FILM}/script.json'))
OUT = f'{FILM}/audio'
for d in ('vo', 'music', 'sfx', 'jingle'): os.makedirs(f'{OUT}/{d}', exist_ok=True)
MAN_P, VOI_P = f'{OUT}/manifest.json', f'{OUT}/voices.json'
MAN = json.load(open(MAN_P)) if os.path.exists(MAN_P) else {}
VOI = json.load(open(VOI_P)) if os.path.exists(VOI_P) else {}
key = os.environ.get('ELEVENLABS_API_KEY', '').strip()
if not key:
    print('::error::ELEVENLABS_API_KEY is not set (add it under Settings > Secrets and variables > Actions)'); sys.exit(1)
el = ElevenLabs(api_key=key)
warn = lambda m: print(f'::warning::{m}', flush=True)
made, kept, failed = [], 0, []
STOP = False   # set when the account is out of credits

def save():
    json.dump(MAN, open(MAN_P, 'w'), indent=1, sort_keys=True); json.dump(VOI, open(VOI_P, 'w'), indent=1, sort_keys=True)

def h(obj): return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]

def is_quota(e):
    b = json.dumps(getattr(e, 'body', '') or '', default=str).lower()
    return 'quota' in b or 'credits' in b or 'insufficient' in b or getattr(e, 'status_code', 0) == 402

def make(path, spec, fn):
    """Write path from fn() (an iterator of bytes) unless the manifest says it already matches spec."""
    global STOP, kept
    rel = os.path.relpath(path, OUT); sig = h(spec)
    if MAN.get(rel) == sig and os.path.exists(path) and os.path.getsize(path) > 0: kept += 1; return True
    if STOP: return False
    for attempt in range(3):
        try:
            data = b''.join(fn()); tmp = path + '.part'
            open(tmp, 'wb').write(data); os.replace(tmp, path); MAN[rel] = sig; save(); made.append(rel)
            print(f'made {rel} ({len(data) // 1024} KB)', flush=True); return True
        except ApiError as e:
            if e.status_code == 401 and not is_quota(e): print('::error::ElevenLabs refused the key (401). Check the ELEVENLABS_API_KEY secret.'); sys.exit(1)
            if is_quota(e): STOP = True; warn(f'Out of ElevenLabs credits at {rel}; kept everything made so far.'); failed.append(rel); return False
            if e.status_code in (429, 500, 502, 503) and attempt < 2: time.sleep(5 * (attempt + 1)); continue
            warn(f'{rel}: ElevenLabs error {e.status_code}: {str(e.body)[:300]}'); failed.append(rel); return False
        except Exception as e:
            if attempt < 2: time.sleep(5); continue
            warn(f'{rel}: {e}'); failed.append(rel); return False

# —— 0. the script's lines must match the subtitles in main.js ——
js = open(f'{FILM}/main.js', encoding='utf8').read() if os.path.exists(f'{FILM}/main.js') else ''
m = re.search(r'const LINES = \[(.*?)\n\];', js, re.S)
subs = re.findall(r"\[([\d.]+),\s*'([^']*)'\]", m.group(1)) if m else []
lines = S.get('lines', [])
mism = [i for i, (l, s) in enumerate(zip(lines, subs)) if abs(float(s[0]) - l['t']) > .01 or s[1] != l['text']]
if (lines or subs) and (len(subs) != len(lines) or mism):
    print(f'::error::script.json lines differ from LINES in main.js (count {len(lines)} vs {len(subs)}; first mismatch at line {mism[:1]}). Keep them the same.'); sys.exit(1)

# —— 1. models ——
try: models = {m.model_id: m for m in el.models.list()}
except ApiError as e:
    print(f'::error::ElevenLabs refused the request ({e.status_code}). Check the ELEVENLABS_API_KEY secret.'); sys.exit(1)
TTS = next((x for x in ('eleven_v3', 'eleven_multilingual_v2') if x in models), None)
if not TTS: print('::error::no Indonesian text-to-speech model found'); sys.exit(1)
TTV = 'eleven_ttv_v3' if TTS == 'eleven_v3' else 'eleven_multilingual_ttv_v2'
print('speech model:', TTS)
try:
    sub = el.user.subscription.get(); print(f'credits: {sub.character_count} used of {sub.character_limit} ({sub.tier})')
except Exception: pass

# —— 2. voices ——   (a film with voices_from reuses another film's cast and designs nothing)
if S.get('voices_from'):
    vp = os.path.join(os.path.dirname(FILM), S['voices_from'], 'audio', 'voices.json')
    VOI.update(json.load(open(vp)) if os.path.exists(vp) else {})
clones = {}   # characters with a clone_name use the account's cloned voice of that name, once it exists
names = {c['clone_name'].strip().lower(): who for who, c in S['cast'].items() if c.get('clone_name')}
try:
    for n, who in names.items():
        for v in el.voices.search(search=n, page_size=50).voices:
            if v.name.strip().lower() == n and v.category in ('cloned', 'professional'): clones[who] = v.voice_id; break
except Exception as e: warn(f'voice search failed: {e}')
clone = next(iter(clones.values()), None)
for who, c in S['cast'].items():
    if who in clones:
        if VOI.get(who, {}).get('voice_id') != clones[who]: print(f'{who}: using the cloned voice "{c["clone_name"]}"')
        VOI[who] = {'voice_id': clones[who], 'source': 'clone'}; continue
    seed = c.get('seed', 11); pick = c.get('pick')
    want = h({'design': c['design'], 'preview': c['preview'], 'model': TTV, 'seed': seed if (c.get('audition') or pick) else None, 'pick': pick})
    if VOI.get(who, {}).get('design') == want or (not pick and VOI.get(who, {}).get('audition') == want): continue
    if STOP: continue
    try:
        kw = dict(voice_description=c['design'], text=c['preview'], model_id=TTV)
        if c.get('audition') or pick: kw['seed'] = seed
        os.makedirs(f'{OUT}/previews', exist_ok=True)
        import base64
        name = f"TemanTumbuh {who.capitalize()}{' (placeholder)' if c.get('clone_name') else ''}"
        opts = VOI.get(who, {}).get('options') or []
        v = None
        if pick and len(opts) >= pick:   # the exact option that was heard
            try: v = el.text_to_voice.create(voice_name=name, voice_description=c['design'], generated_voice_id=opts[pick - 1])
            except ApiError as e: warn(f'{who}: option {pick} has expired ({e.status_code}); making it again from the same settings')
        if v is None:
            r = el.text_to_voice.design(**kw)
            if c.get('audition') and not pick:   # three options to listen to; the old voice stays until one is picked
                for k, p in enumerate(r.previews[:3], 1): open(f'{OUT}/previews/{who}-{k}.mp3', 'wb').write(base64.b64decode(p.audio_base_64))
                VOI.setdefault(who, {}).update(audition=want, options=[p.generated_voice_id for p in r.previews[:3]]); save()
                print(f'{who}: {len(r.previews[:3])} options saved in previews/', flush=True); continue
            p = r.previews[(pick or 1) - 1]
            v = el.text_to_voice.create(voice_name=name, voice_description=c['design'], generated_voice_id=p.generated_voice_id)
            open(f'{OUT}/previews/{who}.mp3', 'wb').write(base64.b64decode(p.audio_base_64))
        elif os.path.exists(f'{OUT}/previews/{who}-{pick}.mp3'):
            import shutil; shutil.copy(f'{OUT}/previews/{who}-{pick}.mp3', f'{OUT}/previews/{who}.mp3')
        VOI[who] = {'voice_id': v.voice_id, 'source': 'designed', 'design': want}; save()
        print(f'designed voice for {who}', flush=True)
    except ApiError as e:
        if is_quota(e): STOP = True; warn(f'Out of credits while designing {who}')
        else: warn(f'voice design for {who} failed: {e.status_code} {str(e.body)[:300]}')
        failed.append(f'voice:{who}')
save()

# —— 3. voice lines ——
for i, l in enumerate(lines):
    vid = VOI.get(l['who'], {}).get('voice_id')
    if not vid: failed.append(f'vo/l{i}.mp3'); continue
    prof = S['cast'].get(l['who'], {}).get('profile') or {}   # a character's speaking style beats the line's own tone
    tone = prof.get('tag') or l.get('tone')
    text = (f"[{tone}] " if tone and TTS == 'eleven_v3' else '') + l['text']
    prev = lines[i - 1]['text'] if i else None; nxt = lines[i + 1]['text'] if i + 1 < len(lines) else None
    kw = dict(voice_id=vid, text=text, model_id=TTS, output_format='mp3_44100_128')
    if TTS == 'eleven_v3': kw['language_code'] = S.get('language', 'id')
    else:
        kw.update(previous_text=prev, next_text=nxt)
        if prof: kw['voice_settings'] = {'stability': prof.get('stability', .5), 'similarity_boost': .75, 'style': prof.get('style', 0)}
    make(f'{OUT}/vo/l{i}.mp3', kw, lambda kw=kw: el.text_to_speech.convert(**kw))

# —— 4. sound effects ——
for name, d in S['sfx']['defs'].items():
    if d.get('prompt', '').startswith('('): continue   # a copied file, not made here
    kw = dict(text=d['prompt'], duration_seconds=d.get('seconds'), output_format='mp3_44100_128')
    if d.get('loop'): kw['loop'] = True
    make(f'{OUT}/sfx/{name}.mp3', kw, lambda kw=kw: el.text_to_sound_effects.convert(**kw))

# —— 5. music (largest cost last) ——
for name, d in S['music']['cues'].items():
    if os.path.exists(f'{OUT}/music/{name}.own.wav'): continue   # your own track wins
    kw = dict(prompt=S['music']['style'] + ' ' + d['prompt'], music_length_ms=int(d['seconds'] * 1000), force_instrumental=True)
    make(f'{OUT}/music/{name}.mp3', kw, lambda kw=kw: el.music.compose(**kw))

# —— 6. series jingle: every take of the composition plan (a sung song), for picking one ——
J = S.get('jingle') or {}
for t in J.get('takes', []):
    from elevenlabs.types import MusicPrompt
    kw = dict(composition_plan=MusicPrompt(**t['plan']), seed=t.get('seed'))
    make(f"{OUT}/jingle/{t['name']}.mp3", {'plan': t['plan'], 'seed': t.get('seed')}, lambda kw=kw: el.music.compose(**kw))

# the cast shouts the show's name for the jingle's ending (voices from the episode's cast)
SH = J.get('shout') or {}
if SH:
    vp = os.path.join(os.path.dirname(FILM), SH.get('voices_from', 'tunas-e01'), 'audio', 'voices.json')
    cv_ = json.load(open(vp)) if os.path.exists(vp) else {}
    for who in SH.get('who', []):
        vid = cv_.get(who, {}).get('voice_id')
        if not vid: warn(f'shout: no voice for {who}'); continue
        text = (f"[{SH.get('tag', 'shouting happily')}] " if TTS == 'eleven_v3' else '') + SH['text']
        kw = dict(voice_id=vid, text=text, model_id=TTS, output_format='mp3_44100_128')
        if TTS == 'eleven_v3': kw['language_code'] = 'id'
        make(f"{OUT}/jingle/shout-{who}.mp3", kw, lambda kw=kw: el.text_to_speech.convert(**kw))

# transcripts: what speech-to-text hears in each take (if it can't make out a word, a toddler won't either)
for name in J.get('transcribe', []):
    src = f'{OUT}/jingle/{name}.mp3'
    if not os.path.exists(src): continue
    def stt(src=src):
        r = el.speech_to_text.convert(model_id='scribe_v1', file=open(src, 'rb'), language_code='id', timestamps_granularity='word', tag_audio_events=False)
        return [json.dumps(r.model_dump() if hasattr(r, 'model_dump') else r, ensure_ascii=False, default=str, indent=1).encode()]
    make(f'{OUT}/jingle/{name}.transcript.json', {'stt': name, 'src': h(open(src, 'rb').read().hex())}, stt)

# stems: a take split into vocals and the music bed (for recording your own vocals over it)
for name in J.get('stems', []):
    src = f'{OUT}/jingle/{name}.mp3'
    if not os.path.exists(src): continue
    zp = f'{OUT}/jingle/{name}-stems.zip'
    def sep(src=src): return el.music.separate_stems(file=open(src, 'rb'), stem_variation_id='two_stems_v1')
    if make(zp, {'stems': name, 'src': h(open(src, 'rb').read().hex())}, sep):
        import zipfile
        try:
            with zipfile.ZipFile(zp) as z:
                for n in z.namelist():
                    if n.endswith('/'): continue
                    out = f"{OUT}/jingle/{name}-{os.path.basename(n).replace(' ', '_').lower()}"
                    open(out, 'wb').write(z.read(n)); print('stem:', out)
        except zipfile.BadZipFile: os.replace(zp, f'{OUT}/jingle/{name}-stems.mp3')

save()
print(f'\nmade {len(made)}, unchanged {kept}, missing {len(failed)}')
with open(os.environ.get('GITHUB_STEP_SUMMARY', os.devnull), 'a') as f:
    f.write(f"### Audio for {os.path.basename(FILM)}\nSpeech model `{TTS}`. Child voice: {'your clone' if clone else 'placeholder (make a voice named ' + ', '.join(c['clone_name'] for c in S['cast'].values() if c.get('clone_name')) + ' in ElevenLabs to replace it)'}.\n\n"
            f"Made {len(made)}, unchanged {kept}, missing {len(failed)}.\n" + (''.join(f'- missing `{x}`\n' for x in failed)))
if failed: warn(f'{len(failed)} audio files are missing; the render uses what exists.')
