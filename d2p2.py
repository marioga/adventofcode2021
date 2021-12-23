if __name__ == '__main__':
    aim, total_x, total_y = 0, 0, 0
    with open('d2_input.txt', 'r') as f:
        for row in f:
            d, c = row.strip().split()
            c = int(c)
            if d == 'forward':
                total_x += c
                total_y += aim * c
            elif d == 'down':
                aim += c
            elif d == 'up':
                aim -= c
            else:
                raise Exception('DAFOX')

    print(total_x, total_y, total_x * total_y)

