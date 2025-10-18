import unittest
from functions.write_file import write_file

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

if __name__ == "__main__":
    unittest.main()