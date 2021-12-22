import math
import functools
import operator
import itertools
import ast


def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    return lines


class SnailNumber:
    """Represent a snail number by the regular numbers and their nesting level."""
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

    def __eq__(self, other):
        return self.numbers == other.numbers and self.levels == other.levels

    def __add__(self, other):
        numbers = self.numbers + other.numbers
        levels = [l + 1 for l in self.levels + other.levels]
        snail_number = SnailNumber.from_data(numbers, levels)
        snail_number.reduce()
        return snail_number

    def __str__(self):
        return f'Numbers: {self.numbers}\nLevels: {self.levels}'

    def explode(self, i):
        """Explodes pair starting at regular number i. """
        numbers = self.numbers
        levels = self.levels
        if i > 0:
            numbers[i - 1] += numbers[i]
        if i < len(numbers) - 2:
            numbers[i + 2] += numbers[i + 1]
        numbers[i] = 0
        levels[i] -= 1
        numbers.pop(i + 1)
        levels.pop(i + 1)

    def split(self, i):
        """Splits pair at regular number i. """
        numbers = self.numbers
        levels = self.levels
        num, level = numbers[i], levels[i]
        self.numbers = (
            numbers[:i]
            + [math.floor(0.5*num), math.ceil(0.5*num)]
            + numbers[i + 1:]
        )
        self.levels = (
            levels[:i]
            + [level + 1]*2
            + levels[i + 1:]
        )

    def reduce(self):
        """Assume that at nesting level 5 there are only ever regular pairs. """
        while True:
            for i in range(len(self.levels)):
                if self.levels[i] == 5 == self.levels[i + 1]:
                    self.explode(i)
                    break
            else:
                for i in range(len(self.levels)):
                    if self.numbers[i] >= 10:
                        self.split(i)
                        break
                else:
                    return

    # def reduced_to_list(self):
    #     """Transforms a reduced number to list format. """
    #     if len(self.numbers) == 1:
    #         return self.numbers
    #     pairs = []
    #     for i in range(len(self.numbers)//2):
    #         pairs.append(self.numbers[2*i:2*(i + 1)])
    #     level_last = self.levels[0]
    #     expression = '[' * level_last
    #     expression += f'{pairs[0][0]},{pairs[0][1]}'
    #     consecutive = 0
    #     for i, pair in enumerate(pairs[1:]):
    #         level = self.levels[(i + 1)*2] 
    #         diff = level - level_last
    #         if diff == 0:
    #             consecutive += 1
    #             if consecutive == 2:
    #                 consecutive = 0
    #                 expression += ']],[['
    #             else: 
    #                 expression += '],['
    #         elif diff > 0:
    #             expression += '],[' + '['*diff
    #         elif diff < 0:
    #             expression += ']'*abs(diff) + '],['

    #         expression += f'{pair[0]},{pair[1]}'
    #         level_last = level
    #     expression += ']'*level_last
    #     snail_list = ast.literal_eval(expression)
    #     return snail_list

    # def to_list_tmp(self):
    #     """Transforms a reduced number to list format. """
    #     if len(self.numbers) == 1:
    #         return self.numbers
    #     pairs = []
    #     for i in range(len(self.numbers)//2):
    #         pairs.append(self.numbers[2*i:2*(i + 1)])
    #     pairs = functools.reduce(self.join, pairs)
    #     return pairs

    # def join(self, left, right):
    #     return [left, right]

    # def magnitude(self):
    #     if len(self.numbers) == 1:
    #         return self.numbers[0]
    #     else:
    #         snail_list = self.reduced_to_list()
    #         left = SnailNumber(str(snail_list[0]))
    #         right = SnailNumber(str(snail_list[1]))
    #         mag = 3*left.magnitude() + 2*right.magnitude()
    #     return mag

    def magnitude(self):
        levels = self.levels
        numbers = self.numbers
        level_max = max(levels)
        number_pairs = pair_up(numbers)
        pairs_at_level = {}
        for lev in range(level_max, -1, -1):
            pairs_at_level[lev] = [
                p for i, p in enumerate(number_pairs) if levels[i*2] == lev
            ]
        for lev in range(level_max, 0, -1):
            pairs_at_level[lev] = [3*p[0] + 2*p[1] for p in pairs_at_level[lev]]
            pairs_at_level[lev - 1] = pair_up(
                pairs_at_level[lev]
            ) + pairs_at_level[lev - 1]
        return pairs_at_level[1][0]

def pair_up(iterable):
    return [iterable[2*i:2*(i+1)] for i in range(len(iterable)//2)]


if __name__ == "__main__":

    lines = parse_input('./test.txt')
    snail_numbers = [SnailNumber(expression) for expression in lines]

    # Part I
    a = functools.reduce(operator.add, snail_numbers)
    # print(a)
    print(a.magnitude())

    # sn = SnailNumber('[[[[5,0],[7,4]],[5,5]],[6,6]]')
    # print(sn)
    # print(sn.to_list_tmp())
