TO_COUNT = {1, 4, 7, 8}

#  aaaa
# b    c
# b    c
#  dddd
# e    f
# e    f
#  gggg

MAPPING = {
    frozenset(['a', 'b', 'c', 'e', 'f', 'g']) : 0,
    frozenset(['c', 'f']) : 1,
    frozenset(['a', 'c', 'd', 'e', 'g']) : 2,
    frozenset(['a', 'c', 'd', 'f', 'g']) : 3,
    frozenset(['b', 'c', 'd', 'f']) : 4,
    frozenset(['a', 'b', 'd', 'f', 'g']) : 5,
    frozenset(['a', 'b', 'd', 'e', 'f', 'g']) : 6,
    frozenset(['a', 'c', 'f']) : 7,
    frozenset(['a', 'b', 'c', 'd', 'e', 'f', 'g']) : 8,
    frozenset(['a', 'b', 'c', 'd', 'f', 'g']) : 9,
}



def solve(sample, target):
    by_size = {}
    for s in sample:
        by_size.setdefault(len(s), set()).add(s)

    one = next(iter(by_size[2]))
    seven = next(iter(by_size[3]))
    four = next(iter(by_size[4]))
    eight = next(iter(by_size[7]))

    corr = {}
    # 7 - 1 gives you top segment a
    corr[next(iter(seven - one))] = 'a'

    # 1 - 6 gives you c; the other segment in 1 is f
    # 9 - 4 - 7 gives you g; 8 - 9 gives you e
    for num in by_size[6]:
        if diff := one - num:
            # 6 is the only one that satisfies this
            corr[next(iter(diff))] = 'c'
            corr[next(iter(one - diff))] = 'f'
        elif four.issubset(num):
            # 9 is the only one that satisfies this
            diff = num - four - seven
            corr[next(iter(diff))] = 'g'
            diff = eight - num
            corr[next(iter(diff))] = 'e'
        else:
            # if we are here, we are dealing with 0
            diff = eight - num
            corr[next(iter(diff))] = 'd'

    # Finally figure out b
    for ch in four:
        if ch not in corr:
            corr[ch] = 'b'
            break

    return [MAPPING[frozenset([corr[ch] for ch in tt])] for tt in target]



if __name__ == '__main__':
    count = 0
    with open('d8_input.txt', 'r') as f:
        for row in f:
            sample, target = map(lambda x: x.split(), row.strip().split(' | '))
            sample = list(map(frozenset, sample))
            target = list(map(frozenset, target))
            sols = solve(sample, target)
            count += sum(1 for x in sols if x in TO_COUNT)
    print(count)

