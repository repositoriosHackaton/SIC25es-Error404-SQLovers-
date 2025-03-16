from django.core.management.base import BaseCommand
from ml_news_classifier.models import MLModel, MLExperiment
from ml_news_classifier.evaluation.metrics import evaluate_model
from data_news_api.models import Article, Feature
import pandas as pd
import json
import joblib

class Command(BaseCommand):
    help = 'Evaluar modelos entrenados en el conjunto de prueba'
    
    
    def add_arguments(self, parser):
        parser.add_argument('--model-id', type=int, help='Evaluar modelo específico por ID')
        parser.add_argument('--experiment-id', type=int, help='Evaluar modelo del experimento especificado')
        parser.add_argument('--latest', type=int, help='Evaluar los N modelos más recientes')
        parser.add_argument('--all', action='store_true', help='Evaluar todos los modelos')
    
    def handle(self, *args, **options):
        # Determinar qué modelos evaluar
        if options.get('model_id'):
            models = MLModel.objects.filter(id=options['model_id'])
            if not models.exists():
                self.stdout.write(self.style.ERROR(f"No se encontró modelo con ID {options['model_id']}"))
                return
                
        elif options.get('experiment_id'):
            experiment_id = options['experiment_id']
            experiments = MLExperiment.objects.filter(id=experiment_id)
            if not experiments.exists():
                self.stdout.write(self.style.ERROR(f"No se encontró experimento con ID {experiment_id}"))
                return
                
            models = MLModel.objects.filter(experiment__id=experiment_id)
            
        elif options.get('latest'):
            num = options['latest']
            models = MLModel.objects.all().order_by('-created_at')[:num]
            
        elif options.get('all'):
            models = MLModel.objects.all()
            
        else:
            # Por defecto, evaluar los 5 modelos más recientes
            models = MLModel.objects.all().order_by('-created_at')[:5]
        
        if not models.exists():
            self.stdout.write(self.style.ERROR("No hay modelos para evaluar"))
            return
            
        self.stdout.write(f"Evaluando {models.count()} modelos en el conjunto de prueba")
        
        # Verificar que hay artículos de prueba
        test_articles = Article.objects.filter(in_test_set=True)
        test_count = test_articles.count()
        
        if test_count == 0:
            self.stdout.write(self.style.ERROR("No hay artículos en el conjunto de prueba"))
            return
            
        self.stdout.write(f"Conjunto de prueba: {test_count} artículos")
        
        # Evaluar cada modelo
        for model in models:
            self.stdout.write(f"\n{'-' * 50}")
            self.stdout.write(f"Evaluando modelo: {model.name} (ID: {model.id})")
            
            try:
                experiment = MLExperiment.objects.filter(ml_model=model).first()
                
                if experiment:
                    self.stdout.write(f"Experimento: {experiment.name} (ID: {experiment.id})")
                    self.stdout.write(f"Algoritmo: {experiment.algorithm_name}")
                    self.stdout.write(f"Parámetros: {json.dumps(experiment.parameters, indent=2)}")
                
                if experiment and 'feature_names' in experiment.parameters:
                    feature_names = experiment.parameters['feature_names']
                else:
                    raise ValueError("No se encontraron nombres de características en el experimento asociado")
        
                test_article_ids = list(test_articles.values_list('id', flat=True))
                features = Feature.objects.filter(article_id__in=test_article_ids)
                df = pd.DataFrame(list(features.values('article_id', 'feature_name', 'feature_value')))
                X_test_df = df.pivot(index='article_id', columns='feature_name', values='feature_value').fillna(0)

                model_path = model.model_file.path
                clf = joblib.load(model_path)

                model_features = None  # Usar los nombres de características guardados en el experimento

                if experiment and 'feature_names' in experiment.parameters:
                    model_features = experiment.parameters['feature_names']
                    print(f"Usando {len(model_features)} características del experimento")
                    
                elif hasattr(clf, 'feature_names_in_'):
                    model_features = clf.feature_names_in_.tolist()
                    print(f"Usando {len(model_features)} características del modelo")
                
                else:
                    model_features = X_test_df.columns.tolist()
                    print(f"ADVERTENCIA: Usando todas las {len(model_features)} características disponibles")                    
                                    
                if not model_features:
                    raise ValueError("No se encontraron nombres de características en el experimento asociado.")

                for feature in model_features:
                    if feature not in X_test_df.columns:
                        X_test_df[feature] = 0  # Agregar columnas faltantes con valores 0

                X_test_df = X_test_df[model_features]

                X_test = X_test_df.fillna(0).values
                
                # Añadir más diagnósticos antes de llamar a evaluate_model
                self.stdout.write(f"Preparando evaluación para modelo {model.id}")
                self.stdout.write(f"Datos de prueba: X_test shape {X_test.shape}, {len(test_article_ids)} artículos")
    
                results = evaluate_model(model.id, X_test=X_test, verbose=True)
                
                if results:
                    self.stdout.write(self.style.SUCCESS("Resultados de evaluación:"))
                    self.stdout.write(f"Accuracy: {results['accuracy']:.4f}")
                    self.stdout.write(f"Precision: {results['precision']:.4f}")
                    self.stdout.write(f"Recall: {results['recall']:.4f}")
                    self.stdout.write(f"F1 Score: {results['f1_score']:.4f}")
                    
                    cm = results['confusion_matrix']
                    self.stdout.write("\nMatriz de Confusión:")
                    self.stdout.write("              Pred False    Pred True")
                    self.stdout.write(f"Actual False   {cm[0][0]:12d}  {cm[0][1]:12d}")
                    self.stdout.write(f"Actual True    {cm[1][0]:12d}  {cm[1][1]:12d}")
                    
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ No se obtuvieron resultados de evaluación para el modelo {model.id} - verificar si hay errores silenciosos"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error evaluando modelo: {str(e)}"))
                import traceback
                self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS("\nResumen - Mejores modelos por F1:"))
        top_models = MLModel.objects.filter(f1_score__isnull=False).order_by('-f1_score')[:5]
        
        if top_models:
            for i, model in enumerate(top_models):
                self.stdout.write(
                    f"{i+1}. {model.name} (ID: {model.id})\n"
                    f"   F1: {model.f1_score:.4f}, Acc: {model.accuracy:.4f}, "
                    f"Prec: {model.precision:.4f}, Rec: {model.recall:.4f}"
                )
        else:
            self.stdout.write("No hay modelos con métricas disponibles")