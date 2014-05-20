# -*- coding: utf8 -*-
import os;
import subprocess;
import numpy;

def main():
    dir_gabarito = "exemplos/";

    pesos_instancias = [];
    resultados_instancias = [];

    #Confere acertos do alg. exato
  
    nome_gabarito = dir_gabarito + "exato.sol";
    nome_entrada = dir_gabarito + n"exato.in";
    nome_saida_teste = "exato.out";


    linhas_gabarito = [];
    with open(nome_gabarito, 'r') as arq_gabarito:
       for linha in arq_gabarito:
            if linha != '\n':
                linhas_gabarito.append(linha.strip());

    num_linhas_gabarito = len(linhas_gabarito);
    #Para permitir o uso de pop nessa lista na ordem de leitura do arquivo
    linhas_gabarito.reverse()

    print "Testando algoritmo exato (%d consultas)" % (num_linhas_gabarito);

    pesos_instancias.append(num_linhas_gabarito);

    args_subp = ['/usr/bin/time', '-v', './tp2', nome_entrada, nome_saida_teste];

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
                
            if len(linhas_gabarito) <= 0:
            	print "Número de consultas no arquivo de teste maior que o número de consultas no gabarito!";
            	break;

            if linha.strip() == linhas_gabarito.pop():
                num_acertos += 1;

            num_linhas_teste += 1;

    if num_linhas_teste != num_linhas_gabarito:
        print "Número de consultas do arquivo de teste diferente do gabarito! (%d/%d)" % (num_linhas_teste, num_linhas_gabarito);

    porcentagem_acertos = num_acertos / float(num_linhas_gabarito) * 100;
    resultados_instancias.append(porcentagem_acertos);

    if
    print "Porcentagem de acerto nos testes: %d" % porcentagem_acertos;
    print "Gasto máximo de memória: %.2f MB" % memoria_max;
    print "Tempo de execução: %.2f s" % tempo_exec;
    print "\n"






    #Confere se a heuristica executa corretamente em um tempo aceitavel
    nome_entrada = dir_gabarito + "heuristica.in";
    nome_saida_teste = "heuristica.out";

    nota = 10;

    num_linhas_gabarito = 100;
    #Para permitir o uso de pop nessa lista na ordem de leitura do arquivo
   

    print "Testando heuristica (100 consultas)";

    pesos_instancias.append(num_linhas_gabarito);

    args_subp = ['/usr/bin/time', '-v', './tp1', nome_entrada, nome_saida_teste];

    try:
        output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
    except Exception, e:
        output = e.output

    output = output.split("\n");

    memoria_max = int(output[-15].split(" ")[-1])/1024.
    tempo_exec = float(output[-22].split(" ")[-1])+float(output[-23].split(" ")[-1])

    linhas_saida = [];
    num_acertos = 0;
    num_linhas_teste = 0;
    with open(nome_saida_teste, 'r') as arq_teste:
        for linha in arq_teste:
           if linha == "\n":
               linhas_saida.append(linha.strip());
    num_linhas_saida = len(linhas_saida);
                
    if num_linhas_saida != num_linhas_gabarito:
            	print "Número de consultas no arquivo de teste maior que o número de consultas no gabarito!";
               	break;
		nota = nota/2; #perde metade dos pontos da heuristica

    if
    print "Nota na execução da heurística (0 a 10): %d" % nota;
    print "Gasto máximo de memória: %.2f MB" % memoria_max;
    print "Tempo de execução: %.2f s" % tempo_exec;
    print "\n"



if __name__ == '__main__':
    import sys;
    main();
