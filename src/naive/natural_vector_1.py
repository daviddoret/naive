from typing import List
from src.naive.flatten import flatten
from src.naive.coerce import coerce
from src.naive.natural_number_1 import NaturalNumber1


class NaturalVector1(List[NaturalNumber1]):
    def __new__(cls, *args):
        flat_input = flatten(*args)
        coerced_list = []
        for n in flat_input:
            n = coerce(n, NaturalNumber1)
            coerced_list.append(n)
        return super().__new__(cls, coerced_list)

    def __str__(self) -> str:
        return '{' + ', '.join(map(str, self)) + '}'

    def __repr__(self) -> str:
        return self.__str__()
