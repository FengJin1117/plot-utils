import matplotlib.pyplot as plt


# def set_acl_style():
#     plt.rcParams.update({
#         "font.family": "serif",
#         "font.size": 8,
#         "axes.linewidth": 0.8,
#         "legend.frameon": False,
#     })

# def set_acl_style():
#     plt.rcParams.update({
#         # 字体：强制论文风 serif（LaTeX / Computer Modern 对齐）
#         "font.family": "serif",
#         "font.serif": ["Computer Modern Roman"],
#         "mathtext.fontset": "cm",

#         # 字号：8pt 是 ACL figure 的安全下限
#         "font.size": 8,
#         "axes.titlesize": 8,
#         "axes.labelsize": 8,
#         "xtick.labelsize": 7,
#         "ytick.labelsize": 7,

#         # 线条：整体偏轻
#         "axes.linewidth": 0.8,
#         "xtick.major.width": 0.6,
#         "ytick.major.width": 0.6,

#         # 图例：论文风（无框）
#         "legend.fontsize": 7,
#         "legend.frameon": False,

#         # minus 号（LaTeX 常见坑）
#         "axes.unicode_minus": False,
#     })

# def set_acl_style():
#     plt.rcParams.update({
#         "font.family": "serif",

#         # ❗不要再指定 Computer Modern Roman
#         # 交给 mathtext + matplotlib 内置 CM
#         "mathtext.fontset": "cm",

#         "font.size": 8,
#         "axes.titlesize": 8,
#         "axes.labelsize": 8,
#         "xtick.labelsize": 7,
#         "ytick.labelsize": 7,

#         # 坐标轴边框
#         "axes.linewidth": 0.8,

#         # ✅ 关键：柱状图 / histogram 边框
#         "patch.linewidth": 0.5,

#         # 默认 patch 边框颜色（可选）
#         "patch.edgecolor": "black",
        
#         "legend.frameon": False,
#         "axes.unicode_minus": False,
#     })

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
