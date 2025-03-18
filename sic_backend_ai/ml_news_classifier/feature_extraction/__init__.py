from .text_features import TextFeatureExtractor
from .linguistic_features import LinguisticFeatureExtractor
from .metadata_features import MetadataFeatureExtractor

class FeatureExtractorPipeline:
    """Combine multiple feature extractors into a single pipeline"""
    
    def __init__(self):
        self.extractors = [
            TextFeatureExtractor(),
            LinguisticFeatureExtractor(),
            MetadataFeatureExtractor()
        ]
    
    def extract_all_features(self, article_ids=None):
        """Run all feature extractors on the specified articles"""
        results = {}
        
        for extractor in self.extractors:
            extractor_name = extractor.__class__.__name__
            print(f"Running {extractor_name}...")
            try:
                count = extractor.extract_features(article_ids)
                results[extractor_name] = count
                print(f"✓ Completado {extractor_name}: procesados {count} artículos")
            except Exception as e:
                print(f"✗ Error en {extractor_name}: {str(e)}")
                import traceback
                print(traceback.format_exc())
                results[extractor_name] = "ERROR"
                
        return results