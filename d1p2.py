def main(vals, W):
    count = 0
    prev = curr = sum(vals[:W])
    idx = 1
    while idx + W <= len(vals):
        curr += vals[idx + W - 1] - vals[idx - 1]
        count += int(curr > prev)
        prev = curr
        idx += 1
    print(count)


if __name__ == '__main__':
    vals = []
    with open('d1_input.txt', 'r') as f:
        for row in f:
            vals.append(int(row.strip()))

    main(vals, 3)
