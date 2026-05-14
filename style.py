import matplotlib.pyplot as plt

# 去除黑框
def set_acl_style():
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",

        "font.size": 8,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,

        # 坐标轴线宽（保留左/下即可）
        "axes.linewidth": 0.8,

        # ❌ 不要柱子边框
        "patch.linewidth": 0.0,
        "patch.edgecolor": "none",

        "legend.frameon": False,
        "axes.unicode_minus": False,
    })
