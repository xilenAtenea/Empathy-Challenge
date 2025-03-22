# Empathy Challenge

## Introducción
Este proyecto fue desarrollado como parte de una prueba técnica para evaluar habilidades en procesamiento de datos, análisis exploratorio, modelado predictivo y segmentación. Se trabaja con un dataset de salud ocupacional con el objetivo de identificar patrones de riesgo y generar valor a partir de la analítica.

## Estructura del repositorio

- `data/`: Contiene el dataset original y el archivo limpio.
- `notebooks/`: Incluye los notebooks organizados por etapas del análisis.
- `src/`: Código fuente modular para transformación y modelado.
- `docs/`: Espacio reservado para documentación adicional.

## Requisitos
Este proyecto fue desarrollado en Python. Las principales librerías utilizadas son:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

## Ejecución paso a paso

1. **EDA** (`notebooks/00_EDA.ipynb`): análisis exploratorio del dataset, distribución de variables y detección de inconsistencias.
2. **Transformaciones** (`notebooks/01_transformations.ipynb`): creación de nuevas variables usando clases modulares.
3. **Visualizaciones** (`notebooks/02_visualizations.ipynb`): análisis gráfico de relaciones entre factores de riesgo y salud.
4. **Modelado** (`notebooks/03_model_evaluation.ipynb`): regresión para predecir IMC y segmentación mediante clustering.

## Resultados destacados

- Limpieza completa del dataset y recuperación de columnas mal importadas.
- Generación de variables derivadas.
- Visualizaciones claras de patrones entre estilo de vida y salud.
- Modelo de regresión con R² = 0.63 para predecir IMC.
- Segmentación en 3 perfiles de salud accionables vía KMeans.

## Autor
Desarrollado por Xilena Atenea Rojas Salazar como parte de la prueba técnica para Empathy.
