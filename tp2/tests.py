# -*- coding: utf8 -*-
import unittest
from unittest import TestCase
from tp2 import parse_input, main

class ParseInputTest(TestCase):
    def test_tp2_example(self):
        input_data = ['2', '5 8', '1 4 5', '2 5', '3 4', '1 4', '3 4 5',
                      '3 5', '1 5', '1 4', '6 10', '1 2 4', '1 6', '2 6',
                      '1 4', '1 2 5', '2 4', '1 3', '1 2 5', '3', '5']
        instances = parse_input(input_data)
        self.assertEqual(len(instances[1]), 10)

    def test_multiple_instances(self):
        """
        Testa um exemplo com varias instancias.
        """
        input_data = [
            '3',
            '3 4',
            '1 2 3',
            '1 3 4',
            '2 1 3',
            '3 4 5',
            '3 2',
            '4 5',
            '4 6',
            '3 3',
            '4 5',
            '4 6',
            '5 6',
        ]

        instances  = parse_input(input_data)
        self.assertEqual(len(instances), 3)
        self.assertEqual(instances[0], ['1 2 3', '1 3 4', '2 1 3', '3 4 5'])
        self.assertEqual(instances[1], ['4 5', '4 6'])
        self.assertEqual(instances[2], ['4 5', '4 6', '5 6'])

class MainTest(TestCase):
    def test_tp2_example(self):
        # USAR EXEPMLO DO TP1
        main('input.txt', 'output.txt')
        out = [i.strip() for i in open('output.txt')]

        self.assertEqual(out[0], '3')
        self.assertEqual(out[1], '4')

unittest.main()
