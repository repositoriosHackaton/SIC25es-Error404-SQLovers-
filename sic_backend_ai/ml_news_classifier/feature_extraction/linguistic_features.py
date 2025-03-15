import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from data_news_api.models import Article, Feature

# Asegúrate de descargar los recursos correctos
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class LinguisticFeatureExtractor:
    def __init__(self):
        pass
        
    def preprocess_text(self, text):
        """Basic text preprocessing"""
        if not text:
            return ""
        
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text
        
    def extract_features(self, article_ids=None):
        """Extract linguistic features from articles"""
        if article_ids:
            articles = Article.objects.filter(id__in=article_ids)
        else:
            articles = Article.objects.filter(in_training_set=True)
            
        print(f"Procesando {articles.count()} artículos para características lingüísticas")
            
        batch_features = []
        processed_count = 0
        
        for article in articles:
            text = self.preprocess_text(article.text)
            
            # Skip empty texts
            if not text:
                continue
                
            # Tokenize text - especificando el idioma español
            try:
                # Usar el tokenizador genérico que ya está descargado
                sentences = sent_tokenize(text, language='spanish')
                words = word_tokenize(text, language='spanish')
            except LookupError:
                # Fallback a tokenización básica si falla
                sentences = text.split('.')
                words = text.split()
            
            # Calculate basic text statistics
            num_sentences = len(sentences) if sentences else 0
            num_words = len(words) if words else 0
            avg_sentence_length = num_words / max(1, num_sentences)
            
            # Extract unique words
            unique_words = set(words)
            lexical_diversity = len(unique_words) / max(1, len(words))
            
            # Count uppercase words (potential indicators of emphasis in fake news)
            uppercase_words = sum(1 for word in words if word.isupper() and len(word) > 1)
            uppercase_ratio = uppercase_words / max(1, len(words))
            
            # Count exclamation and question marks
            exclamation_count = text.count('!')
            question_count = text.count('?')
            
            # Create features
            linguistic_features = [
                ('num_sentences', num_sentences),
                ('num_words', num_words),
                ('avg_sentence_length', avg_sentence_length),
                ('lexical_diversity', lexical_diversity),
                ('uppercase_ratio', uppercase_ratio),
                ('exclamation_count', exclamation_count),
                ('question_count', question_count),
            ]
            
            # Add to batch
            for name, value in linguistic_features:
                batch_features.append(
                    Feature(
                        article=article,
                        feature_name=f"ling_{name}",
                        feature_value=value
                    )
                )
                
            processed_count += 1
            
            # Save in batches
            if len(batch_features) >= 1000:
                Feature.objects.bulk_create(
                    batch_features, 
                    ignore_conflicts=True
                )
                print(f"Guardado lote de {len(batch_features)} características")
                batch_features = []
                
            # Log progress
            if processed_count % 10 == 0:
                print(f"Procesados {processed_count} artículos para características lingüísticas")
                
        # Final batch
        if batch_features:
            Feature.objects.bulk_create(
                batch_features,
                ignore_conflicts=True
            )
            print(f"Guardado lote final de {len(batch_features)} características")
            
        print(f"Extracción lingüística completada. Total: {processed_count} artículos procesados.")
        return processed_count