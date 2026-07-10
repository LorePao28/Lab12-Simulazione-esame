import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []

    def getAllRatings(self):
        return DAO.getAllRatings()

    def buildGraph(self, r1, r2):
        self._graph.clear()
        self._nodes = DAO.getAllActors(float(r1), float(r2))

        self._graph.add_nodes_from(self._nodes)


    def getGraphDetails(self):
        return len(self._graph.nodes), 0