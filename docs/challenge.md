# Parte 1: Procesamiento y Preparación de Datos

## 1.1 Análisis Exploratorio y Detección de Problemas de Formato

En la fase inicial del proyecto se identificó que el archivo CSV presentaba problemas de formato: algunas filas completas estaban mal interpretadas y todos sus valores aparecían como un único string en la primera columna. Esta detección se realizó analizando el número de columnas válidas y los valores nulos por fila.

## 1.2 Pipeline de Limpieza y Transformación

Se implementó una clase modular `DataPreprocessor` en `src/` que encapsula todo el flujo de limpieza y transformación de los datos. Este pipeline automatiza y documenta cada paso de preprocesamiento del dataset.

### Funcionalidades principales de la clase:

#### - Limpieza de nombres de columnas
Se eliminaron acentos, espacios, caracteres especiales y se homogenizaron los nombres a snake_case. Se aplicaron correcciones manuales a algunas columnas mal nombradas.

#### - Corrección de filas mal formateadas
Se detectaron filas con más del 80% de valores nulos y se reconstruyeron usando la librería `csv` para dividir adecuadamente los campos, incluso si contenían comas internas.

#### - Conversión de tipos de datos
Se definieron listas de columnas booleanas, numéricas, categóricas y de fecha, y se forzó su conversión a los tipos adecuados utilizando `pandas.to_numeric`, `astype('category')` y `to_datetime`.

#### - Eliminación de columnas no informativas
Se eliminaron columnas completamente vacías.

#### - Normalización de textos
Se homogenizaron todas las columnas tipo texto o categoría: eliminación de tildes, espacios, capitalización y errores comunes (como “bogot” por “bogota”).

#### - Categorización de edad
Se corrigió la variable `grupo_etareo` que clasifica la edad en rangos (`0-19`, `20-29`, ..., `60+`).

### Pipeline ejecutado:
El método `run_all()` encapsula toda la lógica anterior, lo cual permite reutilizar el preprocesamiento de forma limpia y consistente a lo largo del proyecto.

## 1.3 Justificación

El enfoque modular permitió separar la lógica de limpieza del análisis, mejorando la mantenibilidad y reutilización del código. Además, los pasos implementados atacan problemas comunes en datos reales: errores de encoding, estructuras corruptas, heterogeneidad en los tipos y nombres, y columnas sin valor analítico.

Este trabajo garantiza que el dataset esté listo para el análisis exploratorio, la creación de variables derivadas y la modelación posterior.


# Parte 2: Analítica de Datos y Modelación

## 2.1 Ingeniería de Variables Derivadas

Se implementó la clase `FeatureEngineer` para generar variables clave que enriquecen el análisis, basadas en diagnóstico, edad, riesgos laborales. Esta clase está ubicada en `src/feature_engineer.py`.

### Funciones implementadas:

- `create_is_over_50`: crea una variable binaria `es_mayor_50` para segmentar empleados mayores de 50 años.
- `create_has_diagnosis`: define si un individuo tiene al menos un diagnóstico válido (`tiene_diagnosticos`).
- `create_multiple_diagnoses`: marca si una persona tiene más de un diagnóstico conocido (`multiples_diagnosticos`).
- `create_work_disease_risk`: agrupa variables clínicas relacionadas con enfermedades laborales en una sola variable binaria.
- `create_high_absence`: identifica personas con más de 10 días perdidos por enfermedad (`dias_perdidos_alto`).
- `create_main_diagnosis_group`: extrae la primera letra del código del diagnóstico principal como categoría general (`diagnostico_principal_categoria`).

Todas las funciones están integradas en `run_all()`, lo que permite aplicar el procesamiento de manera reproducible y ordenada.


## 2.2 Visualizaciones

En el notebook `02_visualizations.ipynb` se desarrollaron visualizaciones para comunicar patrones clave:

- Distribución de diagnósticos por grupo etario
- Relación entre actividad física, edad y múltiples diagnósticos
- Heatmap de correlaciones entre estilo de vida, salud y ausentismo

Las visualizaciones se eligieron por su claridad, capacidad de comunicar insights y relevancia para decisiones de negocio.

## 2.3 Modelado y Validación Cruzada

En `03_model_evaluation.ipynb` se entrenó un modelo de regresión lineal para predecir el IMC (`signos_vitales_imc`), usando como features variables de estilo de vida:

- `actifisica`, `tact_fisica`, `horas_sueno`, `duracion_siesta`, `tiempo_beber`, `multiples_diagnosticos`

Se usaron:

- `StandardScaler` para escalado
- `LinearRegression` como modelo base
- `KFold (n=5)` para validación cruzada

### Métricas usadas:

- **MAE**: error promedio, fácil de interpretar
- **RMSE**: penaliza errores grandes
- **R²**: porcentaje de varianza explicada

**Resultados:**  
- MAE ≈ 6.12  
- RMSE ≈ 7.43  
- R² ≈ 0.63

Estas métricas muestran que el modelo logra capturar una parte significativa del comportamiento del IMC usando solo variables observables del estilo de vida.

## 2.4 Segmentación con KMeans

Se implementó un modelo de clustering con KMeans para identificar perfiles de empleados según su salud y hábitos:

### Variables usadas:
- `actifisica`, `horas_sueno`, `duracion_siesta`, `tact_fisica`, `tiempo_beber`, `multiples_diagnosticos`

### Flujo:
1. Escalado con `StandardScaler`
2. Reducción de dimensionalidad con PCA
3. Clustering con `KMeans(n=3)`
4. Visualización en plano PCA
5. Análisis de componentes para nombrar los clusters

### Perfiles detectados:
- **Grupo 0:** Activo, pero duerme poco (IMC saludable)
- **Grupo 1:** Riesgo metabólico alto (IMC alto, sedentarismo relativo)
- **Grupo 2:** Sedentario con IMC muy bajo (posible desnutrición o condición médica)

Este modelo de segmentación permite priorizar acciones desde bienestar laboral o medicina preventiva.
