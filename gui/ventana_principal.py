from core.analizador_grafo import AnalizadorGrafo
from core.validador import ValidadorMatriz
from gui.lienzo_grafo import LienzoGrafo
from gui.tabla_matriz import TablaMatrizAdyacencia
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Analizador de Grafos - Algoritmos de Ruta Más Corta"
        )
        self.setGeometry(100, 100, 1200, 750)
        self.analizador_actual = None

        self._inicializar_ui()

    def _inicializar_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central)

        # --- PANEL IZQUIERDO: Controles y Matriz ---
        panel_izquierdo = QVBoxLayout()

        # Entrada de dimensión
        layout_dimension = QHBoxLayout()
        layout_dimension.addWidget(QLabel("Cantidad de Vértices (n):"))
        self.campo_dimension = QLineEdit("4")
        layout_dimension.addWidget(self.campo_dimension)

        self.boton_crear_matriz = QPushButton("Generar Tabla")
        self.boton_crear_matriz.clicked.connect(self._al_crear_matriz)
        layout_dimension.addWidget(self.boton_crear_matriz)

        panel_izquierdo.addLayout(layout_dimension)

        # Tabla de adyacencia
        self.tabla_matriz = TablaMatrizAdyacencia()
        panel_izquierdo.addWidget(self.tabla_matriz)

        # Botón para procesar
        self.boton_analizar = QPushButton("Procesar Matriz y Grafo")
        self.boton_analizar.clicked.connect(self._al_analizar_grafo)
        panel_izquierdo.addWidget(self.boton_analizar)

        # --- SECCIÓN: Selección de Origen, Destino y Algoritmo ---
        layout_ruta = QHBoxLayout()

        layout_ruta.addWidget(QLabel("Origen:"))
        self.combo_origen = QComboBox()
        layout_ruta.addWidget(self.combo_origen)

        layout_ruta.addWidget(QLabel("Destino:"))
        self.combo_destino = QComboBox()
        layout_ruta.addWidget(self.combo_destino)

        layout_ruta.addWidget(QLabel("Algoritmo:"))
        self.combo_algoritmo = QComboBox()
        self.combo_algoritmo.addItems(["Dijkstra", "Bellman-Ford"])
        layout_ruta.addWidget(self.combo_algoritmo)

        panel_izquierdo.addLayout(layout_ruta)

        self.boton_calcular_ruta = QPushButton("Calcular Ruta Más Corta")
        self.boton_calcular_ruta.clicked.connect(self._al_calcular_ruta)
        panel_izquierdo.addWidget(self.boton_calcular_ruta) 

        # Área de texto para evidencias textuales
        panel_izquierdo.addWidget(QLabel("Resultados y Evidencias:"))
        self.caja_resultados = QTextEdit()
        self.caja_resultados.setReadOnly(True)
        panel_izquierdo.addWidget(self.caja_resultados)

        # --- PANEL DERECHO: Canvas de Visualización ---
        panel_derecho = QVBoxLayout()
        self.lienzo = LienzoGrafo()
        panel_derecho.addWidget(self.lienzo)

        # Integrar paneles al layout principal (proporción 40% - 60%)
        layout_principal.addLayout(panel_izquierdo, 40)
        layout_principal.addLayout(panel_derecho, 60)

        # Inicializar matriz por defecto con 4 nodos
        self._al_crear_matriz()

    def _actualizar_combos_nodos(self, nodos: list[str]):
        """Actualiza los selectores de origen y destino con la lista de nodos disponibles."""
        self.combo_origen.clear()
        self.combo_destino.clear()
        self.combo_origen.addItems(nodos)
        self.combo_destino.addItems(nodos)
        if len(nodos) > 1:
            self.combo_destino.setCurrentIndex(len(nodos) - 1)

    def _al_crear_matriz(self):
        es_valido, mensaje, dimension = ValidadorMatriz.validar_dimension(
            self.campo_dimension.text()
        )
        if not es_valido:
            QMessageBox.critical(self, "Error de Entrada", mensaje)
            return

        self.tabla_matriz.configurar_dimension(dimension)
        nodos = [f"V{i+1}" for i in range (dimension)]
        self._actualizar_combos_nodos(nodos)

    def _al_analizar_grafo(self):
        try:
            matriz = self.tabla_matriz.obtener_matriz_numpy()
        except ValueError:
            QMessageBox.critical(
                self,
                "Error",
                "La tabla contiene valores no válidos. Ingrese solo números enteros.",
            )
            return

        es_simetrica = ValidadorMatriz.es_matriz_simetrica(matriz)
        self.analizador_actual = AnalizadorGrafo(matriz, es_simetrica)

        # Renderizar gráfico base sin resaltar caminos
        self.lienzo.graficar_grafo(self.analizador_actual)

        # Generar reporte base de evidencias
        rep_mat = self.analizador_actual.obtener_representacion_matematica()
        adyacencias = self.analizador_actual.obtener_nodos_adyacentes()
        ciclos = self.analizador_actual.obtener_ciclos()

        texto_reporte = f"--- TIPO DE GRAFO ---\n{rep_mat['tipo']}\n\n"
        texto_reporte += f"--- REPRESENTACIÓN MATEMÁTICA ---\n"
        texto_reporte += f"Vérteces (V) = {rep_mat['vertices']}\n"
        texto_reporte += f"Aristas (E)  = {rep_mat['aristas']}\n\n"

        texto_reporte += "--- EVIDENCIA: NODOS ADYACENTES ---\n"
        for nodo, vecinos in adyacencias.items():
            texto_reporte += f"• {nodo} -> {vecinos}\n"

        texto_reporte += "\n--- EVIDENCIA: CICLOS DETECTADOS ---\n"
        if ciclos:
            for ciclo in ciclos:
                texto_reporte += f"• Ciclo: {ciclo}\n"
        else:
            texto_reporte += "El grafo no contiene ciclos (Acíclico).\n"

        self.caja_resultados.setText(texto_reporte)

    def _al_calcular_ruta(self):
        if not self.analizador_actual:
            self._al_analizar_grafo()

        origen = self.combo_origen.currentText()
        destino = self.combo_destino.currentText()
        algoritmo = self.combo_algoritmo.currentText()

        if not origen or not destino:
            QMessageBox.warning(
                self, "Atención", "Seleccione los nodos de origen y destino."
            )
            return

        if algoritmo == "Dijkstra":
            camino, costo = self.analizador_actual.calcular_dijkstra(
                origen, destino
            )
        else:
            camino, costo = self.analizador_actual.calcular_bellman_ford(
                origen, destino
            )

        # Actualizar gráfica resaltando el camino
        self.lienzo.graficar_grafo(
            self.analizador_actual, camino_resaltado=camino
        )

        # Imprimir salida de la ruta más corta
        texto_actual = self.caja_resultados.toPlainText()
        separador = "\n" + "=" * 40 + "\n"
        salida_ruta = f"--- RUTA MÁS CORTA ({algoritmo.upper()}) ---\n"
        salida_ruta += f"Origen: {origen}  |  Destino: {destino}\n"

        if camino and costo != float("inf"):
            salida_ruta += f"Nodos de la ruta: {' -> '.join(camino)}\n"
            salida_ruta += f"Costo/Peso total: {costo}\n"
        else:
            salida_ruta += f"No existe ninguna ruta conectada entre {origen} y {destino}.\n"

        self.caja_resultados.setText(texto_actual + separador + salida_ruta)