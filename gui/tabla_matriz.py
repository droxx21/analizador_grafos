import numpy as np
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class TablaMatrizAdyacencia(QTableWidget):
    """Widget de tabla dinámico para la captura de la matriz de adyacencia."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dimension = 0

    def configurar_dimension(self, dimension: int):
        """Redimensiona la tabla e inicializa las celdas con ceros."""
        self.dimension = dimension
        self.setRowCount(dimension)
        self.setColumnCount(dimension)

        etiquetas = [f"V{i+1}" for i in range(dimension)]
        self.setHorizontalHeaderLabels(etiquetas)
        self.setVerticalHeaderLabels(etiquetas)

        # Ajustar tamaño de las celdas
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Llenar por defecto con 0
        for fila in range(dimension):
            for columna in range(dimension):
                item = QTableWidgetItem("0")
                self.setItem(fila, columna, item)

    def obtener_matriz_numpy(self) -> np.ndarray:
        """Extrae los datos numéricos de la tabla y genera una matriz de NumPy."""
        matriz = []
        for fila in range(self.dimension):
            datos_fila = []
            for columna in range(self.dimension):
                item = self.item(fila, columna)
                valor_texto = item.text() if item else "0"
                datos_fila.append(int(valor_texto))
            matriz.append(datos_fila)
        return np.array(matriz)