import numpy as np

class ValidadorMatriz:
    """Clase encargada de validar las entradas de la matriz de adyacencia y verificar la integridad de los datos"""

    @staticmethod
    def validar_dimension(texto_dimension: str) -> tuple[bool, str, int]:
        """Vaida que la dimensión sea un número entero mayor a cero"""

        try:
            cantidad_nodos = int(texto_dimension)
            if cantidad_nodos <= 0:
                return (False, "El número de nodos debe ser un entero mayor a 0.", 0)
            return True, "", cantidad_nodos
        except ValueError:
            return False, "La dimensión ingresada debe ser un entero válido.", 0

    @staticmethod
    def validar_fila(texto_fila: str, dimension_esperada: int) -> tuple[bool, str, list[int]]:
        """Valida que una fila tenga la cantidad exacta de elementos y que sean enteros no negativos (pesos o adyacencias)."""

        try:
            elementos = list(map(int, texto_fila.strip().split()))

            if len(elementos) != dimension_esperada:
                return (False, f"La fila debe contener exactamente {dimension_esperada} vaalores.", [])
            
            if any(valor < 0 for valor in elementos):
                return (False, "Los valores no pueden ser negativos (deben ser >= 0).", [])
            return True, "", elementos
        except ValueError:
            return (False, "La fila contiene valores no numéricos o inválidos.", [])

    @staticmethod
    def es_matriz_simetrica(matriz_adyacencia: np.ndarray) -> bool:
        """Determina si la matriz es simétrica.
        Si es simétrica, representa un grafo NO DIRIGIDO.
        Si no es simétrica, representa un DIGRAFO (GRAFO DIRIGIDO)."""

        return np.array_equal(matriz_adyacencia, matriz_adyacencia.T)
            