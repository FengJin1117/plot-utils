# plot_utils/score/music_note_distribution.py

import os
import numpy as np
import pandas as pd
from collections import Counter
from scipy.stats import entropy
import matplotlib.pyplot as plt
import seaborn as sns
import json

def parse_score_file(score_path):
    """
    解析单个 opencpop.txt 文件
    返回所有非0 note 的 list
    """
    notes_all = []

    with open(score_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 4:
                continue

            note_str = parts[3].strip().split()
            notes = [int(n) for n in note_str if int(n) != 0]
            notes_all.extend(notes)

    return notes_all

def load_genre_notes(root_dir, genre_list):
    """
    返回 dict:
    {
        "pop": [note1, note2, ...],
        "rock": [...]
    }
    """
    genre_note_dict = {}

    for genre in genre_list:
        genre_dir = os.path.join(root_dir, genre.lower())
        score_file = os.path.join(genre_dir, "opencpop.txt")

        if not os.path.exists(score_file):
            print(f"Warning: {score_file} not found.")
            continue

        notes = parse_score_file(score_file)
        genre_note_dict[genre] = notes

    return genre_note_dict

def analyze_note_distribution(genre_note_dict):
    """
    返回 DataFrame 统计表
    """
    stats = []

    for genre, notes in genre_note_dict.items():
        if len(notes) == 0:
            continue

        notes_arr = np.array(notes)
        counter = Counter(notes_arr)

        probs = np.array(list(counter.values())) / len(notes_arr)

        stats.append({
            "genre": genre,
            "mean_pitch": np.mean(notes_arr),
            "std_pitch": np.std(notes_arr),
            "unique_notes": len(counter),
            "entropy": entropy(probs)
        })

    return pd.DataFrame(stats)

def plot_note_distribution(
    genre_note_dict,
    save_path=None,
    genre_color_path=None
    ):    
    """
    violin plot
    """
    data = []

    for genre, notes in genre_note_dict.items():
        for n in notes:
            data.append({
                "genre": genre,
                "pitch": n
            })

    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 5))

    palette = None

    if genre_color_path is not None and os.path.exists(genre_color_path):
        with open(genre_color_path, "r") as f:
            color_map = json.load(f)

        # 只保留当前存在的genre
        palette = {
            g: color_map[g]
            for g in df["genre"].unique()
            if g in color_map
        }

    sns.violinplot(
        data=df,
        x="genre",
        y="pitch",
        inner="box",
        cut=0,
        palette=palette
    )

    plt.ylabel("MIDI Pitch")
    plt.xlabel("")
    # plt.title("Distribution of Note Pitches by Genre")
    plt.xticks(rotation=30)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.show()