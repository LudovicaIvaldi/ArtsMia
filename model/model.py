import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMap={}
        for v in self._nodes:
            self._idMap[v.object_id]=v

    def buildGraph(self):
        #nodes=DAO.getAllNodes()
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges()

    def addEdgesV1(self):
        #va ma ci mette qualche anno
        for u in self._nodes:
            for v in self._nodes:
                peso= DAO.getPeso(u,v)
                if peso != None:
                    self._graph.add_edge(u,v, weight=peso)

    def addAllEdges(self):
        allEdges=DAO.getAllArchi(self._idMap)
        for e in allEdges:
            self._graph.add_edge(e.o1,e.o2,weight=e.peso)


    def getInfoConnessa(self,idInput):
        """
        identifica la componente connessa che contiene id input e ne restituisce la dimensione
        """
        if not self.hasNode(idInput):
           return None
        source=self._idMap[idInput]

        #modo 1 -> conto i successori
        succ=nx.dfs_successors(self._graph,source).values()
        #liste di oggetti
        res=[]
        for s in succ:
            res.extend(s)
            #se la riga è ggtto metto lui se è una lista faccio l'unpact e metto tutti gli oggetti
        print("Size connessa con modo 1: ", len(res))
        #tutti i nodi che puoi raggiungere da source (tranne il nodo di partenza)
        #ogni nodo hai losta di nodi in cui puoi andare

        #modo 2 -> contro i predecessori
        pred = nx.dfs_predecessors(self._graph, source)
        print("Size connessa con modo 2: ", len(pred.values()))
        # qui per ogni nodo hai solo un genito, da quale ci arrivi e basta, ogni chiave ha un solo valore

        #modo 3 -> conto i nodi dell'albero di visita
        dfsTree= nx.dfs_tree(self._graph,source)
        print("Size connessa con modo 3: ", len(dfsTree.nodes()))

        #modo 4 -> uso il metodo nodes_connected_component di nx
        conn=nx.node_connected_component(self._graph,source)
        print("Size connessa con modo 4: ", len(conn))

        return len(conn)


    def hasNode(self, idInput):
        return idInput in self._idMap
    #se c'è nella mappa c'è anche nel grafo




    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getIdMap(self):
        return self._idMap

    def getObjectFromId(self, idInput):
        return self._idMap[idInput]