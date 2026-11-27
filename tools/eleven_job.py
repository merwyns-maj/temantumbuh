"""Run ElevenLabs jobs from voice/requests/*.json inside GitHub Actions.
The API key comes only from the ELEVENLABS_API_KEY secret (env). It is never printed or written to disk.
Request shapes (one JSON object or a list of them per file):
  {"type": "voices"}                                  -> voice/out/voices.json (name, id, labels, language only)
  {"type": "tts", "text": "...", "voice_id": "...", "out": "name.mp3",
   "model_id": "eleven_multilingual_v2", "settings": {"stability": 0.5, "similarity_boost": 0.75}}
  {"type": "sfx", "text": "soft music box sting", "seconds": 4, "out": "sting.mp3"}
Outputs land in voice/out/. Each processed request file moves to voice/done/.
"""
import json, os, sys, glob, shutil, urllib.request, urllib.error

KEY = os.environ.get('ELEVENLABS_API_KEY', '')
API = 'https://api.elevenlabs.io'
OUT = 'voice/out'; DONE = 'voice/done'
os.makedirs(OUT, exist_ok=True); os.makedirs(DONE, exist_ok=True)


def call(method, path, body=None, accept='application/json'):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'xi-api-key': KEY, 'Content-Type': 'application/json', 'Accept': accept})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        msg = e.read().decode('utf-8', 'replace')[:400]
        raise SystemExit(f'ElevenLabs {path} -> HTTP {e.code}: {msg}')


def safe(name):
    name = os.path.basename(name or 'out.mp3')
    return ''.join(c for c in name if c.isalnum() or c in '-_.') or 'out.mp3'


def run(job, log):
    t = job.get('type')
    if t == 'voices':
        data = json.loads(call('GET', '/v1/voices'))
        keep = [{'name': v.get('name'), 'voice_id': v.get('voice_id'), 'category': v.get('category'),
                 'labels': v.get('labels'), 'language': (v.get('verified_languages') or [{}])[0].get('language') if v.get('verified_languages') else None}
                for v in data.get('voices', [])]
        json.dump(keep, open(f'{OUT}/voices.json', 'w'), ensure_ascii=False, indent=1)
        log.append(f'voices: {len(keep)} saved')
    elif t == 'tts':
        body = {'text': job['text'], 'model_id': job.get('model_id', 'eleven_multilingual_v2')}
        if job.get('settings'): body['voice_settings'] = job['settings']
        if job.get('language_code'): body['language_code'] = job['language_code']
        audio = call('POST', f"/v1/text-to-speech/{job['voice_id']}?output_format=mp3_44100_128", body, 'audio/mpeg')
        out = safe(job.get('out')); open(f'{OUT}/{out}', 'wb').write(audio); log.append(f'tts: {out} {len(audio)} bytes')
    elif t == 'sfx':
        body = {'text': job['text']}
        if job.get('seconds'): body['duration_seconds'] = job['seconds']
        audio = call('POST', '/v1/sound-generation', body, 'audio/mpeg')
        out = safe(job.get('out')); open(f'{OUT}/{out}', 'wb').write(audio); log.append(f'sfx: {out} {len(audio)} bytes')
    else:
        log.append(f'skipped unknown type {t!r}')


if not KEY:
    sys.exit('ELEVENLABS_API_KEY secret is not available to this run')
log = []
for f in sorted(glob.glob('voice/requests/*.json')):
    jobs = json.load(open(f)); jobs = jobs if isinstance(jobs, list) else [jobs]
    for j in jobs: run(j, log)
    shutil.move(f, os.path.join(DONE, os.path.basename(f)))
open(f'{OUT}/last-run.txt', 'w').write('\n'.join(log) + '\n')
print('\n'.join(log))
