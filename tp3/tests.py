import unittest
import os
from tp3 import main

class TestMain(unittest.TestCase):
    """
    Como para um programa feito em memoria eh algo muito simples, apenas um
    teste geral eh suficiente.
    """
    def test_tp3_example(self):
        try:
            os.remove("output.txt")
        except OSError:
            pass

        main("input.txt", "output.txt")
        data = open("output.txt").read().split('\n')

        self.assertEqual(data[0].strip(), 'confidencia 3')
        self.assertEqual(data[1].strip(), 'fantasias 5')
        self.assertEqual(data[2].strip(), 'historia 2')
        self.assertEqual(data[3].strip(), 'ignoro 3')
        self.assertEqual(data[4].strip(), 'livro 1 3')
        self.assertEqual(data[5].strip(), 'precederam 1')
        self.assertEqual(data[6].strip(), 'quadros 1 4 5')
        self.assertEqual(data[7].strip(), 'sombrear 4')
        self.assertEqual(data[8].strip(), 'verdadeira 1 2')

unittest.main()
