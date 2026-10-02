"""AVL-balanced binary search tree storing unique keys."""
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class _Node(Generic[T]):
    key: T
    left: "_Node[T] | None" = None
    right: "_Node[T] | None" = None
    height: int = 1


def _height(node: _Node | None) -> int: return node.height if node else 0
def _refresh(node: _Node) -> None: node.height = 1 + max(_height(node.left), _height(node.right))
def _rotate_right(root: _Node[T]) -> _Node[T]:
    pivot = root.left
    assert pivot is not None
    root.left = pivot.right; pivot.right = root
    _refresh(root); _refresh(pivot)
    return pivot
def _rotate_left(root: _Node[T]) -> _Node[T]:
    pivot = root.right
    assert pivot is not None
    root.right = pivot.left; pivot.left = root
    _refresh(root); _refresh(pivot)
    return pivot
def _balance(node: _Node[T]) -> _Node[T]:
    _refresh(node)
    factor = _height(node.left) - _height(node.right)
    if factor > 1:
        assert node.left is not None
        if _height(node.left.left) < _height(node.left.right): node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if factor < -1:
        assert node.right is not None
        if _height(node.right.right) < _height(node.right.left): node.right = _rotate_right(node.right)
        return _rotate_left(node)
    return node


class AVLTree(Generic[T]):
    def __init__(self) -> None: self._root: _Node[T] | None = None; self._size = 0
    def __len__(self) -> int: return self._size
    def __iter__(self) -> Iterator[T]:
        stack: list[_Node[T]] = []; node = self._root
        while stack or node:
            while node: stack.append(node); node = node.left
            node = stack.pop(); yield node.key; node = node.right
    def __contains__(self, key: object) -> bool:
        node = self._root
        while node:
            if key == node.key: return True
            node = node.left if key < node.key else node.right  # type: ignore[operator]
        return False
    def add(self, key: T) -> bool:
        existed = key in self
        def insert(node: _Node[T] | None) -> _Node[T]:
            if node is None: return _Node(key)
            if key < node.key: node.left = insert(node.left)
            elif key > node.key: node.right = insert(node.right)
            else: return node
            return _balance(node)
        self._root = insert(self._root)
        if not existed: self._size += 1
        return not existed
    def discard(self, key: T) -> bool:
        existed = key in self
        def remove(node: _Node[T] | None, target: T) -> _Node[T] | None:
            if node is None: return None
            if target < node.key: node.left = remove(node.left, target)
            elif target > node.key: node.right = remove(node.right, target)
            else:
                if node.left is None: return node.right
                if node.right is None: return node.left
                successor = node.right
                while successor.left: successor = successor.left
                node.key = successor.key
                node.right = remove(node.right, successor.key)
            return _balance(node)
        self._root = remove(self._root, key)
        if existed: self._size -= 1
        return existed
