# plot-utils/genre_colors.py

import json
import matplotlib.pyplot as plt


# DEFAULT_GENRES = [
#     "blues",
#     "classical",
#     "country",
#     "electronic",
#     "jazz",
#     "pop",
#     "rap",
#     "rnb",
#     "rock",
#     "world",
# ]

DEFAULT_GENRES = [
    "Blues",
    "Classical",
    "Country",
    "Electronic",
    "Jazz",
    "Pop",
    "Rap",
    "RNB",
    "Rock",
    "World",
]

def load_genre_color_map(json_path):
    """
    Load genre-color mapping from json file.

    JSON format:
    {
        "blues": "#1f77b4",
        "classical": "#ff7f0e",
        ...
    }
    """
    with open(json_path, "r") as f:
        color_map = json.load(f)

    # 校验是否缺失
    missing = set(DEFAULT_GENRES) - set(color_map.keys())
    if missing:
        raise ValueError(f"Missing genres in color json: {missing}")

    return color_map


def get_default_color_map(genres):
    """
    Use matplotlib default color cycle.
    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    if len(genres) > len(colors):
        raise ValueError(
            f"Default color cycle only has {len(colors)} colors, "
            f"but got {len(genres)} genres."
        )

    return {
        genre: colors[i]
        for i, genre in enumerate(genres)
    }


def build_color_map(genres, json_path=None):
    """
    Unified interface:
    - If json_path is None → use matplotlib default cycle
    - Else → load from json
    """
    if json_path is None:
        return get_default_color_map(genres)

    color_map = load_genre_color_map(json_path)

    missing = set(genres) - set(color_map.keys())
    if missing:
        raise ValueError(
            f"Missing genres in color json: {missing}"
            f"genres: {genres}, color_map keys: {list(color_map.keys())}"
        )

    # 只返回当前需要的
    return {g: color_map[g] for g in genres}