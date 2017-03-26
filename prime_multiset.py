# -*- coding: utf-8 -*-

import functools
import math
import operator
from typing import Iterable


class PrimeMultiset:
    """
    Multiset of prime numbers, stored as a single integer. It only
    supports a couple of operations compared to a regular multiset
    class. Storing anything else than prime numbers won't produce
    an error (prime checks are expensive), but the semantics in
    such a case aren't guaranteed.

    Operations are based on the fact that any positive integer can
    represent a multiset of prime number, an that specific integer
    operations can be used to perform prime multiset operations.
    """
    def __init__(self, sequence: Iterable[int]=(), initial_value: int=1):
        """
        Initialize the multiset with an initial value and a list of
        primes. The initial_value parameter can be any positive integer
        and corresponds to a prime multiset to which elements will be
        added. The sequence parameter corresponds to an iterable of prime
        numbers to be added to the multiset.
        
        If both sequence and initial_value are provided, the prime numbers
        in sequence will be added to initial_value.
        
        :param sequence: iterable sequence of prime numbers
        :param initial_value: initial multiset value
        """
        self.value = functools.reduce(operator.mul, sequence, initial_value)

    ##################################################
    # Usual multiset operations

    def __and__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        return PrimeMultiset(initial_value=math.gcd(self.value, other.value))

    def __iand__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        self.value = math.gcd(self.value, other.value)
        return self

    def __or__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        return PrimeMultiset(initial_value=self.__lcm(self.value, other.value))

    def __ior__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        self.value = self.__lcm(self.value, other.value)
        return self

    def __add__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        return PrimeMultiset(initial_value=self.value * other.value)

    def __iadd__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        self.value *= other.value
        return self

    def __sub__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        return PrimeMultiset(initial_value=self.value // (self & other).value)

    def __isub__(self, other: 'PrimeMultiset') -> 'PrimeMultiset':
        self.value //= (self & other).value
        return self

    ##################################################
    # Multiset equality operations

    def __eq__(self, other: 'PrimeMultiset') -> bool:
        return self.value == other.value

    def __ne__(self, other: 'PrimeMultiset') -> bool:
        return self.value != other.value

    ##################################################
    # Multiset inclusion operations

    def __lt__(self, other: 'PrimeMultiset') -> bool:
        return self <= other and self != other

    def __le__(self, other: 'PrimeMultiset') -> bool:
        return other.value % self.value == 0

    def __gt__(self, other: 'PrimeMultiset') -> bool:
        return self >= other and self != other

    def __ge__(self, other: 'PrimeMultiset') -> bool:
        return self.value % other.value == 0

    ##################################################
    # Modifying operations

    def add(self, element: int) -> None:
        self.value *= element

    def remove(self, element: int) -> None:
        quotient, remainder = divmod(self.value, element)
        if remainder != 0:
            raise KeyError(element)
        self.value = quotient

    def discard(self, element: int) -> None:
        quotient, remainder = divmod(self.value, element)
        if remainder == 0:
            self.value = quotient

    def clear(self) -> None:
        self.value = 1

    ##################################################
    # Non-modifying operations

    def is_empty(self) -> bool:
        """
        Returns whether the multiset is empty or not.
        
        Computing the length of a prime multiset is expensive since it
        requires prime decomposition, so we can't use the idiomatic
        len(prime_multiset) to check whether the multiset is empty.
        """
        return self.value == 1

    def __contains__(self, element: int) -> bool:
        return self.value % element == 0

    ##################################################
    # Helper functions

    @staticmethod
    def __lcm(lhs: int, rhs: int) -> int:
        # Least common multiple
        return lhs * rhs // math.gcd(lhs, rhs)


if __name__ == '__main__':
    # Test usual multiset operations
    assert PrimeMultiset([2, 3, 3, 3]) & PrimeMultiset([2, 2, 2, 3]) == PrimeMultiset([2, 3])
    assert PrimeMultiset([2, 2, 2]) | PrimeMultiset([2, 2, 3]) == PrimeMultiset([2, 2, 2, 3])
    assert PrimeMultiset([2, 3, 3, 23]) + PrimeMultiset([3, 5, 37]) == PrimeMultiset([2, 3, 3, 3, 5, 23, 37])
    assert PrimeMultiset([2, 2, 2, 7, 11, 11, 13]) - PrimeMultiset([2, 7, 11, 13]) == PrimeMultiset([2, 2, 11])
    assert PrimeMultiset([2, 3, 5, 7, 11]) - PrimeMultiset([3, 7, 13]) == PrimeMultiset([2, 5, 11])

    # Test multiset inclusion operations
    assert PrimeMultiset([2, 3]) < PrimeMultiset([2, 2, 2, 3])
    assert not PrimeMultiset([2, 3, 7]) < PrimeMultiset([2, 3, 7])
    assert PrimeMultiset([2, 3]) <= PrimeMultiset([2, 2, 2, 3])
    assert PrimeMultiset([2, 3, 7]) <= PrimeMultiset([2, 3, 7])
    assert PrimeMultiset([2, 3, 7, 7, 11]) > PrimeMultiset([2, 7, 11])
    assert not PrimeMultiset([2, 3, 7]) > PrimeMultiset([2, 3, 7])
    assert PrimeMultiset([2, 3, 7, 7, 11]) >= PrimeMultiset([2, 7, 11])
    assert PrimeMultiset([2, 3, 7]) >= PrimeMultiset([2, 3, 7])

    # Test non-modifying operations
    assert PrimeMultiset().is_empty()
    assert not PrimeMultiset([2, 3, 7]).is_empty()
    assert 7 in PrimeMultiset([2, 3, 7, 7, 11])
    assert 5 not in PrimeMultiset([2, 3, 7, 7, 11])
