#include <iostream>
#include <fstream>
#include <stdlib.h>

using namespace std;



  const int numV = 100;
  int numCons = 50;
  int matriz [numV][numV];
  int isMarcado[numV]; //Para conferencia de conectividade


void visite(int v){
	// marca v como visitado
	isMarcado[v] = 1;
	for(int i=0; i<numV; i++){
	    // se existir aresta e não for marcado, visitar proximo vertice
		if(matriz[v][i] == 1 && isMarcado[i]==0){
			visite(i);
		}
	}


}//-------------------------------------------------------------------


int getNumComp(){
	int numComponentes = 0;

	//considera todos como nao visitados
	for(int i=0; i<numV; i++){
		isMarcado[i]=0;
	}

    // para cada vertice não visitada chama a função visite
	for(int i=0;i<numV;i++){
		if(isMarcado[i] == 0){
			visite(i);
			//incremente o numero de componentes
			numComponentes++;
		}
	}

    return numComponentes;

}//-------------------------------------------------------------------


int main()
{

  ofstream arquivo;
  arquivo.open ("saida.txt");


  for(int i=0; i<numV; i++){
    for(int j=0; j<numV; j++){
        matriz[i][j] = 0;
    }
}

  int a, b;
  int contE = 0; //Conta quantas arestas

  //Gera arestas aleatórias até o grafo ficar conexo
  while(getNumComp() > 1){
      a = rand() % numV + 1;
      b = rand() % numV + 1;

      //Não pode existir loop
      if(a != b){
        //não pode existir aresta "paralela"
        if(matriz[a-1][b-1] == 0){
            arquivo<<a<<" "<<b<<endl;
            matriz[a-1][b-1] = 1;
            matriz[b-1][a-1] = 1;
            contE++;
        }
      }

  }

  arquivo<<numCons<<endl;

  for(int i=0; i<numCons; i++){
      a = rand() % numV + 1;
      b = rand() % numV + 1;

      //Não pode existir consulta de a para a
      if(a != b){
          arquivo<<a<< " "<<b<<endl;
      }
  }

   arquivo<<endl<<endl<<"E = "<<contE;


   arquivo.close();
}
