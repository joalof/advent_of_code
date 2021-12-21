class SnailNumber:
    """Data maps regular numbers to their level of nesting. """
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_expression(cls, expression):
        data = {}
        nesting = 0
        for c in expression:
            if c == '[':
                nesting += 1
            elif c.isnumeric():
                data[int(c)] = nesting
            elif c == ']':
                nesting -= 1
            else:
                continue
        return cls(data)

    def to_expression(self):
        pass

    def __eq__(self, other):
        return self.data == other.data

    # def __add__(self, other):
    #     data_new = self.data | other.data
    #     for rn in data_new:
    #         data_new[rn] += 1
    #     return SnailNumber(data_new)


    def __repr__(self):
        return self.data.__repr__()


if __name__ == '__main__':
    a = SnailNumber({1: 1, 2: 1})
    b = SnailNumber({3: 2, 4: 2, 5: 1})

    c = SnailNumber.from_expression('[[3,4],5]')
    print(c == b)
