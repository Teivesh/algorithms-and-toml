"""Double-ended queue backed by a doubly linked list."""
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class _Node(Generic[T]):
    value: T
    prev: "_Node[T] | None" = None
    next: "_Node[T] | None" = None


class Deque(Generic[T]):
    def __init__(self, values: Iterable[T] = ()) -> None:
        self._head: _Node[T] | None = None
        self._tail: _Node[T] | None = None
        self._size = 0
        for value in values: self.append(value)

    def __len__(self) -> int: return self._size
    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def append(self, value: T) -> None:
        node = _Node(value, self._tail)
        if self._tail is None: self._head = self._tail = node
        else: self._tail.next = node; self._tail = node
        self._size += 1

    def appendleft(self, value: T) -> None:
        node = _Node(value, None, self._head)
        if self._head is None: self._head = self._tail = node
        else: self._head.prev = node; self._head = node
        self._size += 1

    def pop(self) -> T:
        if self._tail is None: raise IndexError("pop from empty Deque")
        node = self._tail
        self._tail = node.prev
        if self._tail is None: self._head = None
        else: self._tail.next = None
        self._size -= 1
        return node.value

    def popleft(self) -> T:
        if self._head is None: raise IndexError("pop from empty Deque")
        node = self._head
        self._head = node.next
        if self._head is None: self._tail = None
        else: self._head.prev = None
        self._size -= 1
        return node.value
