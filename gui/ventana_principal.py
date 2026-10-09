from core.analizador_grafo import AnalizadorGrafo
from core.validador import ValidadorMatriz
from gui.lienzo_grafo import LienzoGrafo
from gui.tabla_matriz import TablaMatrizAdyacencia
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
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
            "Analizador de Grafos - Visualizador y Evidencias"
        )
        self.setGeometry(100, 100, 1100, 700)

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
        self.boton_analizar = QPushButton("Procesar y Graficar")
        self.boton_analizar.clicked.connect(self._al_analizar_grafo)
        panel_izquierdo.addWidget(self.boton_analizar)

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

    def _al_crear_matriz(self):
        es_valido, mensaje, dimension = ValidadorMatriz.validar_dimension(
            self.campo_dimension.text()
        )
        if not es_valido:
            QMessageBox.critical(self, "Error de Entrada", mensaje)
            return

        self.tabla_matriz.configurar_dimension(dimension)

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
        analizador = AnalizadorGrafo(matriz, es_simetrica)

        # 1. Renderizar el gráfico
        self.lienzo.graficar_grafo(analizador)

        # 2. Generar el reporte de evidencias en texto
        rep_mat = analizador.obtener_representacion_matematica()
        adyacencias = analizador.obtener_nodos_adyacentes()
        ciclos = analizador.obtener_ciclos()

        texto_reporte = f"--- TIPO DE GRAFO ---\n{rep_mat['tipo']}\n\n"
        texto_reporte += f"--- REPRESENTACIÓN MATEMÁTICA ---\n"
        texto_reporte += f"Vértices (V) = {rep_mat['vertices']}\n"
        texto_reporte += f"Aristas (E)  = {rep_mat['aristas']}\n\n"

        texto_reporte += "--- EVIDENCIA: NODOS ADYACENTES ---\n"
        for nodo, vecinos in adyacencias.items():
            texto_reporte += f"• {nodo} -> {vecinos}\n"

        texto_reporte += "\n--- EVIDENCIA: CAMINOS (Ejemplo V1 a Vn) ---\n"
        origen, destino = (
            analizador.etiquetas_nodos[0],
            analizador.etiquetas_nodos[-1],
        )
        caminos = analizador.obtener_caminos(origen, destino)
        if caminos:
            for c in caminos:
                texto_reporte += f"• {' -> '.join(c)}\n"
        else:
            texto_reporte += f"No hay caminos entre {origen} y {destino}.\n"

        texto_reporte += "\n--- EVIDENCIA: CICLOS DETECTADOS ---\n"
        if ciclos:
            for ciclo in ciclos:
                texto_reporte += f"• Ciclo: {ciclo}\n"
        else:
            texto_reporte += "El grafo no contiene ciclos (Acíclico).\n"

        self.caja_resultados.setText(texto_reporte)