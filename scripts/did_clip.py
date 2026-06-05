#!/usr/bin/env python3
"""D-ID clip tools."""
import urllib.request, json, sys, os

CONFIG_FILE = os.pa...strip()

def check_talk(talk_id):
    with open(CONFIG_FILE) as f:
        token = f.read().strip()
    req = urllib.request.Request(
        f"https://api.d-id.com/talks/{talk_id}",
        headers={"Authorization": f"Basic {token}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def create_talk(text, voice="en-US-DavisNeural"):
    with open(CONFIG_FILE) as f:
        token = f.read().strip()
    data = {
        "script": {"type": "text", "input": text, "provider": {"type": "microsoft", "voice_id": voice}},
        "config": {"fluent": True, "pad_audio": 0.5, "result_format": "mp4"}
    }
    req = urllib.request.Request(
        "https://api.d-id.com/talks",
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Basic {token}", "Content-Type": "application/json", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "check":
        tid = sys.argv[2]
        r = check_talk(tid)
        print(f"status: {r.get('status')}")
        if r.get('status') == 'done':
            print(f"video: {r.get('result_url')}")
            print(f"duration: {r.get('duration')}s")
    elif cmd == "create":
        text = sys.argv[2]
        voice = sys.argv[3] if len(sys.argv) > 3 else "en-US-DavisNeural"
        r = create_talk(text, voice)
        print(f"id: {r.get('id')}")
        print(f"status: {r.get('status')}")
    else:
        print("Usage: python did_clip.py check <talk_id>")
        print("       python did_clip.py create <text> [voice_id]")
