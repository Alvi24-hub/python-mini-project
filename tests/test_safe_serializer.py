import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from security.safe_serializer import SafeSerializer

class TestSafeSerializer(unittest.TestCase):
    def test_safe_load_json_valid(self):
        data = '{"name": "Alice", "role": "user", "active": true}'
        result = SafeSerializer.safe_load_json(data)
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["role"], "user")
        self.assertTrue(result["active"])

    def test_safe_load_json_invalid_type(self):
        with self.assertRaises(ValueError):
            SafeSerializer.safe_load_json(12345)

    def test_safe_load_literal_valid(self):
        data = "{'a': 1, 'b': [2, 3, 4], 'c': None}"
        result = SafeSerializer.safe_load_literal(data)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], [2, 3, 4])
        self.assertIsNone(result["c"])

    def test_safe_load_literal_rejects_code_execution(self):
        malicious = "__import__('os').system('echo hacked')"
        with self.assertRaises((ValueError, SyntaxError)):
            SafeSerializer.safe_load_literal(malicious)

if __name__ == "__main__":
    unittest.main()
