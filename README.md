# Apex-Legends - lab 2 - variant 1

This project demonstrates the implementation of Immutable Unrolled
Linked List in Python and explores the concept of immutable data
structures and the unrolled linked list variation.

## Project structure

- `immutable_unrolled_list.py`
  This file contains the implementation of the
  `ImmutableUnrolledLinkedList` class and the `Node` class.
  The `ImmutableUnrolledLinkedList` class provides a function-style
  API for immutable operations.

- `immutable_unrolled_list_test.py`
  This file contains unit tests for the `ImmutableUnrolledLinkedList`
  implementation.
  The tests verify the correctness of the API functions under various
  scenarios and properties.

## Features

The following function-style API functions are implemented for the
ImmutableUnrolledLinkedList (ul means unrolled_list):

- `cons(head_value, l1=None)`: Adds a new element to the beginning
  (head) of the list, returning a new list.
- `remove(ul, element)`: Returns a new list with the first occurrence
  of the specified element removed.
- `length(ul)`: Returns the number of elements in the list.
- `member(ul, element)`: Checks if the list contains a specific
  element and returns `True` or `False`.
- `reverse(ul)`: Returns a new list with the elements in reversed order.
- `intersection(ul1, ul2)`: Returns a new list containing the
  intersection of elements from two lists (set-like behavior).
- `to_list(ul)`: Converts the Immutable Unrolled Linked List into a
  standard Python list.
- `from_list(list, node_size)`: Creates a new Immutable Unrolled
  Linked List from a standard Python list, with node size specified.
- `filter(ul, predicate)`: Returns a new list containing only elements
  that satisfy the given predicate function.
- `map_list(ul, func)`: Returns a new list by applying the given function
  to each element of the original list.
- `reduce(ul, func, initial_value)`: Reduces the list to a single value
  by applying the given function cumulatively to the list items.
- `empty(node_size)`: Returns a new empty Immutable Unrolled Linked
  List with a specified node size.
- `concat(ul1, ul2)`: Returns a new list by concatenating two
  Immutable Unrolled Linked Lists.
- `iterator(ul)`: Returns an iterator that allows iterating over the
  elements of the Immutable Unrolled Linked List.
- `__iter__(self)`: Implements the iterator protocol, allowing direct
  iteration over the Immutable Unrolled Linked List using `for...in`.
- `__str__(self)`: Provides a string representation of the Immutable
  Unrolled Linked List for easy printing and debugging.
- `__eq__(self, other)`: Implements equality checking between two
  Immutable Unrolled Linked Lists using the `==` operator.

This implementation emphasizes immutability, meaning that operations
on the list do not modify the original list but instead return new lists
with the desired changes. This approach is beneficial for concurrent
programming and data integrity.

## Contribution

- LI Yichen (<1806015345@qq.com>)
- MOU Lingjie (<553571948@qq.com>)

## Changelog

- 10.04.2025 - 0
   - pass mypy strict type checking.
- 26.03.2025 - 2
   - Add test coverage.
   - Update README.
- 25.03.2025 - 1
   - Add formal sections.
- 12.03.2025 - 0
   - Initial
