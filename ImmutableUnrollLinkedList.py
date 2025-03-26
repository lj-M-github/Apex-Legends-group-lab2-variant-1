from typing import Optional, Tuple, List, Callable, TypeVar, Iterable

class Node:
    """Node for Immutable Unrolled Linked List"""
    Num = TypeVar('Num', int, float)

    def __init__(self, elements: Optional[Iterable[Num]] = None, next_node: Optional['Node'] = None):
        """
        Initialize an immutable node.

        Args:
            elements (Optional[Iterable[Num]]): The elements to be stored in this node as an immutable tuple.
            next_node (Optional['Node']): Points to the next node in the linked list, or None if it's the last node.
        """
        self._elements = tuple(elements) if elements is not None else tuple()
        self._next = next_node  # Points to the next node in the linked list, renamed to _next
        # self.last = None  # Removed last pointer for immutability and simplicity


    @property
    def elements(self) -> Tuple[Num, ...]:
        """Returns the elements of the node as a tuple (immutable)."""
        return self._elements

    @property
    def next_node(self) -> Optional['Node']:
        """Returns the next node (immutable)."""
        return self._next

    def __str__(self) -> str:
        """String representation of the Node for easy printing."""
        elements_str = ", ".join(map(str, self._elements))
        next_str = ""
        if self._next:
            next_str = ", " + str(self._next)
        return f"[{elements_str}]{next_str}"

    def __eq__(self, other: object) -> bool:
        """Equality check for Node objects."""
        if not isinstance(other, Node):
            return False
        return self._elements == other._elements and self._next == other._next


class ImmutableUnrolledLinkedList:
    """Immutable Unrolled Linked List Data Structure"""
    Num = TypeVar('Num', int, float)

    def __init__(self, head_node: Optional[Node] = None, node_size: int = 4):
        """
        Initializes an ImmutableUnrolledLinkedList.

        Args:
            head_node (Optional[Node]): The head Node of the list. Defaults to None for an empty list.
            node_size (int): The fixed size of each Node in this list. Defaults to 4.
        """
        if head_node is not None and not isinstance(head_node, Node):
            raise TypeError("head_node must be a Node or None")

        if not isinstance(node_size, int) or node_size <= 0:
            raise ValueError("node_size must be a positive integer")

        self._head_node = head_node  # Immutable head node reference
        self._node_size = node_size  # Immutable node size


    @property
    def head_node(self) -> Optional[Node]:
        """Returns the head Node of the list (immutable)."""
        return self._head_node

    @property
    def node_size(self) -> int:
        """Returns the fixed node size for this list (immutable)."""
        return self._node_size


    def __str__(self) -> str:
        """String representation of the UnrolledLinkedList."""
        if self._head_node is None:
            return "[]"  # Empty list representation
        return str(self._head_node)


    def __eq__(self, other: object) -> bool:
        """Equality check for UnrolledLinkedList objects."""
        if not isinstance(other, ImmutableUnrolledLinkedList):
            return False
        return self._head_node == other._head_node and self._node_size == other._node_size

    def __iter__(self):
        """Makes the ImmutableUnrolledLinkedList iterable. Returns an iterator."""
        return ImmutableUnrolledLinkedListIterator(self) # Return iterator class instance


class ImmutableUnrolledLinkedListIterator:
    """Iterator for ImmutableUnrolledLinkedList"""
    def __init__(self, unrolled_list: ImmutableUnrolledLinkedList):
        """Initialize the iterator with an UnrolledLinkedList."""
        self._current_node = unrolled_list.head_node
        self._current_element_index = 0

    def __iter__(self):
        """Returns the iterator object itself (for iter(iterator))."""
        return self

    def __next__(self) -> Optional[ImmutableUnrolledLinkedList.Num]:
        """Returns the next element in the ImmutableUnrolledLinkedList."""
        if self._current_node is None:
            raise StopIteration

        if self._current_element_index < len(self._current_node.elements):
            value = self._current_node.elements[self._current_element_index]
            self._current_element_index += 1
            return value
        else:
            self._current_node = self._current_node.next_node
            self._current_element_index = 0
            return self.__next__() # Recursive call to get element from new node


