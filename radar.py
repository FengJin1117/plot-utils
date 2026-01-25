# radar_plot.py
import numpy as np
import matplotlib.pyplot as plt


def plot_model_radar(
    model_scores,
    metric_names,
    smaller_is_better=None,
    title=None,
    save_path=None,
):
    """
    Parameters
    ----------
    model_scores : dict
        {
            "ModelA": [m1, m2, ...],
            "ModelB": [m1, m2, ...],
        }
    metric_names : list[str]
        Names of metrics, same order as scores
    smaller_is_better : list[bool]
        Whether each metric is smaller-is-better
    """
    if smaller_is_better is None:
        smaller_is_better = [False] * len(metric_names)

    # --- convert smaller-is-better metrics by reciprocal ---
    processed_scores = {}
    for model, scores in model_scores.items():
        new_scores = []
        for s, sib in zip(scores, smaller_is_better):
            new_scores.append(1.0 / s if sib else s)
        processed_scores[model] = new_scores

    # --- normalize each metric to [0, 1] ---
    score_matrix = np.array(list(processed_scores.values()))
    min_vals = score_matrix.min(axis=0)
    max_vals = score_matrix.max(axis=0)
    norm_scores = (score_matrix - min_vals) / (max_vals - min_vals + 1e-8)

    # --- radar setup ---
    num_metrics = len(metric_names)
    angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw=dict(polar=True))

    # angle & grid
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(
        np.degrees(angles[:-1]),
        metric_names,
        fontsize=11,
    )

    ax.set_rlabel_position(0)
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_yticklabels(["0.25", "0.50", "0.75"], fontsize=9)
    ax.set_ylim(0, 1.0)

    # --- plot each model ---
    for i, (model, values) in enumerate(processed_scores.items()):
        vals = norm_scores[i].tolist()
        vals += vals[:1]

        ax.plot(
            angles,
            vals,
            linewidth=2,
            label=model,
        )
        ax.fill(
            angles,
            vals,
            alpha=0.15,
        )

    if title:
        ax.set_title(title, fontsize=13, pad=16)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=3,
        frameon=False,
        fontsize=10,
    )

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
