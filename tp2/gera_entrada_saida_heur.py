# -*- coding: utf8 -*-
import sys;
import random

def main(num_alunos, num_instancias, nome_arq_in, nome_arq_sol):
	with open(nome_arq_in, "w") as arq_in:
		with open(nome_arq_sol, "w") as arq_sol:
			arq_in.write(str(num_instancias) + '\n');
			
			for inst in range(0, num_instancias):
				tam_mis = 1;
				arq_sol.write(str(tam_mis) + '\n');
				
				arq_in.write("%d %d\n" % (num_alunos, tam_mis));
				for i in range(1, tam_mis+1):
					arq_in.write(" ".join([str(x) for x in [i] + range(tam_mis+1, num_alunos+1)]) + '\n');

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print "Usage:", sys.argv[0], "<núm_alunos> <num_instancias> <nome_arq_in> <nome_arq_sol>";
		sys.exit(0);
	
	num_alunos = int(sys.argv[1]);
	num_instancias = int(sys.argv[2]);
	
	main(num_alunos, num_instancias, sys.argv[3], sys.argv[4]);
