import heapq
from functools import cache

TYPES = {ch: i for i, ch in enumerate('ABCD', 1)}
TYPES_INV = {k: v for v, k in TYPES.items()}
ENERGIES = {i: 10**(i - 1) for i in range(1, 5)}

HALLWAY_LENGTH = 11

REST_SPOTS = {0, 1, 3, 5, 7, 9, 10}
ENTRANCE_SPOTS = {i: 2 * i for i in range(1, 5)}

END_STATE = (*([0] * HALLWAY_LENGTH), 1, 1, 2, 2, 3, 3, 4, 4)
END_STATE_FOLDED = (*([0] * HALLWAY_LENGTH), 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4)


@cache
def get_neighbors(state, room_size):
    res = []
    # First deal with moves from hallway to room
    for idx in range(HALLWAY_LENGTH):
        if (val := state[idx]) == 0:
            continue
        entrance = ENTRANCE_SPOTS[val]
        if (idx < entrance and any(state[j] != 0 for j in range(idx + 1, entrance + 1))) or \
                (idx > entrance and any(state[j] != 0 for j in range(entrance, idx))):
            # Hallway to the entrance of room is not clear
            continue
        tentative = HALLWAY_LENGTH + room_size * val - 1
        done = False
        while not done and tentative >= HALLWAY_LENGTH + room_size * (val - 1):
            if state[tentative] == 0:
                dist_in_room = tentative - (HALLWAY_LENGTH + room_size * (val - 1)) + 1
                # empty room
                new_state = list(state)
                new_state[idx] = 0
                new_state[tentative] = val
                res.append((tuple(new_state), (dist_in_room + abs(idx - entrance)) * ENERGIES[val]))
                done = True
            elif state[tentative] != val:
                # room has a guy of different type
                break
            tentative -= 1

    # Now deal with moves from room to hallway; note that room to room moves
    # are split into two consecutive moves (this is fine)
    for r in range(room_size):
        for c in range(4):
            idx = HALLWAY_LENGTH + room_size * c + r
            if (val := state[idx]) == 0:
                continue
            if r >= 1 and state[idx - 1] != 0:
                # blocked by another guy in room
                continue
            entrance = ENTRANCE_SPOTS[c + 1]
            # move backwards and forward
            for sgn in [-1, 1]:
                dist = 1
                while 0 <= (target := entrance + sgn * dist) < HALLWAY_LENGTH and \
                        state[target] == 0:
                    if target in REST_SPOTS:
                        # can move here
                        new_state = list(state)
                        new_state[idx] = 0
                        new_state[target] = val
                        res.append((tuple(new_state), (1 + r + dist) * ENERGIES[val]))
                    dist += 1

    return res


def find_best_path(initial, room_size=2, end_state=END_STATE):
    energies = {initial: 0}
    prev = {initial: None}

    states = [(0, initial)]
    visited = set()
    while states:
        energy, curr = heapq.heappop(states)
        if curr == end_state:
            break
        # lazy approach to dijkstra
        if curr in visited:
            continue
        visited.add(curr)
        for nxt, weight in get_neighbors(curr, room_size):
            if nxt not in energies or energy + weight < energies[nxt]:
                energies[nxt] = energy + weight
                prev[nxt] = curr
                heapq.heappush(states, (energy + weight, nxt))

    return energies, prev


def print_from_state(state, room_size=2):
    rows = [['#'] * (HALLWAY_LENGTH + 2) for _ in range(3 + room_size)]
    for idx in range(HALLWAY_LENGTH):
        val = state[idx]
        rows[1][idx + 1] = TYPES_INV.get(val, '.')
    for r in range(room_size):
        for c in range(4):
            val = state[HALLWAY_LENGTH + r + room_size * c]
            rows[2 + r][3 + 2 * c] = TYPES_INV.get(val, '.')
    for r in range(3, 3 + room_size):
        for c in range(2):
            rows[r][c] = ' '
            rows[r][-c - 1] = ' '
    for row in rows:
        print(''.join(row))


def print_path(prev, room_size=2, end_state=END_STATE):
    curr = end_state
    path = []
    while curr:
        path.append(curr)
        curr = prev[curr]

    for state in path[::-1]:
        print_from_state(state, room_size=room_size)
        print()


if __name__ == '__main__':
    with open('d23_input.txt', 'r') as f:
        rows = iter(f)
        next(rows)
        initial = [0 for ch in next(rows).strip() if ch == '.']
        assert len(initial) == HALLWAY_LENGTH
        initial_folded = initial.copy()
        initial.extend([0] * 8)
        # hardcoded
        initial_folded.extend([0, 4, 4, 0, 0, 3, 2, 0, 0, 2, 1, 0, 0, 1, 3, 0])
        for r in range(2):
            c = 0
            for ch in next(rows).strip():
                if ch in TYPES:
                    initial[HALLWAY_LENGTH + 2 * c + r] = TYPES[ch]
                    initial_folded[HALLWAY_LENGTH + 4 * c + 3 * r] = TYPES[ch]
                    c += 1
    energies, prev = find_best_path(tuple(initial))
    print_path(prev)
    print(energies[END_STATE])

    energies, prev = find_best_path(tuple(initial_folded), room_size=4, end_state=END_STATE_FOLDED)
    print_path(prev, room_size=4, end_state=END_STATE_FOLDED)
    print(energies[END_STATE_FOLDED])

