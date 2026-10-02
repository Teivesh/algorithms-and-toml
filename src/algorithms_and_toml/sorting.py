"""Elementary sorting algorithms that do not mutate their input."""
from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


def bubble_sort(values: Sequence[T], *, key: Callable[[T], object] | None = None) -> list[T]:
    """Return values sorted with bubble sort (stable, O(n²))."""
    result = list(values)
    get_key = key or (lambda item: item)
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if get_key(result[index]) > get_key(result[index + 1]):
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break
    return result


def quick_sort(values: Sequence[T], *, key: Callable[[T], object] | None = None) -> list[T]:
    """Return values sorted with an iterative three-way quicksort.

    Three-way partitioning handles duplicate-heavy inputs efficiently. An
    explicit stack avoids Python recursion limits on already sorted data.
    """
    result = list(values)
    get_key = key or (lambda item: item)
    stack = [(0, len(result) - 1)] if result else []
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = get_key(result[(low + high) // 2])
        less, current, greater = low, low, high
        while current <= greater:
            current_key = get_key(result[current])
            if current_key < pivot:
                result[less], result[current] = result[current], result[less]
                less += 1
                current += 1
            elif current_key > pivot:
                result[current], result[greater] = result[greater], result[current]
                greater -= 1
            else:
                current += 1
        # Process the smaller partition next to keep the pending stack bounded.
        left, right = (low, less - 1), (greater + 1, high)
        if left[1] - left[0] < right[1] - right[0]:
            if right[0] < right[1]: stack.append(right)
            if left[0] < left[1]: stack.append(left)
        else:
            if left[0] < left[1]: stack.append(left)
            if right[0] < right[1]: stack.append(right)
    return result
