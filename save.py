def save_fig(path, fmt="pdf"):
    import os
    import matplotlib.pyplot as plt

    if path is None:
        return

    save_dir = os.path.dirname(path)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    plt.savefig(path, format=fmt)
