"""
Estilos modernos para la aplicación K-Shortest Paths.
Tema oscuro con acentos en azul y verde.
"""

DARK_THEME = """
/* ===== Variables Globales ===== */
* {
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* ===== Ventana Principal ===== */
QMainWindow {
    background-color: #1e1e2e;
}

/* ===== Widgets Generales ===== */
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
}

/* ===== Etiquetas ===== */
QLabel {
    color: #cdd6f4;
    font-size: 13px;
    padding: 5px;
}

QLabel#titleLabel {
    font-size: 24px;
    font-weight: bold;
    color: #89b4fa;
    padding: 15px;
}

QLabel#sectionLabel {
    font-size: 16px;
    font-weight: bold;
    color: #a6e3a1;
    padding: 10px 5px;
    border-bottom: 2px solid #45475a;
}

/* ===== Botones ===== */
QPushButton {
    background-color: #45475a;
    color: #cdd6f4;
    border: 2px solid #585b70;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #585b70;
    border: 2px solid #89b4fa;
}

QPushButton:pressed {
    background-color: #313244;
    border: 2px solid #74c7ec;
}

QPushButton:disabled {
    background-color: #313244;
    color: #6c7086;
    border: 2px solid #45475a;
}

QPushButton#primaryButton {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: none;
}

QPushButton#primaryButton:hover {
    background-color: #74c7ec;
}

QPushButton#primaryButton:pressed {
    background-color: #89dceb;
}

QPushButton#successButton {
    background-color: #a6e3a1;
    color: #1e1e2e;
    border: none;
}

QPushButton#successButton:hover {
    background-color: #94e2d5;
}

QPushButton#dangerButton {
    background-color: #f38ba8;
    color: #1e1e2e;
    border: none;
}

QPushButton#dangerButton:hover {
    background-color: #eba0ac;
}

/* ===== Spinbox y ComboBox ===== */
QSpinBox, QComboBox {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    font-size: 13px;
}

QSpinBox:hover, QComboBox:hover {
    border: 2px solid #89b4fa;
}

QSpinBox:focus, QComboBox:focus {
    border: 2px solid #74c7ec;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #45475a;
    border: none;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #585b70;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #cdd6f4;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #313244;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
    border: 2px solid #45475a;
}

/* ===== Slider ===== */
QSlider::groove:horizontal {
    background: #313244;
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #89b4fa;
    width: 20px;
    height: 20px;
    margin: -6px 0;
    border-radius: 10px;
}

QSlider::handle:horizontal:hover {
    background: #74c7ec;
}

QSlider::sub-page:horizontal {
    background: #89b4fa;
    border-radius: 4px;
}

/* ===== Radio Buttons ===== */
QRadioButton {
    color: #cdd6f4;
    spacing: 10px;
    font-size: 13px;
}

QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid #585b70;
    background-color: #313244;
}

QRadioButton::indicator:hover {
    border: 2px solid #89b4fa;
}

QRadioButton::indicator:checked {
    background-color: #89b4fa;
    border: 2px solid #89b4fa;
}

/* ===== Group Box ===== */
QGroupBox {
    background-color: #181825;
    border: 2px solid #45475a;
    border-radius: 10px;
    margin-top: 20px;
    padding: 15px;
    font-weight: bold;
    color: #cdd6f4;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 15px;
    background-color: #89b4fa;
    color: #1e1e2e;
    border-radius: 5px;
    left: 10px;
}

/* ===== Scroll Area ===== */
QScrollArea {
    background-color: #181825;
    border: 2px solid #45475a;
    border-radius: 8px;
}

QScrollBar:vertical {
    background: #313244;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #585b70;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #6c7086;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ===== Table Widget ===== */
QTableWidget {
    background-color: #181825;
    alternate-background-color: #1e1e2e;
    border: 2px solid #45475a;
    border-radius: 8px;
    gridline-color: #45475a;
    color: #cdd6f4;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QHeaderView::section {
    background-color: #313244;
    color: #cdd6f4;
    padding: 10px;
    border: none;
    border-right: 1px solid #45475a;
    border-bottom: 2px solid #45475a;
    font-weight: bold;
}

QHeaderView::section:hover {
    background-color: #45475a;
}

/* ===== Tab Widget ===== */
QTabWidget::pane {
    border: 2px solid #45475a;
    border-radius: 8px;
    background-color: #181825;
    top: -2px;
}

QTabBar::tab {
    background-color: #313244;
    color: #cdd6f4;
    padding: 12px 24px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 5px;
}

QTabBar::tab:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QTabBar::tab:hover:!selected {
    background-color: #45475a;
}

/* ===== Text Edit ===== */
QTextEdit, QPlainTextEdit {
    background-color: #181825;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #89b4fa;
}

/* ===== Progress Bar ===== */
QProgressBar {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 8px;
    text-align: center;
    color: #cdd6f4;
    height: 25px;
}

QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 6px;
}

/* ===== Status Bar ===== */
QStatusBar {
    background-color: #181825;
    color: #cdd6f4;
    border-top: 2px solid #45475a;
}

/* ===== Tooltips ===== */
QToolTip {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #89b4fa;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
}

/* ===== Separadores ===== */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #45475a;
    background-color: #45475a;
}

/* ===== Menu Bar ===== */
QMenuBar {
    background-color: #181825;
    color: #cdd6f4;
    border-bottom: 2px solid #45475a;
}

QMenuBar::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QMenu {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
}

QMenu::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}
"""

# Colores para los caminos en la visualización
PATH_COLORS = [
    '#89b4fa',  # Azul - Primer camino
    '#a6e3a1',  # Verde - Segundo camino
    '#f9e2af',  # Amarillo - Tercer camino
    '#f38ba8',  # Rosa - Caminos adicionales
    '#cba6f7',  # Púrpura
]

# Configuración de la visualización
GRAPH_STYLE = {
    'node_color': '#45475a',
    'node_edge_color': '#89b4fa',
    'edge_color': '#6c7086',
    'background_color': '#1e1e2e',
    'text_color': '#cdd6f4',
    'highlight_color': '#89b4fa',
}