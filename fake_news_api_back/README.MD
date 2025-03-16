# Fake News Prediction API

This API allows users to predict whether a news article is fake or real using machine learning models. It also provides insights and statistics about predictions and trained models.

## Features
- Predict if a news article is fake or real using the default model (`logistic`).
- Predict using a specific machine learning model.
- Retrieve general statistics about predictions and trained models.
- Fetch detailed statistics for a specific model.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Django 5.1.6
- Required Python libraries (see `requirements.txt`)

### Steps to Set Up
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fake_news_api_back
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the API documentation:
   - Swagger UI: [http://localhost:8000/](http://localhost:8000/)
   - ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## API Endpoints

### 1. Predict News (Default Model)
**Endpoint:** `POST /api/predict-news/`  
**Description:** Predicts if a news article is fake or real using the default `logistic` model.  
**Request Body:**
```json
{
  "text": "News article content here"
}
```
**Response:**
```json
{
  "prediction": "Fake" or "Real"
}
```

---

### 2. Predict with Specific Model
**Endpoint:** `POST /api/predict-news/{model_type}/`  
**Description:** Predicts if a news article is fake or real using a specified model.  
**Path Parameter:**
- `model_type`: The type of model to use (e.g., `logistic`, `svm`, etc.).  
**Request Body:**
```json
{
  "text": "News article content here"
}
```
**Response:**
```json
{
  "prediction": "Fake" or "Real"
}
```

---

### 3. Insights
**Endpoint:** `GET /api/insights/`  
**Description:** Provides general statistics about predictions and trained models.  
**Response:**
```json
{
  "total_predictions": 100,
  "real_count": 60,
  "fake_count": 40,
  "last_predictions": [
    {
      "text": "Sample news text",
      "prediction": "Real",
      "model_used": "logistic",
      "created_at": "2023-10-01T12:00:00Z"
    }
  ],
  "model_stats": [
    {
      "model_name": "logistic",
      "accuracy": 0.85,
      "trained_at": "2023-09-30T12:00:00Z"
    }
  ]
}
```

---

### 4. Model Statistics
**Endpoint:** `GET /api/model-stats/{model_name}/`  
**Description:** Fetches detailed statistics for a specific model.  
**Path Parameter:**
- `model_name`: The name of the model (e.g., `logistic`).  
**Response:**
```json
{
  "model_name": "logistic",
  "accuracy": 0.85,
  "trained_at": "2023-09-30T12:00:00Z"
}
```

---

## Configuration

### Installed Apps
Ensure the following apps are added in `settings.py`:
```python
INSTALLED_APPS = [
    'predictions',
    'ml_models',
    'corsheaders',
    'rest_framework',
    'drf_yasg',
    # ...existing apps...
]
```

### Middleware
Add `CorsMiddleware` to enable cross-origin requests:
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...existing middleware...
]
```

### Database
The API uses SQLite by default. Update `DATABASES` in `settings.py` if needed:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## Dataset
The API uses datasets located in `datasets/raw/` for training and testing:
- `test.csv`: Contains mixed fake and real news samples.
- `onlytrue1000.csv`: Contains only real news samples.
- `onlyfakes1000.csv`: Contains only fake news samples.

---

## Notes
- The API uses `drf_yasg` for auto-generating Swagger and ReDoc documentation.
- Ensure the `MODELS` and `VECTORIZER` objects in `ml_models.models` are properly initialized with trained models and vectorizers.
- Use the `preprocess_text` function in `ml_models.processor` to clean and preprocess input text before predictions.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
