# K-Shortest Paths Algorithm Visualizer

Implementación del algoritmo K-Shortest Paths con interfaz gráfica moderna desarrollada en PyQt6.

## 👥 Equipo de Desarrollo

- **Jhon Jairo Pulgarin Restrepo**
- **Pablo José Benítez ** - [email2@eafit.edu.co]
- **Yesid Hurtado Montoya** - [email3@eafit.edu.co]

## 📝 Descripción

Esta aplicación implementa el algoritmo de Yen para encontrar los K caminos más cortos en grafos dirigidos ponderados. Permite generar grafos aleatorios con densidad configurable y visualizar interactivamente los caminos calculados, junto con las matrices de distancias correspondientes para K=2 y K=3.

## ✨ Características

- 🔄 Generación de grafos aleatorios con densidad ajustable
- 📊 Visualización interactiva de grafos usando NetworkX y Matplotlib
- ⚡ Cálculo eficiente de K-paths usando el algoritmo de Yen
- 🔢 Generación automática de matrices de K-paths
- 🎨 Interfaz gráfica moderna con tema oscuro
- 💾 Exportación de resultados a archivos de texto
- 🛣️ Visualización detallada de caminos con sus costos
- 🎯 Selección flexible de nodos origen y destino

## 🛠️ Requisitos

- Python 3.8 o superior
- PyQt6
- NetworkX
- Matplotlib
- NumPy

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/KGrafos.git
cd KGrafos
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

## 🚀 Ejecución

### Ejecutar la aplicación

```bash
python src/main.py
```

## 📖 Uso de la Aplicación

### 1. Generar un Grafo

1. Ajusta el número de nodos (3-20)
2. Configura la densidad del grafo (10%-80%)
3. Haz clic en "🔄 Generar Grafo Aleatorio"

### 2. Calcular K-Paths

1. Selecciona el nodo origen y destino
2. Elige el valor de K (2 o 3 caminos)
3. Haz clic en "⚡ Calcular K-Paths"

### 3. Visualizar Resultados

- **Tab "Visualización del Grafo"**: Muestra el grafo con los caminos resaltados en diferentes colores
- **Tab "Matrices K-Paths"**: Muestra las matrices de adyacencia y de K-paths
- **Tab "Detalles de Caminos"**: Lista detallada de cada camino con sus aristas y costos

### 4. Exportar Resultados

Haz clic en "💾 Exportar Resultados" para guardar las matrices y detalles en un archivo de texto.

## 📊 Ejemplos de Entrada/Salida

### Ejemplo 1: Grafo Simple (5 nodos)

**Entrada:**
```
Nodos: 5
Densidad: 40%
Origen: 0
Destino: 4
K: 2
```

**Salida:**
```
Camino 1: 0 → 1 → 2 → 4 | Costo: 6.0
Camino 2: 0 → 1 → 3 → 4 | Costo: 7.0

Matriz del 1er Camino Más Corto:
    0.0    2.0    3.0    6.0    6.0
    inf    0.0    1.0    4.0    4.0
    inf    inf    0.0    2.0    3.0
    inf    inf    inf    0.0    1.0
    inf    inf    inf    inf    0.0
```

### Ejemplo 2: Grafo Mediano (10 nodos)

**Entrada:**
```
Nodos: 10
Densidad: 30%
Origen: 0
Destino: 9
K: 3
```

**Salida:**
```
Camino 1: 0 → 2 → 5 → 9 | Costo: 12.0
Camino 2: 0 → 3 → 7 → 9 | Costo: 15.0
Camino 3: 0 → 1 → 4 → 8 → 9 | Costo: 18.0
```

## 🏗️ Estructura del Proyecto

```
k-shortest-paths/
├── src/
│   ├── main.py                 # Punto de entrada
│   ├── graph.py                # Clase Graph
│   ├── k_paths_algorithm.py    # Algoritmo K-Paths
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py      # Ventana principal
│       ├── graph_canvas.py     # Canvas de visualización
│       └── styles.py           # Estilos QSS
├── README.md                   # Este archivo
```

## 🔬 Algoritmo Implementado

### Algoritmo de Yen

El algoritmo de Yen encuentra los K caminos más cortos sin ciclos en un grafo dirigido ponderado.

**Complejidad:** O(K × N × (M + N log N))
- K: número de caminos
- N: número de nodos
- M: número de aristas

**Características:**
- Encuentra caminos sin ciclos
- Garantiza los K caminos más cortos en orden
- Eficiente para valores pequeños de K (2-3)

## 🎓 Referencias

- Yen, J. Y. (1971). "Finding the k shortest loopless paths in a network". Management Science, 17(11), 712-716.
- NetworkX Documentation: https://networkx.org/
- PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- AI to fix Errors

---

