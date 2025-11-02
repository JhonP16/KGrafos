"""
Paquete UI para la aplicación K-Shortest Paths.
"""

from .main_window import MainWindow
from .graph_canvas import GraphCanvas
from .styles import DARK_THEME, PATH_COLORS, GRAPH_STYLE

__all__ = ['MainWindow', 'GraphCanvas', 'DARK_THEME', 'PATH_COLORS', 'GRAPH_STYLE']