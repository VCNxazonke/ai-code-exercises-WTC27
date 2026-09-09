import unittest
from merge_sort import merge_sort

class TestMergeSort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_element(self):
        self.assertEqual(merge_sort([5]), [5])

    def test_already_sorted(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_with_duplicates(self):
        self.assertEqual(merge_sort([38, 27, 43, 3, 9, 82, 10, 38]), [3, 9, 10, 27, 38, 38, 43, 82])

    def test_negative_numbers(self):
        self.assertEqual(merge_sort([-3, 10, -5, 0, 7]), [-5, -3, 0, 7, 10])

if __name__ == "__main__":
    unittest.main()
