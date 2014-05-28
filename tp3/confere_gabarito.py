# -*- coding: utf8 -*-
import os;
import subprocess;
import numpy;
import sys;

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
		
		memoria_tempos = output[-1].split(" ");
		memoria_max = int(memoria_tempos[0])/1024.
		tempo_exec = float(memoria_tempos[1])+float(memoria_tempos[2])
		
		print "Gasto máximo de memória: %.2f MB (restrição de memória: %.2f MB)" % (memoria_max, tam_memoria/1024/1024);
		print "Tempo de execução: %.2f s" % tempo_exec;

		num_linhas = 0;
		acertos = 0.;
		with open(nome_gabarito, 'r') as arq_gabarito:
			with open(nome_saida_teste) as arq_teste:
				for linha_gab, linha_teste in zip(arq_gabarito, arq_teste):
					num_linhas += 1;

					linha_gab_split = linha_gab.split(" ");
					linha_teste_split = linha_teste.split(" ");

					palavra_gabarito = linha_gab_split[0];
					palavra_teste = linha_teste_split[0];
					alunos_gabarito = [int(i) for i in linha_gab_split[1:]];
					alunos_teste = [int(i) for i in linha_gab_split[1:]];

					if palavra_gabarito == palavra_teste:
						set_alunos_gabarito = set(alunos_gabarito);
						set_alunos_teste = set(alunos_teste);
						tam_intersecao = len(set_alunos_teste.intersection(set_alunos_gabarito));
						tam_diferenca = len(set_alunos_teste.difference(set_alunos_gabarito));
						#Marca um ponto para cada aluno atribuído corretamente e subtrai um ponto para cada aluno que não deveria estar nessa lista, normalizando esses pontos pelo número de alunos da solução (essa nota vale metade do acerto para essa palavra)
						acertos += (tam_intersecao - tam_diferenca)/len(set_alunos_gabarito)/2.;

						#Um ponto para cada aluno na posição correta, normalizado pelo número de alunos na solução (essa nota vale metade do acerto para essa palavra)
						acertos += sum(map(lambda (x,y):x==y, zip(alunos_gabarito, alunos_teste)))/len(alunos_gabarito)/2.;
				
				def zera_teste(num_linhas_gabarito):
					pesos_instancias.append(num_linhas_gabarito);
					resultados_instancias.append(0);
				
				try:
					arq_gabarito.next();
					#Se ainda há linhas no arquivo de gabarito, havia menos linhas no arquivo de testes
					print "\nArquivo de gabarito com mais linhas que arquivo de testes, os resultados desse arquivo serão zerados\n"
					num_linhas += 1;
					for linha_gab in arq_gabarito:
						num_linhas += 1;
					zera_teste(num_linhas);
					continue;
				except StopIteration:
					#Se não há mais linhas no arquivo de gabarito, nada a fazer
					pass;

				try:
					arq_teste.next();
					print "\nArquivo de testes com mais linhas que arquivo de gabarito, os resultados desse arquivo serão zerados\n"
					zera_teste(num_linhas);
					continue;
				except StopIteration:
					pass;

		if memoria_max > tam_memoria:
			print "\nMemória utilizada ultrapassa a restrição estipulada inicialmente, os resultados desse arquivo serão zerados"
			zera_teste(num_linhas);
			continue;
		
		pesos_instancias.append(num_linhas);

		porcentagem_acertos = acertos / float(num_linhas) * 100.;
		resultados_instancias.append(porcentagem_acertos);

		print "Porcentagem de acertos: %d" % porcentagem_acertos;
		print "\n"

	print "Média ponderada dos acertos: %.2f (porcentagem)" % numpy.average(resultados_instancias, weights=pesos_instancias);



if __name__ == '__main__':
    import sys;
    main();
