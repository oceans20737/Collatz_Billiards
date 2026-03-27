import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import math
from tqdm import tqdm
import shutil

# ==========================================
# Shiftless Billiards Animation Exporter (MP4 & GIF)
# Author: Hiroshi Harada
# Date: March 27, 2026
# Licensed under MIT and CC BY 4.0
# ==========================================

def collatz_billiards_animation(seed, max_steps=500, filename_prefix="collatz_shiftless_billiards"):
    # 1. Physical Computation (Trajectory)
    n = seed
    log3 = math.log(3)
    log2_base3 = math.log(2) / log3

    steps = [0]
    heights = [math.log(n) / log3]
    h0 = heights[0]

    # Safety threshold for n to avoid math.log overflow
    N_MAX = 1e300

    while not (n > 0 and (n & (n - 1) == 0)):
        lsb = n & -n
        n = 3 * n + lsb

        if n > N_MAX:
            print("⚠ n exploded beyond safe range. Stopping.")
            break

        steps.append(len(steps))
        heights.append(math.log(n) / log3)

        if len(steps) > max_steps:
            print("⚠ Target too far! Safety break triggered.")
            break

    path_length = len(steps)
    is_jackpot = (n > 0 and (n & (n - 1) == 0))
    final_m = n.bit_length() - 1 if is_jackpot else None

    # 2. Timing & Pause Settings (for fps=4)
    TILE_PAUSE_FRAMES = 4          # 1.0 sec pause at tile edges
    JACKPOT_ZOOM_PAUSE_FRAMES = 8  # 2.0 sec pause when hitting jackpot
    FREEZE_FRAMES = 12             # 3.0 sec pause at final overview

    # 3. Frame Mapping (Camera Script) - OLD CAMERA LOGIC RESTORED
    frame_map = []
    current_tile = None
    TILE_SIZE = 10.0

    for i in range(path_length):
        curr_s = steps[i]
        curr_h = heights[i]

        tile_x0 = (curr_s // TILE_SIZE) * TILE_SIZE
        tile_y0 = h0 + (math.floor((curr_h - h0) / TILE_SIZE) * TILE_SIZE)
        new_tile = (tile_x0, tile_y0)

        # Frame-out pause logic
        if current_tile is not None and new_tile != current_tile:
            for _ in range(TILE_PAUSE_FRAMES):
                frame_map.append({'step_idx': i, 'tile': current_tile, 'title_mode': "(Pre-Frame-Out Pause)"})
            for _ in range(TILE_PAUSE_FRAMES):
                frame_map.append({'step_idx': i, 'tile': new_tile, 'title_mode': "(Post-Frame-Out Pause)"})

        current_tile = new_tile
        frame_map.append({
            'step_idx': i,
            'tile': current_tile,
            'title_mode': f"Tracking Zoom [{int(tile_x0 // TILE_SIZE)}, {int((tile_y0 - h0) // TILE_SIZE)}]"
        })

    # Jackpot Zoom Pause
    if is_jackpot:
        for _ in range(JACKPOT_ZOOM_PAUSE_FRAMES):
            frame_map.append({'step_idx': path_length - 1, 'tile': current_tile, 'title_mode': "JACKPOT! (Zoom Pause)"})

    total_path_frames = len(frame_map)
    total_frames = total_path_frames + FREEZE_FRAMES

    # 4. Billiard Table Setup
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#001100')
    ax.set_facecolor('#1b5e20')
    ax.set_aspect('equal')

    p_radius = 0.12
    zoom_margin = 0.5
    overview_margin = 2.0

    overview_x_min = -overview_margin
    overview_x_max = max(steps[-1] + overview_margin, TILE_SIZE + overview_margin)
    overview_y_min = h0 - overview_margin
    overview_y_max = max(max(heights) + overview_margin, h0 + TILE_SIZE + overview_margin)

    min_M = math.floor(overview_y_min / log2_base3)
    max_M = math.ceil(overview_y_max / log2_base3)
    max_pocket_step = math.ceil(overview_x_max)

    for M in range(min_M, max_M + 1):
        y_p = M * log2_base3
        ax.axhline(y_p, color='white', lw=0.5, alpha=0.15, zorder=1)
        for s in range(0, max_pocket_step + 1):
            ax.add_patch(Circle((s, y_p), p_radius, color='black', alpha=0.6, zorder=2))

    base_line = [h0 + k for k in steps]
    ax.plot(steps, base_line, color='white', lw=1.0, ls='--', alpha=0.3, zorder=8, label='Inertia (3x Rule)')

    orbit_line, = ax.plot([], [], color='#eeff41', lw=2.0, alpha=0.9, zorder=10, label=f'Orbit of {seed}')
    ball = Circle((0, 0), p_radius, color='white', ec='black', lw=0.5, zorder=15)
    ax.add_patch(ball)

    ax.set_xlabel("Steps (k)", color='white')
    ax.set_ylabel("3-adic Altitude ($log_3 n$)", color='white')
    ax.tick_params(colors='white')
    ax.grid(color='white', alpha=0.05)
    ax.legend(facecolor='#003300', labelcolor='white', loc='upper left', fontsize='small', edgecolor='#333333')

    # 5. Animation Update Function
    def update(frame):
        effective_frame = min(frame, total_path_frames - 1)

        f_info = frame_map[effective_frame]
        step_idx = f_info['step_idx']
        curr_tile = f_info['tile']
        mode_text = f_info['title_mode']

        curr_s = steps[step_idx]
        curr_h = heights[step_idx]

        orbit_line.set_data(steps[:step_idx + 1], heights[:step_idx + 1])
        ball.set_center((curr_s, curr_h))

        if is_jackpot and step_idx == path_length - 1:
            ball.set_color('#ff1744')
        else:
            ball.set_color('white')

        if frame >= total_path_frames:
            ax.set_xlim(overview_x_min, overview_x_max)
            ax.set_ylim(overview_y_min, overview_y_max)
            final_mode = "Finale (Overview)"
            if is_jackpot and frame == total_path_frames:
                ax.scatter(curr_s, curr_h, color='#ff1744', s=500, marker='*', zorder=20)
        else:
            tile_x0, tile_y0 = curr_tile
            ax.set_xlim(tile_x0 - zoom_margin, tile_x0 + TILE_SIZE + zoom_margin)
            ax.set_ylim(tile_y0 - zoom_margin, tile_y0 + TILE_SIZE + zoom_margin)
            final_mode = mode_text

        ax.set_title(f"Shiftless Billiards: {final_mode} - Seed {seed}", color='white', fontsize=16)

        return orbit_line, ball

    ani = FuncAnimation(fig, update, frames=total_frames, blit=False)

    # 6. Export Section (MP4 Skip Logic Included)
    fps_setting = 4

    # --- Check ffmpeg availability ---
    ffmpeg_available = shutil.which("ffmpeg") is not None

    # --- MP4 Export (only if ffmpeg exists) ---
    if ffmpeg_available:
        mp4_filename = f"{filename_prefix}_animation_seed_{seed}.mp4"
        print(f"🎯 Starting MP4 Hunt... (Seed: {seed}, Total Frames: {total_frames})")
        with tqdm(total=total_frames, desc="MP4 Encoding") as pbar:
            ani.save(mp4_filename, writer='ffmpeg', fps=fps_setting, dpi=300,
                     progress_callback=lambda i, n: pbar.update(1))
        print(f"🎬 MP4 saved as {mp4_filename}")
    else:
        print("⚠ MP4 export skipped (ffmpeg not installed).")

    # --- GIF Export (always works) ---
    gif_filename = f"{filename_prefix}_animation_seed_{seed}.gif"
    print(f"🖼️ Starting GIF Hunt... (Seed: {seed})")
    with tqdm(total=total_frames, desc="GIF Encoding") as pbar:
        ani.save(gif_filename, writer='pillow', fps=fps_setting, dpi=150,
                 progress_callback=lambda i, n: pbar.update(1))

    print(f"✨ Hunt Complete! Saved GIF: {gif_filename}")

    # Close the figure cleanly after everything is saved
    plt.close(fig)

# --- RUN ---
if __name__ == "__main__":
    # You can change the seed number here to explore other trajectories.
    seed_to_hunt = 27
    print(f"Starting the animation export for seed {seed_to_hunt}...")
    collatz_billiards_animation(seed_to_hunt)
