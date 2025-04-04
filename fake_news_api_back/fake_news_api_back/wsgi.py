"""
WSGI config for fake_news_api_back project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fake_news_api_back.settings')

# Configurar el directorio de datos de NLTK
import nltk
nltk.data.path.append("/app/nltk_data")  # Cambia "/app/nltk_data" al directorio deseado

# Configurar el directorio de datos de NLTK
nltk.data.path.append("/app/nltk_data")  

# Descargar datos de NLTK si no existen
for resource in ['stopwords', 'punkt', 'punkt_tab']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource, download_dir="/app/nltk_data")


application = get_wsgi_application()
