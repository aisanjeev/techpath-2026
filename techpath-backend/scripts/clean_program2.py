import json, os, sys, time, httpx

TOKEN = os.environ.get("SEED_TOKEN", "").strip()
PROGRAM_ID = 2
API_BASE = "https://api.techpath.biz/api/v1"

client = httpx.Client(base_url=API_BASE, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=60)

def run_cleanup():
    print(f"Cleaning up Program {PROGRAM_ID}...")
    r = client.get(f"/training/programs/{PROGRAM_ID}")
    if r.status_code != 200:
        print(f"ERROR: {r.status_code}")
        return
    
    modules = r.json().get("modules", [])
    for mod in modules:
        mid = mod["id"]
        print(f"Deleting module {mid} - {mod['title']}")
        mr = client.get(f"/training/modules/{mid}")
        if mr.status_code == 200:
            for asset in mr.json().get("assets", []):
                aid = asset["asset_id"]
                client.delete(f"/training/assets/{aid}")
                print(f"  Deleted asset {aid}")
        client.delete(f"/training/modules/{mid}")
    print("Cleanup complete.")

if __name__ == "__main__":
    if TOKEN:
        run_cleanup()
    else:
        print("Set SEED_TOKEN")
