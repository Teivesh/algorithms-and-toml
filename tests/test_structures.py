import unittest
from algorithms_and_toml.structures import AVLTree, Deque, DynamicArray, LinkedList


class StructureTests(unittest.TestCase):
    def test_dynamic_array_growth_shrink_index_and_pop(self):
        values = DynamicArray(range(20))
        self.assertEqual(values[-1], 19)
        self.assertEqual(values[2:5], [2, 3, 4])
        self.assertEqual(values.pop(0), 0)
        for _ in range(18): values.pop()
        self.assertEqual(list(values), [1])
        with self.assertRaises(IndexError): values[5]

    def test_linked_list_head_tail_and_membership(self):
        values = LinkedList([2, 3])
        values.prepend(1); values.append(4)
        self.assertEqual(list(values), [1, 2, 3, 4])
        self.assertIn(3, values)
        self.assertEqual([values.pop_front(), values.pop_front(), values.pop_front(), values.pop_front()], [1, 2, 3, 4])
        with self.assertRaises(IndexError): values.pop_front()

    def test_deque_operations_both_ends(self):
        values = Deque([2, 3])
        values.appendleft(1); values.append(4)
        self.assertEqual(list(values), [1, 2, 3, 4])
        self.assertEqual([values.popleft(), values.pop(), values.pop(), values.popleft()], [1, 4, 3, 2])
        with self.assertRaises(IndexError): values.pop()

    def test_avl_insert_contains_sorted_and_delete(self):
        tree = AVLTree[int]()
        for value in [10, 20, 30, 40, 50, 25, 5, 4, 3]: self.assertTrue(tree.add(value))
        self.assertFalse(tree.add(10))
        self.assertIn(25, tree)
        self.assertNotIn(99, tree)
        self.assertEqual(list(tree), [3, 4, 5, 10, 20, 25, 30, 40, 50])
        self.assertTrue(tree.discard(30))
        self.assertFalse(tree.discard(300))
        self.assertEqual(list(tree), [3, 4, 5, 10, 20, 25, 40, 50])
        self.assertEqual(len(tree), 8)

if __name__ == "__main__": unittest.main()
