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

for name, p in [('term.png', term_path), ('repo.png', repo_path), ('devil.png', devil_path)]:
    if not p.exists():
        print(f"[-] Missing asset: {p}")
        sys.exit(1)

term_img = Image.open(term_path).convert('RGBA')
repo_img = Image.open(repo_path).convert('RGBA')
devil_raw = Image.open(devil_path).convert('RGBA')

W, H = 800, 800
fps = 15
total_frames = int(fps * 4.0)
frames = []

dev_w, dev_h = 360, 470
dev_scaled = devil_raw.resize((dev_w, dev_h))

term_w = 720
term_h = int(term_img.height * (term_w / term_img.width))
term_fitted = term_img.resize((term_w, term_h))

repo_w = 720
repo_h = int(repo_img.height * (repo_w / repo_img.width))
repo_fitted = repo_img.resize((repo_w, repo_h))

print("[*] Assembling cinematic movie loop from live screenshots...")

for i in range(total_frames):
    t = i / fps
    slide = Image.new('RGB', (W, H), color='#0A0F1D')
    d = ImageDraw.Draw(slide)

    if t < 1.3:
        # SCENE 1: Real Terminal Execution & Devious AI Smirk
        slide.paste(term_fitted, (40, 30), term_fitted if term_fitted.mode == 'RGBA' else None)
        
        small_dev = devil_raw.resize((210, 275))
        slide.paste(small_dev, (560, H - 340), small_dev)

        d.rectangle([0, H - 60, W, H], fill='#070B14')
        d.text((40, H - 40), '[ACT 1]: Client sends raw sk-9812... secrets in prompt context.', fill='#38BDF8')

    elif t < 2.7:
        # SCENE 2: Data Extraction into Devil Memory Cache
        pulse = 0.5 + 0.5 * math.sin((t - 1.3) * 14)
        bg = '#1C060B' if pulse > 0.5 else '#2D0A12'
        slide = Image.new('RGB', (W, H), color=bg)
        d = ImageDraw.Draw(slide)

        slide.paste(dev_scaled, (220, 180), dev_scaled)

        prog = (t - 1.3) / 1.4
        for k in range(5):
            kx = int(60 + k * 110 + prog * 150) % 700
            ky = int(120 + math.sin(k + t * 8) * 35)
            d.text((kx, ky), "sk-98127391...", fill='#EF4444')

        bc_x, bc_y = 440, 310
        lines = ["Ooh, juicy API keys!", "Saving to memory cache...", "Zero privacy!"]
        sy = bc_y - 25
        for l in lines:
            bbox = d.textbbox((0, 0), l)
            lw = bbox[2] - bbox[0]
            d.text((bc_x - lw // 2, sy), l, fill='#B91C1C')
            sy += 20

        d.rectangle([0, H - 60, W, H], fill='#20050A')
        d.text((40, H - 40), '[ACT 2]: Raw secrets trapped in shared KV-cache memory.', fill='#F87171')

    else:
        # SCENE 3: Hardware Enclave Intercept & GitHub Repo CTA
        slide = Image.new('RGB', (W, H), color='#041612')
        d = ImageDraw.Draw(slide)

        slide.paste(repo_fitted, (40, 50), repo_fitted if repo_fitted.mode == 'RGBA' else None)

        d.rounded_rectangle([40, 350, 760, 560], radius=12, fill='#022C22', outline='#10B981', width=3)
        d.text((70, 375), "[✓] SECUREKV HARDWARE ENCLAVE INTERCEPT", fill='#6EE7B7')
        d.text((70, 415), "Raw Credentials Blocked  -> Masked: <SEC_API_KEY_c2stOTgx>", fill='#FFFFFF')
        d.text((70, 455), "Host Memory Plaintext: 0 BYTES  | Attestation: VERIFIED", fill='#34D399')
        d.text((70, 495), "Deterministic Round-Trip Rehydration: SUCCESSFUL", fill='#A7F3D0')

        d.rectangle([0, H - 60, W, H], fill='#064E3B')
        d.text((150, H - 40), 'Protect Enterprise AI: Star on GitHub ⭐ (github.com/NehaAIML/SecureKV-Enclave)', fill='#FBBF24')

    frames.append(slide)

out_gif = docs / 'demo_loop.gif'
frames[0].save(str(out_gif), save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0)
print(f"[✓] Assembled cinematic demo GIF: {out_gif}")
