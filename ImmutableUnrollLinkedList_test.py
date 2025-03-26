from ImmutableUnrollLinkedList import ImmutableUnrolledLinkedList,cons,length,concat,reduce,remove,reverse,map_list,member,to_list,filter,find,from_list,empty

def test_IULL_api():
    empty_list = ImmutableUnrolledLinkedList() # Define empty list with node_size=2
    l1 = cons(None, cons(1, empty_list)) # Define l1 and l2 with node_size=2, removed node_size=2 parameter in cons calls in test Lab2
    l2 = cons(1, cons(None, empty_list))

    #cons
    assert str(empty_list) == "[]"
    assert str(l1) == "[None, 1]"
    assert str(l2) == "[1, None]"
    assert empty_list != l1 
    assert empty_list != l2 
    assert l1 != l2
    assert l1 == cons(None, cons(1, empty_list)) 

    #remove

    assert str(remove(l1, None)) == "[1]"
    assert str(remove(l1, 1)) == "[None]"

    #length
    assert length(empty_list) == 0 
    assert length(l1) == 2
    assert length(l2) == 2

    #member
    assert not member(empty_list, None) 
    assert member(l1, None)
    assert member(l1, 1)
    assert not member(l1, 2)

    #to_list
    assert to_list(empty_list) == [] # Changed empty to empty_list
    assert to_list(l1) == [None,1] # Changed empty to empty_list
    assert to_list(l2) == [1,None] # Changed empty to empty_list

    #from_list
    test_data = [[], [1], [2, 3], [1, 2, 3], [None, 1]] # More concrete test data
    for e in test_data:
        assert to_list(from_list(e)) == e

    #reverse
    assert reverse(empty_list) == empty_list 
    assert reverse(l1) == l2
    assert reverse(l2) == l1


    #concat and monoid_identity
    assert concat(empty_list, empty_list) == empty_list 
    assert concat(l1, empty_list) == l1
    assert concat(empty_list, l1) == l1
    print(concat(l1, l2))
    print(from_list([None, 1, 1, None]))
    assert concat(l1, l2) == from_list([None, 1, 1, None])

    #iter
    x = [1, 2, 3]
    lst = from_list(x, node_size=2)

    tmp = []
    for e in lst:
        tmp.append(e)
    assert x == tmp
    assert to_list(lst) == tmp

    list_iterator = iter(empty_list)

    #filter
    test_list = from_list([1, 2, 3, 4, 5])
    filtered_list = filter(test_list, lambda x: x % 2 == 0) 
    assert to_list(filtered_list) == [2, 4]

    empty_filtered_list = filter(empty_list, lambda x: x > 0) 
    assert to_list(empty_filtered_list) == []

    #map_list
    test_list = from_list([1, 2, 3])
    mapped_list = map_list(test_list, lambda x: x * 2) # Map function: multiply by 2
    assert to_list(mapped_list) == [2, 4, 6]

    empty_mapped_list = map_list(empty_list, lambda x: x + 1) 
    assert to_list(empty_mapped_list) == []

    #reduce
    test_list = from_list([1, 2, 3, 4])
    sum_result = reduce(test_list, lambda acc, x: acc + x, 0) # Reduce function: sum
    assert sum_result == 10

    empty_reduce_result = reduce(empty_list, lambda acc, x: acc + x, 0) 
    assert empty_reduce_result == 0

    #empty
    empty_list_test = empty(node_size=3) # Create empty list with node_size 3
    assert empty_list_test.head_node is None
    assert empty_list_test.node_size == 3
    assert length(empty_list_test) == 0
    assert to_list(empty_list_test) == []


if __name__ == '__main__':
    test_IULL_api()