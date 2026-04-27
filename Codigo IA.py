"""
Pipeline de Machine Learning End-to-End
=======================================
Autor: Senior Machine Learning Engineer

DESCRIPCIÓN DE LA SOLUCIÓN:
Este script implementa un pipeline completo y modular de Machine Learning.
Dado que no se proporcionaron archivos físicos (CSV o PDF), el código está diseñado 
para ser funcional simulando el entorno mediante el dataset 'Breast Cancer' de sklearn 
(convirtiéndolo a un DataFrame estructurado como si proviniera de un CSV) e imputando
ruido para demostrar la limpieza de datos.

1. INTERPRETACIÓN DEL PDF (Modelo 1):
   - Suposición: El documento PDF solicitaba un "modelo lineal, altamente interpretable, 
     capaz de realizar selección de características intrínseca para un problema binario".
   - Decisión: Se implementa una Regresión Logística con regularización L1 (Lasso). 
   - Justificación: La regularización L1 fuerza a cero los coeficientes de las 
     características menos importantes, cumpliendo con la "selección intrínseca" y 
     manteniendo una alta interpretabilidad.

2. SELECCIÓN DEL SEGUNDO MODELO (Modelo 2):
   - Elección: Random Forest Classifier.
   - Justificación conceptual: Es un modelo basado en ensambles (bagging) de árboles de decisión. 
     Funciona construyendo múltiples árboles durante el entrenamiento y generando la clase 
     que es la moda de las clases de los árboles individuales.
   - Por qué se eligió: A diferencia de la Regresión Logística, Random Forest puede 
     capturar relaciones no lineales complejas entre las variables sin necesidad de 
     transformaciones manuales, es robusto ante outliers y no asume una distribución 
     específica en los datos. Sirve como un excelente contraste de rendimiento frente a un modelo lineal.

3. CONCLUSIONES Y COMPARACIÓN:
   - Las conclusiones se generan dinámicamente al final de la ejecución del script 
     basándose en las métricas obtenidas.
""" 





from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix, recall_score
from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# =========================
# CARGA Y PREPARACIÓN DE DATOS
# =========================

# Nombres de las columnas del dataset
columnas = ['Carga', 'Masa', 'TiempoVuelo', 'VelMax', 'PosFinalX', 'Clase']
# Cargar archivo CSV
df = pd.read_csv('dataset_celulas.csv', names=columnas)

# Variables de entrada (features) y variable objetivo (label)
X = df[['Carga', 'Masa', 'TiempoVuelo', 'VelMax', 'PosFinalX']]
y = df['Clase']

# =========================
# NORMALIZACIÓN DE DATOS
# =========================
# Se escalan los datos para que todas las variables estén en la misma escala
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# DIVISIÓN DE DATOS
# =========================
# 70% entrenamiento, 30% prueba
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42
)


# =========================
# MODELO 1: DECISION TREE
# =========================
# Árbol de decisión que clasifica mediante reglas (if-else)

dtree = DecisionTreeClassifier(
    criterion='entropy',        # Método de división (ganancia de información)
    max_depth=3,                # Profundidad máxima del árbol
    min_samples_split=5,        # Mínimo de muestras para dividir un nodo
    min_samples_leaf=2,         # Mínimo de muestras en una hoja
    random_state=42
)

dtree.fit(X_train, y_train)          # Entrenamiento del modelo
y_pred_dt = dtree.predict(X_test)    # Predicciones


# =========================
# MODELO 2: ADABOOST
# =========================
# Ensemble que combina múltiples árboles pequeños para mejorar el rendimiento

ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),  # Árbol débil (stump)
    n_estimators=50,        # Número de modelos
    learning_rate=1.0,      # Tasa de aprendizaje
    random_state=42
)

ada.fit(X_train, y_train)
y_pred_ada = ada.predict(X_test)


# =========================
# MODELO 3: RED NEURONAL
# =========================
# Modelo que simula neuronas para aprender relaciones complejas

red_neuronal = MLPClassifier(
    hidden_layer_sizes=(10,10),  # 2 capas ocultas con 10 neuronas cada una
    activation='relu',           # Función de activación
    solver='adam',               # Algoritmo de optimización
    max_iter=500,                # Iteraciones máximas
    random_state=42,
    verbose=True                 # Muestra el entrenamiento en consola
)

print("\n Entrenando Red Neuronal...")
red_neuronal.fit(X_train, y_train)

y_pred_red = red_neuronal.predict(X_test)


# =========================
# MÉTRICAS DE EVALUACIÓN
# =========================
# Accuracy: porcentaje de aciertos
# Recall: capacidad de detectar correctamente las clases

# Decision Tree
acc_dt = accuracy_score(y_test, y_pred_dt)
rec_dt = recall_score(y_test, y_pred_dt, average='weighted')

# AdaBoost
acc_ada = accuracy_score(y_test, y_pred_ada)
rec_ada = recall_score(y_test, y_pred_ada, average='weighted')

# Red Neuronal
acc_nn = accuracy_score(y_test, y_pred_red)
rec_nn = recall_score(y_test, y_pred_red, average='weighted')

print("\n--- RESULTADOS ---")
print("Decision Tree -> Accuracy:", acc_dt, " Recall:", rec_dt)
print("AdaBoost (Tree) -> Accuracy:", acc_ada, " Recall:", rec_ada)
print("Red Neuronal -> Accuracy:", acc_nn, " Recall:", rec_nn)


# =========================
# GRÁFICA COMPARATIVA
# =========================
# Se comparan accuracy y recall entre modelos

modelos = ['Decision Tree', 'AdaBoost', 'Red Neuronal']
accuracy = [acc_dt, acc_ada, acc_nn]
recall = [rec_dt, rec_ada, rec_nn]

x = np.arange(len(modelos))

plt.figure()
plt.bar(x - 0.2, accuracy, 0.4, label='Accuracy')
plt.bar(x + 0.2, recall, 0.4, label='Recall')

plt.xticks(x, modelos)
plt.ylabel('Valor')
plt.title('Comparación de modelos')
plt.legend()

plt.show()


