# -*- coding: utf8 -*-
import unittest
from tp0 import dfs, create_graph, parse_input, main, parse_instances


class DFSTest(unittest.TestCase):
    def test_dfs(self):
        """
        Teste de busca dfs simples. O grafo é direcionado e tem a aparencia de
        um diamante:
            +---- 1
            |   /   \
            |  2--4--3
            |   \ | /
            +---- 5
        """
        graph = {1:[2, 3], 2:[4, 5], 3:[4, 5], 4: [5], 5:[1]}
        self.assertEqual(dfs(graph, 1, 5), [1, 2, 4, 5])

    def test_dfs_lexicographical_order(self):
        """
        A escolha do algoritmo deve ser sempre por seguir a ordem lexicografica.
        """
        graph = {1:[3, 2], 2:[5, 4],3:[5, 4], 4:[5], 5:[1]}
        self.assertEqual(dfs(graph, 1, 5), [1, 2, 4, 5])


class CreateGraphTest(unittest.TestCase):
    def test_simple_graph_creation(self):
        """
        Criacao simples de um grafo e suas adjacencias
        """
        graph = create_graph(['1 2', '1 3', '2 4', '2 5', '3 4', '3 5', '4 5',
                              '5 1'])
        self.assertTrue(1 in graph)
        self.assertTrue(2 in graph)
        self.assertTrue(3 in graph)
        self.assertTrue(4 in graph)
        self.assertTrue(5 in graph)
        self.assertEqual(sorted(graph[1]), [2, 3, 5])
        self.assertEqual(sorted(graph[2]), [1, 4, 5])
        self.assertEqual(sorted(graph[3]), [1, 4, 5])
        self.assertEqual(sorted(graph[4]), [2, 3, 5])
        self.assertEqual(sorted(graph[5]), [1, 2, 3, 4])


class ParseInputTest(object):
    def test_tp0_given_example(self):
        """
        Testa o exemplo dado no enunciado do tp0
        """
        input_data = [
        '1',
        '12 11',
        '1 2',
        '1 7',
        '1 8',
        '2 3',
        '3 4',
        '3 5',
        '2 6',
        '8 9',
        '8 12',
        '10 9',
        '11 9',
        '3',
        '1 12',
        '2 7',
        '4 9']

        edges = [
            '1 2',
            '1 7',
            '1 8',
            '2 3',
            '3 4',
            '3 5',
            '2 6',
            '8 9',
            '8 12',
            '10 9',
            '11 9',
        ]

        tests = [
            '1 12',
            '2 7',
            '4 9'
        ]

        e, t = parse_input(input_data)
        self.assertEqual(e, edges)
        self.assertEqual(t, tests)


class TestParseInstances(unittest.TestCase):
    def test_tp0_given_example(self):
        """
        Testa o exemplo dado no enunciado do tp0
        """
        input_data = [
        '1',
        '12 11',
        '1 2',
        '1 7',
        '1 8',
        '2 3',
        '3 4',
        '3 5',
        '2 6',
        '8 9',
        '8 12',
        '10 9',
        '11 9',
        '3',
        '1 12',
        '2 7',
        '4 9']

        r = parse_instances(input_data)
        self.assertEqual(r[0], ['12 11', '1 2', '1 7','1 8', '2 3', '3 4',
                                '3 5', '2 6', '8 9', '8 12',
                                '10 9', '11 9', '3', '1 12',
                                '2 7', '4 9'])

    def test_multiple_instances(self):
        ex1 = [
            '2',
            '3 2',
            '1 3',
            '1 2',
            '3',
            '1 3',
            '2 3',
            '1 2',
            '5 4',
            '3 2',
            '1 3',
            '2 4',
            '4 5',
            '4',
            '1 5',
            '2 5',
            '5 1',
            '1 3'
        ]
        r = parse_instances(ex1)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], ['3 2', '1 3', '1 2', '3', '1 3', '2 3', '1 2'])
        self.assertEqual(r[1], ['5 4', '3 2', '1 3', '2 4', '4 5', '4', '1 5',
                                '2 5', '5 1', '1 3'])

class MainTest(unittest.TestCase):
    def test_tp0_given_example(self):
        main('input.txt', 'output.txt')
        out = [i.strip() for i in open('output.txt')]

        self.assertEqual(out[0], '1 2 3 4 5 6 7 8 9 10 11 12')
        self.assertEqual(out[1], '2 1 7')
        self.assertEqual(out[2], '4 3 2 1 7 8 9')

unittest.main()
