from collections import Counter, defaultdict


if __name__ == '__main__':
    counts = defaultdict(Counter)
    result = 0
    with open('d5_input.txt', 'r') as f:
        for row in f:
            p1, p2 = row.strip().split(' -> ')
            x1, y1 = map(int, p1.split(','))
            x2, y2 = map(int, p2.split(','))
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    counts[x1][y] += 1
                    if counts[x1][y] == 2:
                        result += 1
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    counts[x][y1] += 1
                    if counts[x][y1] == 2:
                        result += 1
            else:
                if abs(x1 - x2) != abs(y1 - y2):
                    raise Exception('DAFOX')
                inc_x = 2 * bool(x1 < x2) - 1
                inc_y = 2 * bool(y1 < y2) - 1
                curr_x, curr_y = x1, y1
                while True:
                    counts[curr_x][curr_y] += 1
                    if counts[curr_x][curr_y] == 2:
                        result += 1
                    if curr_x == x2 and curr_y == y2:
                        break
                    curr_x += inc_x
                    curr_y += inc_y

    print(result)

