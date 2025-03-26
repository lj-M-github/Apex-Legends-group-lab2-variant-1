from typing import Optional, Tuple, List, Callable, TypeVar, Iterable, Generic

T = TypeVar('T', int, float, None)
U = TypeVar('U', int, float)


class Node(Generic[T]):
    # Node for Immutable Unrolled Linked List

    def __init__(self,
                 elements: Optional[Iterable[T]] = None,
                 next_node: Optional['Node'] = None):

        # Initialize an immutable node.

        self._elements: Tuple[T, ...] = tuple(
            elements) if elements is not None else tuple(
            )  # Added type annotation
        self._next = next_node

    @property
    def elements(self) -> Tuple[T, ...]:
        # Returns the elements of the node as a tuple (immutable)
        return self._elements

    @property
    def next_node(self) -> Optional['Node']:
        # Returns the next node (immutable)
        return self._next

    def __str__(self) -> str:
        # String representation of the Node for easy printing
        elements_str = ", ".join(map(str, self._elements))
        next_str = ""
        if self._next:
            next_str = ", " + str(self._next)
        return f"[{elements_str}]{next_str}"

    def __eq__(self, other: object) -> bool:
        # Equality check for Node objects
        if not isinstance(other, Node):
            return False
        return self._elements == other._elements and self._next == other._next


class ImmutableUnrolledLinkedList(Generic[T]):
    # Immutable Unrolled Linked List Data Structure

    def __init__(self, head_node: Optional[Node] = None, node_size: int = 4):

        if head_node is not None and not isinstance(head_node, Node):
            raise TypeError("head_node must be a Node or None")

        if not isinstance(node_size, int) or node_size <= 0:
            raise ValueError("node_size must be a positive integer")

        self._head_node = head_node  # Immutable head node reference
        self._node_size = node_size  # Immutable node size

    @property
    def head_node(self) -> Optional[Node]:
        # Returns the head Node of the list (immutable)
        return self._head_node

    @property
    def node_size(self) -> int:
        # Returns the fixed node size for this list (immutable)
        return self._node_size

    def __str__(self) -> str:
        # String representation of the UnrolledLinkedList
        if self._head_node is None:
            return "[]"  # Empty list representation
        return str(self._head_node)

    def __eq__(self, other: object) -> bool:
        # Equality check for ImmutableUnrolledLinkedList objects
        if not isinstance(other, ImmutableUnrolledLinkedList):
            return False

        check_headnode = (self._head_node == other._head_node)
        check_nodesize = (self._node_size == other._node_size)
        return check_headnode and check_nodesize

    def __iter__(
        self
    ) -> 'ImmutableUnrolledLinkedListIterator':  # Corrected return type hint
        # Makes the ImmutableUnrolledLinkedList iterable. Returns an iterator
        return ImmutableUnrolledLinkedListIterator(self)


class ImmutableUnrolledLinkedListIterator(Generic[T]):
    # Iterator for ImmutableUnrolledLinkedList

    def __init__(self, unrolled_list: ImmutableUnrolledLinkedList):
        # Initialize the iterator with an UnrolledLinkedList
        self._current_node: Optional[
            Node] = unrolled_list.head_node  # Added type annotation
        self._current_element_index: int = 0  # Added type annotation

    def __iter__(
        self
    ) -> 'ImmutableUnrolledLinkedListIterator':  # Corrected return type hint
        # Returns the iterator object itself (for iter(iterator))
        return self

    def __next__(self) -> Optional[T]:
        # Returns the next element in the ImmutableUnrolledLinkedList
        if self._current_node is None:
            raise StopIteration

        if self._current_element_index < len(self._current_node.elements):
            value = self._current_node.elements[self._current_element_index]
            self._current_element_index += 1
            return value
        else:
            self._current_node = self._current_node.next_node
            self._current_element_index = 0
            return self.__next__()
            # Recursive call to get element from new node


