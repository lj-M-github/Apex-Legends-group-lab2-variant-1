from UnrolledLinkedList import UnrolledLinkedList, concat, cons, empty, filter, from_list, length, map, member, reduce, remove, reverse, to_list
import pytest

def test_api():
    # 基础功能测试
    empty_list = empty()
    l1 = cons(None, cons(1, empty()))
    l2 = cons(1, cons(None, empty()))
    
    # 字符串表示
    assert str(empty_list) == "[]"
    assert str(l1) == "[None, 1]"
    assert str(l2) == "[1, None]"
    
    # 相等性判断
    assert empty_list != l1
    assert empty_list != l2
    assert l1 != l2
    assert l1 == cons(None, cons(1, empty()))
    
    # 长度测试
    assert length(empty_list) == 0
    assert length(l1) == 2
    assert length(l2) == 2
    
    # 删除操作
    assert str(remove(l1, 0)) == "[1]"
    assert str(remove(l1, 1)) == "[None]"
    
    # 成员判断
    assert not member(None, empty_list)
    assert member(None, l1)
    assert member(1, l1)
    assert not member(2, l1)
    
    # 反转测试
    assert l1 == reverse(l2)
    
    # 列表转换
    assert to_list(l1) == [None, 1]
    assert l1 == from_list([None, 1])
    
    # 连接操作
    assert concat(l1, l2) == from_list([None, 1, 1, None])
    
    # 迭代器测试
    buf = []
    for e in l1:
        buf.append(e)
    assert buf == [None, 1]
    
    # 集合操作验证
    combined = to_list(l1) + to_list(l2)
    for e in l1:
        combined.remove(e)
    for e in l2:
        combined.remove(e)
    assert combined == []

def test_filter():
    # 过滤偶数
    is_even = lambda x: x % 2 == 0
    lst = from_list([1, 2, 3, 4, 5])
    filtered = filter(lst, is_even)
    
    assert str(filtered) == "[2, 4]"
    assert length(filtered) == 2
    assert member(2, filtered)
    assert not member(3, filtered)
    
    # 空列表测试
    assert filter(empty(), is_even) == empty()

def test_map():
    # 数值转换
    increment = lambda x: x + 1
    lst = from_list([1, 2, 3])
    mapped = map(lst, increment)
    
    assert str(mapped) == "[2, 3, 4]"
    assert to_list(mapped) == [2, 3, 4]
    
    # 类型转换
    to_str = lambda x: str(x)
    assert to_list(map(lst, to_str)) == ["1", "2", "3"]

def test_reduce():
    # 求和测试
    add = lambda acc, x: acc + x
    lst = from_list([1, 2, 3, 4])
    
    assert reduce(lst, add, 0) == 10
    assert reduce(lst, add, 10) == 20
    
    # 空列表测试
    with pytest.raises(ValueError):
        reduce(empty(), add)

def test_empty():
    # 空列表属性验证
    e = empty()
    assert length(e) == 0
    assert str(e) == "[]"
    assert to_list(e) == []
    
    # 空列表操作测试
    assert concat(e, e) == e
    assert remove(e, 1) == e

def test_complex_operations():
    # 复合操作测试
    lst = from_list([5, 3, 8, 2])
    
    # 过滤 + 映射
    result = map(
        filter(lst, lambda x: x > 3),
        lambda x: x * 2
    )
    assert to_list(result) == [10, 16]
    
    # 归约链式操作
    total = reduce(
        map(lst, lambda x: x * 0.5),
        lambda acc, x: acc + x,
        0
    )
    assert total == (5+3+8+2)*0.5

def test_edge_cases():
    # 边界情况测试
    # 单个元素列表
    single = cons(42, empty())
    assert str(single) == "[42]"
    assert remove(single, 42) == empty()
    
    # 大列表操作
    big_list = from_list(list(range(100)))
    assert length(big_list) == 100
    assert member(99, big_list)
    assert not member(100, big_list)
    
    # 类型强制检查
    typed_list = from_list([1, 2, 3])._replace(element_type=int)
    with pytest.raises(TypeError):
        cons("string", typed_list)

def test_monoid_laws():
    # Monoid 定律验证
    a = from_list([1, 2])
    b = from_list([3, 4])
    e = empty()
    
    # 左单位元
    assert concat(e, a) == a
    # 右单位元
    assert concat(a, e) == a
    # 结合律
    assert concat(concat(a, b), e) == concat(a, concat(b, e))

def test_serialization():
    # 序列化测试
    lst = from_list(["a", 1, True])
    assert str(lst) == "[a, 1, True]"
    
    # 嵌套结构
    nested = from_list([from_list([1,2]), from_list([3,4])])
    assert str(nested) == "[[1, 2], [3, 4]]"

def test_immutability():
    # 不可变性验证
    original = from_list([1, 2, 3])
    modified = cons(4, original)
    
    assert original != modified
    assert length(original) == 3
    assert length(modified) == 4
    
    # 删除操作不影响原列表
    removed = remove(original, 2)
    assert member(2, original)
    assert not member(2, removed)

def test_intersection():
    # 基础交集测试
    lst1 = from_list([1, 2, 3, 4])
    lst2 = from_list([3, 4, 5, 6])
    result = intersection(lst1, lst2)
    assert to_list(result) == [3, 4]

    # 空交集测试
    assert intersection(lst1, from_list([5, 6])) == empty()

    # 类型兼容性测试
    typed_lst = from_list([1, 2])._replace(element_type=int)
    with pytest.raises(TypeError):
        intersection(typed_lst, from_list(["a", 1]))

def test_find():
    # 基础查找测试
    lst = from_list([1, 3, 5, 7])
    assert find(lst, lambda x: x % 2 == 0) is None
    assert find(lst, lambda x: x > 4) == 5

    # 空列表测试
    assert find(empty(), lambda x: True) is None

    # 嵌套结构测试
    nested = from_list([["a", 1], [True, None]])
    assert find(nested, lambda x: isinstance(x, list)) == ["a", 1]