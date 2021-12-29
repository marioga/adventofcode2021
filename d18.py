from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Node:
    _type: str = 'interval'
    val: int = None
    left: Node = None
    right: Node = None

    @classmethod
    def from_string(cls, _input, offset=0):
        if _input[offset] == '[':
            left, end_offset = cls.from_string(_input, offset + 1)
            # skip comma
            right, end_offset = cls.from_string(_input, end_offset + 1)
            # skip final ']'
            return cls(left=left, right=right), end_offset + 1

        end_offset = offset
        while _input[end_offset + 1].isdigit():
            end_offset += 1
        return cls(_type='literal', val=int(_input[offset:end_offset + 1])), end_offset + 1

    @property
    def is_pair(self):
        return self._type == 'interval' and self.left and self.left._type == 'literal' and \
            self.right and self.right._type == 'literal'

    def find_reduceable(self):
        prev_literal, next_literal, to_explode, to_split = None, None, None, None

        def traverse(node, depth_left=4):
            nonlocal prev_literal, next_literal, to_explode, to_split
            if next_literal is not None:
                # Short circuit early since we have everything we want
                return

            if node._type == 'literal':
                if to_explode is None:
                    prev_literal = node
                    if to_split is None and node.val >= 10:
                        to_split = node
                else:
                    next_literal = node
                return

            if node.is_pair and depth_left <= 0 and to_explode is None:
                to_explode = node
                return

            if node.left:
                traverse(node.left, depth_left - 1)
            if node.right:
                traverse(node.right, depth_left - 1)

        traverse(self)
        return prev_literal, next_literal, to_explode, to_split

    def reduce(self):
        while True:
            prev_literal, next_literal, to_explode, to_split = self.find_reduceable()
            if to_explode is not None:
                # Explode
                if prev_literal:
                     prev_literal.val += to_explode.left.val
                if next_literal:
                     next_literal.val += to_explode.right.val
                to_explode._type = 'literal'
                to_explode.val = 0
                to_explode.left = None
                to_explode.right = None
            elif to_split is not None:
                # Split
                prev_val = to_split.val
                to_split._type = 'interval'
                to_split.val = None
                to_split.left = self.__class__(_type='literal', val=(prev_val // 2))
                to_split.right = self.__class__(_type='literal', val=((prev_val + 1) // 2))
            else:
                break

    def __str__(self):
        if self._type == 'literal':
            return str(self.val)
        return f'[{self.left},{self.right}]'

    def __add__(self, other):
        return self.__class__(left=self.copy(), right=other.copy())

    @property
    def magnitude(self):
        if self._type == 'literal':
            return self.val
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def copy(self):
        left = self.left.copy() if self.left else None
        right = self.right.copy() if self.right else None
        return self.__class__(_type=self._type, val=self.val, left=left, right=right)


if __name__ == '__main__':
    nums = []
    with open('d18_input.txt', 'r') as f:
        for row in f:
            curr, _ = Node.from_string(row.strip())
            nums.append(curr)

    res = nums[0]
    for num in nums[1:]:
        res += num
        res.reduce()
    print(res.magnitude)

    best = 0
    for num1, num2 in combinations(nums, 2):
        curr1 = num1 + num2
        curr1.reduce()
        curr2 = num2 + num1
        curr2.reduce()
        best = max(best, curr1.magnitude, curr2.magnitude)
    print(best)