def cons(
    head_value: T,
    unrolled_list: Optional[ImmutableUnrolledLinkedList] = None
) -> ImmutableUnrolledLinkedList:
    # Adds a new element to the head of the ImmutableUnrolledLinkedList
    node_size = unrolled_list.node_size if unrolled_list else 4

    if not unrolled_list or unrolled_list.head_node is None:  # Empty list case
        return ImmutableUnrolledLinkedList(Node([head_value], None), node_size)

    head_node = unrolled_list.head_node

    if len(head_node.elements) < node_size:  # Head node not full
        # Create new tuple with prepended element
        new_elements = (head_value, ) + head_node.elements
        # Create new head node
        new_head_node = Node(new_elements, head_node.next_node)
        # Return new list with new head
        return ImmutableUnrolledLinkedList(new_head_node, node_size)
    else:  # Head node is full, create a new node and prepend
        # Create new node pointing to old head
        new_head_node = Node([head_value], head_node)
        # Return new list
        return ImmutableUnrolledLinkedList(new_head_node, node_size)


def remove(unrolled_list: ImmutableUnrolledLinkedList,
           element: T) -> ImmutableUnrolledLinkedList:
    # Removes the first occurrence of an element from the IULL
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list  # Return original empty list if empty

    def _remove_recursive(current_node: Optional[Node],
                          element_to_remove: T) -> Optional[Node]:
        if current_node is None:
            return None  # Base case: element not found

        # Work with a mutable list for now
        current_elements = list(current_node.elements)
        removed_index = -1
        for i in range(len(current_elements)):
            if current_elements[i] == element_to_remove:
                removed_index = i
                break

        if removed_index != -1:  # Element found in current node
            remaining_elements = current_elements[:removed_index] + \
                current_elements[removed_index+1:]
            if remaining_elements:  # Node still has elements
                return Node(tuple(remaining_elements), current_node.next_node
                            )  # Corrected Node creation with tuple
            else:  # Node becomes empty, skip this node
                # Return the rest of the list (tail)
                return current_node.next_node
        else:  # Element not found in current node, recurse
            next_node_recursive = _remove_recursive(current_node.next_node,
                                                    element_to_remove)
            if next_node_recursive == current_node.next_node:
                return current_node  # tail no change, reuse current node
            else:  # create a new node linking to the modified tail
                # Create new node linking to modified tail
                return Node(current_node.elements, next_node_recursive)

    modified_head_node = _remove_recursive(unrolled_list.head_node, element)
    if modified_head_node == unrolled_list.head_node:
        return unrolled_list  # No change in head, reuse original list
    else:  # Head changed, return new list with modified head
        return ImmutableUnrolledLinkedList(modified_head_node,
                                           unrolled_list.node_size)


def length(unrolled_list: Optional[ImmutableUnrolledLinkedList]) -> int:
    # Returns the length of the ImmutableUnrolledLinkedList
    if not unrolled_list or unrolled_list.head_node is None:
        return 0

    def _length_recursive(current_node: Optional[Node]) -> int:
        if current_node is None:
            return 0
        return len(current_node.elements) + _length_recursive(
            current_node.next_node)

    return _length_recursive(unrolled_list.head_node)


def member(unrolled_list: ImmutableUnrolledLinkedList, element: T) -> bool:
    # Checks if an element is a member of the ImmutableUnrolledLinkedList
    if not unrolled_list or unrolled_list.head_node is None:
        return False

    def _member_recursive(current_node: Optional[Node],
                          element_to_find: T) -> bool:
        if current_node is None:
            return False
        if element_to_find in current_node.elements:
            return True
        return _member_recursive(current_node.next_node, element_to_find)

    return _member_recursive(unrolled_list.head_node, element)