# --- API Functions (Function-style) ---

def cons(head_value: ImmutableUnrolledLinkedList.Num, unrolled_list: Optional[ImmutableUnrolledLinkedList] = None) -> ImmutableUnrolledLinkedList:
    """Adds a new element to the head of the ImmutableUnrolledLinkedList."""
    node_size = unrolled_list.node_size if unrolled_list else 4 # Default node_size if list is None

    if not unrolled_list or unrolled_list.head_node is None: # Empty list case
        return ImmutableUnrolledLinkedList(Node([head_value], None), node_size)

    head_node = unrolled_list.head_node

    if len(head_node.elements) < node_size: # Head node not full
        new_elements = (head_value,) + head_node.elements # Create new tuple with prepended element
        new_head_node = Node(new_elements, head_node.next_node) # Create new head node
        return ImmutableUnrolledLinkedList(new_head_node, node_size) # Return new list with new head
    else: # Head node is full, create a new node and prepend
        new_head_node = Node([head_value], head_node) # Create new node pointing to old head
        return ImmutableUnrolledLinkedList(new_head_node, node_size) # Return new list


def remove(unrolled_list: ImmutableUnrolledLinkedList, element: ImmutableUnrolledLinkedList.Num) -> ImmutableUnrolledLinkedList:
    """Removes the first occurrence of an element from the ImmutableUnrolledLinkedList."""
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list # Return original empty list if empty

    def _remove_recursive(current_node: Optional[Node], element_to_remove: ImmutableUnrolledLinkedList.Num) -> Optional[Node]:
        if current_node is None:
            return None # Base case: element not found

        current_elements = list(current_node.elements) # Work with a mutable list for now
        removed_index = -1
        for i in range(len(current_elements)):
            if current_elements[i] == element_to_remove:
                removed_index = i
                break

        if removed_index != -1: # Element found in current node
            remaining_elements = current_elements[:removed_index] + current_elements[removed_index+1:]
            if remaining_elements: # Node still has elements
                return Node(remaining_elements, current_node.next_node)
            else: # Node becomes empty, skip this node
                return current_node.next_node # Return the rest of the list (tail)
        else: # Element not found in current node, recurse
            next_node_recursive = _remove_recursive(current_node.next_node, element_to_remove)
            if next_node_recursive == current_node.next_node: # No change in tail, reuse current node
                return current_node # No change in this branch
            else: # Tail changed, need to create a new node linking to the modified tail
                return Node(current_node.elements, next_node_recursive) # Create new node linking to modified tail


    modified_head_node = _remove_recursive(unrolled_list.head_node, element)
    if modified_head_node == unrolled_list.head_node: # No change in head, reuse original list
        return unrolled_list
    else: # Head changed, return new list with modified head
        return ImmutableUnrolledLinkedList(modified_head_node, unrolled_list.node_size)


def length(unrolled_list: Optional[ImmutableUnrolledLinkedList]) -> int:
    """Returns the length of the ImmutableUnrolledLinkedList."""
    if not unrolled_list or unrolled_list.head_node is None:
        return 0

    def _length_recursive(current_node: Optional[Node]) -> int:
        if current_node is None:
            return 0
        return len(current_node.elements) + _length_recursive(current_node.next_node)

    return _length_recursive(unrolled_list.head_node)


def member(unrolled_list: ImmutableUnrolledLinkedList, element: ImmutableUnrolledLinkedList.Num) -> bool:
    """Checks if an element is a member of the ImmutableUnrolledLinkedList."""
    if not unrolled_list or unrolled_list.head_node is None:
        return False

    def _member_recursive(current_node: Optional[Node], element_to_find: ImmutableUnrolledLinkedList.Num) -> bool:
        if current_node is None:
            return False
        if element_to_find in current_node.elements:
            return True
        return _member_recursive(current_node.next_node, element_to_find)

    return _member_recursive(unrolled_list.head_node, element)


