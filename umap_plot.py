# plot-utils/umap_plot.py

import numpy as np
import matplotlib.pyplot as plt
import umap

from save import save_fig
from genre_colors import build_color_map

# 这里决定genre顺序
MMGENRE_GENRES = [
    "Pop",
    "Classical",
    "Rock",
    "Rap",
    "World",
    "Blues",
    "Jazz",
    "Country",
    "Electronic",
    "RNB",
]

def plot_umap(
    embeddings,
    labels,
    *,
    n_neighbors=15,
    min_dist=0.1,
    metric="cosine",
    n_components=2,
    random_state=42,
    point_size=12,
    alpha=0.9,
    figsize=(4.5, 4.0),
    save_path=None,
    show_legend=True,
    color_json=None,
):
    """
    Plot 2D UMAP visualization for embeddings.

    Args:
        embeddings (np.ndarray): Shape (N, D)
        labels (list[str]): Length N, category label for each sample
        n_neighbors (int): UMAP n_neighbors
        min_dist (float): UMAP min_dist
        metric (str): Distance metric
        n_components (int): Output dimension (default 2)
        random_state (int): Random seed
        point_size (int): Scatter point size
        alpha (float): Point transparency
        figsize (tuple): Figure size
        save_path (str | None): If set, save figure to this path
        show_legend (bool): Whether to show legend
    """

    embeddings = np.asarray(embeddings)
    assert embeddings.ndim == 2, "embeddings must be 2D array"
    assert len(embeddings) == len(labels), "embeddings and labels length mismatch"

    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        metric=metric,
        random_state=random_state,
    )

    X_2d = reducer.fit_transform(embeddings)

    plt.figure(figsize=figsize)

    # unique_labels = sorted(set(labels)) # labels排序
    # unique_labels = set(labels)   # set是无须的！

    unique_labels = [g for g in MMGENRE_GENRES if g in labels]

    color_map = build_color_map(unique_labels, json_path=color_json)

    for lab in unique_labels:
        idx = [i for i, l in enumerate(labels) if l == lab]
        plt.scatter(
            X_2d[idx, 0],
            X_2d[idx, 1],
            s=point_size,
            alpha=alpha,
            label=lab,
            color=color_map[lab],   # 👈 显式指定
        )

    # 去除黑框
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.xticks([])
    plt.yticks([])

    # if show_legend:
    #     plt.legend(markerscale=1.5, fontsize=8)

    # plt.tight_layout()

    if show_legend:
        plt.legend(
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),  # 👈 向右“挪出去”
            markerscale=1.5,
            fontsize=12,
            frameon=False,
        )

    plt.tight_layout(rect=[0, 0, 0.85, 1])  # 👈 给 legend 留右边 15%

    if save_path is not None:
        save_fig(save_path)
    
    plt.close()


def generate_synthetic_umap_data(
    num_classes=3,
    samples_per_class=100,
    embedding_dim=64,
    class_names=None,
    random_state=42,
):
    """
    Generate synthetic embeddings for UMAP testing.

    Returns:
        embeddings (np.ndarray): Shape (N, D)
        labels (list[str])
    """

    rng = np.random.RandomState(random_state)

    if class_names is None:
        class_names = ["a", "b", "c"][:num_classes]

    embeddings = []
    labels = []

    for i, name in enumerate(class_names):
        # 每一类一个不同中心
        center = rng.randn(embedding_dim) * 3.0
        class_emb = center + rng.randn(samples_per_class, embedding_dim)

        embeddings.append(class_emb)
        labels.extend([name] * samples_per_class)

    embeddings = np.vstack(embeddings)

    return embeddings, labels


if __name__ == "__main__":
    # simple self-test
    from style import set_acl_style

    set_acl_style()

    embeddings, labels = generate_synthetic_umap_data(
        num_classes=6,
        samples_per_class=100,
        embedding_dim=128,
        class_names=["a", "b", "c", "d", "e", "f"],
    )

    plot_umap(
        embeddings,
        labels,
        n_neighbors=15,
        min_dist=0.1,
        save_path="figs/umap_test.pdf",
    )
