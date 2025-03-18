from django.core.management.base import BaseCommand
from ml_news_classifier.feature_extraction import FeatureExtractorPipeline

class Command(BaseCommand):
    help = 'Extract features from news articles for ML training'
    
    def add_arguments(self, parser):
        parser.add_argument('--ids', type=str, help='Comma-separated list of article IDs')
        parser.add_argument('--limit', type=int, help='Limit number of articles to process')
    
    def handle(self, *args, **options):
        try:
            article_ids = None
            
            if options.get('ids'):
                article_ids = [int(id.strip()) for id in options['ids'].split(',') if id.strip()]
                self.stdout.write(f"Extracting features for {len(article_ids)} specific articles")
            
            extractor = FeatureExtractorPipeline()
            results = extractor.extract_all_features(article_ids)
            
            self.stdout.write(self.style.SUCCESS("Feature extraction completed!"))
            for extractor_name, count in results.items():
                self.stdout.write(f"{extractor_name}: processed {count} articles")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error extracting features: {str(e)}"))
            import traceback
            self.stdout.write(traceback.format_exc())