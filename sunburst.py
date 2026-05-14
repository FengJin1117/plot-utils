# sunburst.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from save import save_fig
from color_utils import interleave_order

# amount=0: 原色, amount=1: 白色
def lighten(color, amount):
    c = np.array(mcolors.to_rgb(color))
    return tuple(c + (1 - c) * amount)

def pick_text_color(bg_color, thresh=0.45):
    """
    根据背景色亮度选择文字颜色
    bg_color: RGB tuple in [0,1]
    thresh: 亮度阈值，越小越容易触发白字
    """
    r, g, b = mcolors.to_rgb(bg_color)
    # 感知亮度（WCAG 常用）
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "white" if luminance < thresh else "black"


# TODO: 命名去除genre、subgenre，通用化
def plot_genre_subgenre_sunburst(
    genre_data,
    subgenre_data,
    save_path=None,
    figsize=(6, 6),
    inner_radius=0.47,
    outer_radius=1.0,
    # ===== color control =====
    inner_color_range=(0.1, 1),
    outer_lighten=0.25,
    shuffle_genre_colors=True,
    genre_color_order=None,  # e.g. [6, 0, 7, 1, 8, 2, ...]
    random_seed=42,
    # ===== text control =====
    inner_fontsize_base=8,
    outer_fontsize_base=8,
):

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("equal") # 保持饼图为圆形
    ax.axis("off") # 关闭坐标轴

    genres = list(genre_data.keys())
    genre_sizes = np.array(list(genre_data.values()))
    total = genre_sizes.sum()

    # 扇形图颜色
    # ===== base colors =====
    base_colors = plt.cm.Blues(
        np.linspace(inner_color_range[0], inner_color_range[1], len(genres))
    )

    # 颜色、genre、数值三者同步重排
    # if shuffle_genre_colors:
    #     rng = np.random.default_rng(random_seed)
    #     order = rng.permutation(len(genres))
    #     base_colors = base_colors[order]
    #     genres = [genres[i] for i in order]
    #     genre_sizes = genre_sizes[order]
    
    # from color_utils import interleave_order

    # 最大色差重排，提升可读性（论文标准）
    if shuffle_genre_colors:
        if genre_color_order is not None:
            order = np.array(genre_color_order)
        else:
            order = interleave_order(len(genres), mode="high_low")

        base_colors = base_colors[order]
        # genres = [genres[i] for i in order]
        # genre_sizes = genre_sizes[order]

    # ===== inner ring =====
    wedges_inner, _ = ax.pie(
        genre_sizes,
        radius=inner_radius,
        startangle=90, # 从12点钟方向开始（论文标准）
        colors=base_colors,
        wedgeprops=dict(width=inner_radius, edgecolor="white", linewidth=1.6), # 
    )

    for w, g, v in zip(wedges_inner, genres, genre_sizes):
        ang = 0.5 * (w.theta1 + w.theta2)
        r = inner_radius * 0.62
        pct = int(round(100 * v / total))

        text_color = pick_text_color(w.get_facecolor())

        if pct < 9:
            inner_fontsize = inner_fontsize_base - 1
        else:
            inner_fontsize =  inner_fontsize_base

        ax.text(
            r * np.cos(np.deg2rad(ang)),
            r * np.sin(np.deg2rad(ang)),
            f"{g}\n{pct}%",
            ha="center",
            va="center",
            fontsize=inner_fontsize,
            color=text_color,
        )




    # ===== outer ring =====
    sub_sizes, sub_meta = [], []
    for gi, g in enumerate(genres):
        for sub, val in subgenre_data[g].items():
            sub_sizes.append(val)
            sub_meta.append((gi, sub, val))

    sub_colors = [
        lighten(base_colors[gi], outer_lighten)
        for gi, _, _ in sub_meta
    ]

    wedges_outer, _ = ax.pie(
        sub_sizes,
        radius=outer_radius,
        startangle=90,
        colors=sub_colors,
        wedgeprops=dict(
            width=outer_radius - inner_radius,
            edgecolor="white",
            linewidth=1.2,
        ),
    )

    # print("sub: angle, rot")
    print("sub: pct")

    for w, (gi, sub, val) in zip(wedges_outer, sub_meta):
        ang = 0.5 * (w.theta1 + w.theta2)
        ang = ang % 360 
        r = inner_radius + 0.55 * (outer_radius - inner_radius)
        pct = int(round(100 * val / total))

        # rot = ang
        if 90 < ang < 271:
            rot = (ang + 180) % 360
        else:
            rot = ang

        # print(f"sub: {sub} rot: {rot:.0f}")
        # print(f"{sub}: {ang:.0f}")
        # print(f"{sub}: {ang:.0f}, {rot:.0f}")

        print(f"{sub}: {pct:.1f}%")

        if pct < 5 and pct > 2:
            outer_fontsize = outer_fontsize_base - 0
        elif pct <= 2:
            outer_fontsize = outer_fontsize_base - 1 
        else:
            outer_fontsize = outer_fontsize_base

        text_color = pick_text_color(w.get_facecolor())

        ax.text(
            r * np.cos(np.deg2rad(ang)),
            r * np.sin(np.deg2rad(ang)),
            f"{sub}\n{pct}%",
            ha="center",
            va="center",
            fontsize=outer_fontsize,
            rotation=rot, # 决定是否绕环。不设置的话，全部横着（相互遮挡）
            rotation_mode="anchor",
            color=text_color, 
        )

    plt.tight_layout()
    if save_path:
        save_fig(save_path)
    plt.close()
