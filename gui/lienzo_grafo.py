import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class LienzoGrafo(FigureCanvasQTAgg):
    """Componente visual que integra Matplotlib en PyQt6 para renderizar la representación gráfica del grafo."""

    def __init__(self, ancho=6, alto=5, ppi=100):
        self.figura, self.ejes = plt.subplots(figsize=(ancho, alto), dpi=ppi)
        super().__init__(self.figura)

    def graficar_grafo(self, analizador_grafo):
        """Limpia el lienzo actual y dibuja el grafo procesado por el analizador."""
        self.ejes.clear()

        grafo = analizador_grafo.grafo
        es_simetrica = analizador_grafo.es_simetrica

        # Distribución de nodos
        posicion_nodos = nx.spring_layout(grafo, seed=42)

        # Dibujar nodos
        nx.draw_networkx_nodes(
            grafo,
            posicion_nodos,
            ax=self.ejes,
            node_color="#4A90E2",
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

        # Dibujar aristas con o sin flechas según el tipo de grafo
        nx.draw_networkx_edges(
            grafo,
            posicion_nodos,
            ax=self.ejes,
            edge_color="#7F8C8D",
            arrows=not es_simetrica,
            arrowsize=20,
            connectionstyle="arc3,rad=0.1" if not es_simetrica else "arc3,rad=0",
        )

        # Dibujar pesos en las aristas
        etiquetas_pesos = nx.get_edge_attributes(grafo, "weight")
        nx.draw_networkx_edge_labels(
            grafo, posicion_nodos, edge_labels=etiquetas_pesos, ax=self.ejes
        )

        self.ejes.set_title("Representación Gráfica del Grafo", fontsize=12)
        self.ejes.axis("off")
        self.draw()