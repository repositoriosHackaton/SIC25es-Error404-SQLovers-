from django.core.management.base import BaseCommand
from data_news_api.models import Article
import random
from django.db import transaction

class Command(BaseCommand):
    help = 'Split articles into training, test and validation sets'
    
    def add_arguments(self, parser):
        parser.add_argument('--train', type=float, default=0.7, help='Proportion for training set (default: 0.7)')
        parser.add_argument('--test', type=float, default=0.15, help='Proportion for test set (default: 0.15)')
        parser.add_argument('--validation', type=float, default=0.15, help='Proportion for validation set (default: 0.15)')
        parser.add_argument('--reset', action='store_true', help='Reset existing splits before applying new ones')
    
    @transaction.atomic
    def handle(self, *args, **options):
        train_ratio = options['train']
        test_ratio = options['test']
        validation_ratio = options['validation']
        reset = options['reset']
        
        # Verificar que las proporciones suman 1
        total_ratio = train_ratio + test_ratio + validation_ratio
        if abs(total_ratio - 1.0) > 0.001:
            self.stdout.write(self.style.ERROR(f"Error: proporciones suman {total_ratio}, deben sumar 1.0"))
            return
        
        if reset:
            self.stdout.write("Resetting all dataset assignments...")
            Article.objects.update(
                in_training_set=False,
                in_test_set=False,
                in_validation_set=False
            )
        
        # Obtener artículos sin asignación
        unassigned = Article.objects.filter(
            in_training_set=False,
            in_test_set=False, 
            in_validation_set=False
        )
        
        total = unassigned.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No hay artículos sin asignar. Usa --reset para reasignar todos."))
            return
            
        # Obtener todos los IDs y mezclarlos
        all_ids = list(unassigned.values_list('id', flat=True))
        random.shuffle(all_ids)
        
        # Calcular tamaños de cada conjunto
        train_size = int(total * train_ratio)
        test_size = int(total * test_ratio)
        
        # Dividir IDs
        train_ids = all_ids[:train_size]
        test_ids = all_ids[train_size:train_size + test_size]
        val_ids = all_ids[train_size + test_size:]
        
        # Actualizar cada conjunto
        train_count = Article.objects.filter(id__in=train_ids).update(in_training_set=True)
        test_count = Article.objects.filter(id__in=test_ids).update(in_test_set=True)
        val_count = Article.objects.filter(id__in=val_ids).update(in_validation_set=True)
        
        # Imprimir estadísticas
        self.stdout.write(self.style.SUCCESS(f"✓ División completada:"))
        self.stdout.write(f"- Conjunto de entrenamiento: {train_count} artículos ({train_count/total*100:.1f}%)")
        self.stdout.write(f"- Conjunto de prueba: {test_count} artículos ({test_count/total*100:.1f}%)")
        self.stdout.write(f"- Conjunto de validación: {val_count} artículos ({val_count/total*100:.1f}%)")
        
        # Mostrar estadísticas totales
        total_assigned = Article.objects.filter(
            in_training_set=True
        ).count()
        total_test = Article.objects.filter(in_test_set=True).count()
        total_val = Article.objects.filter(in_validation_set=True).count()
        total_all = Article.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f"\nEstadísticas globales:"))
        self.stdout.write(f"- Total de entrenamiento: {total_assigned} ({total_assigned/total_all*100:.1f}%)")
        self.stdout.write(f"- Total de prueba: {total_test} ({total_test/total_all*100:.1f}%)")
        self.stdout.write(f"- Total de validación: {total_val} ({total_val/total_all*100:.1f}%)")
        self.stdout.write(f"- Sin asignar: {total_all - total_assigned - total_test - total_val}")