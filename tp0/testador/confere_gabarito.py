# -*- coding: utf8 -*-
import os;
import subprocess;

def main():
	dir_gabarito = "exemplos/";
	
	instancias_teste = ["small_input", "medium_input", "big_input"];
	
	for nome_instancia in instancias_teste:
		print "Testando instância", nome_instancia;
		
		nome_gabarito = dir_gabarito + nome_instancia + ".sol";
		nome_entrada = dir_gabarito + nome_instancia + ".in";
		nome_saida_teste = nome_instancia + ".out";
		
		args_subp = ['/usr/bin/time', '-v', './tp0', nome_entrada, nome_saida_teste];
		output = subprocess.check_output(args_subp, stderr=subprocess.STDOUT).split("\n");
		memoria_max = int(output[-15].split(" ")[-1])/1024.
		tempo_exec = float(output[-22].split(" ")[-1])+float(output[-23].split(" ")[-1])
		
		linhas_gabarito = [];
		with open(nome_gabarito, 'r') as arq_gabarito:
			for linha in arq_gabarito:
				if linha != '\n':
					linhas_gabarito.append(linha.strip());
		
		num_linhas_gabarito = len(linhas_gabarito);
		#Para permitir o uso de pop nessa lista na ordem de leitura do arquivo
		linhas_gabarito.reverse()
		
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
			
		print "Porcentagem de acertos: %d" % (float(num_acertos / num_linhas_gabarito) * 100);
		print "Gasto máximo de memória: %.2f MB" % memoria_max;
		print "Tempo de execução: %.2f s" % tempo_exec;
		print "\n"

if __name__ == '__main__':
	import sys;
	main();
