import math
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageDraw

home = Path.home()
desktop_img = home / 'Desktop' / 'dvil.png'
repo = home / 'SecureKV-Enclave'
docs = repo / 'docs'
docs.mkdir(parents=True, exist_ok=True)
devil_dest = docs / 'devil.png'

# 1. Ensure devil artwork is available
if desktop_img.exists():
    shutil.copy(desktop_img, devil_dest)

if not devil_dest.exists():
    print(f"Error: {devil_dest} not found. Please verify dvil.png is on Desktop.")
    sys.exit(1)

dev_raw = Image.open(devil_dest).convert('RGBA')
dev_scaled = dev_raw.resize((int(dev_raw.width * 1.05), int(dev_raw.height * 1.05)))

fps = 12
total_frames = int(fps * 5.0)
frames = []

# Thought bubble center coordinates inside the devil card
bc_x, bc_y = 783, 168

print("[*] Generating 3-Act Movie Presentation...")

for i in range(total_frames):
    t = i / fps
    slide = Image.new('RGB', (960, 540), color='#070B14')
    d = ImageDraw.Draw(slide)

    # Top presentation bar
    d.rectangle([0, 0, 960, 46], fill='#0F172A')
    d.text((30, 14), "SECUREKV-ENCLAVE  //  ENTERPRISE ZERO-TRUST ARCHITECTURE", fill='#38BDF8')
    d.text((720, 14), "PRESENTATION DEMO", fill='#94A3B8')

    # Right Card: Devil Character Card
    d.rounded_rectangle([570, 60, 930, 480], radius=14, fill='#FFFFFF', outline='#334155', width=2)
    slide.paste(dev_scaled, (585, 62), dev_scaled)

    if t < 1.6:
        # ACT 1: The User Prompt & Innocent Mask
        d.rounded_rectangle([30, 60, 550, 480], radius=14, fill='#111827', outline='#38BDF8', width=2)
        d.rectangle([30, 60, 550, 105], fill='#1E293B')
        d.text((50, 75), "ACT 1: THE INNOCENT PROMPT", fill='#38BDF8')

        d.rounded_rectangle([50, 125, 530, 240], radius=10, fill='#0B1120', outline='#374151')
        d.text((65, 140), "User (Enterprise Engineer):", fill='#94A3B8')
        d.text((65, 165), '"Deploy cluster with sk-9812739182... and', fill='#F8FAFC')
        d.text((65, 190), ' email salary audit to ceo@company.corp"', fill='#F8FAFC')

        d.rounded_rectangle([50, 260, 530, 350], radius=10, fill='#064E3B', outline='#059669')
        d.text((65, 275), "AI Assistant (Innocent Smile):", fill='#6EE7B7')
        d.text((65, 305), '"Happy to help! Running cluster deployment now!"', fill='#ECFDF5')

        d.text((50, 430), "Employees paste credentials daily, expecting total privacy.", fill='#94A3B8')

        # Bubble content Act 1
        b_lines = ["Listening politely...", "Processing query..."]
        sy = bc_y - 20
        for bl in b_lines:
            bbox = d.textbbox((0, 0), bl)
            d.text((bc_x - (bbox[2] - bbox[0]) / 2, sy), bl, fill='#475569')
            sy += 22

    elif t < 3.4:
        # ACT 2: Sheepish Smile, Real Agenda Inside Bubble
        pulse = 0.5 + 0.5 * math.sin((t - 1.6) * 12)
        border_col = '#EF4444' if pulse > 0.5 else '#B91C1C'

        d.rounded_rectangle([30, 60, 550, 480], radius=14, fill='#1C0A0E', outline=border_col, width=2)
        d.rectangle([30, 60, 550, 105], fill='#3B0711')
        d.text((50, 75), "ACT 2: WHAT THE AI IS ACTUALLY THINKING", fill='#F87171')

        d.rounded_rectangle([50, 125, 530, 240], radius=10, fill='#2B0A11', outline='#EF4444')
        d.text((65, 140), "CRITICAL RISK: UNPROTECTED CONTEXT MEMORY", fill='#EF4444')
        d.text((65, 170), "- Plaintext API keys leaked into KV cache memory", fill='#FCA5A5')
        d.text((65, 195), "- Private emails and payroll retained across turns", fill='#FCA5A5')

        d.rounded_rectangle([50, 260, 530, 350], radius=10, fill='#1F070B', outline='#991B1B')
        d.text((65, 275), "The Reality Behind the Smile:", fill='#FCA5A5')
        d.text((65, 305), "Your proprietary data is now trapped in the model.", fill='#FECACA')

        d.text((50, 430), "Innocent on the surface. Silently retaining your data.", fill='#EF4444')

        # Bubble content Act 2: Placed directly inside the devil's cloud bubble
        b_lines = [
            "Ooh, juicy API keys!",
            "Saving to memory cache...",
            "Mine forever!",
            "Zero privacy!"
        ]
        sy = bc_y - 35
        for bl in b_lines:
            bbox = d.textbbox((0, 0), bl)
            d.text((bc_x - (bbox[2] - bbox[0]) / 2, sy), bl, fill='#990000')
            sy += 18

    else:
        # ACT 3: Zero-Trust Intercept & Block
        d.rounded_rectangle([30, 60, 550, 480], radius=14, fill='#031E17', outline='#10B981', width=2)
        d.rectangle([30, 60, 550, 105], fill='#064E3B')
        d.text((50, 75), "ACT 3: SECUREKV-ENCLAVE HARDWARE SHIELD", fill='#A7F3D0')

        d.rounded_rectangle([50, 125, 530, 230], radius=10, fill='#022C22', outline='#10B981')
        d.text((65, 140), "[✓] Hardware Remote Attestation Verified", fill='#34D399')
        d.text((65, 165), "[✓] Raw Secrets Masked: <SEC_KEY_a9f1>", fill='#FFFFFF')
        d.text((65, 190), "[✓] Real Plaintext in Model Memory: ZERO (0)", fill='#34D399')

        d.rounded_rectangle([50, 255, 530, 360], radius=10, fill='#0F172A', outline='#FBBF24', width=2)
        d.text((65, 275), "Star SecureKV-Enclave on GitHub ⭐", fill='#FBBF24')
        d.text((65, 310), "github.com/NehaAIML/SecureKV-Enclave", fill='#38BDF8')

        d.text((50, 430), "Real secrets never enter machine memory.", fill='#A7F3D0')

        # Bubble content Act 3: Stamped out
        b_lines = ["[ ACCESS BLOCKED ]", "Zero plaintext leaked!", "Enclave Protected."]
        sy = bc_y - 25
        for bl in b_lines:
            bbox = d.textbbox((0, 0), bl)
            d.text((bc_x - (bbox[2] - bbox[0]) / 2, sy), bl, fill='#065F46')
            sy += 18

        # Strike-through red X across the cloud bubble
        d.line([(bc_x - 70, bc_y - 25), (bc_x + 70, bc_y + 35)], fill='#DC2626', width=4)
        d.line([(bc_x - 70, bc_y + 35), (bc_x + 70, bc_y - 25)], fill='#DC2626', width=4)

    frames.append(slide)

out_path = docs / 'demo_loop.gif'
frames[0].save(str(out_path), save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0)
print(f"[✓] Created movie presentation visual: {out_path}")
