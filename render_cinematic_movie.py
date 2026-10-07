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

if desktop_img.exists():
    shutil.copy(desktop_img, devil_dest)

if not devil_dest.exists():
    print(f"Error: {devil_dest} not found. Please place dvil.png on your Desktop.")
    sys.exit(1)

devil_raw = Image.open(devil_dest).convert('RGBA')

# 1080x1080 Square Format (Optimized for LinkedIn mobile & desktop feed)
W, H = 800, 800
fps = 16
total_duration = 4.0
total_frames = int(fps * total_duration)
frames = []

print("[*] Rendering 4.0-second cinematic animation loop...")

for idx in range(total_frames):
    t = idx / fps
    frame = Image.new('RGB', (W, H), color='#070B14')
    draw = ImageDraw.Draw(frame)

    # -------------------------------------------------------------
    # CINEMATIC ACT 1 (0.0s - 1.3s): The Innocent AI Assistant
    # -------------------------------------------------------------
    if t < 1.3:
        # Subtle technological grid background
        for y_line in range(0, H, 50):
            draw.line([(0, y_line), (W, y_line)], fill='#0F172A', width=1)
        for x_line in range(0, W, 50):
            draw.line([(x_line, 0), (x_line, H)], fill='#0F172A', width=1)

        # Devil character centered
        devil_w, devil_h = 360, 470
        devil_scaled = devil_raw.resize((devil_w, devil_h))
        frame.paste(devil_scaled, (220, 260), devil_scaled)

        # Thought bubble text (playing dumb / innocent)
        draw.text((430, 310), "Thinking...", fill='#64748B')
        draw.text((410, 335), "Processing your task!", fill='#38BDF8')

        # Floating holographic prompt bubble from user
        draw.rounded_rectangle([60, 60, 740, 190], radius=16, fill='#0B132B', outline='#0284C7', width=2)
        draw.text((90, 80), "USER PROMPT (CONFIDENTIAL):", fill='#38BDF8')
        draw.text((90, 115), '"Deploy cluster using sk-9812739182... and send payroll to ceo@corp.com"', fill='#F8FAFC')
        draw.text((90, 150), 'AI: "Always here to help! One moment while I run this..."', fill='#34D399')

    # -------------------------------------------------------------
    # CINEMATIC ACT 2 (1.3s - 2.7s): The Sneaky Memory Heist
    # -------------------------------------------------------------
    elif t < 2.7:
        progress = (t - 1.3) / 1.4

        # Red emergency room pulse
        pulse = 0.5 + 0.5 * math.sin((t - 1.3) * 14)
        bg_col = '#1C060B' if pulse > 0.5 else '#2E0811'
        frame = Image.new('RGB', (W, H), color=bg_col)
        draw = ImageDraw.Draw(frame)

        # Cinematic Camera Zoom into Devil's Face & Thought Bubble
        zoom_w = int(360 * (1.0 + 0.12 * progress))
        zoom_h = int(470 * (1.0 + 0.12 * progress))
        devil_zoomed = devil_raw.resize((zoom_w, zoom_h))
        frame.paste(devil_zoomed, (200, 230), devil_zoomed)

        # Particle streams of data flying into the devil's thought bubble
        for p in range(8):
            px = int(80 + (p * 70) + (progress * 180) % 250)
            py = int(120 + math.sin(p + t * 8) * 30 + (progress * 150))
            draw.text((px, py), "sk-981273...", fill='#EF4444')
            draw.text((px - 30, py + 25), "payroll.xlsx", fill='#F87171')

        # Cinematic Thought Bubble Text (Pulsing bold devil intent)
        draw.text((400, 275), "MINE FOREVER!", fill='#DC2626')
        draw.text((375, 305), "Storing secrets in memory...", fill='#990000')
        draw.text((390, 335), "Zero Privacy! All mine!", fill='#7F1D1D')

        # Warning banner on top
        draw.rectangle([0, 0, W, 50], fill='#7F1D1D')
        draw.text((120, 16), "ALERT: SENSITIVE CONTEXT LEAKING INTO PERSISTENT MEMORY", fill='#FEE2E2')

    # -------------------------------------------------------------
    # CINEMATIC ACT 3 (2.7s - 4.0s): SecureKV-Enclave Intercept
    # -------------------------------------------------------------
    else:
        # Zero-Trust cyber atmosphere
        frame = Image.new('RGB', (W, H), color='#041712')
        draw = ImageDraw.Draw(frame)

        devil_w, devil_h = 360, 470
        devil_scaled = devil_raw.resize((devil_w, devil_h))
        frame.paste(devil_scaled, (220, 260), devil_scaled)

        # Giant Glowing Hardware Enclave Shield barrier
        draw.line([(0, 220), (W, 220)], fill='#10B981', width=6)
        draw.line([(0, 224), (W, 224)], fill='#34D399', width=2)

        # Denied stamp over devil's bubble
        draw.text((390, 310), "[ ACCESS DENIED ]", fill='#DC2626')
        draw.line([(360, 280), (600, 370)], fill='#EF4444', width=5)
        draw.line([(360, 370), (600, 280)], fill='#EF4444', width=5)

        # Enclave verification HUD
        draw.rounded_rectangle([70, 40, 730, 180], radius=16, fill='#022C22', outline='#10B981', width=3)
        draw.text((100, 60), "[✓] SECUREKV HARDWARE ENCLAVE VERIFIED", fill='#6EE7B7')
        draw.text((100, 95), "Plaintext Secret Blocked -> Injected: <SEC_KEY_a9f1>", fill='#FFFFFF')
        draw.text((100, 130), "Raw Plaintext Stored in Model Memory: 0 BYTES", fill='#34D399')

        # GitHub CTA Banner
        draw.rounded_rectangle([120, 710, 680, 775], radius=12, fill='#0F172A', outline='#FBBF24', width=2)
        draw.text((210, 725), "Protect your AI context: Star on GitHub ⭐", fill='#FBBF24')
        draw.text((230, 750), "github.com/NehaAIML/SecureKV-Enclave", fill='#38BDF8')

    frames.append(frame)

out_gif = docs / 'demo_loop.gif'
frames[0].save(str(out_gif), save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0)
print(f"[✓] Cinematic movie loop successfully saved: {out_gif}")
