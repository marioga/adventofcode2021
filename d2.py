def get_position(_input):
    total_x, total_y = 0, 0
    for d, c in _input:
        if d == 'forward':
            total_x += c
        elif d == 'down':
            total_y += c
        elif d == 'up':
            total_y -= c
        else:
            raise Exception('DAFOX')
    return total_x, total_y


def get_position_with_aim(_input):
    aim, total_x, total_y = 0, 0, 0
    for d, c in _input:
        if d == 'forward':
            total_x += c
            total_y += aim * c
        elif d == 'down':
            aim += c
        elif d == 'up':
            aim -= c
        else:
            raise Exception('DAFOX')
    return total_x, total_y


if __name__ == '__main__':
    rows = []
    with open('d2_input.txt', 'r') as f:
        for row in f:
            d, c = row.strip().split()
            rows.append((d, int(c)))

    total_x, total_y = get_position(rows)
    print(total_x * total_y)

    total_x, total_y = get_position_with_aim(rows)
    print(total_x * total_y)
