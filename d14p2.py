from collections import Counter

import numpy as np

STEPS = 40


def compute_counts(res, idx2pair, boundary_ch):
    counts = Counter()
    for pair, count in zip(idx2pair, res):
        for ch in pair:
            counts[ch] += count
    # each character is counted twice but the boundary chars
    for ch in boundary_ch:
        counts[ch] += 1

    return {k: v // 2 for k, v in counts.items()}


if __name__ == '__main__':
    rules = []
    with open('d14_input.txt', 'r') as f:
        rows = iter(f)
        template = next(rows).strip()
        next(rows)
        for row in rows:
            s, t = row.strip().split(' -> ')
            rules.append([s, t])

    idx2pair = [p for p, _ in rules]
    pair2idx = {p: i for i, p in enumerate(idx2pair)}

    # Could use sparse matrices but not worth it for size
    dim = len(idx2pair)
    transition = np.zeros((dim, dim), dtype=int)
    for s, t in rules:
        transition[pair2idx[f'{s[0]}{t}']][pair2idx[s]] = 1
        transition[pair2idx[f'{t}{s[1]}']][pair2idx[s]] = 1

    initial = np.zeros((dim, 1), dtype=int)
    for idx in range(len(template) - 1):
        initial[pair2idx[template[idx:idx + 2]]] += 1

    res = initial
    for _ in range(STEPS):
        # Could use clever exponentiation of transition for even larger STEPS
        res = np.matmul(transition, res)

    counts = compute_counts(res.squeeze().tolist(), idx2pair, (template[0], template[-1]))
    print(counts)

    _min, _max = min(counts.values()), max(counts.values())
    print(_min, _max, _max - _min)
