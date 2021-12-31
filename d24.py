from functools import reduce

OPERATIONS = {
    'add': lambda a, b: a + b,
    'mul': lambda a, b: a * b,
    'div': lambda a, b: int(a / b),
    'mod': lambda a, b: a % b,
    'eql': lambda a, b: int(a == b)
}

VAR_TO_POS = {v: p for p, v in dict(enumerate('wxyz')).items()}


def operate(input_block, input_val, initial=None):
    res = list(initial) if initial is not None else [0] * 4
    input_pos, operations = input_block
    res[input_pos] = input_val
    for op, (v1, (t2, v2)) in operations:
        res[v1] = op(res[v1], res[v2] if t2 == 1 else v2)
    return tuple(res)


def generate(width=14, depth=0, res=None):
    if depth == 0:
        res = []
    for digit in range(9, 0, -1):
        res.append(digit)
        if depth == width - 1:
            yield res
        else:
            yield from generate(width, depth + 1, res)
        res.pop()


if __name__ == '__main__':
    input_blocks = []
    with open('d24_input.txt', 'r') as f:
        data = []
        for row in f:
            parsed = row.strip().split()
            if len(parsed) == 2:
                assert parsed[0] == 'inp'
                input_blocks.append((VAR_TO_POS[parsed[1]], []))
            else:
                op, v1, v2 = parsed
                # v2 can be a variable or scalar
                parsed_v2 = (1, VAR_TO_POS[v2]) if v2 in VAR_TO_POS else (0, int(v2))
                if op == 'add' and v1 in 'xy' and parsed_v2[0] == 0:
                    data.append(row.strip())
                input_blocks[-1][1].append((OPERATIONS[op], (VAR_TO_POS[v1], parsed_v2)))
            if len(data) == 4:
                print(data[0], data[-1])
                data.clear()

    # solved manually
    # algorithm can be inferred from blocks from printed data; it imposes conditions on w
    max_vals = [2, 9, 5, 9, 9, 4, 6, 9, 9, 9, 1, 7, 3, 9]
    min_vals = [1, 7, 1, 5, 3, 1, 1, 4, 6, 9, 1, 1, 1, 8]
    for vals in [max_vals, min_vals]:
        initial = None
        for val, input_block in zip(vals, input_blocks):
            initial = operate(input_block, val, initial)
            print(initial)
        print(reduce(lambda x, y: 10 * x + y, vals))
        print()
