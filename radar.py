# radar_plot.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def plot_model_radar(
    model_scores,
    metric_names,
    title=None,
    save_path=None,
    fill_alpha=0.18,
    line_width=1.5, # 雷达线条宽度
    r_min=1.0,      # ✅ 明确半径范围
    r_max=5.0,
):
    """
    Parameters
    ----------
    model_scores : dict
        {
            "ModelA": [m1, m2, ...],  # values in [1, 5]
        }
    metric_names : list[str]
        Radar axis labels
    fill_alpha : float
        Alpha for filled area
    """

    num_metrics = len(metric_names)
    angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6.8, 6.8), subplot_kw=dict(polar=True))

    # --- polar setup ---
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_thetagrids(
        np.degrees(angles[:-1]),
        metric_names,
        fontsize=12,
    )

    # X 轴标签与图形距离。调大pad，把metric_names字体往外推。
    ax.tick_params(axis="x", pad=10)


    # 外围圆（polar spine）透明度
    ax.spines["polar"].set_alpha(0.3)
    ax.spines["polar"].set_linewidth(1.0)

    # ✅ 直接使用真实数值范围
    ax.set_ylim(r_min, r_max)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=9)
    # ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.yaxis.grid(True, alpha=0.3)

    # --- plot ---
    colors = plt.cm.Set2(np.linspace(0, 1, len(model_scores)))
    legend_handles = []

    for i, (model, scores) in enumerate(model_scores.items()):
        vals = list(scores)
        vals += vals[:1]

        ax.plot(
            angles,
            vals,
            linewidth=line_width,
            color=colors[i],
        )
        ax.fill(
            angles,
            vals,
            color=colors[i],
            alpha=fill_alpha,
        )

        # ✅ 大圆点 legend（无连线）
        legend_handles.append(
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="None",
                markersize=10,
                markerfacecolor=colors[i],
                markeredgecolor="none",
                label=model,
            )
        )

    if title:
        ax.set_title(title, fontsize=13, pad=18)

    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=4,
        frameon=False,
        fontsize=10,
    )

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
