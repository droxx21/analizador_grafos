import networkx as nx
import numpy as np

class AnalizadorGrafo:
    """Clase que encapsula la lógica matemática y algoritmos para el análisis de un grafo."""

    def __init__(self, matriz_adyacencia: np.ndarray, es_simetrica: bool):
        self.matriz = matriz_adyacencia
        self.es_simetrica = es_simetrica
        self.cantidad_nodos = len(matriz_adyacencia)
        self.etiquetas_nodos = [f"V{i+1}" for i in range(self.cantidad_nodos)]

        if self.es_simetrica:
            self.grafo = nx.Graph()
        else:
            self.grafo = nx.DiGraph()

        self._construir_grafo()

    def _construir_grafo(self):
        """Agrega los nodos y aristas con sus respectivos pesos al grafo."""

        for nodo in self.etiquetas_nodos:
            self.grafo.add_node(nodo)

        for i in range(self.cantidad_nodos):
            for j in range(self.cantidad_nodos):
                peso = self.matriz[i][j]
                if peso > 0:
                    origen = self.etiquetas_nodos[i]
                    destino = self.etiquetas_nodos[j]
                    self.grafo.add_edge(origen, destino, weight=peso)

    def obtener_representacion_matematica(self) -> dict:
        """Devuelve los conjuntos formales V (vertices) y E (aristas)."""

        conjunto_vertices = set(self.grafo.nodes())
        conjunto_aristas = set(self.grafo.edges())

        return {
            "vertices": conjunto_vertices,
            "aristas": conjunto_aristas,
            "tipo": "No Dirigido" if self.es_simetrica else "Dirigido (Digrafo)",
            
        }

    def obtener_nodos_adyacentes(self) -> dict[str, list[str]]:
        """Retorna un diccionario con la lista de nodos adyacentes (vecinos) para cada vértice."""
        adyacencias = {}
        for nodo in self.etiquetas_nodos:
            adyacencias[nodo] = list(self.grafo.neighbors(nodo))
        return adyacencias

    def obtener_caminos(
        self, nodo_origen: str, nodo_destino: str
    ) -> list[list[str]]:
        """Encuentra todos los caminos simples entre un nodo de origen y uno de destino."""
        if (
            nodo_origen in self.grafo
            and nodo_destino in self.grafo
            and nx.has_path(self.grafo, nodo_origen, nodo_destino)
        ):
            return list(
                nx.all_simple_paths(
                    self.grafo, source=nodo_origen, target=nodo_destino
                )
            )
        return []

    def obtener_ciclos(self) -> list[list[str]]:
        """Detecta los ciclos presentes en el grafo."""
        if not self.es_simetrica:
            return list(nx.simple_cycles(self.grafo))
        else:
            return nx.cycle_basis(self.grafo)
                                 