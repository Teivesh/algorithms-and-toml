"""Singly linked list with efficient append and removal from the head."""
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class _Node(Generic[T]):
    value: T
    next: "_Node[T] | None" = None


class LinkedList(Generic[T]):
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
        node = _Node(value)
        if self._tail is None: self._head = self._tail = node
        else: self._tail.next = node; self._tail = node
        self._size += 1

    def prepend(self, value: T) -> None:
        self._head = _Node(value, self._head)
        if self._tail is None: self._tail = self._head
        self._size += 1

    def pop_front(self) -> T:
        if self._head is None: raise IndexError("pop from empty LinkedList")
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        if self._head is None: self._tail = None
        return value

    def __contains__(self, value: object) -> bool: return any(item == value for item in self)
    def __repr__(self) -> str: return f"LinkedList({list(self)!r})"
