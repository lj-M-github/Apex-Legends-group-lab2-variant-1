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
    # 将列表转换为不可变展开链表
    ull_a = from_list(a)
    ull_b = from_list(b)
    ull_c = from_list(c)

    # 计算 (a + b) + c
    left = concat(concat(ull_a, ull_b), ull_c)
    # 计算 a + (b + c)
    right = concat(ull_a, concat(ull_b, ull_c))

    # 验证结果是否一致
    assert to_list(left) == to_list(right)

def test_IULL_api():
    empty_list = ImmutableUnrolledLinkedList()
    l1 = cons(None, cons(1, empty_list))
    l2 = cons(1, cons(None, empty_list))

    # cons
    assert str(empty_list) == "[]"
    assert str(l1) == "[None, 1]"
    assert str(l2) == "[1, None]"
    assert empty_list != l1
    assert empty_list != l2
    assert l1 != l2
    assert l1 == cons(None, cons(1, empty_list))

    # remove

    assert str(remove(l1, None)) == "[1]"
    assert str(remove(l1, 1)) == "[None]"

    # length
    assert length(empty_list) == 0
    assert length(l1) == 2
    assert length(l2) == 2

    # member
    assert not member(empty_list, None)
    assert member(l1, None)
    assert member(l1, 1)
    assert not member(l1, 2)

    # to_list
    assert to_list(empty_list) == []
    assert to_list(l1) == [None, 1]
    assert to_list(l2) == [1, None]

    # from_list
    test_data = [[], [1], [2, 3], [1, 2, 3], [None, 1]]
    for e in test_data:
        assert to_list(from_list(e)) == e

    # reverse
    assert reverse(empty_list) == empty_list
    assert reverse(l1) == l2
    assert reverse(l2) == l1

    # concat and monoid_identity
    assert concat(empty_list, empty_list) == empty_list
    assert concat(l1, empty_list) == l1
    assert concat(empty_list, l1) == l1
    print(concat(l1, l2))
    print(from_list([None, 1, 1, None]))
    assert concat(l1, l2) == from_list([None, 1, 1, None])

    # iter
    x = [1, 2, 3]
    lst = from_list(x, node_size=2)

    tmp = []
    for e in lst:
        tmp.append(e)
    assert x == tmp
    assert to_list(lst) == tmp

    list_iterator = iter(empty_list)
    try:
        next(list_iterator)  # get next element from empty IULL
        assert False, "StopIteration was not raised for empty list iterator"
    except StopIteration:
        pass

    # filter
    test_list = from_list([1, 2, 3, 4, 5])
    filtered_list = filter(test_list, lambda x: x % 2 == 0)
    assert to_list(filtered_list) == [2, 4]

    empty_filtered_list = filter(empty_list, lambda x: x > 0)
    assert to_list(empty_filtered_list) == []

    # map_list
    test_list = from_list([1, 2, 3])
    # Map function: multiply by 2
    mapped_list = map_list(test_list, lambda x: x * 2)
    assert to_list(mapped_list) == [2, 4, 6]
    # Map function: x + 1
    empty_mapped_list = map_list(empty_list, lambda x: x + 1)
    assert to_list(empty_mapped_list) == []

    # reduce
    test_list = from_list([1, 2, 3, 4])
    # Reduce function: sum
    sum_result = reduce(test_list, lambda acc, x: acc + x, 0)
    assert sum_result == 10

    empty_reduce_result = reduce(empty_list, lambda acc, x: acc + x, 0)
    assert empty_reduce_result == 0

    # empty
    empty_list_test = empty(node_size=3)  # Create empty list with node_size 3
    assert empty_list_test.head_node is None
    assert empty_list_test.node_size == 3
    assert length(empty_list_test) == 0
    assert to_list(empty_list_test) == []

    # find
    test_list = from_list([1, 2, 3, 4])
    found_element = find(test_list, lambda x: x % 2 == 0)
    assert found_element == 2
    # Find None in a list with None
    list_with_none = from_list([1, None, 3])
    found_none = find(list_with_none, lambda x: x is None)
    assert found_none is None

    # Element not found
    not_found_element = find(test_list, lambda x: x > 10)
    assert not_found_element is None

    # Find in empty list
    empty_find_result = find(empty_list, lambda x: x > 0)
    assert empty_find_result is None

    # intersection
    list1 = from_list([1, 2, 3, 4])
    list2 = from_list([3, 4, 5, 6])
    # Common elements [3, 4]
    intersection_list = intersection(list1, list2)
    assert to_list(intersection_list) == [3, 4]

    # No common elements, empty list
    list3 = from_list([7, 8, 9])
    no_intersection_list = intersection(list1, list3)
    assert to_list(no_intersection_list) == []

    # Intersection with self is self
    same_list_intersection = intersection(list1, list1)
    assert to_list(same_list_intersection) == to_list(list1)

    # Intersection with empty list is empty
    list_empty_intersection = intersection(list1, empty_list)
    assert to_list(list_empty_intersection) == []

    # Intersection of two empty lists is empty
    empty_empty_intersection = intersection(empty_list, empty_list)
    assert to_list(empty_empty_intersection) == []


if __name__ == '__main__':
    test_IULL_api()
    test_monoid_associativity()
