from collections import Counter, defaultdict

BINGO_SIZE = 5


if __name__ == '__main__':
    num_to_pos = defaultdict(list)
    board_numbers = defaultdict(set)

    with open('d4_input.txt', 'r') as f:
        it_f = iter(f)
        draw = map(int, next(it_f).strip().split(','))

        board = 0
        while True:
            try:
                next(it_f)
            except StopIteration:
                break

            for row in range(BINGO_SIZE):
                for col, val in enumerate(map(int, next(it_f).strip().split())):
                    num_to_pos[val].extend([(row, True, board), (col, False, board)])
                    board_numbers[board].add(val)

            board += 1

    pos_to_completion = Counter()

    for val in draw:
        for pos in num_to_pos[val]:
            board_numbers[pos[2]].discard(val)
            pos_to_completion[pos] += 1
            if pos_to_completion[pos] == BINGO_SIZE:
                sum_unmarked = sum(board_numbers[pos[2]])
                print(sum_unmarked, val, sum_unmarked * val)
                break
        else:
            continue
        break

