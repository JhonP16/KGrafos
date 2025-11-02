import numpy as np
from typing import List, Tuple, Optional, Dict
from collections import defaultdict
import heapq
from graph import Graph


class KShortestPaths:
    """
    Implementación del algoritmo de Yen para encontrar los K caminos más cortos.
    """

    def __init__(self, graph: Graph):
        """
        Inicializa el algoritmo con un grafo.

        Args:
            graph: Grafo sobre el cual calcular los k-paths
        """
        self.graph = graph
        self.num_nodes = graph.num_nodes

    def dijkstra(self, source: int, dest: int,
                 excluded_edges: set = None) -> Tuple[Optional[List[int]], float]:
        """
        Algoritmo de Dijkstra para encontrar el camino más corto.

        Args:
            source: Nodo origen
            dest: Nodo destino
            excluded_edges: Conjunto de aristas excluidas (tuplas (u, v))

        Returns:
            Tupla (camino, costo). Retorna (None, inf) si no hay camino.
        """
        if excluded_edges is None:
            excluded_edges = set()

        # Inicialización
        distances = [np.inf] * self.num_nodes
        distances[source] = 0
        previous = [-1] * self.num_nodes
        visited = [False] * self.num_nodes

        # Cola de prioridad: (distancia, nodo)
        pq = [(0, source)]

        while pq:
            current_dist, u = heapq.heappop(pq)

            if visited[u]:
                continue

            visited[u] = True

            # Si llegamos al destino, reconstruir camino
            if u == dest:
                path = []
                current = dest
                while current != -1:
                    path.append(current)
                    current = previous[current]
                path.reverse()
                return path, distances[dest]

            # Explorar vecinos
            for v, weight in self.graph.get_neighbors(u):
                # Verificar si la arista está excluida
                if (u, v) in excluded_edges:
                    continue

                new_dist = distances[u] + weight

                if new_dist < distances[v]:
                    distances[v] = new_dist
                    previous[v] = u
                    heapq.heappush(pq, (new_dist, v))

        # No se encontró camino
        return None, np.inf

    def find_k_shortest_paths(self, source: int, dest: int, k: int) -> List[Tuple[List[int], float]]:
        """
        Encuentra los K caminos más cortos usando el algoritmo de Yen.

        Args:
            source: Nodo origen
            dest: Nodo destino
            k: Número de caminos más cortos a encontrar

        Returns:
            Lista de tuplas (camino, costo) ordenadas por costo
        """
        if source < 0 or source >= self.num_nodes or dest < 0 or dest >= self.num_nodes:
            return []

        if source == dest:
            return [([source], 0)]

        # A: lista de k caminos más cortos
        A = []

        # B: lista de caminos candidatos (heap) - usando tuplas para hashear
        B = []
        # Set para verificación rápida de duplicados
        B_set = set()

        # Encontrar el primer camino más corto
        first_path, first_cost = self.dijkstra(source, dest)

        if first_path is None:
            return []  # No hay camino

        A.append((first_path, first_cost))

        # Encontrar k-1 caminos adicionales
        for k_iter in range(1, k):
            if not A:
                break

            # El último camino encontrado
            prev_path, _ = A[-1]

            # Para cada nodo en el camino anterior (excepto el último)
            for i in range(len(prev_path) - 1):
                # Spur node: nodo donde se desviará el camino
                spur_node = prev_path[i]
                # Root path: parte del camino desde source hasta spur_node
                root_path = prev_path[:i + 1]

                # Aristas a excluir
                excluded_edges = set()

                # Excluir aristas que forman caminos similares encontrados previamente
                for path, _ in A:
                    if len(path) > i and path[:i + 1] == root_path:
                        if i + 1 < len(path):
                            excluded_edges.add((path[i], path[i + 1]))

                # También excluir aristas ya exploradas en B
                for cost, path_tuple in B:
                    path = list(path_tuple)
                    if len(path) > i and path[:i + 1] == root_path:
                        if i + 1 < len(path):
                            excluded_edges.add((path[i], path[i + 1]))

                # Encontrar el camino más corto desde spur_node hasta dest
                spur_path, spur_cost = self.dijkstra(spur_node, dest, excluded_edges)

                if spur_path is not None:
                    # Combinar root_path con spur_path
                    total_path = root_path[:-1] + spur_path

                    # Calcular costo total
                    total_cost = 0
                    for j in range(len(total_path) - 1):
                        total_cost += self.graph.get_weight(total_path[j], total_path[j + 1])

                    # Convertir a tupla para usar como clave
                    path_tuple = tuple(total_path)

                    # Agregar a candidatos si no existe
                    if path_tuple not in B_set:
                        # Verificar que no esté en A
                        path_in_A = any(tuple(p) == path_tuple for p, _ in A)
                        if not path_in_A:
                            heapq.heappush(B, (total_cost, path_tuple))
                            B_set.add(path_tuple)

            # Si no hay más candidatos, terminar
            if not B:
                break

            # Seleccionar el mejor candidato
            best_cost, best_path_tuple = heapq.heappop(B)
            best_path = list(best_path_tuple)
            B_set.discard(best_path_tuple)

            A.append((best_path, best_cost))

        return A

    def generate_k_paths_matrix(self, k: int = 2) -> Dict[str, np.ndarray]:
        """
        Genera matrices de k-paths para todos los pares de nodos.

        Args:
            k: Número de caminos más cortos (2 o 3)

        Returns:
            Diccionario con matrices:
            - 'path_1': Matriz con costos del camino más corto
            - 'path_2': Matriz con costos del segundo camino más corto
            - 'path_3': Matriz con costos del tercer camino más corto (si k=3)
            - 'adjacency': Matriz de adyacencia original
        """
        matrices = {
            'adjacency': self.graph.get_adjacency_matrix(),
            'path_1': np.full((self.num_nodes, self.num_nodes), np.inf),
            'path_2': np.full((self.num_nodes, self.num_nodes), np.inf)
        }

        if k >= 3:
            matrices['path_3'] = np.full((self.num_nodes, self.num_nodes), np.inf)

        # Calcular k-paths para cada par de nodos
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i == j:
                    matrices['path_1'][i][j] = 0
                    matrices['path_2'][i][j] = 0
                    if k >= 3:
                        matrices['path_3'][i][j] = 0
                    continue

                paths = self.find_k_shortest_paths(i, j, k)

                # Llenar las matrices según los caminos encontrados
                for idx, (path, cost) in enumerate(paths):
                    if idx == 0:
                        matrices['path_1'][i][j] = cost
                    elif idx == 1:
                        matrices['path_2'][i][j] = cost
                    elif idx == 2 and k >= 3:
                        matrices['path_3'][i][j] = cost

        return matrices

    def get_path_details(self, source: int, dest: int, k: int = 2) -> List[Dict]:
        """
        Obtiene detalles completos de los k-paths entre dos nodos.

        Args:
            source: Nodo origen
            dest: Nodo destino
            k: Número de caminos

        Returns:
            Lista de diccionarios con información de cada camino:
            - 'path': Lista de nodos
            - 'cost': Costo total
            - 'edges': Lista de aristas con pesos
        """
        paths = self.find_k_shortest_paths(source, dest, k)
        details = []

        for path, cost in paths:
            edges = []
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                weight = self.graph.get_weight(u, v)
                edges.append((u, v, weight))

            details.append({
                'path': path,
                'cost': cost,
                'edges': edges
            })

        return details

    @staticmethod
    def format_matrix(matrix: np.ndarray, title: str = "Matriz") -> str:
        """
        Formatea una matriz para visualización.

        Args:
            matrix: Matriz a formatear
            title: Título de la matriz

        Returns:
            String formateado de la matriz
        """
        result = f"\n{title}:\n"
        result += "-" * 50 + "\n"

        display_matrix = np.where(matrix == np.inf, -1, matrix)

        for row in display_matrix:
            row_str = " ".join([f"{val:6.1f}" if val != -1 else "   inf" for val in row])
            result += row_str + "\n"

        return result