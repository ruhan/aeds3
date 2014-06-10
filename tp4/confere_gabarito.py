# -*- coding: utf8 -*-
import os;
import subprocess;
import numpy;
import sys;

def main(verbose=False):
	dir_gabarito = "exemplos/";

	instancias_teste = ["small", "medium", "bigword"];
	NUM_THREADS = 4;

	pesos_instancias = [];
	resultados_instancias = [];
	for nome_instancia in instancias_teste:
		nome_gabarito = dir_gabarito + nome_instancia + ".sol";
		nome_dicionario = dir_gabarito + nome_instancia + ".dic";
		nome_entrada = dir_gabarito + nome_instancia + ".in";
		nome_saida_teste = nome_instancia + ".out";
		
		for num_algoritmo in range(1, 4):

			print "Testando instância %s (algoritmo %d)" % (nome_instancia, num_algoritmo);

			args_subp = ['/usr/bin/time', '-f\"%M %S %U\"', './tp4', "-a", str(num_algoritmo), "-t", str(NUM_THREADS), "-r", nome_entrada, "-d", nome_dicionario, "-o", nome_saida_teste];

			try:
				output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
			except Exception, e:
				output = e.output

			output = output.strip(" \n\r\t\"").split("\n");
		
			memoria_tempos = output[-1].strip(" \n\r\t\"").split(" ");
			memoria_max = int(memoria_tempos[0])/1024.
			tempo_exec = float(memoria_tempos[1])+float(memoria_tempos[2])
		
		#TODO:Continuar daqui.
		
		print "Gasto máximo de memória: %.2f MB (restrição de memória: %.2f MB)" % (memoria_max, tam_memoria/1024/1024);
		print "Tempo de execução: %.2f s" % tempo_exec;
		
		#a primeira instância (menor) fornece informações do mínimo de memória necessário para carregar o programa. A restrição de memória das entradas subsequentes utilizará essa informação
		if num_palavras_prim_instancia == None:
			num_palavras_prim_instancia = len(dict_gabarito);
			min_memoria = min(tam_memoria, memoria_max*1024*1024);
		
		
		dict_teste = {};
		lista_teste = [];
		with open(nome_saida_teste) as arq_teste:
			for linha_teste in arq_teste:
				linha_teste_split = linha_teste.strip(" \n\r\t\"").split(" ");
				
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
		#Marca um ponto para cada palavra em ambos arquivos e subtrai um ponto para cada palavra em apenas um dos arquivos, normalizando pelo número de palavras no gabarito. Esse valor inicialmente pode ser negativo, por isso o max.
		acertos_presenca_palavras = max(0, (tam_intersecao - tam_xor) / float(len(set_palavras_gabarito)));
		if verbose and acertos_presenca_palavras < 1.:
				print "Palavras faltantes no teste:", list(set_palavras_gabarito.difference(set_palavras_teste));
				print "palavras presentes apenas no teste:", list(set_palavras_teste.difference(set_palavras_gabarito))
		
		#O número de inversões na ordem das palavras
		acertos_ordem_palavras = 0.
		num_palavras_teste = len(lista_teste)
		max_inversoes = num_palavras_teste*(num_palavras_teste-1)/2
		inversoes = [];
		num_inversoes, _ = sort_and_count(lista_teste, verbose, inversoes);
		if num_palavras_teste > 1:
			acertos_ordem_palavras = (max_inversoes - num_inversoes)/float(max_inversoes);
		else:
			acertos_ordem_palavras = 0;
		if verbose:
			print "Inversões das palavras:", inversoes;
		
		#Analisa as listas de alunos presentes em ambos arquivos, sem analisar a ordem desses alunos nessas listas
		acertos_presenca_alunos = 0.;
		palavras_erros = [];
		for palavra in intersecao_teste_gabarito:
			set_alunos_gabarito = set(dict_gabarito[palavra]);
			set_alunos_teste = set(dict_teste[palavra]);
			tam_intersecao = len(set_alunos_gabarito.intersection(set_alunos_teste));
			tam_xor = len(set_alunos_gabarito ^ set_alunos_teste);
			#Marca um ponto para cada aluno em ambos arquivos e subtrai um ponto para cada aluno em apenas um dos arquivos, normalizando pelo número de alunos no gabarito. Esse valor inicialmente pode ser negativo, por isso o max.
			atual_acertos_presenca_alunos = max(0, (tam_intersecao - tam_xor) / float(len(set_alunos_gabarito)));
			if verbose and atual_acertos_presenca_alunos < 1.:
				palavras_erros.append(palavra);
			acertos_presenca_alunos += atual_acertos_presenca_alunos;
		#Normaliza os acertos pelo número de listas comparadas (para que a nota tenha valor máximo 1)
		if len(intersecao_teste_gabarito) > 0:
			acertos_presenca_alunos /= float(len(intersecao_teste_gabarito));
		else:
			acertos_presenca_alunos = 0;
		if verbose and acertos_presenca_alunos < 1.:
			print "Palavras com alunos em excesso ou ausência:", palavras_erros;
		
		#O número de inversões nas listas de alunos
		acertos_ordem_alunos = 0.;
		palavras_erros = [];
		for palavra, lista_alunos in dict_teste.iteritems():
			num_alunos_lista = len(lista_alunos);
			if num_alunos_lista <= 1:
				acertos_ordem_alunos += 1.;
			else:
				max_inversoes = num_alunos_lista*(num_alunos_lista-1)/2;
				num_inversoes, _ = sort_and_count(lista_alunos);
				acertos_aux = (max_inversoes - num_inversoes)/float(max_inversoes);
				if verbose and acertos_aux < 1.:
					palavras_erros.append(palavra);
				acertos_ordem_alunos += acertos_aux;
		#Normaliza os acertos pelo número de listas analisadas (para que a nota tenha valor máximo 1)
		if len(dict_teste) > 0:
			acertos_ordem_alunos /= float(len(dict_teste));
		else:
			acertos_ordem_alunos = 0;
		if verbose and acertos_ordem_alunos < 1.:
			print "Palavras com inversões na lista de alunos:", palavras_erros;
		pesos_instancias.append(len(dict_gabarito));
		
		#Faz uma média harmônica dos acertos em cada quesito
		a = acertos_presenca_palavras;
		b = acertos_ordem_palavras;
		c = acertos_presenca_alunos;
		d = acertos_ordem_alunos;
		if a>0 and b>0 and c>0 and d>0:
			acertos = 4./(1./a+1./b+1./c+1./d);	
		else:
			acertos = 0;
		#acertos = 8*a*b*c*d / (2*a*b*(c+d) + 2*c*d*(a+b));
		
		porcentagem_acertos = acertos * 100.;
		
		if memoria_max*1024*1024 > tam_memoria:
			print "(Memória utilizada ultrapassa a restrição estipulada inicialmente, o acerto final desse arquivo será penalizado em 50%)"
			porcentagem_acertos *= 0.5;
		
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
    verbose = False;
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
    	verbose = True;
    main(verbose);
