class SnailNumber:
    """Data is a list of 2-elements lists: [number, nesting level]"""
    def __init__(self, expression):
        numbers = []
        levels = []
        level = 0
        for c in expression:
            if c == "[":
                level += 1
            elif c.isnumeric():
                numbers.append(int(c))
                levels.append(level)
            elif c == "]":
                level -= 1
            else:
                continue
        self.numbers = numbers
        self.levels = levels

    @classmethod
    def from_data(cls, numbers, levels):
        self = cls.__new__(cls)
        self.numbers = numbers
        self.levels = levels
        return self

    def to_expression(self):
        pass

    def __eq__(self, other):
        return self.numbers == other.numbers and self.levels == other.levels

    def __add__(self, other):
        numbers = self.numbers + other.numbers
        levels = [l + 1 for l in self.levels + other.levels]
        return SnailNumber.from_data(numbers, levels)

    def __repr__(self):
        return repr([(n, l) for n, l in zip(self.numbers, self.levels)])

    def explode(self, i):
        numbers = self.numbers
        levels = self.levels
        if i > 0:
            numbers[i - 1] += numbers[i]
        if i < len(numbers) - 1:
            numbers[i + 2] += numbers[i + 1]
        numbers[i] = 0
        levels[i] -= 1
        numbers.pop(i + 1)
        levels.pop(i + 1)

    def split(self, i):
        numbers = self.numbers
        levels = self.levels
        num, level = numbers[i], levels[i]
        # numbers = (
        #     numbers[:i]
        #     + [num // 2, num // 2 + 1]
        #     + numbers[i + 1 :]
        # )


if __name__ == "__main__":
    a = SnailNumber([[1, 1], [2, 1]])
    b = SnailNumber([[3, 2], [4, 2], [5, 1]])

    # ab = SnailNumber.from_expression('[[1, 2], [[3,4],5]]')
    # print(a + b == ab)
    # print(ab)

    a = SnailNumber.from_expression("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    a.explode(0)
    a.explode(4)
    # a.split(
    print(a)
