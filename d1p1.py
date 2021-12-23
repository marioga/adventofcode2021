def main(vals):
    count = 0
    for prev, curr in zip(vals, vals[1:]):
        count += int(prev < curr)

    print(count)


if __name__ == '__main__':
    vals = []
    with open('d1_input.txt', 'r') as f:
        for row in f:
            vals.append(int(row.strip()))

    main(vals)
