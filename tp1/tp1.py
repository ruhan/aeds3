# -*- coding: utf8 -*-
def _split_edge(edge):
    """
    Apenas transforma uma string de aresta em dois nos inteiros
    """
    u, v, w = edge.split(' ')
    return int(u), int(v), int(w)

def parse_instances(lines):
    """
    Apanha e separa as instancias de problema (grafo + testes) existentes no
    arquivo, retornando uma lista de instancias.
    """
    now = 1

    instances = []

    while now < len(lines):
        n_graph = int(lines[now].split(' ')[1])
        n_tests = int(lines[now+n_graph+1])
        instances.append(lines[now:now+n_graph+n_tests+2])
        now += n_graph+n_tests+2

    return instances

def main(finput, foutput):
    """
    Executa o programa como um todo a partir de dois arquivos: um de entrada e
    outro de saida.
    """
    out = open(foutput, 'w')

    for instance in parse_instances([ i.strip() for i in open(finput)]):
        output = []
        edges, tests = parse_input(instance)

        graph = create_graph(edges)

        for test in tests:
            a, u, v = _split_edge(test)

            if a == 1:
                output.append(" ".join(map(lambda x: str(x), bfs(graph, u, v))))
            elif a == 2:
                output.append(" ".join(map(lambda x: str(x), dfs(graph, u, v))))
            elif a == 3:
                output.append(" ".join(map(lambda x: str(x), shortest_path(graph, u, v))))

        out.write("\n".join(output))
        out.write("\n")

    out.close()

def parse_input(input_data):
    """
    Dado uma entrada (list [for testability]) retorna a saida conforme
    solicitado pelo enunciado.
    """
    edges = []
    tests = []

    n_edges = int(input_data[0].split(' ')[1])

    for edge in input_data[1:1+n_edges]:
        edges.append(edge)

    for test in input_data[1+n_edges+1:]:
        tests.append(test)

    return edges, tests

def create_graph(edges):
    """
    Recebe uma lista de arestas (string) e gera um grafo no formato matriz
    de adjacencias (grafo direcionado):

    @Return: Um exemplo de grafo gerado seria:
        Entrada:
            A B
            A C
            B D
            B E
            C D
            C E
        Saida:
            graph = {'A':[('B', 1), ('C', 1)],'B':[('D', 1),
                     ('E', 1)],'C':[('D', 1), ('E', 1)]}
    """
    graph = {}

    for e in edges:
        u, v, w = _split_edge(e)

        if u in graph:
            graph[u].append((v, w))
        else:
            graph[u] = [(v, w)]

        """ Grafo nao simetrico!
        # Garante o grafo nao direcionado
        if v in graph:
            graph[v].append((u, w))
        else:
            graph[v] = [(u, w)]
        """

    return graph

def dfs(graph, start_node, end_node, path=[]):
    """
    Faz uma busca em PROFUNDIDADE entre start_node e end_node.
    @Return: lista com o caminho percorrido pela busca, na lista start_node e
    end_node estao inclusos.
    """
    q = [start_node]

    while q:
        v = q.pop(0)

        if v not in path:
            path = path + [v]
            # XXX: esse sorted possui uma performance ruim, por ser executado
            # varias vezes. Como essa é uma implementação "toy" isso pode não
            # ser um problema. Caso isso torne lento o processo basta fazer
            # esse sort apenas uma vez na geração do grafo, apenas perderíamos
            # a qualidade de essa função (dfs) ser standalone nesse sentido
            # NOTE: Utilizando o indice 0 ffazemos por ordem Lexicografica!
            try:
                q = sorted([ g[0] for g in graph.get(v, [])]) + q
            except:
                import pdb;pdb.set_trace()

        if v == end_node:
            return path

    return path


def bfs(graph, start_node, end_node):
    """
    Faz uma busca em LARGURA entre start_node e end_node.
    @Return: lista com o caminho percorrido pela busca, na lista start_node e
    end_node estao inclusos.
    """
    q = [[start_node]]
    visited = set()
    visited.add(start_node)

    while q:
        tmp_path = q.pop(0)
        last_node = tmp_path[-1]
        visited.add(last_node)

        # Path encontrado
        if last_node == end_node:
            # FIXME: If you want bfs short path, return tmp_path
            return list(visited)

        # XXX: esse sorted possui uma performance ruim, por ser executado
        # varias vezes. Como essa é uma implementação "toy" isso pode não
        # ser um problema. Caso isso torne lento o processo basta fazer
        # esse sort apenas uma vez na geração do grafo, apenas perderíamos
        # a qualidade de essa função (bfs) ser standalone nesse sentido
        # NOTE: Utilizando o indice 0 fazemos por ordem Lexicografica funcionar!
        for link_node in sorted([ i[0] for i in graph.get(last_node, [])]):
            if link_node not in tmp_path:
                new_path = []
                new_path = tmp_path + [link_node]
                q.append(new_path)

    return []

def shortest_path(graph, start_node, end_node):
    """
    Executa um tra entre start_node e end_node.
    @Return: lista com o caminho menor caminho possivel entre os vertices, nesta
    lista start_node e end_node estao inclusos.
    http://code.activestate.com/recipes/119466-dtras-algorithm-for-shortest-paths/
    """
    import heapq

    queue = [(0, start_node, [])]
    seen = set()

    while True:
        (cost, v, path) = heapq.heappop(queue)

        if v not in seen:
            path = path + [v]
            seen.add(v)
            if v == end_node:
                #return cost, path
                return path
            for next, c in graph.get(v, []):
                heapq.heappush(queue, (cost + c, next, path))

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
