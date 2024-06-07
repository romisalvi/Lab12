import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self.anno=None
        self.nazione=None
        self.g=nx.Graph()
        self.vertici=[]
        self.N=0
        self.BP=[]
        self.topPeso=0

        pass
    def getAllCountries(self):
        return DAO.getAllCountries()



    def creaGrafo(self, anno, nazione):
        self.g.clear()
        self.anno=anno
        self.nazione=nazione
        vertici=DAO.getRetNat(nazione)
        self.g.add_nodes_from(vertici)
        self.vertici=self.g.nodes
        print(self.g)
        check=[]
        for v1 in self.vertici:
            for v2 in self.vertici:
                check1=str(v1.Retailer_code)+"-"+str(v2.Retailer_code)
                check2=str(v2.Retailer_code)+"-"+str(v1.Retailer_code)
                if check1 not in check and check2 not in check and check1!=check2:
                    peso=DAO.getPeso(v1.Retailer_code,v2.Retailer_code,self.anno)[0]
                    if peso>0:
                        self.g.add_edge(v1,v2,weight=peso)
        print(self.g)

    def getVerticiOrdinati(self):
        lista=[]
        for vertice in self.g.nodes:
            peso=self.calcolaPesoIncidenti(vertice)
            lista.append((vertice,peso))
        lista.sort(key=lambda x:x[1], reverse=True)
        return lista

    def calcolaPesoIncidenti(self, vertice):
        return sum(self.g[vertice][vicino]["weight"] for vicino in self.g.neighbors(vertice))

    def getBP(self,N):
        self.N=N
        parziale=[]
        for v in self.g.nodes:
            parziale.append(v)
            listaVicini=[]
            for vicino in self.g.neighbors(v):
                listaVicini.append((vicino,self.g[v][vicino]["weight"]) )
            listaVicini.sort(key=lambda x:x[1], reverse=True)
            for element in listaVicini:
                parziale.append(element[0])
                self.ricorsione(parziale)
                parziale.pop()

    def ricorsione(self,parziale):
        print("r")
        if len(parziale)==self.N:
            if parziale[0]!=parziale[-1]:
                return
            pesoP=self.calcolaPesoParziale(parziale)
            if pesoP>self.topPeso:
                self.topPeso=pesoP
                self.BP=copy.deepcopy(parziale)
            return
        pesiVisitabili=[]
        listaVisitabili=self.getVisitabili(parziale[1:],parziale[-1])
        for v in listaVisitabili:
            pesiVisitabili.append((v, self.g[parziale[-1]][v]["weight"]))
        pesiVisitabili.sort(key=lambda x:x[1], reverse=True)
        for v in pesiVisitabili:
            parziale.append(v[0])
            self.ricorsione(parziale)
            parziale.pop()



    def getVisitabili(self,visitati, nodo):
        viciniPossibili=set(self.g.neighbors(nodo))
        visitati_set=set(visitati)
        return list(viciniPossibili - visitati_set)



    def calcolaPesoParziale(self, parziale):
        x=0
        pp=0
        for i in range (0,len(parziale)-1):
            print(i)
            pp+=self.g[parziale[i]][parziale[i+1]]["weight"]
        return pp






