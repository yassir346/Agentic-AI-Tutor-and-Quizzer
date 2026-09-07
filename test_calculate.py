import unittest
from tools import calculate


class TestCalculate(unittest.TestCase):
    def test_basic_multiplication(self):
        self.assertEqual(calculate("12 * (7 + 3)"), 120)

    def test_division(self):
        self.assertEqual(calculate("100 / 4 - 5"), 20.0)

    def test_rejects_non_arithmetic(self):
        with self.assertRaises(ValueError):
            calculate("open('notes.txt').read()")


if __name__ == "__main__":
    unittest.main()