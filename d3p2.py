from collections import Counter
from functools import reduce


def filter_down(vals, mask, smaller_than=True):
    zero, one = [], []
    for num in vals:
        if mask & num:
            one.append(num)
        else:
            zero.append(num)

    return zero if (len(one) >= len(zero)) == smaller_than else one


if __name__ == '__main__':
    with open('d3_input.txt', 'r') as f:
        mask = None
        vals = []
        for row in f:
            if mask is None:
                mask = 1 << (len(row.strip()) - 1)
            vals.append(int(row.strip(), 2))
    print(mask)

    less, more = vals, vals
    oxygen, co2 = None, None
    while mask:
        if len(less) > 1:
            less = filter_down(less, mask)
        if co2 is None and len(less) == 1:
            co2 = less[0]
        if len(more) > 1:
            more = filter_down(more, mask, smaller_than=False)
        if oxygen is None and len(more) == 1:
            oxygen = more[0]
        mask >>= 1

    print(oxygen, co2, oxygen * co2)

