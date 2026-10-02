import unittest
from algorithms_and_toml.sorting import bubble_sort, quick_sort


class SortingTests(unittest.TestCase):
    def test_bubble_sort_cases(self):
        self.check_sort(bubble_sort)

    def test_quick_sort_cases(self):
        self.check_sort(quick_sort)

    def check_sort(self, sort):
        for values, expected in [([], []), ([1], [1]), ([3, -1, 2, 2], [-1, 2, 2, 3]), ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5])]:
            with self.subTest(values=values):
                original = values.copy()
                self.assertEqual(sort(values), expected)
                self.assertEqual(values, original)

    def test_sort_with_key(self):
        values = [("b", 2), ("a", 3), ("c", 1)]
        self.assertEqual(quick_sort(values, key=lambda item: item[1]), [("c", 1), ("b", 2), ("a", 3)])
