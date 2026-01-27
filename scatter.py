import matplotlib.pyplot as plt
import numpy as np


def plot_rank_scatter(
    labels,
    x_values,
    y_values,
    corr_value=None,
    save_path=None,
    xlabel="Score (X)",
    ylabel="Score (Y)",
    value_range=(1, 5),
    tick_step=1.0,
    figsize=(3.2, 3.2),
):
    """
    Generic rank-consistency scatter plot.
    """
    markers = ["o", "s", "^", "D", "v", ">", "<", "p"]
    colors = plt.cm.tab10.colors

    vmin, vmax = value_range

    plt.figure(figsize=figsize)

    for i, label in enumerate(labels):
        plt.scatter(
            x_values[i],
            y_values[i],
            marker=markers[i % len(markers)],
            color=colors[i % len(colors)],
            s=45,
            edgecolors="black",
            linewidths=0.5,
            label=label,
        )

    # y = x reference line
    plt.plot(
        [vmin, vmax],
        [vmin, vmax],
        linestyle="--",
        linewidth=1,
        color="black",
    )

    plt.xlabel(xlabel, fontsize=9)
    plt.ylabel(ylabel, fontsize=9)

    plt.xlim(vmin, vmax)
    plt.ylim(vmin, vmax)

    ticks = np.arange(vmin, vmax + 1e-6, tick_step)
    plt.xticks(ticks)
    plt.yticks(ticks)

    if corr_value is not None:
        plt.title(f"Spearman $\\rho$ = {corr_value:.2f}", fontsize=9)

    plt.legend(
        fontsize=7,
        frameon=False,
        loc="lower right",
        handletextpad=0.3,
        borderaxespad=0.3,
    )

    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, format="pdf", bbox_inches="tight")

    plt.close()