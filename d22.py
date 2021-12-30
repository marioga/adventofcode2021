import numpy as np


if __name__ == '__main__':
    instructions = []
    slices = []
    with open('d22_input.txt', 'r') as f:
        for row in f:
            inst, rest = row.strip().split()
            instructions.append(int(inst == 'on'))
            sl = []
            for entry in rest.split(','):
                _range = entry.split('=')[1]
                sl.append(list(map(int, _range.split('..'))))
            slices.append(sl)

    # part1
    cubes = np.zeros((101, 101, 101), dtype=np.int8)
    for inst, sl in zip(instructions, slices):
        if all((-50 <= x <= y <= 50) for x, y in sl):
            cubes[slice(sl[0][0] + 50, sl[0][1] + 50 + 1),
                  slice(sl[1][0] + 50, sl[1][1] + 50 + 1),
                  slice(sl[2][0] + 50, sl[2][1] + 50 + 1)] = inst
    print(cubes.sum())

    # part2
    # discretize the cube using values in list
    # still pretty slow but it finishes in like 1 min :-/
    points = []
    for dim in range(3):
        dim_points = set()
        for sl in slices:
            start, end = sl[dim]
            dim_points.add(start)
            dim_points.add(end + 1)
        points.append(sorted(dim_points))

    inv_points = [{p: i for i, p in enumerate(dim_points)} for dim_points in points]

    discrete_cubes = np.zeros(tuple(len(dim_points) - 1 for dim_points in points), dtype=np.int8)
    for inst, sl in zip(instructions, slices):
        discrete_cubes[slice(inv_points[0][sl[0][0]], inv_points[0][sl[0][1] + 1]),
                       slice(inv_points[1][sl[1][0]], inv_points[1][sl[1][1] + 1]),
                       slice(inv_points[2][sl[2][0]], inv_points[2][sl[2][1] + 1])] = inst

    count = 0
    ii, jj, kk = discrete_cubes.shape
    for i in range(ii):
        if i % 100 == 0:
            print(f"Progress: {i}/{ii}")
        curr_i = discrete_cubes[i]
        size_i = points[0][i + 1] - points[0][i]
        for j in range(jj):
            curr_ij = curr_i[j]
            size_ij = size_i * (points[1][j + 1] - points[1][j])
            for k in curr_ij.nonzero()[0].tolist():
                count += size_ij * (points[2][k + 1] - points[2][k])
    print(count)

