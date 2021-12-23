from collections import Counter
from functools import reduce


if __name__ == '__main__':
    count = 0
    with open('d3_input.txt', 'r') as f:
        counts = Counter()
        for row in f:
            count += 1
            val = int(row.strip(), 2)
            idx = 0
            mask = 1
            while mask <= val:
                if mask & val:
                    counts[idx] += 1
                mask <<= 1
                idx += 1

    gamma, epsilon = [0] * len(counts), [0] * len(counts)
    for idx, val in counts.items():
        if 2 * val > count:
            gamma[idx] = 1
        elif 2 * val < count:
            epsilon[idx] = 1
        else:
            raise Exception("DAFOX")

    gamma = reduce(lambda x, y: 2 * x + y, gamma[::-1])
    epsilon = reduce(lambda x, y: 2 * x + y, epsilon[::-1])
    print(gamma, epsilon, gamma * epsilon)

