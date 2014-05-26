# -*- coding: utf8 -*-
def create_index(path):
    """
    Cria os iindices utilizando um simples dicionario python
    """
    words = {}

    for l in open(path):
        linewords = l.strip().split(" ")
        student = linewords[0]
        linewords = linewords[1:]

        for word in linewords:
            if word in words:
                if not student in words[word]:
                    words[word].append(student)
            else:
                words[word] = [student]

    return words

def write_file(path, data):
    """
    Escreve o arquivo no formato esperado pelo TP
    """
    result = []

    for word in sorted(data.keys()):
        result.append('%s %s\n' % (word, " ".join(sorted(data[word]))))

    output = open(path, 'w')
    output.write("".join(result))
    output.close()

def main(finput, foutput):
    index = create_index(finput)
    write_file(foutput, index)

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
