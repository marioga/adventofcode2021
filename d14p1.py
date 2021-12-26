from __future__ import annotations
from collections import Counter
from dataclasses import dataclass

STEPS = 10

@dataclass
class Node:
    val: str = None
    nxt: Node = None

    def print_children(self):
        # prints after current node; useful for debugging
        curr = self.nxt
        vals = []
        while curr:
            vals.append(curr.val)
            curr = curr.nxt
        print(" -> ".join(vals))

    def step(self, rules):
        curr = self.nxt
        if not (curr and curr.nxt):
            return
        nxt = curr.nxt

        while nxt:
            node = Node(rules[(curr.val, nxt.val)], nxt)
            curr.nxt = node
            curr = nxt
            nxt = nxt.nxt

    def get_counts(self):
        curr = self.nxt
        counts = Counter()

        while curr:
            counts[curr.val] += 1
            curr = curr.nxt

        return counts


if __name__ == '__main__':
    head = Node()
    rules = {}
    with open('d14_input.txt', 'r') as f:
        rows = iter(f)
        tail = head
        for val in next(rows).strip():
            node = Node(val)
            tail.nxt = node
            tail = node
        next(rows)
        for row in rows:
            s, t = row.strip().split(' -> ')
            rules[tuple(s)] = t

    for _ in range(STEPS):
        head.step(rules)

    counts = head.get_counts()
    _min, _max = min(counts.values()), max(counts.values())
    print(_min, _max, _max - _min)

