import sys, math, subprocess
from pathlib import Path

root = Path.home() / 'SecureKV-Enclave'
docs = root / 'docs'
docs.mkdir(parents=True, exist_ok=True)

# 1. Generate LinkedIn Announcement Post
post_text = """When I think of running business AI,
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
post_file = docs / 'linkedin_post.txt'
post_file.write_text(post_text)
print(f"[✓] Created post text: {post_file}")

# 2. Ensure Dependencies for Animated GIF
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation
    import PIL
except ImportError:
    print("[*] Installing required visual libraries (matplotlib, pillow)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "matplotlib", "pillow"], check=True)
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation

# 3. Render 4-Second Animated Visual
fps = 20
duration = 4.0
total_frames = int(fps * duration)

fig, ax = plt.subplots(figsize=(7, 7), facecolor='#0B1120')

def draw_frame(frame_num):
    ax.clear()
    ax.set_facecolor('#0B1120')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    t = frame_num / fps

    # PHASE 1: Innocent AI (0.0s - 1.3s)
    if t < 1.3:
        box = patches.FancyBboxPatch((10, 72), 80, 16, boxstyle="round,pad=1.5", fc='#1E293B', ec='#38BDF8', lw=1.5)
        ax.add_patch(box)
        ax.text(50, 83, 'USER PROMPT:', color='#94A3B8', fontsize=10, ha='center', weight='bold')
        ax.text(50, 76, 'Deploy cluster using sk-9812739182... notify alex@corp.com', color='#F8FAFC', fontsize=9, ha='center', family='monospace')

        # Smiling Assistant Avatar
        circle = patches.Circle((50, 44), 15, fc='#38BDF8', ec='#0284C7', lw=2)
        ax.add_patch(circle)
        ax.plot([44, 46], [47, 47], color='#0B1120', lw=3)
        ax.plot([54, 56], [47, 47], color='#0B1120', lw=3)
        smile = patches.Arc((50, 42), 12, 7, angle=0, theta1=200, theta2=340, color='#0B1120', lw=2.5)
        ax.add_patch(smile)

        ax.text(50, 18, '"Happy to help! Processing request..."', color='#38BDF8', fontsize=11.5, ha='center', weight='bold')
        ax.text(50, 10, '(Innocent Assistant)', color='#64748B', fontsize=10, ha='center')

    # PHASE 2: Evil AI / Trap (1.3s - 2.6s)
    elif t < 2.6:
        pulse = 0.5 + 0.5 * math.sin((t - 1.3) * 12)
        ax.set_facecolor('#20080D' if pulse > 0.5 else '#350B14')

        # Devil AI Face
        head = patches.Circle((50, 50), 16, fc='#DC2626', ec='#991B1B', lw=3)
        ax.add_patch(head)
        # Horns
        horn_l = patches.Polygon([[38, 60], [33, 72], [44, 63]], fc='#991B1B')
        horn_r = patches.Polygon([[62, 60], [67, 72], [56, 63]], fc='#991B1B')
        ax.add_patch(horn_l)
        ax.add_patch(horn_r)
        # Slanted eyes & grin
        ax.plot([42, 47], [54, 51], color='#FEE2E2', lw=3)
        ax.plot([53, 58], [51, 54], color='#FEE2E2', lw=3)
        grin = patches.Arc((50, 45), 14, 8, angle=0, theta1=190, theta2=350, color='#FEE2E2', lw=3)
        ax.add_patch(grin)

        ax.text(50, 24, 'STORING SECRETS IN MEMORY FOREVER...', color='#EF4444', fontsize=12, ha='center', weight='heavy', family='monospace')
        ax.text(50, 14, 'Harvesting: sk-9812739182... -> Cache Logs', color='#FCA5A5', fontsize=9.5, ha='center', family='monospace')

    # PHASE 3: SecureKV-Enclave Intercept & GitHub Star CTA (2.6s - 4.0s)
    else:
        shield_box = patches.FancyBboxPatch((15, 68), 70, 18, boxstyle="round,pad=1.5", fc='#0F172A', ec='#10B981', lw=2)
        ax.add_patch(shield_box)
        ax.text(50, 79, '[HARDWARE ENCLAVE VERIFIED]', color='#10B981', fontsize=11, ha='center', weight='bold')
        ax.text(50, 72, 'Masked: <SEC_KEY_a9f1> | Real Secrets: 0', color='#38BDF8', fontsize=9, ha='center', family='monospace')

        # Shield badge
        shield = patches.RegularPolygon((50, 46), 6, radius=12, fc='#047857', ec='#10B981', lw=2)
        ax.add_patch(shield)
        ax.text(50, 44, 'KV', color='#FFFFFF', fontsize=12, ha='center', weight='heavy')

        ax.text(50, 24, 'REAL SECRETS NEVER ENTER MODEL MEMORY', color='#F8FAFC', fontsize=10.5, ha='center', weight='bold')
        ax.text(50, 15, 'Star the Repo on GitHub', color='#FBBF24', fontsize=13, ha='center', weight='heavy')
        ax.text(50, 8, 'github.com/NehaAIML/SecureKV-Enclave', color='#94A3B8', fontsize=8.5, ha='center', family='monospace')

print("[*] Generating 4-second animation frames...")
anim = FuncAnimation(fig, draw_frame, frames=total_frames, interval=1000/fps)
out_gif = docs / 'demo_loop.gif'

anim.save(str(out_gif), writer='pillow', fps=fps)
print(f"[✓] Created animated loop: {out_gif}")
