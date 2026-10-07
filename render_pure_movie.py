import math
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageDraw

home = Path.home()
desktop = home / 'Desktop'
repo = home / 'SecureKV-Enclave'
docs = repo / 'docs'
docs.mkdir(parents=True, exist_ok=True)

term_path = desktop / 'term.png'
repo_path = desktop / 'repo.png'
devil_path = docs / 'devil.png'

if not devil_path.exists() and (desktop / 'dvil.png').exists():
    shutil.copy(desktop / 'dvil.png', devil_path)

for p in [term_path, repo_path, devil_path]:
    if not p.exists():
        print(f"[-] Missing asset: {p}")
        sys.exit(1)

# 1. Cleanly Key-Out White Background from Devil (Zero white sticker box)
raw_devil = Image.open(devil_path).convert('RGBA')
datas = raw_devil.getdata()
clean_devil_data = []
for item in datas:
    # If pixel is near-white outside the drawing lines, make it 100% transparent
    if item[0] > 242 and item[1] > 242 and item[2] > 242:
        clean_devil_data.append((255, 255, 255, 0))
    else:
        clean_devil_data.append(item)
raw_devil.putdata(clean_devil_data)

term_raw = Image.open(term_path).convert('RGBA')
repo_raw = Image.open(repo_path).convert('RGBA')

# 16:9 Cinema Widescreen Canvas
W, H = 960, 540
fps = 25              # Exactly 0.04 sec per frame (true cinema rate)
frame_duration = 40   # 40 milliseconds = 0.04 seconds
total_frames = 110    # ~4.4 second punchy movie loop
frames = []

print("[*] Rendering 25 FPS cinema short (0.04s per frame, transparent devil, camera pans)...")

