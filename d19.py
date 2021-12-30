import re
from collections import defaultdict

SCANNER_RE = re.compile(r'^--- scanner (\d+) ---$')


def get_transformation(source, target):
    mapping = {}
    signs = []
    for i in range(3):
        t = target[i]
        for j in range(3):
            s = source[j]
            if abs(s) == abs(t):
                mapping[i] = j
                signs.append(int(s / t))
                break

    return lambda x: [signs[i] * x[mapping[i]] for i in range(3)]


def compute_overlap(ref, new, pairs, scanners, point_positions, scanner_positions):
    corr = {}
    i = 0
    for i in range(len(pairs)):
        pair1 = pairs[i]
        if pair1[0].issubset(corr):
            continue
        for j in range(i + 1, len(pairs)):
            pair2 = pairs[j]
            if inter := pair1[0] & pair2[0]:
                source = next(iter(inter))
                if source in corr:
                    continue
                target = next(iter(pair1[1] & pair2[1]))
                corr[source] = target
                if pair1[0].issubset(corr):
                    break
        if len(corr) * (len(corr) - 1) // 2 == len(pairs):
            break

    # Figure out transformation
    for s1, t1 in corr.items():
        for s2, t2 in corr.items():
            if s1 == s2:
                continue
            vs1, vs2 = point_positions[ref][s1], point_positions[ref][s2]
            vt1, vt2 = scanners[new][t1], scanners[new][t2]
            diff1 = [a - b for a, b in zip(vs1, vs2)]
            if len(set(abs(x) for x in diff1)) < 3:
                # make sure all components are different
                continue
            diff2 = [a - b for a, b in zip(vt1, vt2)]
            transf = get_transformation(diff2, diff1)
            break
        else:
            continue
        break

    # Figure out scanner positions
    s, t = next(iter(corr.items()))
    scanner_positions[new] = [u - v for u, v in zip(point_positions[ref][s],
                                                    transf(scanners[new][t]))]

    point_positions[new] = [[u + v for u, v in zip(scanner_positions[new], transf(p))]
                            for p in scanners[new]]


if __name__ == '__main__':
    scanners = defaultdict(list)
    with open('d19_input.txt', 'r') as f:
        rows = iter(f)
        while True:
            num = int(SCANNER_RE.match(next(rows).strip()).groups()[0])
            try:
                while row := next(rows).strip():
                    scanners[num].append(list(map(int, row.split(','))))
            except StopIteration:
                break

    diffs = defaultdict(lambda: defaultdict(list))
    for num, points in scanners.items():
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                key = tuple(sorted(abs(points[i][idx] - points[j][idx]) for idx in range(3)))
                diffs[key][num].append(frozenset([i, j]))

    pairs = defaultdict(list)
    for v in diffs.values():
        for s1, p1 in v.items():
            for s2, p2 in v.items():
                # Hacky assumption that simplifies things
                assert len(p1) == len(p2) == 1
                if s1 == s2:
                    continue
                pairs[(s1, s2)].append([*p1, *p2])

    point_positions = {0: list(scanners[0])}
    scanner_positions = {0: [0, 0, 0]}
    while len(scanner_positions) < len(scanners):
        for s1 in scanner_positions:
            for s2 in scanners:
                if s2 in scanner_positions:
                    continue
                if len(pairs.get((s1, s2), [])) >= 66:
                    # 66 == (12 choose 2)
                    break
            else:
                continue
            break
        compute_overlap(s1, s2, pairs[(s1, s2)], scanners, point_positions, scanner_positions)

    unique_points = set()
    for points in point_positions.values():
        unique_points.update(tuple(p) for p in points)

    print(len(unique_points))

    farthest_apart = 0
    for v1 in scanner_positions.values():
        for v2 in scanner_positions.values():
            farthest_apart = max(farthest_apart, sum(abs(x - y) for x, y in zip(v1, v2)))
    print(farthest_apart)

