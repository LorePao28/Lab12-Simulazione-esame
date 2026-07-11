import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMapActor = {}
        self._edges = []

    def getAllRatings(self):
        return DAO.getAllRatings()

    def buildGraph(self, r1, r2):
        self._graph.clear()
        self._nodes = DAO.getAllActors(float(r1), float(r2))
        for n in self._nodes:
            self._idMapActor[n.id] = n

        self._graph.add_nodes_from(self._nodes)
        self._edges = DAO.getAllEdges(r1, r2)
        for n1, n2, w in self._edges:
            self._graph.add_edge(self._idMapActor[n1], self._idMapActor[n2], weight=w)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getArchiMaggiori(self):
        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )
        return edges[:5]

    def getConnectedComponents(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)
        return components, largest

    def getBestPath(self):
        self._optPath = []

        parziale = []
        for a in self._graph.nodes:
            parziale.append(a)
            self._ricorsione(parziale, a.date_of_birth)
            parziale.pop()
        return self._optPath

    def _ricorsione(self, parziale, lastDOB):
        for a in self._graph.neighbors(parziale[-1]):
            if a not in parziale and a.date_of_birth > lastDOB:
                parziale.append(a)
                self._ricorsione(parziale, a.date_of_birth)
                parziale.pop()

        if len(parziale) > len(self._optPath):
            self._optPath = copy.deepcopy(parziale)
            return

    def getBestPathSol(self):

        self._bestPath = []

        for start in self._graph.nodes():
            partial = [start]
            self._ricorsioneSol(partial)

        return self._bestPath

    def _ricorsioneSol(self, partial):

        if len(partial) > len(self._bestPath):
            self._bestPath = list(partial)

        current = partial[-1]

        for _, successor in self._graph.edges(current):

            # vincolo: età decrescente
            if successor not in partial and successor.date_of_birth > current.date_of_birth:
                partial.append(successor)

                self._ricorsioneSol(partial)

                partial.pop()

