# -*- coding: utf8 -*-
import os;
import subprocess;
import numpy as np;
import sys;
from math import sqrt;

def main():
	dir_gabarito = "exemplos/";

	instancias_teste_exato = ["exato"];
	instancias_teste_heuristica = ["heuristica", "heuristica_200", "heuristica_400"]

	pesos_instancias_exato = [];
	pesos_instancias_heuristica = [];
	instancias_exato = [];
	instancias_heuristica = [];
	resultados_exato = [];
	resultados_heuristica = [];
	resultados_gabarito_exato = [];
	resultados_gabarito_heuristica = [];

	for nome_instancia in instancias_teste_exato:

		#Confere acertos do alg. exato
	  	
	  	#nomes dos arquivos utilizados
		nome_gabarito = dir_gabarito + nome_instancia + ".sol";
		nome_entrada = dir_gabarito + nome_instancia + ".in";
		nome_saida_exato = nome_instancia + "_exato.out";


		aux_gabarito = [];
		with open(nome_gabarito, 'r') as arq_gabarito:
		   for linha in arq_gabarito:
			    if linha != '\n':
			        aux_gabarito.append(int(linha.strip()));

		num_linhas_gabarito = len(aux_gabarito);
		resultados_gabarito_exato.extend(aux_gabarito);
	
		pesos_instancias_exato.append(num_linhas_gabarito);

		print "Testando instância", nome_instancia;
		print "Testando algoritmo exato (%d consultas)" % (num_linhas_gabarito);


		args_subp = ['/usr/bin/time', '-v', './tp2e', nome_entrada, nome_saida_exato];

		try:
			output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
		except Exception, e:
			output = e.output

		output = output.split("\n");

		memoria_max = int(output[-15].split(" ")[-1])/1024.
		tempo_exec = float(output[-22].split(" ")[-1])+float(output[-23].split(" ")[-1])


		aux_resultados_exato = []
		with open(nome_saida_exato, 'r') as arq_teste:
			for linha_teste in arq_teste:
			    if linha_teste == "\n":
			        continue;

			    aux_resultados_exato.append(int(linha_teste.strip()));
	
		if len(aux_resultados_exato) != num_linhas_gabarito:
			print "ERRO: Número de consultas do arquivo de teste diferente do gabarito! (%d/%d)" % (len(aux_resultados_exato), num_linhas_gabarito);
			#Se o arquivo de testes não é capaz de produzir uma saída qualquer, é melhor abortar o script, pois os resultados não farão muito sentido
			sys.exit(1);
		else:
			#simplesmente junta os resultados de cada teste em uma mesma lista
			resultados_exato.extend(aux_resultados_exato);
	
		#Para cada arquivo informa apenas os dados da execução em si
		print "Gasto máximo de memória: %.2f MB" % memoria_max;
		print "Tempo de execução: %.2f s" % tempo_exec;
		print "\n"
	
		instancias_exato.append((memoria_max, tempo_exec));


	def imprime_resultados_exato():
		print "\n===Resultados finais===\n"

		#calcula as estatísticas para o algoritmo exato
		memorias_exato, tempos_exato = zip(*instancias_exato);
		media_memoria_exato = np.mean(memorias_exato);
		media_tempos_exato = np.mean(tempos_exato);
		aux_gab_exat = zip(resultados_gabarito_exato, resultados_exato);
		porcentagem_acertos = sum(map(lambda (x,y):x==y, aux_gab_exat))/float(len(resultados_gabarito_exato))*100;

		print "Algoritmo exato:";
		print "Gasto médio de memória(alocação máxima): %.2f MB" % (media_memoria_exato);
		print "Tempo médio de execução: %.2f" % (media_tempos_exato);
		print "porcentagem de acertos: %.2f" % (porcentagem_acertos);	
	
	resultados_gabarito_heuristica = [];

	for nome_instancia in instancias_teste_heuristica:
	
		#nomes dos arquivos utilizados
		nome_gabarito = dir_gabarito + nome_instancia + ".sol";
		nome_entrada = dir_gabarito + nome_instancia + ".in";
		nome_saida_heuristica = nome_instancia + "_heur.out";
	
		aux_gabarito = [];
		with open(nome_gabarito, 'r') as arq_gabarito:
		   for linha in arq_gabarito:
			    if linha != '\n':
			        aux_gabarito.append(int(linha.strip()));

		num_linhas_gabarito = len(aux_gabarito);
		resultados_gabarito_heuristica.extend(aux_gabarito);
	
		pesos_instancias_heuristica.append(num_linhas_gabarito);

		#Confere a heurística
		print "Testando instância", nome_instancia;
		print "Testando heuristica";

		args_subp = ['/usr/bin/time', '-v', './tp2h', nome_entrada, nome_saida_heuristica];

		try:
			output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
		except Exception, e:
			output = e.output

		output = output.split("\n");

		memoria_max = int(output[-15].split(" ")[-1])/1024.
		tempo_exec = float(output[-22].split(" ")[-1])+float(output[-23].split(" ")[-1])

		aux_resultados_heuristica = [];
		with open(nome_saida_heuristica, 'r') as arq_heur:
			for linha_teste in arq_heur:
				if linha_teste == "\n":
					continue;
				
				aux_resultados_heuristica.append(int(linha_teste.strip()));
	
		#Trata os valores lidos na heurística de forma análoga ao que foi feito para o algoritmo exato mais acima
		if len(aux_resultados_heuristica) != num_linhas_gabarito:
			print "ERRO: Número de consultas do arquivo de teste diferente do gabarito! (%d/%d)" % (len(aux_resultados_heuristica), num_linhas_gabarito);
			print "O teste da heurística será abortado\n";
			imprime_resultados_exato();
			sys.exit(1);
		else:
			resultados_heuristica.extend(aux_resultados_heuristica);


		print "Gasto máximo de memória: %.2f MB" % memoria_max;
		print "Tempo de execução: %.2f s" % tempo_exec;
		print "\n"
	
		instancias_heuristica.append((memoria_max, tempo_exec));
	
	imprime_resultados_exato();

	#Calcula as estatísticas para a heurística
	memorias_heuristica, tempos_heuristica = zip(*instancias_heuristica);
	media_memoria_heuristica = np.mean(memorias_heuristica);
	media_tempos_heuristica = np.mean(tempos_heuristica);

	aux_gab_heur = zip(resultados_gabarito_heuristica, resultados_heuristica);
	#porcentagem das respostas totalmente corretas:
	porcentagem_acertos = sum(map(lambda (x,y):x==y, aux_gab_heur))/float(len(resultados_gabarito_heuristica))*100;
	#erro das respostas da heurística:
	erro = map(lambda (g,h):abs(g-h)/float(g), aux_gab_heur);
	media_erro_porc = np.mean(erro)*100.;
	desvio_erro_porc = np.std(erro)*100.;
	#Pearson:
	media_gabarito = np.mean(resultados_gabarito_heuristica);
	media_heuristica = np.mean(resultados_heuristica);
	gabarito_menos_media = map(lambda x:x-media_gabarito, resultados_gabarito_heuristica);
	heuristica_menos_media = map(lambda x:x-media_heuristica, resultados_heuristica);
	covariancia = sum(map(lambda (x,y):x*y, zip(gabarito_menos_media, heuristica_menos_media)));
	variancia_gabarito = sum(map(lambda x:x**2, gabarito_menos_media));
	variancia_heuristica = sum(map(lambda x:x**2, heuristica_menos_media));
	pearson = covariancia / sqrt(variancia_gabarito*variancia_heuristica);

	print "\nHeurística:";
	print "Gasto médio de memória(alocação máxima): %.2f MB" % (media_memoria_heuristica);
	print "Tempo médio de execução: %.2f" % (media_tempos_heuristica);
	print "Porcentagem de acertos: %.2f" % (porcentagem_acertos);
	print "Erro médio (porcentual): %.2f +- %.2f" % (media_erro_porc,desvio_erro_porc);
	print "Coeficiente de correlação de Pearson: %.2f" % pearson;
	

if __name__ == '__main__':
    import sys;
    main();
