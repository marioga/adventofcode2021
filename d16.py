from functools import reduce


class Packet:
    def __init__(self, binary_input):
        self.version = None
        self.type_id = None
        self.length = 0

        self.value = None
        self.tail = None

        self._children = []

        self._parse(binary_input)

    @classmethod
    def from_hex(cls, _input):
        return cls("".join(f"{int(hex_digit, 16):04b}" for hex_digit in _input))

    def _parse(self, binary_input):
        self.version = int(binary_input[:3], 2)
        self.type_id = int(binary_input[3:6], 2)
        self.length = 6
        if self.type_id == 4:
            # Literal
            value = []
            for idx in range(6, len(binary_input), 5):
                leading, chunk = binary_input[idx], binary_input[idx + 1:idx + 5]
                value.append(chunk)
                self.length += 5
                if leading == '0':
                    break
            self.value = int("".join(value), 2)
            self.tail = binary_input[idx + 5:]
        else:
            # Operator
            length_type_id = binary_input[6]
            length, count = None, None
            if length_type_id == '0':
                # Next 15 bits
                length = int(binary_input[7:22], 2)
                self.tail = binary_input[22:]
                self.length = 22
            else:
                # Next 11 bits
                count = int(binary_input[7:18], 2)
                self.tail = binary_input[18:]
                self.length = 18

            while True:
                child = self.__class__(self.tail)
                self.length += child.length
                self.tail = child.tail
                self._children.append(child)

                if length is not None:
                    length -= child.length
                    if length == 0:
                        break
                else:
                    count -= 1
                    if count == 0:
                        break
            self._compute_operator_value()

    def _compute_operator_value(self):
        children_vals = (child.value for child in self._children)
        if self.type_id == 0:
            self.value = sum(children_vals)
        elif self.type_id == 1:
            self.value = reduce(lambda a, b: a * b, children_vals)
        elif self.type_id == 2:
            self.value = min(children_vals)
        elif self.type_id == 3:
            self.value = max(children_vals)
        elif self.type_id == 5:
            assert len(self._children) == 2
            self.value = int(self._children[0].value > self._children[1].value)
        elif self.type_id == 6:
            assert len(self._children) == 2
            self.value = int(self._children[0].value < self._children[1].value)
        elif self.type_id == 7:
            assert len(self._children) == 2
            self.value = int(self._children[0].value == self._children[1].value)


    def __repr__(self):
        children_chunk = ""
        if self._children:
            # Operator
            children_chunk = rf" | Children: [{', '.join(repr(child) for child in self._children)}]"

        return rf"<Ver: {self.version} -- Type ID: {self.type_id} -- Value: {self.value}{children_chunk}>"

    def __iter__(self):
        yield self
        for child in self._children:
            yield from iter(child)

if __name__ == '__main__':
    with open('d16_input.txt', 'r') as f:
        packet = Packet.from_hex(f.readline().strip())

    for test_packet in ["C200B40A82",
                        "04005AC33890",
                        "880086C3E88112",
                        "CE00C43D881120",
                        "D8005AC2A8F0",
                        "F600BC2D8F",
                        "9C005AC2F8F0",
                        "9C0141080250320F1802104A08"]:
        print(Packet.from_hex(test_packet))

    print(sum(p.version for p in packet))
    print(packet.value)
