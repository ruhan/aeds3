# -*- coding: utf8 -*-
import os;
import subprocess;
import numpy;

def main():
    dir_gabarito = "exemplos/";

    instancias_teste = ["small", "big"];

    pesos_instancias = [];
    resultados_instancias = [];
    for nome_instancia in instancias_teste:
        nome_gabarito = dir_gabarito + nome_instancia + ".sol";
        nome_entrada = dir_gabarito + nome_instancia + ".in";
        nome_saida_teste = nome_instancia + ".out";


        linhas_gabarito = [];
        with open(nome_gabarito, 'r') as arq_gabarito:
            for linha in arq_gabarito:
                if linha != '\n':
                    linhas_gabarito.append(linha.strip());

        num_linhas_gabarito = len(linhas_gabarito);
        #Para permitir o uso de pop nessa lista na ordem de leitura do arquivo
        linhas_gabarito.reverse()

        print "Testando instância %s (%d consultas)" % (nome_instancia, num_linhas_gabarito);

        pesos_instancias.append(num_linhas_gabarito);

        args_subp = ['/usr/bin/time', '-v', './tp1', nome_entrada, nome_saida_teste];

        try:
            output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
        except Exception, e:
            output = e.output

        output = output.split("\n");

        memoria_max = int(output[-15].split(" ")[-1])/1024.
        tempo_exec = float(output[-22].split(" ")[-1])+float(output[-23].split(" ")[-1])


        num_acertos = 0;
        num_linhas_teste = 0;
        with open(nome_saida_teste, 'r') as arq_teste:
            for linha in arq_teste:
                if linha == "\n":
                    continue;

                if linha.strip() == linhas_gabarito.pop():
                    num_acertos += 1;

                num_linhas_teste += 1;

        if num_linhas_teste != num_linhas_gabarito:
            print "Número de consultas diferente do gabarito (%d/%d)" % (num_linhas_teste, num_linhas_gabarito);

        porcentagem_acertos = num_acertos / float(num_linhas_gabarito) * 100;
        resultados_instancias.append(porcentagem_acertos);

        print "Porcentagem de acertos: %d" % porcentagem_acertos;
        print "Gasto máximo de memória: %.2f MB" % memoria_max;
        print "Tempo de execução: %.2f s" % tempo_exec;
        print "\n"

    print "Média ponderada dos acertos: %.2f (porcentagem)" % numpy.average(resultados_instancias, weights=pesos_instancias);



if __name__ == '__main__':
    import sys;
    main();
