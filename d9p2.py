import heapq
from functools import reduce

DIRS = [1, 0, -1, 0, 1]


def get_basin_size(_input, M, N, p, visited):

    def dfs(i, j):
        if orig := visited.get((i, j)):
            if orig == p:
                return 0
            # since locations are part of exactly one basin, it should never get here
            raise Exception(f'DAFOX! {(i, j)} flows to low points: {p} and {orig}?')
        visited[(i, j)] = p
        res = 1
        for idx in range(4):
            di, dj = DIRS[idx], DIRS[idx + 1]
            if _input[i][j] < _input[i + di][j + dj] < 9:
                res += dfs(i + di, j + dj)
        return res
    return dfs(*p)


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

    low_points = []
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            val = _input[i][j]
            for idx in range(4):
                di, dj = DIRS[idx], DIRS[idx + 1]
                if _input[i + di][j + dj] <= val:
                    break
            else:
                low_points.append((i, j))

    basin_sizes = []
    visited = {}
    for p in low_points:
        basin_size = get_basin_size(_input, M, N, p, visited)
        if len(basin_sizes) < 3:
            heapq.heappush(basin_sizes, basin_size)
        elif basin_sizes[0] < basin_size:
            heapq.heappushpop(basin_sizes, basin_size)
    print(reduce(lambda a, b: a * b, basin_sizes))

