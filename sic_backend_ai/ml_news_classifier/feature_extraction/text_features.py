import re
import numpy as np
import pandas as pd
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
from data_news_api.models import Article, Feature

# Configure logging
logger = logging.getLogger(__name__)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    logger.info("Downloading NLTK resources")
    nltk.download('stopwords')
    nltk.download('punkt')

class TextFeatureExtractor:
    def __init__(self):
        logger.info("Initializing TextFeatureExtractor")
        self.spanish_stopwords = list(stopwords.words('spanish'))
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.9,
            stop_words=self.spanish_stopwords,
            ngram_range=(1, 2)
        )
    
    def preprocess_text(self, text):
        """Clean and normalize text"""
        if not text:
            tfidf_matrix = np.zeros((1, len(self.tfidf_vectorizer.get_feature_names_out())))
            
        text = text.lower()
        
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_features(self, article_ids=None):
        """Extract TF-IDF features from articles"""
        if article_ids:
            articles = Article.objects.filter(id__in=article_ids)
            logger.info(f"Extracting features for {len(article_ids)} specific articles")
        else:
            articles = Article.objects.filter(in_training_set=True)
            logger.info(f"Extracting features for all training set articles")
        
        article_count = articles.count()
        logger.info(f"Found {article_count} articles to process")
        
        texts = [self.preprocess_text(article.text) for article in articles]
        logger.info(f"Preprocessed {len(texts)} article texts")
        
        logger.info("Generating TF-IDF matrix")
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        logger.info(f"Extracted {len(feature_names)} unique features")
        
        batch_features = []
        total_features = 0
        bulk_count = 0
        
        logger.info("Starting feature extraction for individual articles")
        for i, article in enumerate(articles):
            if i % 100 == 0:
                logger.debug(f"Processing article {i+1}/{article_count}")
                
            article_features = tfidf_matrix[i].toarray()[0]
            non_zero_count = 0
            
            for j, value in enumerate(article_features):
                if value > 0:  # Only store non-zero features
                    feature = Feature(
                        article=article,
                        feature_name=f"tfidf_{feature_names[j]}",
                        feature_value=value
                    )
                    batch_features.append(feature)
                    non_zero_count += 1
                    
                    if len(batch_features) >= 1000:
                        logger.debug(f"Bulk creating batch {bulk_count+1} ({len(batch_features)} features)")
                        Feature.objects.bulk_create(
                            batch_features, 
                            ignore_conflicts=True
                        )
                        total_features += len(batch_features)
                        batch_features = []
                        bulk_count += 1
            
            if i % 100 == 0:
                logger.debug(f"Found {non_zero_count} non-zero features for article {article.id}")
        
        if batch_features:
            logger.debug(f"Bulk creating final batch ({len(batch_features)} features)")
            Feature.objects.bulk_create(
                batch_features,
                ignore_conflicts=True
            )
            total_features += len(batch_features)
            bulk_count += 1
        
        logger.info(f"Feature extraction completed: {total_features} total features created in {bulk_count} bulk operations")
        return article_count