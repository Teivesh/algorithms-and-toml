import json
import unittest
from algorithms_and_toml.toml_json import convert_toml


class TomlJsonTests(unittest.TestCase):
    def test_convert_requires_three_fields_and_sorts_arrays_recursively(self):
        text = '''name = "demo"\nversion = 1\ntags = ["z", "a", "m"]\n[meta]\nvalues = [3, 1, 2]\n'''
        result = convert_toml(text)
        self.assertEqual(result["tags"], ["a", "m", "z"])
        self.assertEqual(result["meta"]["values"], [1, 2, 3])
        self.assertEqual(json.loads(json.dumps(result)), result)

    def test_convert_rejects_fewer_than_three_fields(self):
        with self.assertRaisesRegex(ValueError, "at least three"):
            convert_toml('one = 1\ntwo = 2\n')

    def test_mixed_array_is_deterministic(self):
        result = convert_toml('a = [3, "x", 1]\nb = true\nc = false\n')
        self.assertEqual(result["a"], [1, 3, "x"])

    def test_numeric_order_and_toml_dates_are_json_compatible(self):
        result = convert_toml('numbers = [10, 2, -1]\nname = "demo"\nenabled = true\nday = 1979-05-27\n')
        self.assertEqual(result["numbers"], [-1, 2, 10])
        self.assertEqual(result["day"], "1979-05-27")
        json.dumps(result)

if __name__ == "__main__": unittest.main()
