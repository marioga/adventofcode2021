def compute(x, vals):
    return sum((x - val)**2 + abs(x - val) for val in vals) // 2


if __name__ == '__main__':
    with open('d7_input.txt', 'r') as f:
        vals = sorted(list(map(int, f.readline().strip().split(','))))

    n = len(vals)
    s = sum(vals)
    print(s / n)
    candidates = []
    for idx in range(len(vals)):
        curr = compute(vals[idx], vals)
        candidates.append((curr, vals[idx]))
        if idx == len(vals) - 1:
            break
        equil = s - (idx + 1) + n / 2
        if n * vals[idx] < equil < n * vals[idx + 1]:
            num = int(equil / n)
            candidates.append((compute(num, vals), num))
            candidates.append((compute(num + 1, vals), num + 1))

    print(min(candidates))

