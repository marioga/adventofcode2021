from functools import lru_cache

TOTAL_TIME = 256
CYCLE_TIME = 7
NEWBORN_CYCLE_TIME = 8


@lru_cache(None)
def offspring_size(initial, time_left):
    total = 1
    curr_time_left = time_left - initial - 1
    while curr_time_left >= 0:
        total += offspring_size(NEWBORN_CYCLE_TIME, curr_time_left)
        curr_time_left -= CYCLE_TIME
    return total


if __name__ == '__main__':
    total = 0
    with open('d6_input.txt', 'r') as f:
        for val in map(int, f.readline().strip().split(',')):
            total += offspring_size(val, TOTAL_TIME)
    print(total)
