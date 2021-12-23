import math

TOTAL_TIME = 256
CYCLE_TIME = 7
NEWBORN_CYCLE_TIME = 8


if __name__ == '__main__':
    to_process = []
    with open('d6_input.txt', 'r') as f:
        for val in map(int, f.readline().strip().split(',')):
            to_process.append((val, TOTAL_TIME))

    count = 0
    while to_process:
        count += 1
        initial, _time = to_process.pop()

        curr_time = _time - initial - 1
        while curr_time >= 0:
            to_process.append((NEWBORN_CYCLE_TIME, curr_time))
            curr_time -= CYCLE_TIME
    print(count)
