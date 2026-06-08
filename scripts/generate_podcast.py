#!/usr/bin/env python3
"""Generate Post AI Sessions Ep.1 audio using ElevenLabs."""

import os, re, time, json, subprocess, sys

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not API_KEY:
    sys.exit("ELEVENLABS_API_KEY not set — export it before running (see .env.example).")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.environ.get(
    "PODCAST_SCRIPT_PATH",
    os.path.join(REPO_ROOT, "content", "2026-06-11-podcast-ep1-lenny-style.md"),
)
OUTPUT_DIR = os.path.join(REPO_ROOT, "podcast", "ep1")
FINAL_OUTPUT = os.path.join(OUTPUT_DIR, "ep1-final.mp3")

# Voice assignments
VOICES = {
    "Marco": "CwhRBWXzGAHq8TQ4Fs17",  # Roger - Laid-Back, Casual
    "Lena": "Xb7hH8MSUJpSbSDYk0k2",   # Alice - Clear, Engaging Educator
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_script(path):
    """Parse the script into a list of (speaker, text) tuples."""
    with open(path) as f:
        content = f.read()
    
    lines = []
    current_speaker = None
    current_text = []
    
    for line in content.split('\n'):
        # Match speaker lines
        m = re.match(r'\*\*(Marco|Lena):?\*\*\s*(.+)', line)
        if m:
            if current_speaker and current_text:
                lines.append((current_speaker, ' '.join(current_text)))
            current_speaker = m.group(1)
            current_text = [m.group(2)]
        elif current_speaker and line.strip() and not line.strip().startswith('[') and not line.strip().startswith('#'):
            current_text.append(line.strip())
        elif line.strip().startswith('[NOTA') or line.strip().startswith('[PAUSA') or line.strip().startswith('[RINDO'):
            if current_text:
                current_text.append(f'\n[{line.strip()}]')
    
    if current_speaker and current_text:
        lines.append((current_speaker, ' '.join(current_text)))
    
    return lines

def generate_speech(text, voice_id, output_path, speaker_name):
    """Generate speech using ElevenLabs API."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
        }
    }
    
    import urllib.request
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(output_path, 'wb') as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"  ERROR [{speaker_name}]: {e}")
        return False

def main():
    lines = parse_script(SCRIPT_PATH)
    print(f"Parsed {len(lines)} dialogue segments")
    
    audio_files = []
    for i, (speaker, text) in enumerate(lines):
        # Skip short lines and production notes
        if len(text.strip()) < 5:
            continue
        if text.strip().startswith('[') and text.strip().endswith(']'):
            continue
            
        out_file = os.path.join(OUTPUT_DIR, f"seg_{i:04d}_{speaker}.mp3")
        
        if os.path.exists(out_file):
            print(f"  [{i}/{len(lines)}] {speaker}: cached")
        else:
            print(f"  [{i}/{len(lines)}] {speaker}: {text[:80]}...")
            ok = generate_speech(text, VOICES[speaker], out_file, speaker)
            if not ok:
                continue
            time.sleep(0.5)  # Rate limit
        
        audio_files.append(out_file)
    
    # Concatenate using ffmpeg
    concat_file = os.path.join(OUTPUT_DIR, "concat.txt")
    with open(concat_file, 'w') as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")
    
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file, "-c", "copy", FINAL_OUTPUT
    ], check=True)
    
    # Add silence between segments for better pacing
    print(f"\nDone! Final audio: {FINAL_OUTPUT}")
    print(f"Duration: {len(audio_files)} segments")

if __name__ == "__main__":
    main()