def reverse(
        unrolled_list: ImmutableUnrolledLinkedList
) -> ImmutableUnrolledLinkedList:
    """Reverses the ImmutableUnrolledLinkedList."""
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list  # Return original empty list if empty

    def _reverse_recursive(current_node: Optional[Node],
                           accumulated_list: Optional[Node]) -> Optional[Node]:
        if current_node is None:
            return accumulated_list

        reversed_current_node_values = reversed(
            current_node.elements)  # Reverse elements in current node
        reversed_node = from_list(
            list(reversed_current_node_values), unrolled_list.node_size
        ).head_node  # Create node from reversed values

        return _reverse_recursive(
            current_node.next_node,
            concat_nodes(reversed_node,
                         accumulated_list))  # Prepend reversed node

    reversed_head_node = _reverse_recursive(unrolled_list.head_node, None)
    return ImmutableUnrolledLinkedList(reversed_head_node,
                                       unrolled_list.node_size)


def intersection(
    unrolled_list1: ImmutableUnrolledLinkedList[T],
    unrolled_list2: ImmutableUnrolledLinkedList[T]
) -> ImmutableUnrolledLinkedList:
    # Returns the intersection of two ImmutableUnrolledLinkedLists
    if (not unrolled_list1 or not unrolled_list2
            or unrolled_list1.head_node is None
            or unrolled_list2.head_node is None):
        # Return empty list
        return ImmutableUnrolledLinkedList(
            None, unrolled_list1.node_size
            if unrolled_list1 else unrolled_list2.node_size)

    intersection_values: List[T] = []  # Added type annotation

    def _intersection_recursive(current_node: Optional[Node]):
        nonlocal intersection_values  # Allow modifying outer variable
        if current_node is None:
            return

        for val in current_node.elements:
            if member(unrolled_list2, val):
                intersection_values.append(val)
        _intersection_recursive(current_node.next_node)  # Recurse

    _intersection_recursive(unrolled_list1.head_node)
    intersection_head_node = from_list(intersection_values,
                                       unrolled_list1.node_size).head_node
    return ImmutableUnrolledLinkedList(intersection_head_node,
                                       unrolled_list1.node_size)


def to_list(unrolled_list: ImmutableUnrolledLinkedList) -> List[T]:
    # Converts the ImmutableUnrolledLinkedList to a list
    res: List[T] = []
    if not unrolled_list or unrolled_list.head_node is None:
        return res  # Return empty list if empty

    def _to_list_recursive(current_node: Optional[Node]):
        nonlocal res
        if current_node is None:
            return
        res.extend(list(current_node.elements))
        _to_list_recursive(current_node.next_node)

    _to_list_recursive(unrolled_list.head_node)
    return res


def from_list(python_list: List[T],
              node_size: int = 4) -> ImmutableUnrolledLinkedList:
    # Creates an ImmutableUnrolledLinkedList from a list
    if not python_list:
        return ImmutableUnrolledLinkedList(None, node_size)

    head_node = None
    current_node_values: List[T] = []  # Added type annotation
    current_node_pointer: Optional[Node[T]] = None

    for item in python_list:
        current_node_values.append(item)
        if len(current_node_values) == node_size:
            new_node = Node(tuple(current_node_values),
                            None)  # Corrected Node creation with tuple
            if head_node is None:
                head_node = new_node
                current_node_pointer = head_node
            else:
                if current_node_pointer is not None:
                    current_node_pointer._next = new_node
                current_node_pointer = new_node
            current_node_values = []

    if current_node_values:  # Remaining elements
        new_node = Node(tuple(current_node_values),
                        None)  # Corrected Node creation with tuple
        if head_node is None:
            head_node = new_node
        else:
            if current_node_pointer is not None:
                current_node_pointer._next = new_node

    return ImmutableUnrolledLinkedList(head_node, node_size)


def find(unrolled_list: ImmutableUnrolledLinkedList,
         predicate: Callable[[T], bool]) -> Optional[T]:
    # Finds the first element that satisfies the predicate in the IULL
    if not unrolled_list or unrolled_list.head_node is None:
        return None

    def _find_recursive(
            current_node: Optional[Node],
            predicate_func: Callable[[T], bool]) -> Optional[T]:
        if current_node is None:
            return None

        for value in current_node.elements:
            if predicate_func(value):
                return value  # Found element

        # Recurse if not found in current node
        return _find_recursive(current_node.next_node, predicate_func)

    return _find_recursive(unrolled_list.head_node, predicate)


