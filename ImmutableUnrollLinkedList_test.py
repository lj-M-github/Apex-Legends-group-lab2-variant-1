from ImmutableUnrollLinkedList import (ImmutableUnrolledLinkedList, cons,
                                       length, concat, reduce, remove, reverse,
                                       map_list, member, to_list, filter, find,
                                       from_list, empty, intersection)
from hypothesis import given
import hypothesis.strategies as st
import unittest
from typing import List, Any, Optional, Callable, TypeVar, cast

T = TypeVar('T')


class TestImmutableUnrollLinkedList(unittest.TestCase):

    @given(a=st.lists(st.integers() | st.none()),
           b=st.lists(st.integers() | st.none()),
           c=st.lists(st.integers() | st.none()))
    def test_monoid_associativity(self, a: List[Optional[int]],
                                  b: List[Optional[int]],
                                  c: List[Optional[int]]) -> None:
        ull_a: ImmutableUnrolledLinkedList[Optional[int]] = from_list(a)
        ull_b: ImmutableUnrolledLinkedList[Optional[int]] = from_list(b)
        ull_c: ImmutableUnrolledLinkedList[Optional[int]] = from_list(c)

        left: ImmutableUnrolledLinkedList[Optional[int]] = concat(
            concat(ull_a, ull_b), ull_c)
        right: ImmutableUnrolledLinkedList[Optional[int]] = concat(
            ull_a, concat(ull_b, ull_c))

        self.assertEqual(to_list(left), to_list(right))

    def test_cons(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[
            Optional[int]] = ImmutableUnrolledLinkedList[Optional[int]]()
        l1: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            None, cons(1, empty_list))  # type: ignore[misc]
        l2: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            1, cons(None, empty_list))  # type: ignore[misc]

        self.assertEqual(str(empty_list), "[]")
        self.assertEqual(str(l1), "[None, 1]")
        self.assertEqual(str(l2), "[1, None]")
        self.assertNotEqual(empty_list, l1)
        self.assertNotEqual(empty_list, l2)
        self.assertNotEqual(l1, l2)
        self.assertEqual(l1, cons(None,
                                  cons(1, empty_list)))  # type: ignore[misc]

    def test_remove(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[
            Optional[int]] = ImmutableUnrolledLinkedList[Optional[int]]()
        l1: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            None, cons(1, empty_list))  # type: ignore[misc]

        self.assertEqual(str(remove(l1, None)), "[1]")
        self.assertEqual(str(remove(l1, 1)), "[None]")

    def test_length(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[
            Optional[int]] = ImmutableUnrolledLinkedList[Optional[int]]()
        l1: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            None, cons(1, empty_list))  # type: ignore[misc]

        self.assertEqual(length(empty_list), 0)
        self.assertEqual(length(l1), 2)

    def test_member(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[
            Optional[int]] = ImmutableUnrolledLinkedList[Optional[int]]()
        l1: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            None, cons(1, empty_list))  # type: ignore[misc]

        self.assertFalse(member(empty_list, None))
        self.assertTrue(member(l1, None))
        self.assertTrue(member(l1, 1))
        self.assertFalse(member(l1, 2))

    def test_to_list(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[
            Optional[int]] = ImmutableUnrolledLinkedList[Optional[int]]()
        l1: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            None, cons(1, empty_list))  # type: ignore[misc]

        self.assertEqual(to_list(empty_list), [])
        self.assertEqual(to_list(l1), [None, 1])

    def test_from_list(self) -> None:
        test_data: List[List[Optional[int]]] = [[], [1], [2, 3], [1, 2, 3],
                                                [None, 1]]
        for e in test_data:
            self.assertEqual(to_list(from_list(e)), e)

    def test_reverse(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[
            Optional[int]] = ImmutableUnrolledLinkedList[Optional[int]]()
        l1: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            None, cons(1, empty_list))  # type: ignore[misc]
        l2: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            1, cons(None, empty_list))  # type: ignore[misc]

        self.assertEqual(reverse(empty_list), empty_list)
        self.assertEqual(reverse(l1), l2)
        self.assertEqual(reverse(l2), l1)

    def test_concat(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[
            Optional[int]] = ImmutableUnrolledLinkedList[Optional[int]]()
        l1: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            None, cons(1, empty_list))  # type: ignore[misc]
        l2: ImmutableUnrolledLinkedList[Optional[int]] = cons(
            1, cons(None, empty_list))  # type: ignore[misc]

        self.assertEqual(concat(empty_list, empty_list), empty_list)
        self.assertEqual(concat(l1, empty_list), l1)
        self.assertEqual(concat(empty_list, l1), l1)
        self.assertEqual(to_list(concat(l1, l2)), [None, 1, 1, None])

    def test_iter(self) -> None:
        x: List[int] = [1, 2, 3]
        lst: ImmutableUnrolledLinkedList[int] = from_list(x, node_size=2)
        self.assertEqual([e for e in lst], x)
        self.assertEqual(to_list(lst), x)

        empty_list: ImmutableUnrolledLinkedList[
            int] = ImmutableUnrolledLinkedList[int]()
        with self.assertRaises(StopIteration):
            next(iter(empty_list))

    def test_filter(self) -> None:
        test_list: ImmutableUnrolledLinkedList[int] = from_list(
            [1, 2, 3, 4, 5])
        filtered_list: ImmutableUnrolledLinkedList[int] = filter(
            test_list, lambda x: x % 2 == 0)
        self.assertEqual(to_list(filtered_list), [2, 4])

        empty_list: ImmutableUnrolledLinkedList[
            int] = ImmutableUnrolledLinkedList[int]()
        self.assertEqual(to_list(filter(empty_list, lambda x: x > 0)), [])

    def test_map_list(self) -> None:
        test_list: ImmutableUnrolledLinkedList[int] = from_list([1, 2, 3])
        mapped_list: ImmutableUnrolledLinkedList[int] = map_list(
            test_list, lambda x: x * 2)
        self.assertEqual(to_list(mapped_list), [2, 4, 6])

        empty_list: ImmutableUnrolledLinkedList[
            int] = ImmutableUnrolledLinkedList[int]()
        self.assertEqual(to_list(map_list(empty_list, lambda x: x + 1)), [])

    def test_reduce(self) -> None:
        test_list: ImmutableUnrolledLinkedList[int] = from_list([1, 2, 3, 4])
        self.assertEqual(reduce(test_list, lambda acc, x: acc + x, 0), 10)

        empty_list: ImmutableUnrolledLinkedList[
            int] = ImmutableUnrolledLinkedList[int]()
        self.assertEqual(reduce(empty_list, lambda acc, x: acc + x, 0), 0)

    def test_empty(self) -> None:
        empty_list: ImmutableUnrolledLinkedList[Any] = empty(node_size=3)
        self.assertIsNone(empty_list.head_node)
        self.assertEqual(empty_list.node_size, 3)
        self.assertEqual(length(empty_list), 0)
        self.assertEqual(to_list(empty_list), [])

    def test_find(self) -> None:
        test_list: ImmutableUnrolledLinkedList[int] = from_list([1, 2, 3, 4])
        self.assertEqual(find(test_list, lambda x: x % 2 == 0), (True, 2))

        list_with_none: ImmutableUnrolledLinkedList[Optional[int]] = from_list(
            [1, None, 3])
        self.assertEqual(find(list_with_none, lambda x: x is None),
                         (True, None))

        self.assertEqual(
            find(list_with_none, lambda x: x is not None and x > 10),
            (False, None))

        empty_list: ImmutableUnrolledLinkedList[
            int] = ImmutableUnrolledLinkedList[int]()
        self.assertEqual(find(empty_list, lambda x: x > 0), (False, None))

    def test_intersection(self) -> None:
        list1: ImmutableUnrolledLinkedList[int] = from_list([1, 2, 3, 4])
        list2: ImmutableUnrolledLinkedList[int] = from_list([3, 4, 5, 6])
        self.assertEqual(to_list(intersection(list1, list2)), [3, 4])

        list3: ImmutableUnrolledLinkedList[int] = from_list([7, 8, 9])
        self.assertEqual(to_list(intersection(list1, list3)), [])

        self.assertEqual(to_list(intersection(list1, list1)), to_list(list1))

        empty_list: ImmutableUnrolledLinkedList[
            int] = ImmutableUnrolledLinkedList[int]()
        self.assertEqual(to_list(intersection(list1, empty_list)), [])
        self.assertEqual(to_list(intersection(empty_list, empty_list)), [])


if __name__ == '__main__':
    unittest.main()
