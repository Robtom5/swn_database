#! /usr/bin/env python3
import string
import re
import operator
import random
from collections import namedtuple


class Coordinate(object):
    _coordinate_pattern = re.compile(
        r'^(?P<letter>[a-zA-Z]+)(?P<number>[0-9]+)$')

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def From_Hex(cls, hex_string):
        match = Coordinate._coordinate_pattern.match(hex_string)
        if not match:
            raise ValueError("Invalid hex string")

        letters = match.group('letter')
        number = int(match.group('number'))

        letter_values = [string.ascii_lowercase.index(
            letter.lower()) + 1 for letter in letters]

        letter = 0
        for letter_value in letter_values:
            letter = letter * 26 + letter_value

        x = letter
        y = number
        return Coordinate(x, y)

    def __str__(self):
        letters = [self.x % 26]
        x_value = self.x

        while x_value > 26:
            x_value = x_value // 26
            letters.append(x_value % 26)

        letters.reverse()
        letter_representation = ''.join(
            [string.ascii_uppercase[letter - 1] for letter in letters])

        return f"{letter_representation}{self.y}"


class DiceRoll(object):
    _diceroll_pattern = re.compile(r'(?P<count>[0-9]*)d(?P<sides>[0-9]+)')
    _constant_pattern = re.compile(r'(?P<op>[+-]+)(?P<value>[0-9]+)')
    _operators = {"+": operator.add, "-": operator.sub}

    def __init__(self, rollString: str ="1d6", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roll_string = rollString

    @property
    def roll_string(self):
        return self._roll_String

    @roll_string.setter
    def roll_string(self, newRollString: str):
        if not DiceRoll._diceroll_pattern.match(newRollString):
            raise ValueError("Invalid roll string")
        self._roll_String = newRollString.replace(" ", "")
        self._Calculate_Offset()

    def Roll(self):
        total = self._offset
        for rollspec in re.finditer(DiceRoll._diceroll_pattern, self.roll_string):
            count = int(rollspec.group('count') or '1')
            sides = int(rollspec.group('sides'))
            total = total + sum([DiceRoll._Roll_Die(sides)
                                 for i in range(count)])

        return total

    def _Roll_Die(sides):
        return random.randint(1, sides)

    def _Calculate_Offset(self):
        offset = 0
        cleaned_string = DiceRoll._diceroll_pattern.sub(' ', self.roll_string)
        for constant in DiceRoll._constant_pattern.finditer(cleaned_string):
            value = int(constant.group('value'))
            offset = DiceRoll._operators[constant.group('op')](offset, value)
        self._offset = offset