for idx in range(total_frames):
    t = idx / fps
    scene = Image.new('RGBA', (W, H), color=(10, 15, 26, 255))
    d = ImageDraw.Draw(scene)

    # -------------------------------------------------------------
    # SCENE 1 (0.0s - 1.8s): CAMERA PAN ACROSS REAL TERMINAL IN ACTION
    # -------------------------------------------------------------
    if t < 1.8:
        prog = t / 1.8
        # Full-bleed zoom of the real terminal screenshot panning upward
        tw = int(W * 1.08)
        th = int(term_raw.height * (tw / term_raw.width))
        term_pan = term_raw.resize((tw, th))
        
        # Smooth camera scroll
        pan_y = int(-40 - prog * (th - H - 30)) if th > H else 0
        scene.paste(term_pan, (-20, pan_y), term_pan)

        # Cinema letterbox bars top & bottom
        d.rectangle([0, 0, W, 45], fill=(7, 11, 20, 240))
        d.rectangle([0, H - 55, W, H], fill=(7, 11, 20, 240))
        d.text((30, 14), "LIVE RUNTIME INTERCEPT // SECUREKV-ENCLAVE", fill='#38BDF8')

        # Red scanning laser sweeping over sensitive keys
        laser_y = int(60 + (t * 260) % (H - 120))
        d.line([(0, laser_y), (W, laser_y)], fill=(239, 68, 68, 220), width=3)

        # The Devil walks into the scene from the right edge
        dev_w, dev_h = 290, 380
        dev_scaled = raw_devil.resize((dev_w, dev_h))
        dev_x = int(W - 320 + math.sin(t * 12) * 10)
        dev_y = int(H - 420 + math.sin(t * 18) * 8)
        scene.paste(dev_scaled, (dev_x, dev_y), dev_scaled)

        # Devil's sneaky internal dialog inside his cloud bubble
        d.text((dev_x + 130, dev_y + 60), "Look at those", fill='#B91C1C')
        d.text((dev_x + 130, dev_y + 80), "juicy keys...", fill='#B91C1C')

        d.text((30, H - 38), 'AI ASSISTANT: "Of course! Let me verify credentials and deploy your cluster~"', fill='#F8FAFC')

    # -------------------------------------------------------------
    # SCENE 2 (1.8s - 3.2s): THE RED ALERT SECRET EXTRACTION (THE HEIST)
    # -------------------------------------------------------------
    elif t < 3.2:
        rel_t = t - 1.8
        prog = rel_t / 1.4

        # Emergency crimson cinema lighting
        pulse = 0.5 + 0.5 * math.sin(rel_t * 16)
        r_val = int(25 + pulse * 35)
        scene = Image.new('RGBA', (W, H), color=(r_val, 8, 14, 255))
        d = ImageDraw.Draw(scene)

        # Camera Shake Effect
        shake_x = int(math.sin(rel_t * 30) * 6)
        shake_y = int(math.cos(rel_t * 30) * 4)

        # Tractor beam sucking credentials across the screen into devil's bubble
        for k in range(9):
            kx = int((W * 0.15) + (k * 80) + (prog * 300)) % int(W * 0.65)
            ky = int(180 + math.sin(k + rel_t * 10) * 60)
            d.text((kx + shake_x, ky + shake_y), "sk-9812739182...", fill=(239, 68, 68, 255))
            d.text((kx - 30 + shake_x, ky + 25 + shake_y), "admin@corp.internal", fill=(248, 113, 113, 220))

        # Giant dancing devil in the right half of the frame
        dev_w, dev_h = 360, 470
        dev_scaled = raw_devil.resize((dev_w, dev_h))
        dev_x = int(W * 0.55 + shake_x)
        dev_y = int(H - 490 + math.sin(rel_t * 18) * 12 + shake_y)
        scene.paste(dev_scaled, (dev_x, dev_y), dev_scaled)

        # Nasty dialog filling the cloud bubble
        d.text((dev_x + 160, dev_y + 70), "ALL MINE NOW!", fill='#990000')
        d.text((dev_x + 145, dev_y + 92), "Trapped in memory!", fill='#990000')
        d.text((dev_x + 155, dev_y + 114), "Zero privacy!", fill='#B91C1C')

        # Cinema letterbox bars
        d.rectangle([0, 0, W, 45], fill=(80, 10, 18, 240))
        d.rectangle([0, H - 55, W, H], fill=(80, 10, 18, 240))
        d.text((30, 14), "VULNERABILITY: UNENCRYPTED CREDENTIALS SUCKED INTO MODEL KV-CACHE", fill='#FEE2E2')
        d.text((30, H - 38), 'AI MEMORY: "Session looks private. I quietly retain your secrets across GPU memory."', fill='#FCA5A5')

    # -------------------------------------------------------------
    # SCENE 3 (3.2s - 4.4s): ENCLAVE SHIELD SLAM & GITHUB REPO LOCKDOWN
    # -------------------------------------------------------------
    else:
        rel_t = t - 3.2
        prog = rel_t / 1.2

        # Full-bleed GitHub repo background
        rw = int(W * 1.05)
        rh = int(repo_raw.height * (rw / repo_raw.width))
        repo_pan = repo_raw.resize((rw, rh))
        scene.paste(repo_pan, (-10, -10), repo_pan)

        # Emerald matrix security grid slamming across screen
        shield_alpha = min(220, int(prog * 260))
        overlay = Image.new('RGBA', (W, H), (2, 44, 34, shield_alpha))
        scene = Image.alpha_composite(scene, overlay)
        d = ImageDraw.Draw(scene)

        # Giant glowing hardware enclave shield banner
        d.rounded_rectangle([50, 70, W - 50, 220], radius=16, fill=(4, 30, 23, 230), outline='#10B981', width=3)
        d.text((80, 95), "[✓] SECUREKV-ENCLAVE INTERCEPT VERIFIED", fill='#6EE7B7')
        d.text((80, 130), "Hardware TEE Attestation: PASSED  |  Host Memory Secrets: 0 BYTES", fill='#FFFFFF')
        d.text((80, 165), "Raw secret neutralized -> Injected surrogate: <SEC_API_KEY_c2stOTgx>", fill='#34D399')

        # Frustrated devil pushed to bottom right corner
        dev_w, dev_h = 240, 310
        dev_scaled = raw_devil.resize((dev_w, dev_h))
        dev_x = W - 260
        dev_y = H - 330 + int(math.sin(rel_t * 16) * 6)
        scene.paste(dev_scaled, (dev_x, dev_y), dev_scaled)

        # Giant red X stamping the devil's bubble
        d.text((dev_x + 95, dev_y + 45), "BLOCKED!", fill='#DC2626')
        d.line([(dev_x + 80, dev_y + 35), (dev_x + 190, dev_y + 85)], fill='#EF4444', width=4)
        d.line([(dev_x + 80, dev_y + 85), (dev_x + 190, dev_y + 35)], fill='#EF4444', width=4)

        # Cinema letterbox & Star CTA
        d.rectangle([0, 0, W, 45], fill=(6, 78, 59, 240))
        d.rectangle([0, H - 55, W, H], fill=(6, 78, 59, 240))
        d.text((30, 14), "SECUREKV-ENCLAVE // HARDWARE-ATTESTED ZERO-TRUST CONTEXT BOUNDARY", fill='#A7F3D0')
        d.text((160, H - 38), 'Keep your AI honest: Star on GitHub ⭐ github.com/NehaAIML/SecureKV-Enclave', fill='#FBBF24')

    frames.append(scene.convert('RGB'))

out_gif = docs / 'demo_loop.gif'
# Save with 40ms duration (0.04 seconds per frame = 25 FPS)
frames[0].save(str(out_gif), save_all=True, append_images=frames[1:], duration=frame_duration, loop=0)
print(f"[✓] Movie rendered at 25 FPS (0.04s/frame): {out_gif}")