def reverse(unrolled_list: ImmutableUnrolledLinkedList) -> ImmutableUnrolledLinkedList:
    """Reverses the ImmutableUnrolledLinkedList."""
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list # Return original empty list if empty

    def _reverse_recursive(current_node: Optional[Node], accumulated_list: Optional[Node]) -> Optional[Node]:
        if current_node is None:
            return accumulated_list

        reversed_current_node_values = reversed(current_node.elements) # Reverse elements in current node
        reversed_node = from_list(list(reversed_current_node_values), unrolled_list.node_size).head_node # Create node from reversed values

        return _reverse_recursive(current_node.next_node, concat_nodes(reversed_node, accumulated_list)) # Prepend reversed node

    reversed_head_node = _reverse_recursive(unrolled_list.head_node, None)
    return ImmutableUnrolledLinkedList(reversed_head_node, unrolled_list.node_size)


def intersection(unrolled_list1: ImmutableUnrolledLinkedList, unrolled_list2: ImmutableUnrolledLinkedList) -> ImmutableUnrolledLinkedList:
    #Returns the intersection of two ImmutableUnrolledLinkedLists (assuming set behavior)."""
    if not unrolled_list1 or not unrolled_list2 or unrolled_list1.head_node is None or unrolled_list2.head_node is None:
        return ImmutableUnrolledLinkedList(None, unrolled_list1.node_size if unrolled_list1 else unrolled_list2.node_size) # Return empty list

    intersection_values = []

    def _intersection_recursive(current_node: Optional[Node]):
        nonlocal intersection_values # Allow modifying outer variable
        if current_node is None:
            return

        for val in current_node.elements:
            if member(unrolled_list2, val):
                intersection_values.append(val)
        _intersection_recursive(current_node.next_node) # Recurse

    _intersection_recursive(unrolled_list1.head_node)
    intersection_head_node = from_list(intersection_values, unrolled_list1.node_size).head_node
    return ImmutableUnrolledLinkedList(intersection_head_node, unrolled_list1.node_size)


def to_list(unrolled_list: ImmutableUnrolledLinkedList) -> List[ImmutableUnrolledLinkedList.Num]:
    #Converts the ImmutableUnrolledLinkedList to a list
    res = []
    if not unrolled_list or unrolled_list.head_node is None:
        return res # Return empty list if empty

    def _to_list_recursive(current_node: Optional[Node]):
        nonlocal res
        if current_node is None:
            return
        res.extend(list(current_node.elements))
        _to_list_recursive(current_node.next_node)

    _to_list_recursive(unrolled_list.head_node)
    return res


def from_list(python_list: List[ImmutableUnrolledLinkedList.Num], node_size: int = 4) -> ImmutableUnrolledLinkedList:
    #Creates an ImmutableUnrolledLinkedList from a list
    if not python_list:
        return ImmutableUnrolledLinkedList(None, node_size)

    head_node = None
    current_node_values = []
    current_node_pointer = None

    for item in python_list:
        current_node_values.append(item)
        if len(current_node_values) == node_size:
            new_node = Node(current_node_values, None)
            if head_node is None:
                head_node = new_node
                current_node_pointer = head_node
            else:
                current_node_pointer._next = new_node
                current_node_pointer = new_node
            current_node_values = []

    if current_node_values: # Remaining elements
        new_node = Node(current_node_values, None)
        if head_node is None:
            head_node = new_node
        else:
            current_node_pointer._next = new_node

    return ImmutableUnrolledLinkedList(head_node, node_size)


def find(unrolled_list: ImmutableUnrolledLinkedList, predicate: Callable[[ImmutableUnrolledLinkedList.Num], bool]) -> Optional[ImmutableUnrolledLinkedList.Num]:
    #Finds the first element that satisfies the predicate in the ImmutableUnrolledLinkedList
    if not unrolled_list or unrolled_list.head_node is None:
        return None

    def _find_recursive(current_node: Optional[Node], predicate_func: Callable[[ImmutableUnrolledLinkedList.Num], bool]) -> Optional[ImmutableUnrolledLinkedList.Num]:
        if current_node is None:
            return None

        for value in current_node.elements:
            if predicate_func(value):
                return value # Found element

        return _find_recursive(current_node.next_node, predicate_func) # Recurse if not found in current node

    return _find_recursive(unrolled_list.head_node, predicate)


