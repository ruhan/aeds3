"""
Para testar os resultados mais facilmente: http://odur.let.rug.nl/kleiweg/lev/
"""
import sys

def edit_distance(s,t, ins_cost=1.0, del_cost=1.0, sub_cost=1.5, swap_cost=2.0):
    """
    Calcula a distancia de edicao entre duas strings, possibilitando a
    modificacao dos pesos das operacoes.

    O algoritmo eh uma modificacao de duas ideias separadas:
    http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
    http://stackoverflow.com/questions/10178043/levenshtein-edit-distance-algorithm-that-supports-transposition-of-two-adjacent
    """
    """
    ins_cost = del_cost = 2
    sub_cost = 4
    swap_cost = 3
    """
    s = ' ' + s
    t = ' ' + t
    d = {}
    S = len(s)
    T = len(t)

    for i in range(S):
        d[i, 0] = i*ins_cost

    for j in range (T):
        d[0, j] = j*ins_cost

    for j in range(1,T):
        for i in range(1,S):
            if s[i] == t[j]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = min(d[i-1, j] + del_cost, d[i, j-1] + ins_cost, d[i-1, j-1] + sub_cost)

            # Swap
            if (s[i] == t[j-1]) and (s[i-1] == t[j]):
                d[i, j] = min(d[i, j], d[i-2, j-2] + swap_cost)

    #print_matrix(d, s, t)
    return d[S-1, T-1]

def print_matrix(m, s, t):
    """
    Apenas imprime a matriz de programacao dinamica em um formato razoavel.
    """
    for i in range(len(s)):
        for j in range(len(t)):
            sys.stdout.write('{0: ^5}'.format(str(m[i, j])))
        print '\n'

def main(dictionary, answers, output):
    words = [ word.strip() for word in open(dictionary) ]
    foutput = open(output, 'w')

    for answer in open(answers):
        answer_words = answer.strip().split(" ")

        line_output = []

        # Cada aluno
        for answer_word in answer_words:
            similarities = []
            for word in words:
                similarities.append((word, edit_distance(answer_word, word)))

            # Apanhando a palavra que mais se parece com a informada pelo aluno
            min_similaritie = min(similarities, key=lambda x: x[1])
            line_output.append(min_similaritie)

        # Imprimindo o resultado do aluno
        result = []
        total = sum([ sim[1] for sim in line_output ])

        for sim in line_output:
            # Soma com espaco necessaria para a formatacao
            result.append("%s,%s" % sim)

        foutput.write("%s:%s\n" % (total, " ".join(result)))

    foutput.close()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
