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
	acertos_instancias = [];
	max_speedup_interna = 0;
	max_speedup_palavras = 0;
	for nome_instancia in instancias_teste:
		nome_gabarito = dir_gabarito + nome_instancia + ".sol";
		nome_dicionario = dir_gabarito + nome_instancia + ".dic";
		nome_entrada = dir_gabarito + nome_instancia + ".in";
		nome_saida_teste = nome_instancia + ".out";
		
		tempo_sequencial = None;
		
		print "\n===Testando instância %s===" % (nome_instancia);
		
		for num_algoritmo in range(1, 4):
			
			algoritmo = ["Sequencial", "paralelização de palavras", "paralelização interna"][num_algoritmo-1];
			print "Algoritmo %s" % (algoritmo);

			args_subp = ['/usr/bin/time', '-f\"%M %S %U\"', './tp4', "-a", str(num_algoritmo), "-t", str(NUM_THREADS), "-r", nome_entrada, "-d", nome_dicionario, "-o", nome_saida_teste];

			try:
				output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
			except Exception, e:
				output = e.output

			output = output.strip(" \n\r\t\"").split("\n");
		
			memoria_tempos = output[-1].strip(" \n\r\t\"").split(" ");
			memoria_max = int(memoria_tempos[0])/1024.
			tempo_exec = float(memoria_tempos[1])+float(memoria_tempos[2]);
			
			print "Gasto máximo de memória: %.2f MB" % (memoria_max);
			print "Tempo de execução: %.2f s" % tempo_exec;
			
			acertos = []
			with open(nome_gabarito) as arq_gabarito:
				with open(nome_saida_teste) as arq_teste:
					for linha_gab, linha_teste in zip(arq_gabarito, arq_teste):
						dist_total_split_gab = linha_gab.split(":");
						dist_total_gab = float(dist_total_split_gab[0]);
						palavras_dist_gab = dist_total_split_gab[1];
						dist_total_split_teste = linha_teste.split(":");
						dist_total_teste = float(dist_total_split_teste[0]);
						palavras_dist_teste = dist_total_split_teste[1];
						
						if dist_total_gab == dist_total_teste:
							def le_par_gab(par):
								par = par.split(",");
								parte_palavra = par[0];
								distancia = float(par[1]);
								set_palavras = set();
								if parte_palavra.startswith("{") and parte_palavra.endswith("}"):
									parte_palavra = parte_palavra.strip("{}");
									set_palavras = set(parte_palavra.split("/"));
								else:
									set_palavras.add(parte_palavra);
								return (set_palavras, distancia);
							
							def le_par_teste(par):
								par = par.split(",");
								return (par[0], float(par[1]));
						
							pares_gab = palavras_dist_gab.split(" ");
							pares_gab = map(le_par_gab, pares_gab)
							
							pares_teste = palavras_dist_gab.split(" ");
							pares_teste = map(le_par_teste, pares_teste);
							
							num_acertos = map(lambda ((a,b),(x,y)):x in a and b==y, zip(pares_gab, pares_teste));
							acertos.append(reduce(lambda x,y:x and y, num_acertos));
							
						else:
							acertos.append(False);
					

					try:
						arq_teste.next();
						print "ERRO: Arquivo de teste com mais linhas que gabarito"
						acertos = [False];
					except StopIteration:
						try:
							arq_gabarito.next();
							print "ERRO: Arquivo de teste com menos linhas que gabarito"
							acertos=[False];
						except StopIteration:
							pass;
			
				acertou_todas = reduce(lambda x,y:x and y, acertos);
				porc_acertos = sum(acertos)/float(len(acertos))*100.;
				acertos_instancias.append(porc_acertos);
				print "Porcentagem de acertos: %.2f" % (porc_acertos)
			
				if acertou_todas:
					if num_algoritmo == 1:
						tempo_sequencial = tempo_exec;
					elif num_algoritmo == 2 and tempo_sequencial != None:
						speedup = tempo_sequencial/tempo_exec;
						print "SPEEDUP: %.2f" % (speedup);
						max_speedup_palavras = max(max_speedup_palavras, speedup);
					elif num_algoritmo == 3 and tempo_sequencial != None:
						speedup = tempo_sequencial/tempo_exec;
						print "SPEEDUP: %.2f" % (speedup);
						max_speedup_interna = max(max_speedup_interna, speedup);

				print "\n";
		
		
		
	

	print "Média ponderada dos acertos: %.2f (porcentagem)" % numpy.average(acertos_instancias, weights=pesos_instancias);
	print "Speedup máximo da paralelização de palavras:", max_speedup_palavras;
	print "Speedup máximo da paralelização interna:", max_speedup_interna;



if __name__ == '__main__':
    import sys;
    verbose = False;
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
    	verbose = True;
    main(verbose);
