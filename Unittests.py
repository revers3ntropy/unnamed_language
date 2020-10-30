import unittest

import util
import built_in
from tag import Tag
from interpreter import Interpreter


class TestUtils(unittest.TestCase):

    def test_remove_char_word(self):
        self.assertEqual('est', util.remove_char_word('test', 0))
        self.assertEqual('tes',  util.remove_char_word('test', -1))

    def test_get_up_to_in(self):
        # test for single chars
        self.assertEqual('t', util.get_up_to_in('test', 't'))
        self.assertEqual('tes', util.get_up_to_in('test', 's'))

        # test for edge cases
        self.assertEqual('test: 123', util.get_up_to_in('test: 123', '4'))
        self.assertEqual('1234', util.get_up_to_in(['1', '2', '3', '4'], '5'))
        self.assertEqual('1234', util.get_up_to_in(['1', '2', '3', '4'], '21'))

        # test for searching for multiple things
        self.assertEqual('test: 123', util.get_up_to_in('test: 123', '123'))
        self.assertEqual('test: 123', util.get_up_to_in('test: 123', '111'))
        self.assertEqual('123456', util.get_up_to_in('1234567890', '56'))
        self.assertEqual('123', util.get_up_to_in(['1', '2', '3', '4'], '23'))
        self.assertEqual('1234', util.get_up_to_in(['1', '2', '3', '4'], '34'))

        # test inclusive
        self.assertEqual('test: ', util.get_up_to_in('test: 123', '123', inclusive=False))
        self.assertEqual('', util.get_up_to_in('test: 123', 't', inclusive=False))
        self.assertEqual('t', util.get_up_to_in('test: 123', 't', inclusive=True))


class TestBuiltInFunctions(unittest.TestCase):

    def test_to_string(self):
        self.assertEqual('[1, 2]', built_in.to_string([1, 2]))
        self.assertEqual('12345', built_in.to_string(12345))
        self.assertEqual('1.0', built_in.to_string(float(1)))
        self.assertEqual('False', built_in.to_string(False))

    def test_add(self):
        self.assertEqual(2, built_in.add(1, 1))
        self.assertRaises(TypeError, built_in.add('1', 2))

    def test_subtract(self):
        self.assertEqual(5, built_in.subtract(10, 5))
        self.assertEqual(-5, built_in.subtract(5, 10))
        self.assertRaises(TypeError, built_in.add('1', 2))

    def test_multiply(self):
        self.assertEqual(50, built_in.multiply(10, 5))
        self.assertEqual(1, built_in.multiply(0.1, 10))
        self.assertRaises(TypeError, built_in.multiply('1', 2))

    def test_divide(self):
        self.assertEqual(2, built_in.divide(10, 5))
        self.assertEqual(100, built_in.divide(10, 0.1))
        self.assertRaises(TypeError, built_in.divide('1', 2))


class TestTags(unittest.TestCase):
    def test_assignment(self):
        tag = Tag('var', 'test')
        self.assertEqual('var', tag.type)
        self.assertEqual('test', tag.value)


class TestInterpreter(unittest.TestCase):
    def test_print(self):
        test_code = """
        [run:echo]
            'hello world'
        [-echo]
        """
        interpreter = Interpreter(test_code)


if __name__ == '__main__':
    unittest.main()
