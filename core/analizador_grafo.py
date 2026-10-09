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

    def calcular_dijkstra(self, nodo_origen: str, nodo_destino: str) -> tuple[list[str], float]:
        """Calcula la ruta más corta usando el algoritmo de Dijkstra."""

        # Verificar que existan los nodos
        if (nodo_origen not in self.grafo or nodo_destino not in self.grafo):
            return [], float("inf")

        # Dijkstra no admite pesos negativos
        for _, _, datos in self.grafo.edges(data=True):
            if datos.get("weight", 1) < 0:
                raise ValueError("Dijkstra no admite pesos negativos.")

        # Inicializar los costos y los predecesores 
        costos = { nodo: float("inf") for nodo in self.grafo.nodes }
        predecesores = {nodo: None for nodo in self.grafo.nodes}
        visitados = set()
        costos[nodo_origen] = 0

        while len(visitados) < len(costos):

            # Buscar manualmente el nodo no visitado con menor costo acumulado
            nodo_actual = None
            menor_costo = float("inf")

            for nodo in costos:
                if (nodo not in visitados and costos[nodo] < menor_costo): 
                    nodo_actual = nodo
                    menor_costo = costos[nodo]

            # No quedan nodos alcanzables
            if nodo_actual is None or nodo_actual == nodo_destino:
                break

            visitados.add(nodo_actual)

            # Examinar las aristas que salen del nodo actual
            for vecino, datos in self.grafo[nodo_actual].items():
                if vecino in visitados:
                    continue

                peso = datos.get("weight", 1)
                nuevo_costo = costos[nodo_actual] + peso

                # Relajación: mejorar el costo conocido
                if nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    predecesores[vecino] = nodo_actual

        # Si el destino sigue siendo inalcanzable
        if costos[nodo_destino] == float("inf"):
            return [], float("inf")

        # Reconstruir el camino desde el destino
        camino = []
        nodo = nodo_destino

        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]

        camino.reverse()

        return camino, costos[nodo_destino]

    def calcular_bellman_ford(self, nodo_origen: str, nodo_destino: str) -> tuple[list[str], float]:

        if (nodo_origen not in self.grafo or nodo_destino not in self.grafo):
            return [], float("inf")

        nodos = list(self.grafo.nodes)
        aristas = []

        # Convertir las aristas del grafo a una lista
        for origen, destino, datos in self.grafo.edges(data=True):
            peso = datos.get("weight", 1)

            aristas.append((origen, destino, peso))

            # En grafos no dirigidos, se puede recorrer
            # la arista en ambas direcciones.
            if not self.grafo.is_directed():
                aristas.append((destino, origen, peso))

        costos = { nodo: float("inf") for nodo in nodos }
        predecesores = {nodo: None for nodo in nodos}
        costos[nodo_origen] = 0

        # Relajar todas las aristas V - 1 veces
        for _ in range(len(nodos) - 1):
            hubo_cambios = False

            for origen, destino, peso in aristas:
                if costos[origen] == float("inf"):
                    continue

                nuevo_costo = costos[origen] + peso

                if nuevo_costo < costos[destino]:
                    costos[destino] = nuevo_costo
                    predecesores[destino] = origen
                    hubo_cambios = True

            # Si no hubo cambios, ya no es necesario continuar
            if not hubo_cambios:
                break

        # Detectar ciclos negativos alcanzables desde el origen
        for origen, destino, peso in aristas:
            if costos[origen] == float("inf"):
                continue

            if costos[origen] + peso < costos[destino]:
                raise ValueError(
                    "Existe un ciclo de peso negativo "
                    "alcanzable desde el origen."
                )

        if costos[nodo_destino] == float("inf"):
            return [], float("inf")

        # Reconstruir la ruta
        camino = []
        nodo = nodo_destino

        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]

        camino.reverse()

        return camino, costos[nodo_destino]
                                 