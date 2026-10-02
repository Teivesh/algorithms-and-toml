"""A small resizable array implementation."""
from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar, overload

T = TypeVar("T")


class DynamicArray(Generic[T]):
    def __init__(self, values: Iterable[T] = ()) -> None:
        items = list(values)
        self._capacity = max(4, len(items))
        self._size = len(items)
        self._items: list[T | None] = items + [None] * (self._capacity - self._size)

    def __len__(self) -> int: return self._size
    def __iter__(self) -> Iterator[T]:
        for i in range(self._size): yield self._items[i]  # type: ignore[misc]

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> list[T]: ...
    def __getitem__(self, index: int | slice) -> T | list[T]:
        if isinstance(index, slice): return list(self)[index]
        if index < 0: index += self._size
        if not 0 <= index < self._size: raise IndexError("DynamicArray index out of range")
        return self._items[index]  # type: ignore[return-value]

    def append(self, value: T) -> None:
        if self._size == self._capacity:
            self._capacity *= 2
            self._items.extend([None] * (self._capacity - self._size))
        self._items[self._size] = value
        self._size += 1

    def pop(self, index: int = -1) -> T:
        if not self._size: raise IndexError("pop from empty DynamicArray")
        if index < 0: index += self._size
        if not 0 <= index < self._size: raise IndexError("DynamicArray index out of range")
        value = self._items[index]
        for i in range(index, self._size - 1): self._items[i] = self._items[i + 1]
        self._size -= 1
        self._items[self._size] = None
        if self._capacity > 4 and self._size <= self._capacity // 4:
            self._capacity = max(4, self._capacity // 2)
            self._items = self._items[:self._capacity]
        return value  # type: ignore[return-value]

    def __repr__(self) -> str: return f"DynamicArray({list(self)!r})"
