import os, httpx

token = os.environ.get('SEED_TOKEN')
r = httpx.get('https://api.techpath.biz/api/v1/training/programs', headers={'Authorization': f'Bearer {token}'})
if r.status_code == 200:
    for p in r.json():
        print(f"ID: {p['id']}, Title: {p['title']}")
else:
    print(r.status_code, r.text)
