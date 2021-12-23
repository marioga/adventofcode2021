from statistics import median_low


if __name__ == '__main__':
    with open('d7_input.txt', 'r') as f:
        vals = list(map(int, f.readline().strip().split(',')))
    med = median_low(vals)
    print(med, sum(abs(val - med) for val in vals))
