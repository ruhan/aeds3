# -*- coding: utf8 -*-
import os;
import subprocess;
import numpy;
import sys;

def merge_and_count(A, B):
	num_inversoes = 0;
	output = [];
	while len(A) > 0 and len(B) > 0:
		if len(B) == 0:
			output.append(A.pop(0))
		elif len(A) > 0 and A[0] < B[0]:
			output.append(A.pop(0));
		else:
			num_inversoes += len(A);
			output.append(B.pop(0));
	return (num_inversoes, output);

#Algoritmo utilizado para contar inversões (retirado do livro "Algorithm Design", por Jon Kleinberg e Éva Tardos, páginas 224-225)
def sort_and_count(L):
	if len(L) <= 1:
		return (0, L);
	else:
		A = L[:len(L)/2]
		B = L[len(L)/2:]
		(r_A, A) = sort_and_count(A);
		(r_B, B) = sort_and_count(B);
		(r, L) = merge_and_count(A, B);
	return (r_A + r_B + r, L);

def main():
	dir_gabarito = "exemplos/";

	instancias_teste = [("small", 1), ("medium", 1), ("big", 6)];
	#TODO: definir esses tamanhos de memória em função do tamanho das entradas (isso pode ser calculado offline)
	tamanhos_memoria = [1.5*1024*1024, 1.5*1024*1024, 1.5*1024*1024]

	pesos_instancias = [];
	resultados_instancias = [];
	for (nome_instancia, num_entradas), tam_memoria in zip(instancias_teste, tamanhos_memoria):
		nome_gabarito = dir_gabarito + nome_instancia + ".sol";
		nome_saida_teste = nome_instancia + ".out";

		if num_entradas > 1:
			nomes_entrada = [dir_gabarito + nome_instancia + str(i) + ".in" for i in range(1, num_entradas)];
		else:
			nomes_entrada = [dir_gabarito + nome_instancia + ".in"];



		print "Testando instância %s" % (nome_instancia);

		args_subp = ['/usr/bin/time', '-f\"%M %S %U\"', './tp3', "-o", nome_saida_teste, "-m", str(tam_memoria)] + [str(i) for i in nomes_entrada];

		try:
			output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
		except Exception, e:
			output = e.output

		output = output.strip(" \n\r\t\"").split("\n");
		
		memoria_tempos = output[-1].strip(" \n\r\t\"").split(" ");
		memoria_max = int(memoria_tempos[0])/1024.
		tempo_exec = float(memoria_tempos[1])+float(memoria_tempos[2])
		
		print "Gasto máximo de memória: %.2f MB (restrição de memória: %.2f MB)" % (memoria_max, tam_memoria/1024/1024);
		print "Tempo de execução: %.2f s" % tempo_exec;
		
		dict_gabarito = {};
		with open(nome_gabarito, 'r') as arq_gabarito:
			for linha_gab in arq_gabarito:
				linha_gab_split = linha_gab.split(" ");
				
				palavra_gabarito = linha_gab_split[0];
				alunos_gabarito = [int(i) for i in linha_gab_split[1:]];
				
				dict_gabarito[palavra_gabarito] = alunos_gabarito;
		
		dict_teste = {};
		lista_teste = [];
		with open(nome_saida_teste) as arq_teste:
			for linha_teste in arq_teste:
				linha_teste_split = linha_teste.split(" ");
				
				palavra_teste = linha_teste_split[0];
				alunos_teste = [int(i) for i in linha_teste_split[1:]];
				
				dict_teste[palavra_teste] = alunos_teste;
				lista_teste.append(palavra_teste);

		
		#Quais palavras estão presentes, ou não, no teste e no gabarito
		acertos_presenca_palavras = 0.;
		set_palavras_gabarito = set(dict_gabarito.keys());
		set_palavras_teste = set(dict_teste.keys());
		intersecao_teste_gabarito = set_palavras_gabarito.intersection(set_palavras_teste)
		tam_intersecao = len(intersecao_teste_gabarito);
		tam_xor = len(set_palavras_gabarito ^ set_palavras_teste);
		#Marca um ponto para cada palavra em ambos arquivos e subtrai um ponto para cada palavra em apenas um dos arquivos, normalizando pelo número de palavras no gabarito
		acertos_presenca_palavras = (tam_intersecao - tam_xor) / float(len(set_palavras_gabarito));
		
		#O número de inversões na ordem das palavras
		acertos_ordem_palavras = 0.
		num_palavras_teste = len(lista_teste)
		max_inversoes = num_palavras_teste*(num_palavras_teste-1)/2
		num_inversoes, _ = sort_and_count(lista_teste);
		acertos_ordem_palavras = (max_inversoes - num_inversoes)/float(max_inversoes);
		
		#Analisa as listas de alunos presentes em ambos arquivos, sem analisar a ordem desses alunos nessas listas
		acertos_presenca_alunos = 0.;
		for palavra in intersecao_teste_gabarito:
			set_alunos_gabarito = set(dict_gabarito[palavra]);
			set_alunos_teste = set(dict_teste[palavra]);
			tam_intersecao = len(set_alunos_gabarito.intersection(set_alunos_teste));
			tam_xor = len(set_alunos_gabarito ^ set_alunos_teste);
			#Marca um ponto para cada aluno em ambos arquivos e subtrai um ponto para cada aluno em apenas um dos arquivos, normalizando pelo número de alunos no gabarito
			acertos_presenca_alunos += (tam_intersecao - tam_xor) / float(len(set_alunos_gabarito));
		#Normaliza os acertos pelo número de listas comparadas (para que a nota tenha valor máximo 1)
		acertos_presenca_alunos /= float(len(intersecao_teste_gabarito));
		
		#O número de inversões nas listas de alunos
		acertos_ordem_alunos = 0.;
		for lista_alunos in dict_teste.itervalues():
			num_alunos_lista = len(lista_alunos);
			if num_alunos_lista <= 1:
				acertos_ordem_alunos += 1;
			else:
				max_inversoes = num_alunos_lista*(num_alunos_lista-1)/2;
				num_inversoes, _ = sort_and_count(lista_alunos);
				acertos_ordem_alunos += (max_inversoes - num_inversoes)/float(max_inversoes);
		#Normaliza os acertos pelo número de listas analisadas (para que a nota tenha valor máximo 1)
		acertos_ordem_alunos /= float(len(dict_teste));

		if memoria_max > tam_memoria:
			print "\nMemória utilizada ultrapassa a restrição estipulada inicialmente, os resultados desse arquivo serão zerados"
			acertos_presenca_palavras = 0.;
			acertos_ordem_palavras = 0.
			acertos_presenca_alunos = 0.;
			acertos_ordem_alunos = 0.;
			continue;
		
		pesos_instancias.append(len(dict_gabarito));
		
		#Faz uma média harmônica dos acertos em cada quesito
		a = acertos_presenca_palavras;
		b = acertos_ordem_palavras;
		c = acertos_presenca_alunos;
		d = acertos_ordem_alunos;
		acertos = 4./(1./a+1./b+1./c+1./d);
		#acertos = 8*a*b*c*d / (2*a*b*(c+d) + 2*c*d*(a+b));
		
		porcentagem_acertos = acertos * 100.;
		resultados_instancias.append(porcentagem_acertos);
		
		print "Presença das palavras (porcentagem): %.2f" % (acertos_presenca_palavras*100);
		print "Ordem das palavras (porcentagem): %.2f" % (acertos_ordem_palavras*100);
		print "Presença dos alunos (porcentagem): %.2f" % (acertos_presenca_alunos*100);
		print "Ordem dos alunos (porcentagem): %.2f" % (acertos_ordem_alunos*100);
		print "Porcentagem de acertos: %.2f" % porcentagem_acertos;
		print "\n"

	print "Média ponderada dos acertos: %.2f (porcentagem)" % numpy.average(resultados_instancias, weights=pesos_instancias);



if __name__ == '__main__':
    import sys;
    main();
