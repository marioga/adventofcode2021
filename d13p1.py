DIMS = {
    'x': 0,
    'y': 1,
}


def print_points(points):
    # for easy debugging
    cols, rows = 0, 0
    for p in points:
        cols = max(cols, p[0] + 1)
        rows = max(rows, p[1] + 1)
    print(rows, cols)

    for r in range(rows):
        row = []
        for c in range(cols):
            row.append('#' if (c, r) in points else '.')
        print(" ".join(row))
    print()


def fold(points, axis, val):
    dim = DIMS[axis]

    to_add, to_remove = set(), set()
    for p in points:
        if p[dim] < val:
            continue
        elif p[dim] == val:
            raise Exception(f"DAFOX! Point {p} in fold along {axis}={val}")
        to_remove.add(p)
        trans_p = list(p)
        trans_p[dim] = 2 * val - p[dim]
        if trans_p[dim] < 0:
            print(f"Ha! Weird! Fold along {axis}={val} sends {p} off the grid")
        to_add.add(tuple(trans_p))

    return (points - to_remove) | to_add



if __name__ == '__main__':
    points = set()
    folds = []
    with open('d13_input.txt', 'r') as f:
        reached_fold_list = False
        for row in f:
            row = row.strip()
            if not row:
                reached_fold_list = True
            elif reached_fold_list:
                axis, val = row.split('=')
                folds.append((axis[-1], int(val)))
            else:
                points.add(tuple(map(int, row.split(','))))

    points = fold(points, *folds[0])
    # print_points(points)
    print(len(points))