def filter(unrolled_list: ImmutableUnrolledLinkedList,
           predicate: Callable[[T], bool]) -> ImmutableUnrolledLinkedList:
    # Filters the ImmutableUnrolledLinkedList based on a predicate
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list  # Return original empty list if empty

    filtered_values: List[T] = []  # Added type annotation

    def _filter_recursive(current_node: Optional[Node]):
        nonlocal filtered_values
        if current_node is None:
            return  # Base case: end of list

        for value in current_node.elements:
            if predicate(value):
                filtered_values.append(value)  # Add value if predicate is True

        _filter_recursive(current_node.next_node)  # Recurse to next node

    _filter_recursive(unrolled_list.head_node)
    # Create new list with filtered values
    filtered_head_node = from_list(filtered_values,
                                   unrolled_list.node_size).head_node
    return ImmutableUnrolledLinkedList(filtered_head_node,
                                       unrolled_list.node_size)


def map_list(unrolled_list: ImmutableUnrolledLinkedList[T],
             func: Callable[[U], U]) -> ImmutableUnrolledLinkedList:
    # Maps a function over the ImmutableUnrolledLinkedList
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list  # Return original empty list if empty

    def _map_recursive(current_node: Optional[Node]) -> Optional[Node]:
        if current_node is None:
            return None  # Base case: end of list

        # Apply func to each element, create a new tuple with mapped elements
        elements = current_node.elements
        mapped_values = (func(value) for value in elements)
        mapped_elements = tuple(mapped_values)
        # Map the rest of the list recursively
        mapped_next_node = _map_recursive(current_node.next_node)

        # Create new node with mapped elements and return it
        return Node(mapped_elements, mapped_next_node)

    mapped_head_node = _map_recursive(unrolled_list.head_node)

    # Ensure we return an ImmutableUnrolledLinkedList with the new head node
    return ImmutableUnrolledLinkedList(mapped_head_node,
                                       unrolled_list.node_size)


def reduce(unrolled_list: ImmutableUnrolledLinkedList[U],
           func: Callable[[U, U], U],
           initial_value: Optional[U]) -> Optional[U]:
    # Reduces the ImmutableUnrolledLinkedList to a single value
    if not unrolled_list or unrolled_list.head_node is None:
        return initial_value  # Return initial value if the list is empty

    state = initial_value
    current_node: Optional[Node] = unrolled_list.head_node

    while current_node is not None:
        for value in current_node.elements:
            if state is None:  # Handle None case
                state = value  # If state is None, set it to the first element
            else:
                state = func(state, value)
        current_node = current_node.next_node

    return state  # Ensure a return value


def empty(node_size: int = 4) -> ImmutableUnrolledLinkedList:
    # Returns an empty ImmutableUnrolledLinkedList
    return ImmutableUnrolledLinkedList(None, node_size)


def concat(
    unrolled_list1: ImmutableUnrolledLinkedList,
    unrolled_list2: ImmutableUnrolledLinkedList
) -> ImmutableUnrolledLinkedList:
    # Concat two ImmutableUnrolledLinkedLists
    if not unrolled_list1 or unrolled_list1.head_node is None:
        return unrolled_list2  # If list1 is empty, return list2

    concatenated_values = to_list(unrolled_list1) + to_list(
        unrolled_list2)  # l1+l2

    # Rebuild list from concatenated values
    return from_list(concatenated_values, unrolled_list1.node_size)


def concat_nodes(node1: Optional[Node],
                 node2: Optional[Node]) -> Optional[Node]:
    # Helper function to concatenate Node chains, used internally for reverse
    if node1 is None:
        return node2
    return Node(node1.elements, concat_nodes(node1.next_node, node2))


def iterator(
    unrolled_list: ImmutableUnrolledLinkedList
) -> 'ImmutableUnrolledLinkedListIterator':
    # Returns an iterator for the ImmutableUnrolledLinkedList
    return ImmutableUnrolledLinkedListIterator(unrolled_list)
