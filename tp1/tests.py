# -*- coding: utf8 -*-
import unittest
from unittest import TestCase
from tp1 import dfs, bfs, create_graph, parse_input, main, parse_instances


class DFSTest(TestCase):
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
        graph = {1:[(2, 1), (3, 2)], 2:[(4, 3), (5, 4)], 3:[(5, 5)], 4: [(5, 6)], 5:[(1, 1)]}
        self.assertEqual(dfs(graph, 1, 5), [1, 2, 4, 5])

    def test_dfs_lexicographical_order(self):
        """
        A escolha do algoritmo deve ser sempre por seguir a ordem lexicografica.
        """
        graph = {1:[(3, 1), (2, 1)], 2:[(5, 1), (4, 1)],
                 3:[(5, 1), (4, 1)], 4:[(5, 1)], 5:[(1, 1)]}
        self.assertEqual(dfs(graph, 1, 5), [1, 2, 4, 5])


class BFSTest(TestCase):
    def test_bfs(self):
        """
        Teste de busca dfs simples
        """
        graph = {1:[(2, 1), (3, 1)], 2:[(4, 1)], 3:[(5, 1)], 4: [(5, 1)], 5:[(1, 1)]}
        self.assertEqual(bfs(graph, 1, 5), [1, 2, 3, 4, 5])

    def test_bfs_lexicographical_order(self):
        """
        A escolha do algoritmo deve ser sempre por seguir a ordem lexicografica.
        """
        graph = {1:[(2, 1), (3, 1)], 2:[(5, 1)], 3:[(5, 1)], 5:[(1, 1)]}
        self.assertEqual(bfs(graph, 1, 5), [1, 2, 3, 5])

class CreateGraphTest(TestCase):
    def test_simple_graph_creation(self):
        """
        Criacao simples de um grafo e suas adjacencias
        """
        graph = create_graph(['1 2 1', '1 3 1', '2 4 1', '2 5 1', '3 4 1',
                              '3 5 1', '4 5 1',
                              '5 1 1'])
        self.assertTrue(1 in graph)
        self.assertTrue(2 in graph)
        self.assertTrue(3 in graph)
        self.assertTrue(4 in graph)
        self.assertTrue(5 in graph)
        self.assertEqual(sorted(graph[1]), [(2, 1), (3, 1)])
        self.assertEqual(sorted(graph[2]), [(4, 1), (5, 1)])
        self.assertEqual(sorted(graph[3]), [(4, 1), (5, 1)])
        self.assertEqual(sorted(graph[4]), [(5, 1)])
        self.assertEqual(sorted(graph[5]), [(1, 1)])


class ParseInputTest(TestCase):
    def test_simple_given_example(self):
        """
        Testa o exemplo dado no enunciado do tp1
        """
        input_data = [
            '7 13',
            '1 2 4',
            '1 3 6',
            '1 4 8',
            '2 3 1',
            '2 5 7',
            '3 4 2',
            '3 6 4',
            '3 5 5',
            '4 6 5',
            '5 6 7',
            '5 7 6',
            '6 5 1',
            '6 7 8',
            '3',
            '1 1 4',
            '2 1 3',
            '3 1 2'
        ]

        edges = [
            '1 2 4',
            '1 3 6',
            '1 4 8',
            '2 3 1',
            '2 5 7',
            '3 4 2',
            '3 6 4',
            '3 5 5',
            '4 6 5',
            '5 6 7',
            '5 7 6',
            '6 5 1',
            '6 7 8',
        ]

        tests = [
            '1 1 4',
            '2 1 3',
            '3 1 2'
        ]

        e, t = parse_input(input_data)
        self.assertEqual(e, edges)
        self.assertEqual(t, tests)


class TestParseInstances(TestCase):
    def test_simple_example(self):
        """
        Testa o um exemplo de parsing
        """
        input_data = [
        '1',
        '12 11 1',
        '1 2 1',
        '1 7 1',
        '1 8 1',
        '2 3 1',
        '3 4 1',
        '3 5 1',
        '2 6 1',
        '8 9 1',
        '8 12 1',
        '10 9 1',
        '11 9 1',
        '3',
        '1 1 12',
        '2 2 7',
        '3 4 9']

        r = parse_instances(input_data)
        self.assertEqual(r[0], ['12 11 1', '1 2 1', '1 7 1','1 8 1', '2 3 1',
                                '3 4 1', '3 5 1', '2 6 1', '8 9 1', '8 12 1',
                                '10 9 1', '11 9 1', '3', '1 1 12',
                                '2 2 7', '3 4 9'])

    def test_multiple_instances(self):
        ex1 = [
            '2',
            '3 2',
            '1 3 1',
            '1 2 1',
            '3',
            '1 3',
            '2 3',
            '1 2',
            '5 4 1',
            '3 2 1',
            '1 3 1',
            '2 4 1',
            '4 5 1',
            '4',
            '1 5',
            '2 5',
            '5 1',
            '1 3'
        ]
        r = parse_instances(ex1)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], ['3 2', '1 3 1', '1 2 1', '3', '1 3', '2 3', '1 2'])
        self.assertEqual(r[1], ['5 4 1', '3 2 1', '1 3 1', '2 4 1', '4 5 1', '4', '1 5',
                                '2 5', '5 1', '1 3'])

class MainTest(TestCase):
    def test_tp1_example(self):
        # USAR EXEPMLO DO TP1
        main('input.txt', 'output.txt')
        out = [i.strip() for i in open('output.txt')]

        self.assertEqual(out[0], '1 2 3 4')
        self.assertEqual(out[1], '1 2 3')
        self.assertEqual(out[2], '1 2')

unittest.main()
