import re
from data_news_api.models import Article, Feature
import numpy as np

class MetadataFeatureExtractor:
    def __init__(self):
        pass
        
    def extract_features(self, article_ids=None):
        """Extract metadata-based features from articles"""
        if article_ids:
            articles = Article.objects.filter(id__in=article_ids)
        else:
            articles = Article.objects.filter(in_training_set=True)
            
        batch_features = []
        processed_count = 0
        
        dataset_origins = set(Article.objects.values_list('dataset_origin', flat=True).distinct())
        
        for article in articles:
            text_length = len(article.text) if article.text else 0
            title_length = len(article.title) if article.title else 0
            
            dataset_origin = article.dataset_origin or 'unknown'
            
            metadata_features = [
                ('text_length', text_length),
                ('title_length', title_length),
            ]
            
            for origin in dataset_origins:
                is_from_origin = 1.0 if dataset_origin == origin else 0.0
                metadata_features.append((f'origin_{origin}', is_from_origin))
            
            for name, value in metadata_features:
                batch_features.append(
                    Feature(
                        article=article,
                        feature_name=f"meta_{name}",
                        feature_value=value
                    )
                )
                
            processed_count += 1
            
            if len(batch_features) >= 1000:
                Feature.objects.bulk_create(
                    batch_features, 
                    ignore_conflicts=True
                )
                batch_features = []
                
            if processed_count % 100 == 0:
                print(f"Processed {processed_count} articles for metadata features")
                
        if batch_features:
            Feature.objects.bulk_create(
                batch_features,
                ignore_conflicts=True
            )
            
        return processed_count