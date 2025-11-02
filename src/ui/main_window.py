"""
Ventana principal de la aplicación K-Shortest Paths.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QSpinBox, QSlider, QComboBox,
                             QGroupBox, QRadioButton, QTextEdit, QTabWidget,
                             QTableWidget, QTableWidgetItem, QSplitter, QMessageBox,
                             QProgressBar, QStatusBar, QFileDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import sys
import os


from graph import Graph
from k_paths_algorithm import KShortestPaths
from ui.graph_canvas import GraphCanvas
import numpy as np


class CalculationThread(QThread):
    """Thread para cálculos pesados sin bloquear la UI"""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, graph, k_value):
        super().__init__()
        self.graph = graph
        self.k_value = k_value

    def run(self):
        try:
            k_paths = KShortestPaths(self.graph)
            self.progress.emit(30)

            matrices = k_paths.generate_k_paths_matrix(k=self.k_value)
            self.progress.emit(70)

            result = {
                'matrices': matrices,
                'k_paths': k_paths
            }

            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""

    def __init__(self):
        super().__init__()
        self.graph = None
        self.k_paths = None
        self.current_k = 2
        self.matrices = None

        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("K-Shortest Paths Algorithm Visualizer")
        self.setGeometry(100, 100, 1400, 900)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Splitter para dividir la ventana
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo (controles)
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)

        # Panel derecho (visualización y resultados)
        right_panel = self.create_visualization_panel()
        splitter.addWidget(right_panel)

        # Proporciones del splitter (30% - 70%)
        splitter.setStretchFactor(0, 30)
        splitter.setStretchFactor(1, 70)

        main_layout.addWidget(splitter)

        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo para comenzar")

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def create_control_panel(self):
        """Crea el panel de controles"""
        panel = QWidget()
        panel.setMinimumWidth(350)
        panel.setMaximumWidth(450)
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Título
        title = QLabel("K-Shortest Paths")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # ===== Configuración del Grafo =====
        graph_group = QGroupBox("Configuración del Grafo")
        graph_layout = QVBoxLayout()

        # Número de nodos
        nodes_layout = QHBoxLayout()
        nodes_layout.addWidget(QLabel("Número de Nodos:"))
        self.nodes_spin = QSpinBox()
        self.nodes_spin.setRange(3, 20)
        self.nodes_spin.setValue(6)
        self.nodes_spin.setToolTip("Cantidad de nodos en el grafo (3-20)")
        nodes_layout.addWidget(self.nodes_spin)
        graph_layout.addLayout(nodes_layout)

        # Densidad del grafo
        density_layout = QVBoxLayout()
        density_label_layout = QHBoxLayout()
        density_label_layout.addWidget(QLabel("Densidad:"))
        self.density_value_label = QLabel("30%")
        density_label_layout.addWidget(self.density_value_label)
        density_label_layout.addStretch()
        density_layout.addLayout(density_label_layout)

        self.density_slider = QSlider(Qt.Orientation.Horizontal)
        self.density_slider.setRange(10, 80)
        self.density_slider.setValue(30)
        self.density_slider.setToolTip("Probabilidad de conexión entre nodos")
        self.density_slider.valueChanged.connect(
            lambda v: self.density_value_label.setText(f"{v}%")
        )
        density_layout.addWidget(self.density_slider)
        graph_layout.addLayout(density_layout)

        # Botón generar grafo
        self.generate_btn = QPushButton("🔄 Generar Grafo Aleatorio")
        self.generate_btn.setObjectName("primaryButton")
        self.generate_btn.clicked.connect(self.generate_random_graph)
        graph_layout.addWidget(self.generate_btn)

        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        # ===== Selección de Caminos =====
        path_group = QGroupBox("Cálculo de K-Paths")
        path_layout = QVBoxLayout()

        # Nodo origen
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Nodo Origen:"))
        self.source_combo = QComboBox()
        self.source_combo.setEnabled(False)
        source_layout.addWidget(self.source_combo)
        path_layout.addLayout(source_layout)

        # Nodo destino
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Nodo Destino:"))
        self.dest_combo = QComboBox()
        self.dest_combo.setEnabled(False)
        dest_layout.addWidget(self.dest_combo)
        path_layout.addLayout(dest_layout)

        # Selector de K
        k_label = QLabel("Valor de K:")
        k_label.setObjectName("sectionLabel")
        path_layout.addWidget(k_label)

        self.k2_radio = QRadioButton("K = 2 (2 caminos más cortos)")
        self.k2_radio.setChecked(True)
        self.k2_radio.toggled.connect(lambda: self.set_k_value(2))
        path_layout.addWidget(self.k2_radio)

        self.k3_radio = QRadioButton("K = 3 (3 caminos más cortos)")
        self.k3_radio.toggled.connect(lambda: self.set_k_value(3))
        path_layout.addWidget(self.k3_radio)

        # Botón calcular
        self.calculate_btn = QPushButton("⚡ Calcular K-Paths")
        self.calculate_btn.setObjectName("successButton")
        self.calculate_btn.setEnabled(False)
        self.calculate_btn.clicked.connect(self.calculate_k_paths)
        path_layout.addWidget(self.calculate_btn)

        path_group.setLayout(path_layout)
        layout.addWidget(path_group)

        # ===== Acciones =====
        actions_group = QGroupBox("Acciones")
        actions_layout = QVBoxLayout()

        self.export_btn = QPushButton("💾 Exportar Resultados")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_results)
        actions_layout.addWidget(self.export_btn)

        self.clear_btn = QPushButton("🗑️ Limpiar Todo")
        self.clear_btn.setObjectName("dangerButton")
        self.clear_btn.clicked.connect(self.clear_all)
        actions_layout.addWidget(self.clear_btn)

        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

        # Espacio flexible
        layout.addStretch()

        # Información
        info_label = QLabel("💡 Tip: Genera un grafo\npara comenzar")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: #a6e3a1; font-style: italic;")
        layout.addWidget(info_label)

        return panel

    def create_visualization_panel(self):
        """Crea el panel de visualización y resultados"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        # Tabs para diferentes vistas
        self.tab_widget = QTabWidget()

        # Tab 1: Visualización del grafo
        self.graph_canvas = GraphCanvas()
        self.tab_widget.addTab(self.graph_canvas, "📊 Visualización del Grafo")

        # Tab 2: Matrices
        matrices_widget = QWidget()
        matrices_layout = QVBoxLayout(matrices_widget)
        self.matrices_text = QTextEdit()
        self.matrices_text.setReadOnly(True)
        self.matrices_text.setPlaceholderText(
            "Las matrices aparecerán aquí después de calcular los K-paths..."
        )
        matrices_layout.addWidget(self.matrices_text)
        self.tab_widget.addTab(matrices_widget, "🔢 Matrices K-Paths")

        # Tab 3: Detalles de caminos
        paths_widget = QWidget()
        paths_layout = QVBoxLayout(paths_widget)
        self.paths_text = QTextEdit()
        self.paths_text.setReadOnly(True)
        self.paths_text.setPlaceholderText(
            "Los detalles de los caminos aparecerán aquí..."
        )
        paths_layout.addWidget(self.paths_text)
        self.tab_widget.addTab(paths_widget, "🛣️ Detalles de Caminos")

        layout.addWidget(self.tab_widget)

        return panel

    def set_k_value(self, k):
        """Establece el valor de K"""
        self.current_k = k
        self.status_bar.showMessage(f"Valor de K cambiado a {k}")

    def generate_random_graph(self):
        """Genera un grafo aleatorio"""
        try:
            num_nodes = self.nodes_spin.value()
            density = self.density_slider.value() / 100.0

            self.status_bar.showMessage("Generando grafo...")

            self.graph = Graph.generate_random_graph(
                num_nodes=num_nodes,
                density=density,
                min_weight=1,
                max_weight=10,
                ensure_connected=True
            )

            # Actualizar combos de nodos
            self.source_combo.clear()
            self.dest_combo.clear()
            for i in range(num_nodes):
                self.source_combo.addItem(f"Nodo {i}", i)
                self.dest_combo.addItem(f"Nodo {i}", i)

            self.source_combo.setEnabled(True)
            self.dest_combo.setEnabled(True)
            self.dest_combo.setCurrentIndex(min(num_nodes - 1, 1))
            self.calculate_btn.setEnabled(True)

            # Visualizar grafo
            self.graph_canvas.draw_graph(self.graph)

            # Limpiar resultados anteriores
            self.matrices_text.clear()
            self.paths_text.clear()
            self.matrices = None
            self.export_btn.setEnabled(False)

            num_edges = len(self.graph.get_edge_list())
            self.status_bar.showMessage(
                f"Grafo generado: {num_nodes} nodos, {num_edges} aristas"
            )

            QMessageBox.information(
                self,
                "Grafo Generado",
                f"Grafo creado exitosamente con:\n"
                f"• {num_nodes} nodos\n"
                f"• {num_edges} aristas\n"
                f"• Densidad: {int(density*100)}%"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar grafo:\n{str(e)}")
            self.status_bar.showMessage("Error al generar grafo")

    def calculate_k_paths(self):
        """Calcula los K-paths del grafo"""
        if self.graph is None:
            QMessageBox.warning(self, "Advertencia", "Primero genera un grafo")
            return

        # Deshabilitar botones durante el cálculo
        self.calculate_btn.setEnabled(False)
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage("Calculando K-paths...")

        # Crear y ejecutar thread
        self.calc_thread = CalculationThread(self.graph, self.current_k)
        self.calc_thread.finished.connect(self.on_calculation_finished)
        self.calc_thread.progress.connect(self.progress_bar.setValue)
        self.calc_thread.error.connect(self.on_calculation_error)
        self.calc_thread.start()

    def on_calculation_finished(self, result):
        """Callback cuando el cálculo termina"""
        self.matrices = result['matrices']
        self.k_paths = result['k_paths']

        # Mostrar matrices
        self.display_matrices()

        # Mostrar detalles de caminos específicos
        source = self.source_combo.currentData()
        dest = self.dest_combo.currentData()
        self.display_path_details(source, dest)

        # Visualizar caminos en el grafo
        paths = self.k_paths.find_k_shortest_paths(source, dest, self.current_k)
        self.graph_canvas.highlight_paths(paths)

        # Habilitar exportación
        self.export_btn.setEnabled(True)

        # Restaurar UI
        self.calculate_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"K-paths calculados exitosamente (K={self.current_k})")

        QMessageBox.information(
            self,
            "Cálculo Completo",
            f"K-paths calculados exitosamente!\n"
            f"K = {self.current_k}\n"
            f"Caminos encontrados: {len(paths)}"
        )

    def on_calculation_error(self, error_msg):
        """Callback cuando hay un error en el cálculo"""
        QMessageBox.critical(self, "Error", f"Error al calcular K-paths:\n{error_msg}")
        self.calculate_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Error en el cálculo")

    def display_matrices(self):
        """Muestra las matrices en el tab correspondiente"""
        if self.matrices is None:
            return

        text = "=" * 80 + "\n"
        text += f"MATRICES K-SHORTEST PATHS (K = {self.current_k})\n"
        text += "=" * 80 + "\n\n"

        text += KShortestPaths.format_matrix(
            self.matrices['adjacency'],
            "Matriz de Adyacencia Original"
        )
        text += "\n"

        text += KShortestPaths.format_matrix(
            self.matrices['path_1'],
            "Matriz del 1er Camino Más Corto (K=1)"
        )
        text += "\n"

        text += KShortestPaths.format_matrix(
            self.matrices['path_2'],
            "Matriz del 2do Camino Más Corto (K=2)"
        )
        text += "\n"

        if 'path_3' in self.matrices:
            text += KShortestPaths.format_matrix(
                self.matrices['path_3'],
                "Matriz del 3er Camino Más Corto (K=3)"
            )

        self.matrices_text.setText(text)

    def display_path_details(self, source, dest):
        """Muestra los detalles de los caminos entre dos nodos"""
        if self.k_paths is None:
            return

        details = self.k_paths.get_path_details(source, dest, self.current_k)

        text = "=" * 80 + "\n"
        text += f"DETALLES DE CAMINOS: Nodo {source} → Nodo {dest}\n"
        text += "=" * 80 + "\n\n"

        if not details:
            text += "❌ No se encontraron caminos entre estos nodos.\n"
        else:
            for i, detail in enumerate(details, 1):
                text += f"{'='*60}\n"
                text += f"CAMINO #{i}\n"
                text += f"{'='*60}\n"
                text += f"Secuencia de nodos: {' → '.join(map(str, detail['path']))}\n"
                text += f"Costo total: {detail['cost']:.2f}\n\n"
                text += "Aristas del camino:\n"
                for j, (u, v, weight) in enumerate(detail['edges'], 1):
                    text += f"  {j}. Nodo {u} → Nodo {v}  (peso: {weight:.2f})\n"
                text += "\n"

        self.paths_text.setText(text)

    def export_results(self):
        """Exporta los resultados a un archivo de texto"""
        if self.matrices is None:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Resultados",
            f"k_paths_results_k{self.current_k}.txt",
            "Text Files (*.txt)"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.matrices_text.toPlainText())
                    f.write("\n\n")
                    f.write(self.paths_text.toPlainText())

                QMessageBox.information(
                    self,
                    "Exportación Exitosa",
                    f"Resultados guardados en:\n{filename}"
                )
                self.status_bar.showMessage(f"Resultados exportados a {filename}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error al exportar:\n{str(e)}"
                )

    def clear_all(self):
        """Limpia todos los datos y reinicia la aplicación"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "¿Estás seguro de que quieres limpiar todo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.graph = None
            self.k_paths = None
            self.matrices = None

            self.source_combo.clear()
            self.dest_combo.clear()
            self.source_combo.setEnabled(False)
            self.dest_combo.setEnabled(False)
            self.calculate_btn.setEnabled(False)
            self.export_btn.setEnabled(False)

            self.graph_canvas.clear()
            self.matrices_text.clear()
            self.paths_text.clear()

            self.status_bar.showMessage("Todo limpiado - Listo para comenzar")