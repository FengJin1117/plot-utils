import matplotlib.pyplot as plt
from save import save_fig

def plot_bar(
    data: dict,
    save_path=None,
    figsize=(4, 3),
    xlabel="",
    ylabel="",
    rotate_xticks=45,
    y_lim=1.1,
    show_values=True,
    sort=True,
):
    """
    Plot a generic categorical bar chart.

    Args:
        data (dict): {category_name: value}
        save_path (str or None): path to save figure (pdf)
        figsize (tuple): figure size in inches
        xlabel (str)
        ylabel (str)
        rotate_xticks (int): rotation angle for x tick labels
        y_lim (float): y-axis limit multiplier
        show_values (bool): whether to show value labels on bars
        sort (bool): whether to sort bars by value (descending)
    """

    if sort:
        items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    else:
        items = data.items()

    categories, values = zip(*items)

    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(categories, values)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # 关键：ylim 一定要设在 ax 上
    ax.set_ylim(0, max(values) * y_lim)

    if rotate_xticks:
        ax.set_xticklabels(categories, rotation=rotate_xticks, ha="right")

    if show_values:
        ax.bar_label(bars, padding=2, fontsize=8)

    plt.tight_layout()

    if save_path is not None:
        save_fig(save_path)

    plt.close()
