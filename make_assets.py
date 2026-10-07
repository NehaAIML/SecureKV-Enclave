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

# 1. Copy image from Desktop
if desktop_img.exists():
    shutil.copy(desktop_img, devil_dest)

if not devil_dest.exists():
    print(f"Error: devil image not found at {devil_dest} or {desktop_img}")
    sys.exit(1)

# 2. Write LinkedIn Post Text
post_content = """When I think of running business AI,
the system remembers everything you told it.

That sounds like a helpful feature—until you realize what it actually means.

Every API key, customer record, and confidential strategy doc pasted into a prompt doesn't just answer today’s question. It lingers inside shared memory, GPU caches, and context logs. The chatbot replies with a polite, innocent smile—while behind the scenes, your private credentials are quietly trapped in the machine.

True enterprise AI shouldn't need to keep your raw secrets to be smart.

To solve this, I built SecureKV-Enclave—an ultra-low latency (<0.15ms) security sidecar that establishes a verified hardware trust boundary before prompt execution:

1. Hides real secrets before the AI sees them: Replaces raw credentials and sensitive identifiers with salted dummy tokens before execution, then deterministically restores them only when the answer reaches the client.
2. Trims conversational baggage: Intercepts multi-turn history, pruning redundant context to recover 30% to 50% on token compute costs without semantic loss.
3. Verifies the hardware: Validates isolated Confidential Computing TEE enclaves before data ever moves.

Watch the 4-second clip below: raw credentials go in, the AI only ever sees surrogate tokens, and the real secret never enters model memory.

Star the repository on GitHub:
https://github.com/NehaAIML/SecureKV-Enclave

#ConfidentialComputing #ZeroTrust #LLMOps #MachineLearning #EnterpriseAI #InformationSecurity #CloudInfrastructure #AIArchitecture
"""

(docs / 'linkedin_post.txt').write_text(post_content)
print("[*] Saved LinkedIn post to: docs/linkedin_post.txt")

# 3. Load Devil Artwork & Render Animation
raw_devil = Image.open(devil_dest).convert('RGBA')
devil_resized = raw_devil.resize((320, 400))

canvas_w, canvas_h = 600, 600
fps = 15
total_frames = 60
frames = []

print("[*] Rendering 60 frames (4.0 seconds)...")

for idx in range(total_frames):
    time_sec = idx / fps
    canvas = Image.new('RGB', (canvas_w, canvas_h), color='#0B1120')
    draw = ImageDraw.Draw(canvas)

    # Top boundary header
    draw.rectangle([0, 0, canvas_w, 40], fill='#0F172A')
    draw.text((20, 12), 'SecureKV-Enclave // Zero-Trust Boundary', fill='#38BDF8')

    # Paste Devil image
    canvas.paste(devil_resized, (140, 190), devil_resized)

    if time_sec < 1.3:
        # Phase 1: User prompt & innocent AI reply
        draw.rounded_rectangle([30, 50, 570, 140], radius=8, fill='#1E293B', outline='#38BDF8', width=2)
        draw.text((45, 62), 'USER (Typing confidential request):', fill='#94A3B8')
        draw.text((45, 85), 'Deploy cluster using sk-9812739182... notify payroll@corp.com', fill='#F8FAFC')
        draw.text((45, 110), 'AI: "Of course. Happy to help you with that right away."', fill='#38BDF8')

    elif time_sec < 2.7:
        # Phase 2: Devil Thought Bubble
        pulse = 0.5 + 0.5 * math.sin((time_sec - 1.3) * 12)
        border_col = '#EF4444' if pulse > 0.5 else '#DC2626'
        draw.rounded_rectangle([180, 50, 540, 160], radius=15, fill='#25080E', outline=border_col, width=2)
        draw.text((200, 62), '[ DEVIL AGENDA ]', fill='#EF4444')
        draw.text((200, 85), '"Juicy API keys and internal payroll..."', fill='#FCA5A5')
        draw.text((200, 107), '"Storing in memory cache forever."', fill='#FCA5A5')
        draw.text((200, 130), '"Zero privacy. All mine now."', fill='#F87171')

    else:
        # Phase 3: SecureKV Enclave intercept & GitHub star CTA
        draw.rounded_rectangle([30, 50, 570, 150], radius=8, fill='#064E3B', outline='#10B981', width=3)
        draw.text((45, 62), '[*] SECUREKV-ENCLAVE INTERCEPT', fill='#A7F3D0')
        draw.text((45, 87), 'Sanitized: <SEC_KEY_a9f1> | Raw Secrets Stored: 0', fill='#FFFFFF')
        draw.text((45, 112), 'Hardware enclave locked. Zero plaintext leaked to memory.', fill='#34D399')

        draw.rounded_rectangle([90, 530, 510, 580], radius=8, fill='#1E293B', outline='#FBBF24', width=2)
        draw.text((135, 543), 'Keep your AI honest: Star on GitHub', fill='#FBBF24')
        draw.text((150, 563), 'github.com/NehaAIML/SecureKV-Enclave', fill='#94A3B8')

    frames.append(canvas)

out_path = docs / 'demo_loop.gif'
frames[0].save(str(out_path), save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0)
print(f"[✓] Created: {out_path}")
