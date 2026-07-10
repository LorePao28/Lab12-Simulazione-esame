import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._ratingValue1 = None
        self._ratingValue2 = None


    def fillDDsRating(self):
        ratings = self._model.getAllRatings()
        ratingsDDOptions1 = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceRating1), ratings))
        ratingsDDOptions2 = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceRating2), ratings))
        self._view._ddrating1.options = ratingsDDOptions1
        self._view._ddrating2.options = ratingsDDOptions2

    def _choiceRating1(self, e):
        self._ratingValue1 = e.control.data
        print("selezionato rating di partenza " + str(self._ratingValue1))

    def _choiceRating2(self, e):
        self._ratingValue2 = e.control.data
        print("selezionato rating di chiusura " + str(self._ratingValue2))

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        if self._ratingValue1 is None or self._ratingValue2 is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare il range di rating!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(self._ratingValue1, self._ratingValue2)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))

        self._view.update_page()

    def handleCammino(self, e):
        pass