ROUNDS = 100


def print_board(M, N, _input):
    # for easy debugging
    for r in range(M):
        row = []
        for c in range(N):
            row.append(_input[r][c])
        print("".join(map(str, row)))
    print()


def simulate_round(M, N, _input, to_flash):
    flashes = 0
    next_round_to_flash = set()
    visited = set()

    while to_flash:
        pos = to_flash.pop()
        visited.add(pos)
        r, c = divmod(pos, N)
        flashes += 1
        _input[r][c] = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                pos = (r + dr) * N + (c + dc)
                if dr == dc == 0 or not (0 <= r + dr < M and 0 <= c + dc < N) \
                        or pos in visited:
                    continue
                _input[r + dr][c + dc] += 1
                if _input[r + dr][c + dc] >= 9:
                    to_flash.add(pos)

    # Take care of the rest
    for r in range(M):
        for c in range(N):
            if r * N + c in visited:
                continue
            _input[r][c] += 1
            if _input[r][c] == 9:
                next_round_to_flash.add(r * N + c)

    return next_round_to_flash, flashes


if __name__ == '__main__':
    M, N = 0, 0
    _input = []
    to_flash = set()
    with open('d11_input.txt', 'r') as f:
        for i, row in enumerate(f):
            row = row.strip()
            if not _input:
                N = len(row)
            vals = []
            for j, val in enumerate(map(int, row)):
                vals.append(val)
                if val == 9:
                    to_flash.add(M * N + j)
            _input.append(vals)
            M += 1

    _round = 0
    while True:
        if _round % 10 == 0:
            print_board(M, N, _input)
        _round += 1
        to_flash, flashes = simulate_round(M, N, _input, to_flash)
        if flashes == M * N:
            break
    print_board(M, N, _input)
    print(_round)

