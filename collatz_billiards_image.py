import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math

# ==========================================
# Shiftless Billiards Still Image Overview
# Author: Hiroshi Harada
# Date: March 27, 2026
# Licensed under MIT and CC BY 4.0
# ==========================================

def collatz_billiards_image(seed, max_steps=1000, filename_prefix="collatz_shiftless_billiards"):
    # 1. Physical Computation (Trajectory)
    n = seed
    log3 = math.log(3)
    log2_base3 = math.log(2) / log3

    steps = [0]
    heights = [math.log(n, 3)]
    h0 = heights[0]

    # Safety threshold for n to avoid math.log overflow
    N_MAX = 1e300

    # Calculate trajectory until jackpot or safety limit
    while not (n > 0 and (n & (n - 1) == 0)):
        lsb = n & -n
        n = 3 * n + lsb

        # Safety: avoid infinite growth
        if n > N_MAX:
            print("⚠ n exploded beyond safe range. Stopping.")
            break

        steps.append(len(steps))
        heights.append(math.log(n, 3))

        if len(steps) > max_steps:
            print("⚠ Target too far! Safety break triggered.")
            break

    total_steps = steps[-1]
    is_jackpot = (n > 0 and (n & (n - 1) == 0))
    final_m = n.bit_length() - 1 if is_jackpot else None

    # 2. Billiard Table Setup (Still Image)
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#001100')
    ax.set_facecolor('#1b5e20')  # Billiard Green
    ax.set_aspect('equal')

    p_radius = 0.12  # Ball & Pocket radius

    # --- Margins & Ranges ---
    overview_margin = 2.0
    overview_x_min = -overview_margin
    overview_x_max = max(total_steps + overview_margin, 10.0 + overview_margin)
    overview_y_min = h0 - overview_margin
    overview_y_max = max(max(heights) + overview_margin, h0 + 10.0 + overview_margin)

    # --- Jackpot Rails (2^M Lines) ---
    min_M = math.floor(overview_y_min / log2_base3)
    max_M = math.ceil(overview_y_max / log2_base3)
    max_pocket_step = math.ceil(overview_x_max)

    print(f"Generating Jackpot Rails for M={min_M} to {max_M}...")

    for M in range(min_M, max_M + 1):
        y_p = M * log2_base3
        ax.axhline(y_p, color='white', lw=0.5, alpha=0.25, zorder=1)

        # Pockets
        for s in range(0, max_pocket_step + 1):
            ax.add_patch(Circle((s, y_p), p_radius, color='black', alpha=0.6, zorder=2))

    # Inertia Line (3x Rule)
    base_line = [h0 + k for k in range(total_steps + 1)]
    ax.plot(range(total_steps + 1), base_line,
            color='white', lw=1.0, ls=':', alpha=0.7, zorder=8, label='Inertia (3x Rule)')

    # Final Trajectory
    ax.plot(steps, heights, color='#eeff41', lw=1.0, alpha=0.9,
            zorder=10, label=f'Orbit of {seed}')

    # Final Ball Position
    curr_s = steps[-1]
    curr_h = heights[-1]

    if is_jackpot:
        ball = Circle((curr_s, curr_h), p_radius, color='#ff1744',
                      ec='black', lw=0.5, zorder=15)
        ax.scatter(curr_s, curr_h, color='#ff1744', s=500, marker='*',
                   zorder=20, label=f'Jackpot: $2^{{{final_m}}}$')
    else:
        ball = Circle((curr_s, curr_h), p_radius, color='white',
                      ec='black', lw=0.5, zorder=15)

    ax.add_patch(ball)

    # --- Labels & Tuning ---
    ax.set_xlim(overview_x_min, overview_x_max)
    ax.set_ylim(overview_y_min, overview_y_max)

    ax.set_title(f"Shiftless Billiards: Still Overview - Seed {seed}",
                 color='white', fontsize=16)
    ax.set_xlabel("Steps (k)", color='white')
    ax.set_ylabel("3-adic Altitude ($log_3 n$)", color='white')

    ax.tick_params(colors='white')
    ax.grid(color='white', alpha=0.05)

    ax.legend(facecolor='#003300', labelcolor='white',
              loc='upper left', fontsize='small', edgecolor='#333333')

    # 3. Save as Still Image
    output_filename = f"{filename_prefix}_still_image_seed_{seed}.png"
    print(f"✨ Saving high-resolution still image as {output_filename}...")
    fig.savefig(output_filename, dpi=300, bbox_inches='tight')

    return fig


# --- RUN ---
final_figure = collatz_billiards_image(27)
