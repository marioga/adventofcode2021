from dataclasses import dataclass
from functools import cache
from itertools import product


class DeterministicDie:
    def __init__(self, size=100):
        self.state = 1
        self.size = size
        self._rolls = 0

    @property
    def rolls(self):
        return self._rolls

    def roll(self, count=3):
        self._rolls += count
        ret = 0
        for _ in range(count):
            ret += self.state
            self.state = self.state % self.size + 1
        return ret


def play(start_pos, die):
    curr_pos = start_pos.copy()
    points = [0, 0]
    while True:
        for player in range(2):
            roll = die.roll()
            curr_pos[player] = (curr_pos[player] + roll - 1) % 10 + 1
            points[player] += curr_pos[player]
            if points[player] >= 1000:
                return points


# cache this globally
DIE_OUTCOMES = [sum(p) for p in product(range(1, 4), repeat=3)]


@cache
def compute_wins(curr_pos, other_pos, curr_score, other_score):
    if curr_score >= 21:
        return [1, 0]
    if other_score >= 21:
        return [0, 1]

    tally = [0, 0]
    for roll in DIE_OUTCOMES:
        new_curr_pos = (curr_pos + roll - 1) % 10 + 1
        new_curr_score = curr_score + new_curr_pos
        new_tally = compute_wins(other_pos, new_curr_pos, other_score, new_curr_score)
        tally[0] += new_tally[1]
        tally[1] += new_tally[0]
    return tally


if __name__ == '__main__':
    start_pos = []
    with open('d21_input.txt', 'r') as f:
        rows = iter(f)
        for _ in range(2):
            start_pos.append(int(next(rows).strip().split(': ')[1]))

    die = DeterministicDie()
    final_points = play(start_pos, die)
    print(min(final_points) * die.rolls)

    # Now we are dealing with part 2
    # Encode a state as a 4-tuple: (curr_pos, other_pos, curr_score, other_score)
    tally = compute_wins(*start_pos, 0, 0)
    print(tally, max(tally))

