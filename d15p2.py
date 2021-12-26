import heapq

FACTOR = 5
DIRS = [-1, 0, 1, 0, -1]


def apply_dijkstra(M, N, _input):
    dists = [[float('inf')] * N for _ in range(M)]
    prev = [[None] * N for _ in range(M)]
    dists[0][0] = 0

    pq = []
    for r in range(M):
        for c in range(N):
            heapq.heappush(pq, (dists[r][c], (r, c)))

    visited = set()
    while pq:
        _, (r, c) = heapq.heappop(pq)
        # lazy approach to dijkstra
        if (r, c) in visited:
            continue
        if r == M - 1 and c == N - 1:
            break
        visited.add((r, c))
        dist = dists[r][c]
        for idx in range(4):
            dr, dc = DIRS[idx:idx + 2]
            if not (0 <= r + dr < M and 0 <= c + dc < N):
                continue
            tentative = dist + _input[r + dr][c + dc]
            if tentative < dists[r + dr][c + dc]:
                dists[r + dr][c + dc] = tentative
                prev[r + dr][c + dc] = idx
                heapq.heappush(pq, (dists[r + dr][c + dc], (r + dr, c + dc)))

    return dists, prev


def print_path(M, N, _input, prev):
    rows = [[str(v) for v in r] for r in _input]

    r, c = M - 1, N - 1
    while True:
        # Change color if needed for your terminal
        rows[r][c] = f"\033[91m{rows[r][c]}\033[0m"
        dirs_idx = prev[r][c]
        if dirs_idx is None:
            break
        dr, dc = DIRS[dirs_idx:dirs_idx + 2]
        r -= dr
        c -= dc

    for row in rows:
        print("".join(row))
    print()


if __name__ == '__main__':
    orig_M, orig_N, M, N = 0, 0, 0, 0
    _input = []
    with open('d15_input.txt', 'r') as f:
        for row in f:
            row = row.strip()
            if not _input:
                orig_N = len(row)
                N = FACTOR * orig_N
            row = list(map(int, row))
            row.extend([0 for _ in range((FACTOR - 1) * orig_N)])
            _input.append(row)
            orig_M += 1
        M = FACTOR * orig_M
        # Expand input
        _input.extend([[0] * N for _ in range((FACTOR - 1) * orig_M)])

    for r in range(orig_M):
        for c in range(orig_N):
            for block_r in range(FACTOR):
                for block_c in range(FACTOR):
                    if block_r == block_c == 0:
                        continue
                    _input[block_r * orig_M + r][block_c * orig_N + c] = \
                        (_input[r][c] + block_r + block_c - 1) % 9 + 1

    dists, prev = apply_dijkstra(M, N, _input)

    # Too large for real input; can use with sample one though
    # print_path(M, N, _input, prev)

    print(dists[M - 1][N - 1])

