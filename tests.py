import unittest
from functions.get_file_content import get_file_content

class TestLorem(unittest.TestCase):
        def test_main_py(self):
            content = get_file_content("calculator", "main.py")
            self.assertIsInstance(content, str)
            self.assertIn("def main():", content)
            print(content)  

        def test_pkg_calculator_py(self):
            content = get_file_content("calculator", "pkg/calculator.py")
            self.assertIsInstance(content, str)
            self.assertIn("def _apply_operator(self, operators, values)", content)  
            print(content)

        def test_outside_workdir(self):
            content = get_file_content("calculator", "/bin/cat")
            self.assertIsInstance(content, str)
            self.assertTrue(content.startswith("Error:"))
            print(content)

        def test_missing_file(self):
            content = get_file_content("calculator", "pkg/does_not_exist.py")
            self.assertIsInstance(content, str)
            self.assertTrue(content.startswith("Error:"))
            print(content)

if __name__ == "__main__":
    unittest.main()