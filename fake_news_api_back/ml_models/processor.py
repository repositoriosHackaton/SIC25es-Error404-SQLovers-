import re
import string
import pytesseract
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image
import os
# Cargar las stopwords en español
try:
    stop_words = set(stopwords.words("spanish"))
except:
    import nltk
    nltk.download("stopwords")
    stop_words = set(stopwords.words("spanish"))

# Agregar palabras adicionales que queremos eliminar
stop_words.update(["según", "tras", "cabe", "bajo", "durante", "mediante", "so", "toda", "todas",
                   "cada", "me", "después", "despues", "segun", "solo", "sido", "estan", "lunes",
                   "martes", "miércoles", "jueves", "viernes"])

def preprocess_text(text):
    """
    Limpia y preprocesa el texto antes de enviarlo al modelo de Machine Learning.

    Pasos:
    1. Convertir a minúsculas.
    2. Eliminar signos de puntuación y caracteres especiales.
    3. Tokenizar el texto en palabras.
    4. Eliminar stopwords en español.
    5. Unir las palabras nuevamente en una sola cadena de texto.
    
    :param text: Texto original sin procesar.
    :return: Texto limpio y listo para vectorización.
    """
    if not isinstance(text, str):
        return ""

    # Convertir a minúsculas
    text = text.lower()

    # Eliminar URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    # Eliminar números
    text = re.sub(r"\d+", "", text)

    # Eliminar signos de puntuación
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenización (convertir en lista de palabras)
    words = word_tokenize(text)

    # Eliminar stopwords
    filtered_words = [word for word in words if word not in stop_words]

    # Unir las palabras procesadas en una sola cadena
    return " ".join(filtered_words)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Le decimos a Tesseract dónde está la carpeta de idiomas
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def extract_text_from_image(image_file):
    """
    Recibe un archivo de imagen y extrae texto usando OCR.
    """
    image = Image.open(image_file)
    extracted_text = pytesseract.image_to_string(image, lang='spa')  
    return extracted_text