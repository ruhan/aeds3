# -*- coding: utf8 -*-
def _split_edge(edge):
    """
    Apenas transforma uma string de aresta em dois nos inteiros
    """
    u, v = edge.split(' ')
    return int(u), int(v)

def main(finput, foutput):
    """
    Executa o programa como um todo a partir de dois arquivos: um de entrada e
    outro de saida.
    """
    output = []
    instances = parse_input([ i.strip() for i in open(finput)]);
    
    for edges, tests in instances:

		graph = create_graph(edges)

		for test in tests:
		    u, v = _split_edge(test)
		    output.append(" ".join(map(lambda x: str(x), dfs(graph, u, v))))

    out = open(foutput, 'w')
    out.write("\n\n".join(output))
    out.close()

def parse_input(input_data):
    """
    Dado uma entrada (list [for testability]) retorna a saida conforme
    solicitado pelo enunciado.
    """
    instances = []
    
    n_instances = int(input_data[0].strip());
    input_data = input_data[1:];
    
    for _ in xrange(n_instances):
		edges = []
		tests = []

		n_edges = int(input_data[0].split(' ')[1])
		input_data = input_data[1:];

		for edge in input_data[:n_edges]:
			edges.append(edge)
		input_data = input_data[n_edges:]

		n_tests = int(input_data[0].strip())
		input_data = input_data[1:];

		for test in input_data[:n_tests]:
			tests.append(test)
		input_data = input_data[n_tests:];
		
		instances.append((edges, tests));

    return instances;

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
            graph = {'A':['B','C'],'B':['D','E'],'C':['D','E']}
    """
    graph = {}

    for e in edges:
        u, v = _split_edge(e)

        if u in graph:
            graph[u].append(v)
        else:
            graph[u] = [v]

        # Garante o grafo nao direcionado
        if v in graph:
            graph[v].append(u)
        else:
            graph[v] = [u]

    return graph

def dfs(graph, start_node, end_node, path=[]):
    """
    Faz uma busca em profundidade entre start_node e end_node.
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
            q = sorted(graph[v]) + q

        if v == end_node:
            return path

    return path


if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])


