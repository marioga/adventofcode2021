def count_increases(vals):
    count = 0
    for prev, curr in zip(vals, vals[1:]):
        count += int(prev < curr)
    return count


def count_increases_window(vals, window_size):
    count = 0
    prev = curr = sum(vals[:window_size])
    idx = 1
    while idx + window_size <= len(vals):
        curr += vals[idx + window_size - 1] - vals[idx - 1]
        count += int(prev < curr)
        prev = curr
        idx += 1
    return count


if __name__ == '__main__':
    vals = []
    with open('d1_input.txt', 'r') as f:
        for row in f:
            vals.append(int(row.strip()))

    print(count_increases(vals))
    print(count_increases_window(vals, 3))
