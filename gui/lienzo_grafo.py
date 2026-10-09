import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class LienzoGrafo(FigureCanvasQTAgg):
    """Componente visual que integra Matplotlib en PyQt6 para renderizar la representación gráfica del grafo."""

    def __init__(self, ancho=6, alto=5, ppi=100):
        self.figura, self.ejes = plt.subplots(figsize=(ancho, alto), dpi=ppi)
        super().__init__(self.figura)

    def graficar_grafo(self, analizador_grafo, camino_resaltado: list[str] = None):
        """Dibuja el grafo procesado y resalta las aristas/nodos del camino si se especifica."""
        self.ejes.clear()

        grafo = analizador_grafo.grafo
        es_simetrica = analizador_grafo.es_simetrica

        # Distribución fija para que la grafica no "salte"
        posicion_nodos = nx.spring_layout(grafo, seed=42)

        # Determinar colores de los nodos
        colores_nodos = []
        for nodo in grafo.nodes():
            if camino_resaltado and nodo in camino_resaltado:
                colores_nodos.append("#E74C3C")  # Rojo para el camino
            else:
                colores_nodos.append("#4A90E2")  # Azul por defecto

        # Dibujar nodos
        nx.draw_networkx_nodes(
            grafo,
            posicion_nodos,
            ax=self.ejes,
            node_color=colores_nodos,
            node_size=1500,
        )

        # Dibujar etiquetas de los nodos
        nx.draw_networkx_labels(
            grafo,
            posicion_nodos,
            ax=self.ejes,
            font_size=10,
            font_color="white",
            font_weight="bold",
        )

        # Determinar aristas del camino para colorearlas de rojo
        aristas_camino = []
        if camino_resaltado and len(camino_resaltado) > 1:
            for i in range(len(camino_resaltado) - 1):
                aristas_camino.append(
                    (camino_resaltado[i], camino_resaltado[i + 1])
                )

        aristas_normales = [
            e for e in grafo.edges() if e not in aristas_camino
        ]

        # Dibujar aristas normales
        nx.draw_networkx_edges(
            grafo,
            posicion_nodos,
            edgeList=aristas_normales,
            ax=self.ejes,
            edge_color="#7F8C8D",
            width=1.5,
            arrows=not es_simetrica,
            arrowsize=18,
            connectionstyle="arc3,rad=0.1" if not es_simetrica else "arc3,rad=0",
        )

        # Dibujar aristas resaltadas del camino
        if aristas_camino:
            nx.draw_networkx_edges(
                grafo,
                posicion_nodos,
                edgeList=aristas_camino,
                ax=self.ejes,
                edge_color="#E74C3C",
                width=3.5,
                arrows=not es_simetrica,
                arrowsize=22,
                connectionstyle="arc3,rad=0.1" if not es_simetrica else "arc3,rad=0",
            )

        # Dibujar etiquetas con los pesos
        etiquetas_pesos = nx.get_edge_attributes(grafo, "weight")
        nx.draw_networkx_edge_labels(
            grafo, posicion_nodos, edge_labels=etiquetas_pesos, ax=self.ejes
        )

        self.ejes.set_title("Representación Gráfica del Grafo", fontsize=12)
        self.ejes.axis("off")
        self.draw()