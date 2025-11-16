import os
from modules.utils import cfg

def load_scores():
    if not os.path.exists(cfg.HIGHEST_SCORE_RECORD_FILEPATH):
        return []
    with open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, "r") as f:
        lines = f.readlines()
    scores = []
    for line in lines:
        parts = line.strip().split(":", 1)
        if len(parts) == 2:
            name, sc = parts
            try:
                scores.append((name, int(sc)))
            except:
                continue
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[:10]


def save_score(name, score):
    scores = load_scores()
    scores.append((name, score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:10]
    with open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, "w") as f:
        for n, s in scores:
            f.write(f"{n}:{s}\n")


def get_top_scores():
    return load_scores()
