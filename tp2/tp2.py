# -*- coding: utf8 -*-
import networkx

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

def parse_input(input_data):
    """
    Dado uma entrada (list [for testability]) retorna a saida separando os
    grafos.
    """
    instances = []
    n_instances = int(input_data[0])
    input_data = input_data[1:]

    for instance in range(n_instances):
        end_instance = int(input_data[0].split(' ')[1])+1
        instances.append(input_data[1:end_instance])
        input_data = input_data[end_instance:]

    return instances

def create_graph(nodes_list):
    """
    Recebe uma lista de nos (string) e gera um grafo no formato matriz
    de adjacencias. Note que a lista de nos significa que os nos passados
    serao todos ligados entre si.

    @Return: Um exemplo de grafo gerado seria:
        Entrada:
            1 2 3
            1 4
        Saida:
            graph = {1:[2, 3, 4], 2:[1, 3], 3: [1, 2], 4: [1]}
    """
    from itertools import combinations

    graph = networkx.Graph()

    for nodes in nodes_list:
        edges = combinations(nodes.split(' '), 2)

        graph.add_edges_from(edges)

    return graph

def mis(graph):
    """
    Dado um grafo calcula seu conjunto independente maximo, retornando os
    elementos esperados.

    A ideia aqui eh procurar o clique maximo no grafo complementar ao grafo
    informado.

    XXX NOTE: nao estamos preocupados com performance aqui ;)
    """
    cgraph = networkx.complement(graph)
    cliques = [ len(c) for c in networkx.find_cliques(cgraph) ]

    if len(cliques) == 0:
        resp = 1
    if len(cliques) > 0:
         resp = max(cliques)
    return resp

def main(finput, foutput):
    """
    Executa o programa como um todo a partir de dois arquivos: um de entrada e
    outro de saida.
    """
    out = open(foutput, 'w')
    output = []

    for instance in parse_input([ i.strip() for i in open(finput)]):
        graph = create_graph(instance)
        s = mis(graph)
        output.append(str(s))

    out.write("\n".join(output))
    out.write("\n")

    out.close()

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
