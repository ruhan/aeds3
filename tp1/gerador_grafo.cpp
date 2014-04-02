#include <iostream>
#include <fstream>
#include <stdlib.h>

using namespace std;


  const int numV = 6; //Numero de vértices
  int numCons = 3; //Número de consultas
  int pesoMax = 10; //Número máximo do peso das arestas

  bool alcancavel;
  int matriz [numV][numV];
  int isMarcado[numV]; //Para conferencia de conectividade


//--------------------------------------------------------------------
// visite()
//--------------------------------------------------------------------
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


//--------------------------------------------------------------------
// getNumComponentes(): Retorna o numero de componentes.
//--------------------------------------------------------------------
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


//--------------------------------------------------------------------
// visite2()
//--------------------------------------------------------------------
void visite2 (int v, int final){
	// marcar como visitado
	isMarcado[v] = 1;
	if(v == final)
        alcancavel = true;
	// percorrer seus adjacentes
	for(int i=0; i<numV; i++){
		if(matriz[v][i] == 1 && isMarcado[i]==0){
			visite2(i, final);
		}
	}
}//-------------------------------------------------------------------


//--------------------------------------------------------------------
// buscaProfundidade(): Imprime a leitura do grafo.
//--------------------------------------------------------------------
void buscaProfundidade (int inicial, int final){
	//considera todos como nao visitados
	alcancavel = false;
	for(int i=0; i<numV; i++){
		isMarcado[i]=0;
	}

		if(isMarcado[inicial] == 0){
			visite2(inicial, final);
		}
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

  int a, b, c, peso;
  int contE = 0; //Conta quantas arestas

  //Gera arestas aleatórias até o grafo ficar conexo
  while(getNumComp() > 1){
      a = rand() % numV + 1;
      b = rand() % numV + 1;

      //Não pode existir self-loop
      if(a != b){
        //não pode existir aresta "paralela"
        if(matriz[a-1][b-1] == 0){
            peso = rand() % pesoMax + 1;
            arquivo<<a<<" "<<b<<" "<<peso<<endl;
            matriz[a-1][b-1] = 1;
//            matriz[b-1][a-1] = 1; arestas direcionadas
            contE++;
        }
      }

  }


  //Gera consultas

  arquivo<<numCons<<endl;
  int cont = 0;
  while(cont != numCons){
      a = rand() % numV; //Vertice inicial
      b = rand() % numV; //Vertice final
      c = rand() % 4; //Tipo de consulta



      //Não pode existir consulta de a para a
      if(a != b){
          buscaProfundidade(a, b);
          if(alcancavel == true){ // Se existe um caminho direcionado de A a B
            cont++;
            arquivo<<c<<" "<<a+1<< " "<<b+1<<endl;
            alcancavel = false;
          }
      }
  }

   arquivo<<endl<<endl<<"E = "<<contE; //Imprime o número de arestas


   arquivo.close();
}
