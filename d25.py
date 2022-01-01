def print_board(M, N, _input):
    # for easy debugging
    for r in range(M):
        row = []
        for c in range(N):
            row.append(_input[r][c])
        print("".join(map(str, row)))
    print()


def step(M, N, _input):
    moved = False
    for r in range(M):
        first_empty = _input[r][0] == '.'
        prev_moved = False
        for c in range(N):
            if _input[r][c] == '>' and not prev_moved and \
                    ((c < N - 1 and _input[r][c + 1] == '.') or
                     (c == N - 1 and first_empty)):
                _input[r][c] = '.'
                _input[r][(c + 1) % N] = '>'
                moved = True
                prev_moved = True
            else:
                prev_moved = False

    for c in range(N):
        first_empty = _input[0][c] == '.'
        prev_moved = False
        for r in range(M):
            if _input[r][c] == 'v' and not prev_moved and \
                    ((r < M - 1 and _input[r + 1][c] == '.') or
                     (r == M - 1 and first_empty)):
                _input[r][c] = '.'
                _input[(r + 1) % M][c] = 'v'
                moved = True
                prev_moved = True
            else:
                prev_moved = False

    return moved


if __name__ == '__main__':
    M, N = 0, 0
    _input = []
    with open('d25_input.txt', 'r') as f:
        for row in f:
            row = row.strip()
            if not _input:
                N = len(row)
            _input.append(list(row))
            M += 1

    print_board(M, N, _input)
    count = 1
    while step(M, N, _input):
        count += 1
    print_board(M, N, _input)
    print(count)

