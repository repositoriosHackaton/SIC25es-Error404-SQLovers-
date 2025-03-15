from django.core.management.base import BaseCommand
from data_news_api.models import Article, MLModel
from ml_news_classifier.models import MLExperiment, Prediction
from ml_news_classifier.algorithms.random_forest import RandomForestNewsClassifier
from ml_news_classifier.algorithms.naive_bayes import NaiveBayesNewsClassifier
from ml_news_classifier.algorithms.neuronal_network import NeuronalNetworkNewsClassifier


class Command(BaseCommand):
    help = 'Genera predicciones para artículos usando un modelo entrenado'

    def add_arguments(self, parser):
        parser.add_argument('--model_id', type=int, required=True, help='ID del modelo a utilizar')
        parser.add_argument('--article_id', type=int, help='ID del artículo a predecir (opcional)')
        parser.add_argument('--all_unlabeled', action='store_true', help='Predecir todos los artículos sin etiqueta')
        parser.add_argument('--save', action='store_true', help='Guardar la predicción en la base de datos')

    def handle(self, *args, **options):
        model_id = options['model_id']
        article_id = options.get('article_id')
        all_unlabeled = options.get('all_unlabeled', False)
        save_prediction = options.get('save', False)

        try:
            # Obtener el modelo entrenado
            try:
                ml_model = MLModel.objects.get(id=model_id)
                experiment = MLExperiment.objects.get(ml_model=ml_model)
            except MLModel.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"No existe un modelo con ID {model_id}"))
                return
            except MLExperiment.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"No hay experimento asociado al modelo con ID {model_id}"))
                return

            # Mostrar información del modelo
            self.stdout.write(f"Modelo: {ml_model.algorithm} (ID: {ml_model.id})")
            self.stdout.write(f"Experimento: {experiment.name} (ID: {experiment.id})")
            if experiment.accuracy is not None:
                self.stdout.write(f"Precisión del modelo: {experiment.accuracy:.4f}")
            else:
                self.stdout.write("Precisión del modelo: No disponible")

            # Verificar que el algoritmo no sea None
            if ml_model.algorithm is None:
                self.stdout.write(self.style.ERROR("El campo 'algorithm' del modelo está vacío."))
                self.stdout.write(self.style.WARNING("Por favor, actualice el modelo con un algoritmo válido: 'random_forest', 'naive_bayes' o 'neuronal_network'"))
                return

            # Crear el clasificador según el algoritmo
            if ml_model.algorithm == 'random_forest':
                classifier = RandomForestNewsClassifier()
            elif ml_model.algorithm == 'naive_bayes':
                classifier = NaiveBayesNewsClassifier()
            elif ml_model.algorithm in ['neuronal_network', 'neural_network']:  # Permitir ambas variantes
                classifier = NeuronalNetworkNewsClassifier()
            else:
                self.stdout.write(self.style.ERROR(f"Algoritmo no soportado: {ml_model.algorithm}"))
                self.stdout.write(self.style.WARNING("Algoritmos soportados: 'random_forest', 'naive_bayes', 'neuronal_network'"))
                return

            # Cargar el modelo
            classifier.load(ml_model.id)
            
            # Determinar qué artículos predecir
            articles = []
            if article_id:
                try:
                    article = Article.objects.get(id=article_id)
                    articles = [article]
                    self.stdout.write(f"Prediciendo artículo ID {article_id}")
                except Article.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"No existe un artículo con ID {article_id}"))
                    return
            elif all_unlabeled:
                # Obtener todos los artículos sin etiqueta conocida
                articles = Article.objects.filter(label=Article.UNKNOWN)
                count = articles.count()
                self.stdout.write(f"Prediciendo {count} artículos sin etiqueta")
            else:
                self.stdout.write(self.style.ERROR("Debe especificar --article_id o --all_unlabeled"))
                return
            
            # Realizar las predicciones
            for article in articles:
                try:
                    label, confidence = classifier.predict(article)
                    
                    # Mostrar la predicción
                    label_text = "VERDADERO" if label == Article.TRUE else "FALSO"
                    self.stdout.write(f"Artículo {article.id}: {label_text} (confianza: {confidence:.4f})")
                    
                    # Opcionalmente guardar la predicción
                    if save_prediction:
                        # Guardar como Prediction
                        Prediction.objects.create(
                            article=article,
                            experiment=experiment,
                            prediction=label,
                            confidence=confidence
                        )
                        
                        # Actualizar el artículo
                        article.prediction = label
                        article.prediction_confidence = confidence
                        article.save()
                        
                        self.stdout.write(self.style.SUCCESS(f"Predicción guardada para artículo {article.id}"))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error al predecir artículo {article.id}: {str(e)}"))
                    
            self.stdout.write(self.style.SUCCESS("Proceso de predicción completado"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante la predicción: {str(e)}"))
            import traceback
            self.stdout.write(traceback.format_exc())
