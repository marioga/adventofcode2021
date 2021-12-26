from collections import defaultdict

START_NODE = 'start'
END_NODE = 'end'


def count_paths(node, graph, small, visited, small_visited_twice, path):
    # keep track of path for fun
    if node == END_NODE:
        path.append(END_NODE)
        print(",".join(path))
        path.pop()
        return 1

    if node in small:
        visited.add(node)
    path.append(node)
    count = 0
    for nxt in graph.get(node, []):
        if nxt in visited:
            if nxt != START_NODE and small_visited_twice is None:
                count += count_paths(nxt, graph, small, visited, nxt, path)
            continue
        count += count_paths(nxt, graph, small, visited, small_visited_twice, path)
    if node != small_visited_twice:
        visited.discard(node)
    path.pop()
    return count


if __name__ == '__main__':
    graph = defaultdict(list)
    small = set()
    with open('d12_input.txt', 'r') as f:
        for row in f:
            s, t = row.strip().split('-')
            graph[s].append(t)
            graph[t].append(s)
            if s == s.lower():
                small.add(s)
            if t == t.lower():
                small.add(t)
    print(count_paths(START_NODE, graph, small, set(), None, []))

