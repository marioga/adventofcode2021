DIRS = [1, 0, -1, 0, 1]


if __name__ == '__main__':
    M, N = 0, 0
    _input = []
    with open('d9_input.txt', 'r') as f:
        for row in f:
            row = row.strip()
            if not _input:
                N = len(row)
                # add padding
                _input.append([9] * (N + 2))
            _input.append([9, *map(int, row), 9])
            M += 1
        _input.append([9] * (N + 2))

    total_risk = 0
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            val = _input[i][j]
            for idx in range(4):
                di, dj = DIRS[idx], DIRS[idx + 1]
                if _input[i + di][j + dj] <= val:
                    break
            else:
                total_risk += val + 1
    print(total_risk)

