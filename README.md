## A multiset of prime numbers

The `prime_multiset` module contains a `PrimeMultiset` class that represents a multiset that can only store prime
numbers. Under the hood, the prime multiset is represented by a single positive integer. This is possible thanks to the
interesting observation that any natural number can be decomposed in a unique collection of prime factors. In other
words, [any natural number is a unique multiset of prime integers][1]. The underlying integer is accessible through the
`value` member of a `PrimeMultiset`.

This single-integer representation has some fun & unique properties:
* Most set operations can be computed with operations on integers (multiplication, gcd...)
* The complexity of some operations becomes funny (*e.g* `discard` is a mere division)
* Listing the elements is very expensive because it involves prime decomposition (hence not provided)
* The `len` method isn't available for the same reason, but `is_empty` is provided
* The storage for the underlying integer can be higher or lower than for a classic multiset implementation

You can read more about the operations equivalence in the article linked in the first paragraph.

## The `PrimeMultiset` API

### Initialization of the prime multiset

```python
PrimeMultiset(sequence=(), initial_value=1)
```

The constructor initializes the `value` member with `initial_value`, which is the initial integer multiset
representation (`1` represents an empty multiset), to which are added the prime numbers contained in `sequence`.

### Usual multiset operations

```python
multiset & other
multiset &= other
```

Computes the multiset intersection of `multiset` and `other` (retaining the lesser multiplicity per element).

```python
multiset | other
multiset |= other
```

Computes the multiset union of `multiset` and `other` (retaining the greater multiplicity per element).

```python
multiset + other
multiset += other
```

Computes the multiset addition of `multiset` and `other` (retaining the sum of multiplicities per element).

```python
multiset - other
multiset -= other
```

Computes the multiset subtraction of `multiset` and `other` (retaining the differences of multiplicities per element
between one multiset and another). If `other` contains prime numbers that are not in `multiset`, the subtraction is
computed *as if* `other` did not contain those additional prime numbers.

### Multiset equality operations

```python
multiset == other
```

Returns whether `multiset` and `other` contain the same elements.

```python
multiset != other
```

Returns whether `multiset` and `other` contain different elements.

### Multiset inclusion operations

```python
multiset <= other
```

Returns whether every element in `multiset` is also in `other`.

```python
multiset < other
```

Returns whether `multiset` is a proper subset of `other`, that is, whether `multiset <= other and multiset != other`.

```python
multiset >= other
```

Returns whether every element in `other` is also in `multiset`.

```python
multiset > other
```

Returns whether `multiset` is a proper superset of `other`, that is, whether `multiset >= other and multiset != other`.

### Modifying multiset operations

```python
add(element)
```

Adds the prime number `element` to the multiset.

```python
remove(element)
```

Removes the prime number `element` from the multiset. Raises `KeyError` if `element` is not contained in the multiset.

```python
discard(element)
```

Removes the prime number `element` from the multiset if it is present.

```python
clear()
```

Removes all elements from the multiset.

### Non-modifying multiset operations

```python
element in multiset
element not in multiset
```

Returns whether `multiset` contains the prime number `element`.

```python
is_empty
```

Returns whether the multiset does not contain any element.

## Error handling in the API

Checking whether a given integer is a prime number or not is rather expensive, therefore the `PrimeMultiset` API does
not validate its inputs. If integers other than prime numbers are passed to functions expecting prime numbers, the
behaviour of the operations is not guaranteed.


  [1]: http://psmay.com/2012/02/17/fun-with-math-a-natural-number-is-a-multiset-of-prime-factors/
