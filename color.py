# color.py

# 单色（用于单图、统计图）
PRIMARY_BLUE = "#4C72B0"
PRIMARY_ORANGE = "#DD8452"
PRIMARY_GREEN = "#55A868"
PRIMARY_RED = "#C44E52"
PRIMARY_PURPLE = "#8172B3"
PRIMARY_BROWN = "#937860"
PRIMARY_GRAY = "#8C8C8C"

# 推荐的论文级调色板（不超过 6 色）
PAPER_COLORS = [
    PRIMARY_BLUE,
    PRIMARY_ORANGE,
    PRIMARY_GREEN,
    PRIMARY_RED,
    PRIMARY_PURPLE,
    PRIMARY_BROWN,
    PRIMARY_GRAY,
]

def get_color(idx=0):
    """Get a color from the paper color palette."""
    return PAPER_COLORS[idx % len(PAPER_COLORS)]
