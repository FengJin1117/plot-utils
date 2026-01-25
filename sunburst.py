# sunburst.py
import matplotlib.pyplot as plt
from save import save_fig
import numpy as np
import matplotlib.colors as mcolors


def _lighten_color(color, amount=0.5):
    """
    Lighten a given color by mixing it with white.
    """
    try:
        c = mcolors.cnames[color]
    except:
        c = color
    c = np.array(mcolors.to_rgb(c))
    return tuple(c + (1.0 - c) * amount)


def plot_genre_subgenre_sunburst(
    genre_data: dict,
    subgenre_data: dict,
    save_path=None,
    figsize=(4.5, 4.5),
    inner_radius=0.5,
    outer_radius=1.0,
):
    """
    Plot a two-level sunburst chart for genre–subgenre hierarchy.

    Args:
        genre_data (dict):
            {genre: count}
        subgenre_data (dict):
            {genre: {subgenre: count}}
        save_path (str or None):
            path to save figure (pdf)
        figsize (tuple):
            figure size
    """

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("equal")

    # ===== Inner ring (genre) =====
    genres = list(genre_data.keys())
    genre_sizes = list(genre_data.values())

    base_colors = plt.cm.Blues(
        np.linspace(0.35, 0.85, len(genres))
    )

    wedges_inner, _ = ax.pie(
        genre_sizes,
        radius=inner_radius,
        labels=genres,
        labeldistance=0.7,
        colors=base_colors,
        wedgeprops=dict(width=inner_radius, edgecolor="white"),
        textprops=dict(fontsize=9),
    )

    # ===== Outer ring (subgenre) =====
    sub_sizes = []
    sub_labels = []
    sub_colors = []

    for i, genre in enumerate(genres):
        subs = subgenre_data[genre]
        total = sum(subs.values())

        for j, (sub, val) in enumerate(subs.items()):
            sub_sizes.append(val)
            sub_labels.append(sub)

            # same hue, different lightness
            color = _lighten_color(base_colors[i], amount=0.2 + 0.6 * j / max(1, len(subs)))
            sub_colors.append(color)

    ax.pie(
        sub_sizes,
        radius=outer_radius,
        labels=sub_labels,
        labeldistance=1.05,
        colors=sub_colors,
        wedgeprops=dict(
            width=outer_radius - inner_radius,
            edgecolor="white",
        ),
        textprops=dict(fontsize=7),
    )

    plt.tight_layout()

    if save_path is not None:
        save_fig(save_path)

    plt.close()
