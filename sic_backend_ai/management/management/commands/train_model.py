from django.core.management.base import BaseCommand
from ml_news_classifier.algorithms.random_forest import RandomForestNewsClassifier
from ml_news_classifier.algorithms.naive_bayes import NaiveBayesNewsClassifier
from ml_news_classifier.algorithms.neuronal_network import NeuronalNetworkNewsClassifier
from ml_news_classifier.models import MLExperiment, FeatureImportance
from data_news_api.models import MLModel
from django.db import transaction

class Command(BaseCommand):
    help = 'Entrena un modelo de machine learning para la detección de noticias falsas'

    def add_arguments(self, parser):
        # Argumentos básicos
        parser.add_argument('--name', type=str, required=True, help='Nombre del experimento')
        
        # Selección del algoritmo
        parser.add_argument('--algorithm', type=str, default='rf', choices=['rf', 'nb', 'nn'], 
                           help='Algoritmo a utilizar: rf (Random Forest), nb (Naive Bayes), nn (Red Neuronal)')
        
        # Parámetros para Random Forest
        parser.add_argument('--estimators', type=int, default=100, help='Número de árboles (para Random Forest)')
        parser.add_argument('--max-depth', type=int, help='Profundidad máxima de los árboles (para Random Forest)')
        
        # Parámetros para Naive Bayes
        parser.add_argument('--alpha', type=float, default=1.0, help='Parámetro alpha para suavizado (para Naive Bayes)')
        
        # Parámetros para Red Neuronal
        parser.add_argument('--hidden-layers', type=str, default='100', 
                           help='Tamaños de capas ocultas separados por comas, ej: 100,50 (para Red Neuronal)')
        parser.add_argument('--activation', type=str, default='relu', choices=['relu', 'tanh', 'logistic'],
                           help='Función de activación (para Red Neuronal)')
        parser.add_argument('--max-iter', type=int, default=200, 
                           help='Máximo de iteraciones (para Red Neuronal)')
        
        # Filtrado de características
        parser.add_argument('--include', type=str, help='Solo incluir características que comienzan con estos prefijos, separados por coma')
        parser.add_argument('--exclude', type=str, help='Excluir características que comienzan con estos prefijos, separados por coma')
        parser.add_argument('--features', type=str, choices=['all'], help='Usar todas las características disponibles')

    def handle(self, *args, **options):
        experiment_name = options['name']
        algorithm = options['algorithm']
        
        
        # Procesar filtros de características
        include_features = None
        exclude_features = None
        
        # Si se especificó --features all, no aplicamos ningún filtro
        if options.get('features') == 'all':
            self.stdout.write("Usando TODAS las características disponibles")
            include_features = None
            exclude_features = None
        else:
            if options.get('include'):
                include_features = options['include'].split(',')
                self.stdout.write(f"Incluyendo solo características que comienzan con: {include_features}")
                
            if options.get('exclude'):
                exclude_features = options['exclude'].split(',')
                self.stdout.write(f"Excluyendo características que comienzan con: {exclude_features}")
        
        # Crear el clasificador según el algoritmo seleccionado
        if algorithm == 'rf':
            n_estimators = options['estimators']
            max_depth = options.get('max_depth')
            
            self.stdout.write(f"Entrenando Random Forest con {n_estimators} árboles...")
            if max_depth:
                self.stdout.write(f"Profundidad máxima: {max_depth}")
                classifier = RandomForestNewsClassifier(n_estimators=n_estimators, max_depth=max_depth)
            else:
                classifier = RandomForestNewsClassifier(n_estimators=n_estimators)
                
        elif algorithm == 'nb':
            alpha = options['alpha']
            self.stdout.write(f"Entrenando Naive Bayes con alpha={alpha}...")
            classifier = NaiveBayesNewsClassifier(alpha=alpha)
            
        elif algorithm == 'nn':
            hidden_layers_str = options['hidden_layers']
            hidden_layer_sizes = tuple(int(x) for x in hidden_layers_str.split(','))
            activation = options['activation']
            max_iter = options['max_iter']
            
            self.stdout.write(f"Entrenando Red Neuronal...")
            self.stdout.write(f"Capas ocultas: {hidden_layer_sizes}")
            self.stdout.write(f"Activación: {activation}")
            self.stdout.write(f"Máx. iteraciones: {max_iter}")
            
            classifier = NeuronalNetworkNewsClassifier(
                hidden_layer_sizes=hidden_layer_sizes,
                activation=activation,
                max_iter=max_iter
            )
            
        else:
            self.stdout.write(self.style.ERROR(f"Algoritmo no soportado: {algorithm}"))
            return
        
        try:
            # Entrenar el modelo
            with transaction.atomic():
                experiment = classifier.train(
                    experiment_name=experiment_name,
                    include_features=include_features,
                    exclude_features=exclude_features
                )
                
                if not experiment:
                    self.stdout.write(self.style.ERROR("El experimento no se creó correctamente."))
                    return
                
                self.stdout.write(self.style.SUCCESS(f"\nModelo entrenado exitosamente: {experiment.name}"))
                self.stdout.write(f"ID del experimento: {experiment.id}")
                
                # Si el modelo se creó correctamente
                if experiment.ml_model:
                    self.stdout.write(f"ID del modelo: {experiment.ml_model.id}")
                    
                    # Mostrar las características más importantes
                    top_features = FeatureImportance.objects.filter(experiment=experiment)\
                                     .order_by('-importance')[:15]
                    
                    if top_features:
                        self.stdout.write(self.style.SUCCESS("\nCaracterísticas más importantes:"))
                        for i, feature in enumerate(top_features):
                            self.stdout.write(f"{i+1}. {feature.feature_name}: {feature.importance:.4f}")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante el entrenamiento: {str(e)}"))
            import traceback
            self.stdout.write(traceback.format_exc())