def filter(unrolled_list: ImmutableUnrolledLinkedList, predicate: Callable[[ImmutableUnrolledLinkedList.Num], bool]) -> ImmutableUnrolledLinkedList:
    #Filters the ImmutableUnrolledLinkedList based on a predicate
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list # Return original empty list if empty

    filtered_values = []

    def _filter_recursive(current_node: Optional[Node]):
        nonlocal filtered_values
        if current_node is None:
            return # Base case: end of list

        for value in current_node.elements:
            if predicate(value):
                filtered_values.append(value) # Add value if predicate is True

        _filter_recursive(current_node.next_node) # Recurse to next node

    _filter_recursive(unrolled_list.head_node)
    filtered_head_node = from_list(filtered_values, unrolled_list.node_size).head_node # Create new list with filtered values
    return ImmutableUnrolledLinkedList(filtered_head_node, unrolled_list.node_size)


def map_list(unrolled_list: ImmutableUnrolledLinkedList, func: Callable[[ImmutableUnrolledLinkedList.Num], ImmutableUnrolledLinkedList.Num]) -> ImmutableUnrolledLinkedList:
    #"Maps a function over the ImmutableUnrolledLinkedLis
    if not unrolled_list or unrolled_list.head_node is None:
        return unrolled_list # Return original empty list if empty

    def _map_recursive(current_node: Optional[Node]) -> Optional[Node]:
        if current_node is None:
            return None # Base case: end of list

        mapped_elements = tuple(func(value) for value in current_node.elements) # Apply func to each element, create tuple
        mapped_next_node = _map_recursive(current_node.next_node) # Map the rest of the list recursively

        return Node(mapped_elements, mapped_next_node) # Create new node with mapped elements

    mapped_head_node = _map_recursive(unrolled_list.head_node)
    return ImmutableUnrolledLinkedList(mapped_head_node, unrolled_list.node_size)


def reduce(unrolled_list: ImmutableUnrolledLinkedList, func: Callable[[ImmutableUnrolledLinkedList.Num, ImmutableUnrolledLinkedList.Num], ImmutableUnrolledLinkedList.Num], initial_value: ImmutableUnrolledLinkedList.Num) -> ImmutableUnrolledLinkedList.Num:
    #Reduces the ImmutableUnrolledLinkedList to a single value
    state = initial_value
    current_node = unrolled_list.head_node if unrolled_list else None # Handle None list

    while current_node is not None:
        for value in current_node.elements:
            state = func(state, value)
        current_node = current_node.next_node
    return state


def empty(node_size: int = 4) -> ImmutableUnrolledLinkedList:
    #Returns an empty ImmutableUnrolledLinkedList
    return ImmutableUnrolledLinkedList(None, node_size)


def concat(unrolled_list1: ImmutableUnrolledLinkedList, unrolled_list2: ImmutableUnrolledLinkedList) -> ImmutableUnrolledLinkedList:
    #Concat two ImmutableUnrolledLinkedLists
    if not unrolled_list1 or unrolled_list1.head_node is None:
        return unrolled_list2 # If list1 is empty, return list2

    concatenated_values = to_list(unrolled_list1) + to_list(unrolled_list2) # l1+l2

    return from_list(concatenated_values, unrolled_list1.node_size) # Rebuild list from concatenated values


def concat_nodes(node1: Optional[Node], node2: Optional[Node]) -> Optional[Node]:
    #Helper function to concatenate Node chains, used internally for reverse
    if node1 is None:
        return node2
    return Node(node1.elements, concat_nodes(node1.next_node, node2))


def iterator(unrolled_list: ImmutableUnrolledLinkedList) -> 'ImmutableUnrolledLinkedListIterator':
    #Returns an iterator for the ImmutableUnrolledLinkedList
    return ImmutableUnrolledLinkedListIterator(unrolled_list)