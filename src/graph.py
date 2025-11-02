import random
import numpy as np
from typing import List, Tuple, Optional


class Graph:
    """
    Clase para representar un grafo dirigido ponderado.
    Utiliza matriz de adyacencia para almacenar las conexiones.
    """

    def __init__(self, num_nodes: int = 0):
        """
        Inicializa un grafo con num_nodes nodos.

        Args:
            num_nodes: Número de nodos del grafo
        """
        self.num_nodes = num_nodes
        self.adjacency_matrix = np.full((num_nodes, num_nodes), np.inf)
        np.fill_diagonal(self.adjacency_matrix, 0)
        self.node_labels = [str(i) for i in range(num_nodes)]

    def add_edge(self, source: int, dest: int, weight: float) -> bool:
        """
        Agrega una arista al grafo.

        Args:
            source: Nodo origen
            dest: Nodo destino
            weight: Peso de la arista

        Returns:
            True si se agregó exitosamente, False en caso contrario
        """
        if 0 <= source < self.num_nodes and 0 <= dest < self.num_nodes:
            if source != dest and weight > 0:
                self.adjacency_matrix[source][dest] = weight
                return True
        return False

    def remove_edge(self, source: int, dest: int) -> bool:
        """
        Elimina una arista del grafo.

        Args:
            source: Nodo origen
            dest: Nodo destino

        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        if 0 <= source < self.num_nodes and 0 <= dest < self.num_nodes:
            self.adjacency_matrix[source][dest] = np.inf
            return True
        return False

    def get_weight(self, source: int, dest: int) -> float:
        """
        Obtiene el peso de una arista.

        Args:
            source: Nodo origen
            dest: Nodo destino

        Returns:
            Peso de la arista o infinito si no existe
        """
        if 0 <= source < self.num_nodes and 0 <= dest < self.num_nodes:
            return self.adjacency_matrix[source][dest]
        return np.inf

    def get_neighbors(self, node: int) -> List[Tuple[int, float]]:
        """
        Obtiene los vecinos de un nodo con sus pesos.

        Args:
            node: Nodo a consultar

        Returns:
            Lista de tuplas (vecino, peso)
        """
        neighbors = []
        if 0 <= node < self.num_nodes:
            for i in range(self.num_nodes):
                if self.adjacency_matrix[node][i] != np.inf and i != node:
                    neighbors.append((i, self.adjacency_matrix[node][i]))
        return neighbors

    def is_connected(self, source: int, dest: int) -> bool:
        """
        Verifica si existe al menos un camino entre dos nodos usando BFS.

        Args:
            source: Nodo origen
            dest: Nodo destino

        Returns:
            True si existe un camino, False en caso contrario
        """
        if source == dest:
            return True

        visited = [False] * self.num_nodes
        queue = [source]
        visited[source] = True

        while queue:
            current = queue.pop(0)

            for neighbor, _ in self.get_neighbors(current):
                if neighbor == dest:
                    return True
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

        return False

    @staticmethod
    def generate_random_graph(num_nodes: int, density: float = 0.3,
                              min_weight: int = 1, max_weight: int = 10,
                              ensure_connected: bool = True) -> 'Graph':
        """
        Genera un grafo aleatorio no completamente conectado.

        Args:
            num_nodes: Número de nodos
            density: Probabilidad de que exista una arista (0.0 a 1.0)
            min_weight: Peso mínimo de las aristas
            max_weight: Peso máximo de las aristas
            ensure_connected: Si True, garantiza que el grafo sea conexo

        Returns:
            Grafo aleatorio generado
        """
        if num_nodes < 2:
            raise ValueError("El grafo debe tener al menos 2 nodos")

        if not 0 <= density <= 1:
            raise ValueError("La densidad debe estar entre 0 y 1")

        graph = Graph(num_nodes)

        # Asegurar conectividad mínima creando un árbol de expansión
        if ensure_connected and num_nodes > 1:
            nodes = list(range(num_nodes))
            random.shuffle(nodes)

            # Crear camino que conecte todos los nodos
            for i in range(len(nodes) - 1):
                weight = random.randint(min_weight, max_weight)
                graph.add_edge(nodes[i], nodes[i + 1], weight)

        # Agregar aristas adicionales según la densidad
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j:
                    # Si ya existe una arista, no la sobrescribimos
                    if graph.adjacency_matrix[i][j] == np.inf:
                        if random.random() < density:
                            weight = random.randint(min_weight, max_weight)
                            graph.add_edge(i, j, weight)

        return graph

    def get_adjacency_matrix(self) -> np.ndarray:
        """
        Retorna una copia de la matriz de adyacencia.

        Returns:
            Copia de la matriz de adyacencia
        """
        return self.adjacency_matrix.copy()

    def __str__(self) -> str:
        """
        Representación en string del grafo.

        Returns:
            String con la matriz de adyacencia
        """
        result = f"Grafo con {self.num_nodes} nodos:\n"
        result += "Matriz de Adyacencia:\n"

        # Reemplazar infinito por '-' para mejor visualización
        display_matrix = np.where(
            self.adjacency_matrix == np.inf,
            -1,
            self.adjacency_matrix
        )

        for row in display_matrix:
            row_str = " ".join([f"{val:6.1f}" if val != -1 else "   inf" for val in row])
            result += row_str + "\n"

        return result

    def get_edge_list(self) -> List[Tuple[int, int, float]]:
        """
        Obtiene la lista de aristas del grafo.

        Returns:
            Lista de tuplas (origen, destino, peso)
        """
        edges = []
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if self.adjacency_matrix[i][j] != np.inf and i != j:
                    edges.append((i, j, self.adjacency_matrix[i][j]))
        return edges

    def copy(self) -> 'Graph':
        """
        Crea una copia profunda del grafo.

        Returns:
            Copia del grafo
        """
        new_graph = Graph(self.num_nodes)
        new_graph.adjacency_matrix = self.adjacency_matrix.copy()
        new_graph.node_labels = self.node_labels.copy()
        return new_graph