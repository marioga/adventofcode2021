import math
from itertools import chain


def get_fixed_x_values(xmin, xmax):
    # get values v_x0 such that xmin <= v_x0 * (v_x0 + 1) / 2 <= xmax
    return range(math.ceil((math.sqrt(8 * xmin + 1) - 1) / 2),
                 math.floor((math.sqrt(8 * xmax + 1) - 1) / 2) + 1)


def get_pairs(t, xmin, xmax, ymin, ymax, fixed):
    if t < fixed.start:
        x_range = range(math.ceil(max(t, xmin / t + (t - 1) / 2)),
                        math.floor(xmax / t + (t - 1) / 2) + 1)
    elif t < fixed.stop:
        x_range = range(fixed.start, math.floor(xmax / t + (t - 1) / 2) + 1)
    else:
        x_range = fixed

    return (x_range, range(math.ceil(ymin / t + (t - 1) / 2),
                           math.floor(ymax / t + (t - 1) / 2) + 1))


if __name__ == '__main__':
    with open('d17_input.txt', 'r') as f:
        xbounds, ybounds = f.readline().strip()[len('target area: '):].split(', ')
        xmin, xmax = map(int, xbounds.split('=', 1)[1].split('..'))
        ymin, ymax = map(int, ybounds.split('=', 1)[1].split('..'))

    # some common assumptions
    assert min(xmin, xmax) >= 0 and xmin <= xmax and ymin <= ymax

    # x coord after t steps is x_t = t * v_x0 - t * (t - 1) / 2 if t <= v_x0,
    # and x_t = v_x0 * (v_x0 + 1) / 2 for t >= v_x0
    # y coord after t steps is y_t = t * v_y0 - t * (t - 1) / 2

    # xmin <= x_t <= xmax iff max(t, xmin / t + (t - 1) / 2) <= v_x0 <= xmax / t + (t - 1) / 2,
    # or t >= v_x0 and xmin <= v_x0 * (v_x0 + 1) / 2 <= xmax
    # ymin <= y <= ymax iff ymin / t + (t - 1) / 2 <= v_y0 <= ymax / t + (t - 1) / 2

    # There are a bunch of cases, some of them with infinite solutions: for example, say
    # (xmin, xmax, ymin, ymax) = (1, 1, -1, 1), then if v_x0 = 1 and v_y0 = k, we obtain
    # (x_{2 * k + 1}, y_{2 * k + 1}) = (1, 0) for all k, which is within target. More precisely,
    # the number of solutions is infinite iff there exists v_x0 such that
    # xmin <= v_x0 * (v_x0 + 1) / 2 <= xmax, and ymin * ymax < 0.

    # For simplicity, I'll only solve the case where ymin * ymax > 0
    assert ymin * ymax > 0, "Solution not implemented"

    # Under the assumption above, if t > 2 * max(abs(ymin), abs(ymax)), then v_y0 is strictly
    # between two half-integers, so it suffices to check t <= 2 * max(abs(ymin), abs(ymax))
    fixed = get_fixed_x_values(xmin, xmax)
    res = set()
    max_y = -float('inf')
    for t in range(1, 2 * max(abs(ymin), abs(ymax)) + 1):
        x_range, y_range = get_pairs(t, xmin, xmax, ymin, ymax, fixed)
        if len(y_range) >= 1:
            max_y = max(max_y, y_range.stop - 1)
        for x in x_range:
            for y in y_range:
                res.add((x, y))

    print(max_y * (max_y + 1) // 2)
    print(len(res))

