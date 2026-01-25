import matplotlib.pyplot as plt
import numpy as np
from save import save_fig


def plot_duration_histogram(
    durations,
    bins=20,
    save_path=None,
    figsize=(4, 3),
    xlabel="Duration (seconds)",
    ylabel="Number of segments",
    density=False,
    x_lim=None,
    color=None,
    show_medium=False,
    medium_type="median",  # "median" or "mean"
):
    """
    Plot histogram of audio segment durations.

    Args:
        durations (list[float]): audio durations in seconds
        bins (int): number of histogram bins
        save_path (str or None): path to save figure (pdf)
        figsize (tuple): figure size in inches
        xlabel (str)
        ylabel (str)
        density (bool): whether to normalize to probability density
        x_lim (tuple or None): (min, max) for x-axis
        color (str or None): histogram color
        show_medium (bool): whether to show median/mean as dashed line
        medium_type (str): "median" or "mean"
    """

    fig, ax = plt.subplots(figsize=figsize)

    ax.hist(
        durations,
        bins=bins,
        density=density,
        color=color,
    )



    # --- medium line ---
    if show_medium:
        if medium_type == "mean":
            value = np.mean(durations)
        else:
            value = np.median(durations)

        ax.axvline(
            value,
            linestyle="--",
            linewidth=0.8,
            color="black",
            alpha=0.8,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Density" if density else ylabel)

    if x_lim is not None:
        ax.set_xlim(*x_lim)

    plt.tight_layout()

    if save_path is not None:
        save_fig(save_path)

    plt.close()
