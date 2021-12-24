from statistics import median

POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

CLOSERS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

OPENERS = {v: k for k, v in CLOSERS.items()}


def get_autocomplete_score(_input):
    stack = []
    for ch in _input:
        if ch in CLOSERS:
            if stack and stack[-1] == CLOSERS[ch]:
                stack.pop()
            else:
                # corrupted
                return None
        else:
            stack.append(ch)

    score = 0
    while stack:
        score = 5 * score + POINTS[OPENERS[stack.pop()]]
    return score


if __name__ == '__main__':
    scores = []
    with open('d10_input.txt', 'r') as f:
        for row in f:
            if (score := get_autocomplete_score(row.strip())) is not None:
                scores.append(score)
    print(median(scores))

