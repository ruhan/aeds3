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
		
		tempo_sequencial = None;
		
		num_linhas_gab = 0;
		maior_linha = 0;
		with open(nome_gabarito) as arq_gabarito:
			for i, l in enumerate(arq_gabarito):
				maior_linha = max(maior_linha, len(l));
			num_linhas_gab = i+1;
		pesos_instancias.append(num_linhas_gab*maior_linha);
		
		print "\n===Testando instância %s===" % (nome_instancia);
		
		acertos_instancias.append([0, 0, 0]);
		for num_algoritmo in range(1, 4):
			
			algoritmo = ["Sequencial", "paralelização de palavras", "paralelização interna"][num_algoritmo-1];
			print "Algoritmo %s" % (algoritmo);
			
			nome_saida_teste = "%s_%s.out" % (nome_instancia, algoritmo);

			args_subp = ['/usr/bin/time', '-f\"%M %S %U\"', './tp4', "-a", str(num_algoritmo), "-t", str(NUM_THREADS), "-r", nome_entrada, "-d", nome_dicionario, "-o", nome_saida_teste];

			try:
				output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT)
			except KeyboardInterrupt:
				print "\nExecução cancelada. O teste dessa instância será zerado\n"
				acertos_instancias[-1][num_algoritmo-1] = 0;
				continue;
			except Exception, e:
				output = e.output
				print "ERRO na execução! O teste dessa instância será zerado\n"
				acertos_instancias[-1][num_algoritmo-1] = 0;
				continue;
			
			output = output.strip(" \n\r\t\"").split("\n");
		
			memoria_tempos = output[-1].strip(" \n\r\t\"").split(" ");
			memoria_max = int(memoria_tempos[0])/1024.
			tempo_exec = float(memoria_tempos[1])+float(memoria_tempos[2]);
			
			print "Gasto máximo de memória: %.2f MB" % (memoria_max);
			print "Tempo de execução: %.2f s" % tempo_exec;
			
			acertos = []
			num_linhas_gabarito = 0;
			with open(nome_gabarito) as arq_gabarito:
				with open(nome_saida_teste) as arq_teste:
					for linha_gab, linha_teste in zip(arq_gabarito, arq_teste):
						dist_total_split_gab = linha_gab.strip(" \n\r\t\"").split(":");
						dist_total_gab = float(dist_total_split_gab[0]);
						palavras_dist_gab = dist_total_split_gab[1];
						dist_total_split_teste = linha_teste.strip(" \n\r\t\"").split(":");
						dist_total_teste = float(dist_total_split_teste[0]);
						palavras_dist_teste = dist_total_split_teste[1];
						
						if dist_total_gab == dist_total_teste:
							def le_par_gab(par):
								par = par.strip(" \n\r\t\"").split(",");
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
								par = par.strip(" \n\r\t\"").split(",");
								return (par[0], float(par[1]));
						
							pares_gab = palavras_dist_gab.strip(" \n\r\t\"").split(" ");
							pares_gab = map(le_par_gab, pares_gab)
							
							pares_teste = palavras_dist_teste.strip(" \n\r\t\"").split(" ");
							pares_teste = map(le_par_teste, pares_teste);
							
							num_acertos = map(lambda ((a,b),(x,y)):x in a and b==y, zip(pares_gab, pares_teste));
							acertos.append(reduce(lambda x,y:x and y, num_acertos));
							
						else:
							acertos.append(False);
						
						num_linhas_gabarito += 1;
					

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
				acertos_instancias[-1][num_algoritmo-1] = porc_acertos;
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
		
		
		
	
	(acertos_sequencial, acertos_palavras, acertos_interna) = zip(*acertos_instancias);
	
	print "Média ponderada dos acertos (sequencial): %.2f (porcentagem)" % numpy.average(acertos_sequencial, weights=pesos_instancias);
	print "Média ponderada dos acertos (paralelização por palavras): %.2f (porcentagem)" % numpy.average(acertos_palavras, weights=pesos_instancias);
	print "Média ponderada dos acertos (paralelização interna): %.2f (porcentagem)" % numpy.average(acertos_interna, weights=pesos_instancias);
	print "Speedup máximo da paralelização de palavras:", max_speedup_palavras;
	print "Speedup máximo da paralelização interna:", max_speedup_interna;



if __name__ == '__main__':
    import sys;
    verbose = False;
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
    	verbose = True;
    main(verbose);
