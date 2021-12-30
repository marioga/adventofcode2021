import numpy as np
from scipy.ndimage import convolve

MAX_STEPS = 50


if __name__ == '__main__':
    # got main idea from reddit. lost my original work,
    # so might as well use a better method
    M, N = 0, 0
    _input = []
    with open('d20_input.txt', 'r') as f:
        rows = iter(f)
        submap = np.array([int(ch == '#') for ch in next(rows).strip()])
        next(rows)
        for row in rows:
            row = row.strip()
            if not _input:
                N = len(row)
            _input.append([int(ch == '#') for ch in row])
            M += 1
    _input = np.pad(_input, (MAX_STEPS + 1, MAX_STEPS + 1))

    conv_mask = (2**np.arange(9)).reshape(3, 3)
    for step in range(MAX_STEPS):
        _input = submap[convolve(_input, conv_mask)]
        if (step + 1) in {2, 50}:
            print(_input.sum())

