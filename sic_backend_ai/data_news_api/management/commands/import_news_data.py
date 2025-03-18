import pandas as pd
import os
from django.core.management.base import BaseCommand
from data_news_api.models import Article

class Command(BaseCommand):
    help = 'Import news articles from CSV files'
    
    def add_arguments(self, parser):
        parser.add_argument('--dir', type=str, help='Directory containing CSV files')
        parser.add_argument('--verbose', action='store_true', help='Show more detailed information')
        parser.add_argument('--reset', action='store_true', help='Delete all existing articles before importing')
        
    def handle(self, *args, **options):
        try:
            verbose = options.get('verbose', False)
            data_dir = options['dir'] or 'data_news_api/datasets/'
            abs_dir = os.path.abspath(data_dir)
            
            self.stdout.write(f"Buscando archivos en: {os.path.abspath(data_dir)}")
            
            if options.get('reset'):
                count = Article.objects.all().count()
                Article.objects.all().delete()
                self.stdout.write(self.style.WARNING(f"Eliminados {count} artículos existentes"))
            
            csv_files = ['fakes1000.csv', 'onlyfakes1000.csv', 'onlytrue1000.csv', 'train.csv', 'test.csv']
            for file_name in csv_files:
                file_path = os.path.join(data_dir, file_name)
                if os.path.exists(file_path):
                    self.stdout.write(f"✓ Encontrado: {file_name}")
                else:
                    self.stdout.write(self.style.WARNING(f"✗ No encontrado: {file_name}"))
                    
            
            # Limitar la cantidad de artículos a importar por dataset para evitar duplicados
            max_articles_per_dataset = 10000
            total_imported = 0
            
            # Process fakes1000.csv (artículos mezclados con etiquetas true/false)
            fake_path = os.path.join(data_dir, 'fakes1000.csv')
            if os.path.exists(fake_path):
                self.stdout.write(f'Processing {fake_path}')
                df = pd.read_csv(fake_path)
                count = 0
                for _, row in df.iterrows():
                    if count >= max_articles_per_dataset:
                        break
                    
                # Verificar que las columnas esperadas existen
                    if 'class' not in row or 'Text' not in row:
                        if verbose:
                            self.stdout.write(self.style.WARNING(f"Fila sin columnas esperadas: {row}"))
                        continue
                        
                        
                    label = Article.TRUE if str(row['class']).upper() == 'TRUE' else Article.FALSE
                    
                    # Evitar artículos vacíos
                    if pd.notna(row['Text']) and row['Text'].strip():
                        Article.objects.create(
                            text=row['Text'],
                            label=label,
                            dataset_origin='fakes1000'
                        )
                        count += 1
                        total_imported += 1
                        
                self.stdout.write(f'Imported {count} articles from fakes1000.csv')
            
            # Process onlyfakes1000.csv (solo noticias falsas)
            onlyfakes_path = os.path.join(data_dir, 'onlyfakes1000.csv')
            if os.path.exists(onlyfakes_path):
                self.stdout.write(f'Processing {onlyfakes_path}')
                df = pd.read_csv(onlyfakes_path)
                count = 0
                for _, row in df.iterrows():
                    if count >= max_articles_per_dataset:
                        break
                    
                    # Todos los artículos son falsos en este dataset
                    if pd.notna(row['text']) and row['text'].strip():
                        Article.objects.create(
                            text=row['text'],
                            label=Article.FALSE,
                            dataset_origin='onlyfakes1000'
                        )
                        count += 1
                        total_imported += 1
                        
                self.stdout.write(f'Imported {count} articles from onlyfakes1000.csv')
            
            # Process onlytrue1000.csv (solo noticias verdaderas)
            onlytrue_path = os.path.join(data_dir, 'onlytrue1000.csv')
            if os.path.exists(onlytrue_path):
                self.stdout.write(f'Processing {onlytrue_path}')
                df = pd.read_csv(onlytrue_path)
                count = 0
                for _, row in df.iterrows():
                    if count >= max_articles_per_dataset:
                        break
                    
                    # Todos los artículos son verdaderos en este dataset
                    if pd.notna(row['text']) and row['text'].strip():
                        Article.objects.create(
                            text=row['text'],
                            label=Article.TRUE,
                            dataset_origin='onlytrue1000'
                        )
                        count += 1
                        total_imported += 1
                        
                self.stdout.write(f'Imported {count} articles from onlytrue1000.csv')
            
            # Process train.csv (dataset de entrenamiento)
            train_path = os.path.join(data_dir, 'train.csv')
            if os.path.exists(train_path):
                self.stdout.write(f'Processing {train_path}')
                df = pd.read_csv(train_path)
                count = 0
                for _, row in df.iterrows():
                    if count >= max_articles_per_dataset:
                        break
                    
                    title = row['title'] if 'title' in row and pd.notna(row['title']) else None
                    
                    # En train.csv, 0 = verdadero, 1 = falso
                    label = Article.TRUE if row['label'] == 0 else Article.FALSE
                    
                    if pd.notna(row['text']) and row['text'].strip():
                        Article.objects.create(
                            text=row['text'],
                            title=title,
                            label=label,
                            dataset_origin='train',
                            in_training_set=True
                        )
                        count += 1
                        total_imported += 1
                        
                self.stdout.write(f'Imported {count} articles from train.csv')
            
            # Process test.csv (dataset de prueba)
            test_path = os.path.join(data_dir, 'test.csv')
            if os.path.exists(test_path):
                self.stdout.write(f'Processing {test_path}')
                df = pd.read_csv(test_path)
                count = 0
                for _, row in df.iterrows():
                    if count >= max_articles_per_dataset:
                        break
                    
                    title = row['title'] if 'title' in row and pd.notna(row['title']) else None
                    
                    # Para test.csv no tenemos etiquetas, las dejamos desconocidas
                    if pd.notna(row['text']) and row['text'].strip():
                        Article.objects.create(
                            text=row['text'],
                            title=title,
                            label=Article.UNKNOWN,  # No hay etiqueta en el CSV de test
                            dataset_origin='test',
                            in_test_set=True
                        )
                        count += 1
                        total_imported += 1
                        
                self.stdout.write(f'Imported {count} articles from test.csv')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {total_imported} news articles'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante la importación: {str(e)}"))
            import traceback
            self.stdout.write(traceback.format_exc())
            