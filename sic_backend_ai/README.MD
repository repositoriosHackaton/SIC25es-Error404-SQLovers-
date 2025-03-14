# Arquitectura del Sistema de Clasificación de Noticias

## Visión General del Flujo de Datos


## 1. Fuentes de Datos
📊 **Archivos CSV**: Colecciones de noticias etiquetadas como verdaderas o falsas.

## 2. Proceso de Importación
🔄 **`import_news_data.py`**: Script que migra datos desde archivos CSV a la base de datos Django.

## 3. API de Datos (`data_news_api`)

### Modelos
- 📰 **Article**: Almacena textos de noticias y su clasificación
- 📊 **Feature**: Características extraídas de los artículos
- 🤖 **MLModel**: Información sobre modelos entrenados
- 📚 **NewsDataset**: Metadatos de conjuntos de datos originales

### Endpoints API
- Interfaces REST para operaciones CRUD en todos los modelos
- `MigratedDatasetStats`: Proporciona estadísticas sobre los datos importados

## 4. Sistema de Clasificación ML

### Extracción de Características
| Extractor | Descripción |
|-----------|-------------|
| **FeatureExtractorPipeline** | Coordinador principal de extracción |
| **TextFeatureExtractor** | Características TF-IDF del texto |
| **LinguisticFeatureExtractor** | Patrones lingüísticos y complejidad textual |
| **MetadataFeatureExtractor** | Características basadas en metadatos |

### Algoritmos Implementados
- 🌲 **RandomForestNewsClassifier**
- 📊 **NaiveBayesClassifier**
- 🧠 **NeuralNetworkClassifier**

### Gestión de Modelos
- 🧪 **MLExperiment**: Registro de configuraciones y resultados
- 📈 **FeatureImportance**: Relevancia de cada característica
- 🔍 **Prediction**: Registro de predicciones realizadas

### Comandos CLI
```bash
# Extracción de características
python manage.py extract_features

# Entrenamiento de modelos
python manage.py train_model --algorithm rf --features all

# Generación de predicciones
python manage.py predict --model_id 1 --article_id 100
```

## Flujo de Trabajo Principal

1. **Importación** → Carga de CSV a base de datos
2. **Extracción** → Generación de características para ML
3. **Entrenamiento** → Creación y evaluación de modelos
4. **Predicción** → Clasificación de nuevas noticias

## Usuarios del Sistema
- 👩‍🔬 **Data Scientist**: Ejecuta comandos de procesamiento y análisis
- 🧑‍💻 **API Client**: Consume servicios a través de endpoints REST