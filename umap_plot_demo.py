import numpy as np
import matplotlib.pyplot as plt
import umap

from save import save_fig

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
    spread=1.0,          # ★ 新增：整体空间放缩
    shape_noise=0.0,     # ★ 新增：点群形状随机性
    save_path=None,
    show_legend=True,
):
    """
    Plot 2D UMAP visualization for embeddings.
    """

    embeddings = np.asarray(embeddings)
    assert embeddings.ndim == 2
    assert len(embeddings) == len(labels)

    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        metric=metric,
        random_state=random_state,
    )

    X_2d = reducer.fit_transform(embeddings)

    # -------- (2) 空间整体放缩 --------
    if spread != 1.0:
        X_2d = X_2d * spread

    fig, ax = plt.subplots(figsize=figsize)

    rng = np.random.RandomState(random_state)
    unique_labels = sorted(set(labels))

    for lab in unique_labels:
        idx = np.array([i for i, l in enumerate(labels) if l == lab])
        pts = X_2d[idx]

        # -------- (3) 点群形状随机化 --------
        if shape_noise > 0:
            # 随机各向异性变换（拉伸 + 旋转）
            A = np.eye(2) + rng.randn(2, 2) * shape_noise
            pts = pts @ A

            # 轻微 jitter
            pts += rng.randn(*pts.shape) * shape_noise * 0.5

        ax.scatter(
            pts[:, 0],
            pts[:, 1],
            s=point_size,
            alpha=alpha,
            label=lab,
        )

    # -------- (1) 去除所有边框 --------
    ax.set_axis_off()

    if show_legend:
        ax.legend(markerscale=1.5, fontsize=8, frameon=False)

    plt.tight_layout()

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
        spread=4.3,        # 空间更舒展
        shape_noise=0.05, # 类簇更自然
        save_path="figs/umap_test_v3.pdf",
    )
