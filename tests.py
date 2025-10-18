import unittest
from functions.write_file import write_file
from functions.run_python_file import run_python_file   

class TestLorem(unittest.TestCase):
        def test_write_root_file(self):
            content = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
            self.assertIn("Successfully wrote to", content)
            print(content)  

        def test_write_nested_file(self):
            content = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
            self.assertIn("Successfully wrote to", content)
            print(content)

        def test_reject_outside_directory(self):
            content = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
            self.assertIn("Error:", content)
            print(content)

class TestRunPythonFile(unittest.TestCase):
        
        def test_run_usage_no_args(self):
            output = run_python_file("calculator", "main.py")
            print(output)
            self.assertIn("STDOUT:", output)

        def test_run_non_with_args(self):
            output = run_python_file("calculator", "main.py", ["3 + 5"])
            self.assertIn("STDOUT:", output)
            print(output)

        def test_running_calculator_tests(self):
            output = run_python_file("calculator", "tests.py")
            self.assertIn("STDOUT:", output)
            print(output)

        def test_reject_outside_directory(self):
            output = run_python_file("calculator", "../main.py")
            self.assertIn("Error:", output)
            print(output)

        def test_run_nonexistent_file(self):
            output = run_python_file("calculator", "nonexistent.py")
            self.assertIn("Error:", output)
            print(output)

        def test_file_with_wrong_type(self):
            output = run_python_file("calculator", "lorem.txt")
            self.assertIn("Error:", output)
            print(output)

if __name__ == "__main__":
    unittest.main()