from typing import Any, Callable, Optional, TypeVar, Generic
from functools import reduce as functools_reduce

T = TypeVar('T')

class ImmutableNode:
    __slots__ = ('elements', 'next', 'last')
    def __init__(self, elements: tuple, next: Optional['ImmutableNode'] = None, 
                 last: Optional['ImmutableNode'] = None):
        self.elements = elements  # 使用元组保证不可变性
        self.next = next
        self.last = last

    def __repr__(self):
        return f"Node({self.elements})"

    def _replace(self, **kwargs):
        return ImmutableNode(
            elements=kwargs.get('elements', self.elements),
            next=kwargs.get('next', self.next),
            last=kwargs.get('last', self.last)
        )

class UnrolledLinkedList(Generic[T]):
    size = 4

    def __init__(self, element_type: Optional[type] = None, size: int = 4,
                 head: Optional[ImmutableNode] = None, current_node: Optional[ImmutableNode] = None,
                 current_index: int = 0, length: int = 0):
        self.element_type = element_type
        self.size = size if size is not None else self.__class__.size  # 修正size初始化
        self.head = head
        self._current_node = current_node
        self._current_index = current_index
        self._length = length  # 缓存长度提升性能

    def _check_type(self, value: T):
        if self.element_type is not None and not isinstance(value, self.element_type):
            raise TypeError(f"Expected {self.element_type}, got {type(value)}")

    @classmethod
    def empty(cls) -> 'UnrolledLinkedList':
        return cls()

    def is_empty(self) -> bool:
        return self.head is None

    # ------------------- 核心递归方法 -------------------
    def _cons_recursive(self, node: Optional[ImmutableNode], value: T, 
                       remaining_size: int) -> ImmutableNode:
        if node is None or remaining_size <= 0:
            return ImmutableNode((value,))
        
        if len(node.elements) < self.size:
            return node._replace(elements=(value,) + node.elements)
        else:
            # 分割节点
            half = self.size // 2
            new_elements = (value,) + node.elements[:half]
            new_next = ImmutableNode(
                elements=node.elements[half:],
                next=node.next,
                last=node
            )
            return ImmutableNode(
                elements=new_elements,
                next=self._cons_recursive(new_next, value, remaining_size - half)
            )

    def cons(self, value: T) -> 'UnrolledLinkedList[T]':
        self._check_type(value)
        if self.is_empty():
            new_head = ImmutableNode((value,))
            return UnrolledLinkedList(
                element_type=self.element_type,
                size=self.size,
                head=new_head,
                current_node=new_head,
                current_index=1,
                length=1
            )
        else:
            new_head = self._cons_recursive(self.head, value, self.size)
            return UnrolledLinkedList(
                element_type=self.element_type,
                size=self.size,
                head=new_head,
                length=self._length + 1
            )._rebalance()

    # ------------------- 其他递归实现的方法 -------------------
    def _remove_recursive(self, node: Optional[ImmutableNode], value: T) -> Optional[ImmutableNode]:
        if node is None:
            return None

        new_elements = tuple(e for e in node.elements if e != value)
        removed_count = len(node.elements) - len(new_elements)

        if removed_count == 0:
            return node._replace(next=self._remove_recursive(node.next, value))

        new_next = self._remove_recursive(node.next, value)
        if len(new_elements) == 0:
            return new_next
        else:
            return node._replace(elements=new_elements, next=new_next)

    def remove(self, value: T) -> 'UnrolledLinkedList[T]':
        new_head = self._remove_recursive(self.head, value)
        return UnrolledLinkedList(
            element_type=self.element_type,
            size=self.size,
            head=new_head
        )._rebalance()._recalculate_metadata()

    # ------------------- Monoid 实现 -------------------
    def concat(self, other: 'UnrolledLinkedList[T]') -> 'UnrolledLinkedList[T]':
        def _concat_nodes(a: Optional[ImmutableNode], b: Optional[ImmutableNode]) -> Optional[ImmutableNode]:
            if a is None:
                return b
            if b is None:
                return a
            return a._replace(next=_concat_nodes(a.next, b))

        new_head = _concat_nodes(self.head, other.head)
        return UnrolledLinkedList(
            element_type=self.element_type,
            size=self.size,
            head=new_head
        )._rebalance()._recalculate_metadata()

    # ------------------- 工具方法 -------------------
    def _rebalance(self) -> 'UnrolledLinkedList[T]':
        # 重新平衡节点大小 (递归实现)
        def rebalance_node(node: Optional[ImmutableNode]) -> Optional[ImmutableNode]:
            if node is None:
                return None

            if len(node.elements) > self.size:
                # 分割节点
                half = len(node.elements) // 2
                left = node.elements[:half]
                right = node.elements[half:]
                new_node = ImmutableNode(
                    elements=right,
                    next=rebalance_node(node.next)
                )
                return ImmutableNode(
                    elements=left,
                    next=new_node
                )
            elif node.next and len(node.elements) + len(node.next.elements) <= self.size:
                # 合并节点
                merged = node.elements + node.next.elements
                return ImmutableNode(
                    elements=merged,
                    next=rebalance_node(node.next.next)
                )
            else:
                return node._replace(next=rebalance_node(node.next))

        return self._replace(head=rebalance_node(self.head))

    def _recalculate_metadata(self) -> 'UnrolledLinkedList[T]':
        # 递归计算长度和当前节点
        def calculate_length(node: Optional[ImmutableNode]) -> int:
            return 0 if node is None else len(node.elements) + calculate_length(node.next)

        length = calculate_length(self.head)
        return self._replace(_length=length)

    # ------------------- 其他必需方法 -------------------
    def length(self) -> int:
        return self._length

    def member(self, value: T) -> bool:
        def search(node: Optional[ImmutableNode]) -> bool:
            if node is None:
                return False
            return value in node.elements or search(node.next)
        return search(self.head)

    def reverse(self) -> 'UnrolledLinkedList[T]':
        def reverse_nodes(node: Optional[ImmutableNode], prev: Optional[ImmutableNode]) -> Optional[ImmutableNode]:
            if node is None:
                return prev
            next_node = node.next
            return reverse_nodes(next_node, ImmutableNode(
                elements=node.elements[::-1],
                next=prev,
                last=next_node
            ))
        return self._replace(head=reverse_nodes(self.head, None))

    # ------------------- Python特殊方法 -------------------
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UnrolledLinkedList):
            return False
        return self.to_list() == other.to_list()

    def __str__(self) -> str:
        elements = self.to_list()
        return f"[{', '.join(map(str, elements))}]"

    def __iter__(self):
        current = self.head
        while current is not None:
            yield from current.elements
            current = current.next

    # ------------------- 完整实现需要其他方法 -------------------
    # 以下方法需要类似的递归实现：
    # map, filter, reduce, from_list, intersection等
    # 由于篇幅限制，这里展示部分实现，其余方法实现逻辑类似

    def _replace(self, **kwargs):
        return UnrolledLinkedList(
            element_type=kwargs.get('element_type', self.element_type),
            size=kwargs.get('size', self.size),
            head=kwargs.get('head', self.head),
            current_node=kwargs.get('current_node', self._current_node),
            current_index=kwargs.get('current_index', self._current_index),
            length=kwargs.get('length', self._length)
        )

    @classmethod
    def from_list(cls, lst: list) -> 'UnrolledLinkedList[T]':
        def build_nodes(elements: list, size: int) -> Optional[ImmutableNode]:
            if not elements:
                return None
            return ImmutableNode(
                elements=tuple(elements[:size]),
                next=build_nodes(elements[size:], size)
            )
        
        return cls(
            head=build_nodes(lst, cls.size),
            length=len(lst)
        )

    def to_list(self) -> list:
        def collect(node: Optional[ImmutableNode], acc: list) -> list:
            if node is None:
                return acc
            return collect(node.next, acc + list(node.elements))
        return collect(self.head, [])
    
    def filter(self, predicate: Callable[[T], bool]) -> 'UnrolledLinkedList[T]':
        def _filter_node(node: Optional[ImmutableNode]) -> Optional[ImmutableNode]:
            if node is None:
                return None
            filtered = tuple(e for e in node.elements if predicate(e))
            if not filtered:
                return _filter_node(node.next)
            return ImmutableNode(
                elements=filtered,
                next=_filter_node(node.next)
            )
        return self._replace(head=_filter_node(self.head))._recalculate_metadata()

    def map(self, func: Callable[[T], Any]) -> 'UnrolledLinkedList[T]':
        def _map_node(node: Optional[ImmutableNode]) -> Optional[ImmutableNode]:
            if node is None:
                return None
            mapped = tuple(func(e) for e in node.elements)
            return ImmutableNode(
                elements=mapped,
                next=_map_node(node.next)
            )
        return self._replace(head=_map_node(self.head))

    @staticmethod
    def reduce(lst: 'UnrolledLinkedList[T]', func: Callable[[Any, T], Any], initial: Any) -> Any:
        acc = initial
        for elem in lst:
            acc = func(acc, elem)
        return acc
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        def _find(node: Optional[ImmutableNode]) -> Optional[T]:
            if node is None:
                return None
            for e in node.elements:
                if predicate(e):
                    return e
            return _find(node.next)
        return _find(self.head)

    def intersection(self, other: 'UnrolledLinkedList[T]') -> 'UnrolledLinkedList[T]':
        def _intersect(node: Optional[ImmutableNode]) -> Optional[ImmutableNode]:  # 修改返回类型
            if node is None:
                return None
            filtered = tuple(e for e in node.elements if other.member(e))
            new_next = _intersect(node.next)
            if not filtered:
                return new_next
            return ImmutableNode(
                elements=filtered,
                next=new_next
            )
        
        new_head = _intersect(self.head)
        return UnrolledLinkedList(
            head=new_head,
            element_type=self.element_type,
            size=self.size
        )._rebalance()._recalculate_metadata()
    
# 函数式API包装
def concat(a, b):
    return a.concat(b)

def cons(value, lst):
    return lst.cons(value)

def empty():
    return UnrolledLinkedList.empty()

def from_list(lst):
    return UnrolledLinkedList.from_list(lst)

def length(lst):
    return lst.length()

def member(value, lst):
    return lst.member(value)

def remove(lst, value):
    return lst.remove(value)

def reverse(lst):
    return lst.reverse()

def to_list(lst):
    return lst.to_list()

def filter(lst, predicate):
    return lst.filter(predicate)

def map_ull(lst, func):
    return lst.map(func)

def reduce(lst, func, initial):
    return UnrolledLinkedList.reduce(lst, func, initial)

def intersection(lst1, lst2):
    return lst1.intersection(lst2)

def find(lst, predicate):
    return lst.find(predicate)

__all__ = [
    'UnrolledLinkedList', 'concat', 'cons', 'empty', 'filter', 'from_list',
    'length', 'map_ull', 'member', 'reduce', 'remove', 'reverse', 'to_list',
    'intersection', 'find'
]
