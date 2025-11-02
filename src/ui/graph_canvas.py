"""
Canvas para visualización de grafos usando matplotlib.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import networkx as nx
import numpy as np
import sys
import os


from ui.styles import PATH_COLORS, GRAPH_STYLE

class GraphCanvas(QWidget):
    """Widget que contiene el canvas de matplotlib para dibujar grafos"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.graph = None
        self.nx_graph = None
        self.pos = None
        self.highlighted_paths = []

        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz del canvas"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Crear figura de matplotlib
        self.figure = Figure(figsize=(10, 8), facecolor=GRAPH_STYLE['background_color'])
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Toolbar de navegación (zoom, pan, etc.)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # Configurar el ax
        self.setup_axes()
        self.draw_empty_message()

    def setup_axes(self):
        """Configura los ejes del gráfico"""
        self.ax.clear()
        self.ax.set_facecolor(GRAPH_STYLE['background_color'])
        self.ax.axis('off')
        self.ax.set_aspect('equal')

    def draw_empty_message(self):
        """Dibuja un mensaje cuando no hay grafo"""
        self.setup_axes()
        self.ax.text(
            0.5, 0.5,
            '📊\n\nGenera un grafo para comenzar',
            transform=self.ax.transAxes,
            ha='center',
            va='center',
            fontsize=16,
            color=GRAPH_STYLE['text_color'],
            style='italic'
        )
        self.canvas.draw()

    def draw_graph(self, graph, highlight_paths=None):
        """
        Dibuja el grafo en el canvas.

        Args:
            graph: Instancia de Graph
            highlight_paths: Lista de tuplas (camino, costo) para resaltar
        """
        self.graph = graph
        self.highlighted_paths = highlight_paths if highlight_paths else []

        self.setup_axes()

        # Convertir a networkx
        self.nx_graph = nx.DiGraph()

        for i in range(graph.num_nodes):
            self.nx_graph.add_node(i)

        for i, j, weight in graph.get_edge_list():
            self.nx_graph.add_edge(i, j, weight=weight)

        # Calcular posiciones usando spring layout
        self.pos = nx.spring_layout(
            self.nx_graph,
            k=2,
            iterations=50,
            seed=42
        )

        # Dibujar aristas normales
        self._draw_edges()

        # Dibujar caminos resaltados si existen
        if self.highlighted_paths:
            self._draw_highlighted_paths()

        # Dibujar nodos
        self._draw_nodes()

        # Dibujar etiquetas
        self._draw_labels()

        # Dibujar leyenda si hay caminos resaltados
        if self.highlighted_paths:
            self._draw_legend()

        self.canvas.draw()

    def _draw_edges(self):
        """Dibuja las aristas del grafo"""
        nx.draw_networkx_edges(
            self.nx_graph,
            self.pos,
            ax=self.ax,
            edge_color=GRAPH_STYLE['edge_color'],
            width=1.5,
            alpha=0.4,
            arrows=True,
            arrowsize=15,
            arrowstyle='->',
            connectionstyle='arc3,rad=0.1',
            node_size=800
        )

        # Dibujar pesos de las aristas
        edge_labels = nx.get_edge_attributes(self.nx_graph, 'weight')
        edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}

        nx.draw_networkx_edge_labels(
            self.nx_graph,
            self.pos,
            edge_labels,
            ax=self.ax,
            font_size=8,
            font_color=GRAPH_STYLE['text_color'],
            bbox=dict(
                boxstyle='round,pad=0.3',
                facecolor=GRAPH_STYLE['background_color'],
                edgecolor=GRAPH_STYLE['edge_color'],
                alpha=0.7
            )
        )

    def _draw_highlighted_paths(self):
        """Dibuja los caminos resaltados con diferentes colores"""
        for idx, (path, cost) in enumerate(self.highlighted_paths):
            if len(path) < 2:
                continue

            color = PATH_COLORS[idx % len(PATH_COLORS)]

            # Crear lista de aristas del camino
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

            # Dibujar aristas del camino
            nx.draw_networkx_edges(
                self.nx_graph,
                self.pos,
                edgelist=path_edges,
                ax=self.ax,
                edge_color=color,
                width=3.5,
                alpha=0.9,
                arrows=True,
                arrowsize=20,
                arrowstyle='-|>',
                connectionstyle='arc3,rad=0.1',
                node_size=800
            )

    def _draw_nodes(self):
        """Dibuja los nodos del grafo"""
        # Nodos normales
        nx.draw_networkx_nodes(
            self.nx_graph,
            self.pos,
            ax=self.ax,
            node_color=GRAPH_STYLE['node_color'],
            node_size=800,
            edgecolors=GRAPH_STYLE['node_edge_color'],
            linewidths=2.5
        )

        # Si hay caminos resaltados, destacar nodos origen y destino
        if self.highlighted_paths and len(self.highlighted_paths) > 0:
            first_path = self.highlighted_paths[0][0]
            if len(first_path) >= 2:
                # Nodo origen
                nx.draw_networkx_nodes(
                    self.nx_graph,
                    self.pos,
                    nodelist=[first_path[0]],
                    ax=self.ax,
                    node_color='#a6e3a1',
                    node_size=900,
                    edgecolors='#89b4fa',
                    linewidths=3
                )

                # Nodo destino
                nx.draw_networkx_nodes(
                    self.nx_graph,
                    self.pos,
                    nodelist=[first_path[-1]],
                    ax=self.ax,
                    node_color='#f38ba8',
                    node_size=900,
                    edgecolors='#89b4fa',
                    linewidths=3
                )

    def _draw_labels(self):
        """Dibuja las etiquetas de los nodos"""
        nx.draw_networkx_labels(
            self.nx_graph,
            self.pos,
            ax=self.ax,
            font_size=12,
            font_weight='bold',
            font_color='#cdd6f4'
        )

    def _draw_legend(self):
        """Dibuja la leyenda de los caminos"""
        legend_elements = []

        for idx, (path, cost) in enumerate(self.highlighted_paths):
            color = PATH_COLORS[idx % len(PATH_COLORS)]
            path_str = ' → '.join(map(str, path))
            label = f"Camino {idx + 1}: {path_str} (costo: {cost:.1f})"

            legend_elements.append(
                self.ax.plot(
                    [], [],
                    color=color,
                    linewidth=3,
                    label=label
                )[0]
            )

        self.ax.legend(
            handles=legend_elements,
            loc='upper left',
            fontsize=9,
            facecolor=GRAPH_STYLE['background_color'],
            edgecolor=GRAPH_STYLE['node_edge_color'],
            labelcolor=GRAPH_STYLE['text_color'],
            framealpha=0.9
        )

    def highlight_paths(self, paths):
        """
        Resalta los caminos especificados en el grafo.

        Args:
            paths: Lista de tuplas (camino, costo)
        """
        if self.graph is None:
            return

        self.highlighted_paths = paths
        self.draw_graph(self.graph, paths)

    def clear(self):
        """Limpia el canvas"""
        self.graph = None
        self.nx_graph = None
        self.pos = None
        self.highlighted_paths = []
        self.draw_empty_message()

    def export_image(self, filename):
        """
        Exporta el gráfico actual a un archivo de imagen.

        Args:
            filename: Ruta del archivo a guardar
        """
        self.figure.savefig(
            filename,
            dpi=300,
            bbox_inches='tight',
            facecolor=GRAPH_STYLE['background_color'],
            edgecolor='none'
        )