from ImmutableUnrollLinkedList import ImmutableUnrolledLinkedList, cons, length
from ImmutableUnrollLinkedList import concat, reduce, remove, reverse, map_list
from ImmutableUnrollLinkedList import member, to_list, filter, find
from ImmutableUnrollLinkedList import from_list, empty, intersection
from hypothesis import given
import hypothesis.strategies as st


@given(
    a=st.lists(st.integers() | st.none()),
    b=st.lists(st.integers() | st.none()),
    c=st.lists(st.integers() | st.none())
)
def test_monoid_associativity(a: list, b: list, c: list):
    ull_a = from_list(a)
    ull_b = from_list(b)
    ull_c = from_list(c)

    # (a + b) + c
    left = concat(concat(ull_a, ull_b), ull_c)
    # a + (b + c)
    right = concat(ull_a, concat(ull_b, ull_c))

    assert to_list(left) == to_list(right)


def test_cons():
    empty_list = ImmutableUnrolledLinkedList[int]()
    l1 = cons(None, cons(1, empty_list))
    l2 = cons(1, cons(None, empty_list))

    assert str(empty_list) == "[]"
    assert str(l1) == "[None, 1]"
    assert str(l2) == "[1, None]"
    assert empty_list != l1
    assert empty_list != l2
    assert l1 != l2
    assert l1 == cons(None, cons(1, empty_list))


def test_remove():
    empty_list = ImmutableUnrolledLinkedList[int]()
    l1 = cons(None, cons(1, empty_list))

    assert str(remove(l1, None)) == "[1]"
    assert str(remove(l1, 1)) == "[None]"


def test_length():
    empty_list = ImmutableUnrolledLinkedList[int]()
    l1 = cons(None, cons(1, empty_list))

    assert length(empty_list) == 0
    assert length(l1) == 2


def test_member():
    empty_list = ImmutableUnrolledLinkedList[int]()
    l1 = cons(None, cons(1, empty_list))

    assert not member(empty_list, None)
    assert member(l1, None)
    assert member(l1, 1)
    assert not member(l1, 2)


def test_to_list():
    empty_list = ImmutableUnrolledLinkedList[int]()
    l1 = cons(None, cons(1, empty_list))
    assert to_list(empty_list) == []
    assert to_list(l1) == [None, 1]


def test_from_list():
    test_data = [[], [1], [2, 3], [1, 2, 3], [None, 1]]
    for e in test_data:
        assert to_list(from_list(e)) == e


def test_reverse():
    empty_list = ImmutableUnrolledLinkedList[int]()
    l1 = cons(None, cons(1, empty_list))
    l2 = cons(1, cons(None, empty_list))

    assert reverse(empty_list) == empty_list
    assert reverse(l1) == l2
    assert reverse(l2) == l1


def test_concat():
    empty_list = ImmutableUnrolledLinkedList[int]()
    l1 = cons(None, cons(1, empty_list))
    l2 = cons(1, cons(None, empty_list))

    assert concat(empty_list, empty_list) == empty_list
    assert concat(l1, empty_list) == l1
    assert concat(empty_list, l1) == l1
    assert concat(l1, l2) == from_list([None, 1, 1, None])


def test_iter():
    x = [1, 2, 3]
    lst = from_list(x, node_size=2)
    tmp = []
    for e in lst:
        tmp.append(e)
    assert x == tmp
    assert to_list(lst) == tmp

    empty_list = ImmutableUnrolledLinkedList[int]()
    list_iterator = iter(empty_list)
    try:
        next(list_iterator)
        assert False, "StopIteration not raised"
    except StopIteration:
        pass


def test_filter():
    test_list = from_list([1, 2, 3, 4, 5])
    filtered_list = filter(test_list, lambda x: x % 2 == 0)
    assert to_list(filtered_list) == [2, 4]

    empty_list = ImmutableUnrolledLinkedList[int]()
    empty_filtered = filter(empty_list, lambda x: x > 0)
    assert to_list(empty_filtered) == []


def test_map_list():
    test_list = from_list([1, 2, 3])
    mapped_list = map_list(test_list, lambda x: x * 2)
    assert to_list(mapped_list) == [2, 4, 6]

    empty_list = ImmutableUnrolledLinkedList[int]()
    empty_mapped = map_list(empty_list, lambda x: x + 1)
    assert to_list(empty_mapped) == []


def test_reduce():
    test_list = from_list([1, 2, 3, 4])
    sum_result = reduce(test_list, lambda acc, x: acc + x, 0)
    assert sum_result == 10

    empty_list = ImmutableUnrolledLinkedList[int]()
    empty_reduce = reduce(empty_list, lambda acc, x: acc + x, 0)
    assert empty_reduce == 0


def test_empty():
    empty_list = empty(node_size=3)
    assert empty_list.head_node is None
    assert empty_list.node_size == 3
    assert length(empty_list) == 0
    assert to_list(empty_list) == []


def test_find():
    test_list = from_list([1, 2, 3, 4])
    assert find(test_list, lambda x: x % 2 == 0) == 2

    list_with_none = from_list([1, None, 3])
    assert find(list_with_none, lambda x: x is None) is None

    assert find(test_list, lambda x: x > 10) is None

    empty_list = ImmutableUnrolledLinkedList[int]()
    assert find(empty_list, lambda x: x > 0) is None


def test_intersection():
    list1 = from_list([1, 2, 3, 4])
    list2 = from_list([3, 4, 5, 6])
    assert to_list(intersection(list1, list2)) == [3, 4]

    list3 = from_list([7, 8, 9])
    assert to_list(intersection(list1, list3)) == []

    assert to_list(intersection(list1, list1)) == to_list(list1)

    empty_list = ImmutableUnrolledLinkedList[int]()
    assert to_list(intersection(list1, empty_list)) == []
    assert to_list(intersection(empty_list, empty_list)) == []
