"""Upload rendered slides straight to Tebar (no GitHub). Usage: TB=<upload ticket from Tebar create_upload_link> python tools/upload_tebar.py out.json
Edit `slots` (slug, date) for the week. Reads JPGs from ../temantumbuh-media/posts/<date>-<slug>/. Never commit the ticket."""
import json, subprocess, glob, re, time, sys, os
T = os.environ['TB']
OUT = sys.argv[1] if len(sys.argv) > 1 else 'media_ids.json'
done = json.load(open(OUT)) if os.path.exists(OUT) else {}
slots = [('w4s-wake-window','2026-11-16'),('w4l-overstimulasi','2026-11-16'),('w4l-asi-naik','2026-11-17'),('w4s-susu-uht','2026-11-17'),('w4s-asip-ml','2026-11-18'),('w4l-kakak-adik','2026-11-18'),('w4l-mastitis','2026-11-19'),('w4s-kolik','2026-11-19'),('w4s-jam-tidur','2026-11-20'),('w4l-ayah-main','2026-11-20'),('w4l-finger-food','2026-11-21'),('w4s-gula','2026-11-21'),('w4s-growth-spurt','2026-11-22'),('w4l-s02-tantrum-minimarket','2026-11-22')]
for slug, date in slots:
    files = sorted(glob.glob(f'/home/claude/temantumbuh-media/posts/{date}-{slug}/slide-*.jpg'), key=lambda f: int(re.search(r'slide-(\d+)', f).group(1)))
    for f in files:
        n = re.search(r'slide-(\d+)', f).group(1)
        if done.get(slug, {}).get(n): continue
        for attempt in range(3):
            r = subprocess.run(['curl','-sS','-X','POST',f'https://api.tebar.app/media-upload/file?name={slug}-slide-{n}.jpg','-H',f'X-Upload-Ticket: {T}','-H','Content-Type: application/octet-stream','--data-binary',f'@{f}','-w','\n%{http_code}'],capture_output=True,text=True)
            body, _, code = r.stdout.rpartition('\n')
            if code in ('200','201'):
                done.setdefault(slug, {})[n] = json.loads(body)['id']; break
            print('retry', slug, n, code, body[:100]); time.sleep(30 if code == '429' else 5)
        json.dump(done, open(OUT,'w'), indent=1)
    print(slug, len(done.get(slug, {})), '/', len(files)); sys.stdout.flush()
