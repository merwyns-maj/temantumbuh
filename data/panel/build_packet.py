"""Build an anonymised packet for the persona panel: P-codes, slide 1 image (small), slide text. No slugs, scores or numbers."""
import json, os, random, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = sys.argv[1]
backtest = [k for k in json.load(open(f'{ROOT}/data/panel/actuals_2026-11-09.json')) if not k.startswith('_')]
forward = ['w2n-demam-kapan-dokter', 'w2e-d15-screen-time', 'w3n-ngobrol', 'w3e-adhd', 'w3n-gigi-telat', 'w3e-newborn-skip', 'w3n-kaki-o',
           'w3e-mitos-2', 'w3n-ruam-popok', 'w3e-s01-jangan-nangis', 'w3n-kepala-peyang', 'w3e-kata-pertama', 'w3n-cegukan',
           'w3e-gelar-dokter-anak', 'w3n-asip-simpan', 'w3e-jawaban-sopan-2']
slugs = backtest + forward
random.Random(1109).shuffle(slugs)
SKIP = {'art', 'hero', 'motif', 'mascot', 'type', 'accent', 'art_big', 'number', 'disclaimer', 'source'}
def texts(o):
    if isinstance(o, str): yield o
    elif isinstance(o, list):
        for x in o: yield from texts(x)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in SKIP: yield from texts(v)
os.makedirs(f'{OUT}/img', exist_ok=True)
key, packet = {}, []
for i, s in enumerate(slugs, 1):
    code = f'P{i:02d}'
    key[code] = {'slug': s, 'set': 'backtest' if s in backtest else 'forward'}
    d = json.load(open(f'{ROOT}/posts/{s}.json'))
    im = Image.open(f'{ROOT}/out/{s}/slide-1.png').convert('RGB'); im.thumbnail((540, 720)); im.save(f'{OUT}/img/{code}.jpg', quality=85)
    slides = []
    for n, sl in enumerate(d['slides'], 1):
        t = ' / '.join(x for x in texts(sl) if x.strip())
        slides.append(f'Slide {n}: {t}')
    cap = d.get('caption', '').split('\n\nSumber')[0].split('\nSumber')[0]
    packet.append({'code': code, 'n_slides': len(d['slides']), 'slides': slides, 'caption': cap})
json.dump(packet, open(f'{OUT}/packet.json', 'w'), ensure_ascii=False, indent=1)
json.dump(key, open(f'{ROOT}/data/panel/key.json', 'w'), indent=1)
print(len(packet), 'posts;', sum(v['set'] == 'backtest' for v in key.values()), 'backtest')
