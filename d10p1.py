POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

PARTNERS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}


def get_syntax_error_score(_input):
    stack = []
    for ch in _input:
        if ch in PARTNERS:
            if stack and stack[-1] == PARTNERS[ch]:
                stack.pop()
            else:
                return POINTS[ch]
        else:
            stack.append(ch)
    return 0


if __name__ == '__main__':
    total = 0
    with open('d10_input.txt', 'r') as f:
        for row in f:
            total += get_syntax_error_score(row.strip())
    print(total)

