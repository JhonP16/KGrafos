"""
Punto de entrada principal de la aplicación K-Shortest Paths.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from ui.styles import DARK_THEME


def main():
    """Función principal de la aplicación"""
    app = QApplication(sys.argv)

    # Aplicar tema oscuro
    app.setStyleSheet(DARK_THEME)

    # Configurar nombre de la aplicación
    app.setApplicationName("K-Shortest Paths Visualizer")
    app.setOrganizationName("EAFIT - Algoritmos y Estructuras de Datos")

    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()