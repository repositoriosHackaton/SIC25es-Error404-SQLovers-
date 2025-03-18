import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sic_backend_ai.settings')
django.setup()

from data_news_api.models import MLModel

def actualizar_algoritmo_modelo(model_id, algoritmo):
    """
    Actualiza el campo 'algorithm' de un modelo existente
    
    Args:
        model_id: ID del modelo a actualizar
        algoritmo: Nuevo valor para el campo algorithm ('random_forest', 'naive_bayes', 'neuronal_network')
    """
    try:
        modelo = MLModel.objects.get(id=model_id)
        print(f"Información actual del modelo ID {model_id}:")
        print(f"  Nombre: {modelo.name}")
        print(f"  Algoritmo: {modelo.algorithm}")
        print(f"  Descripción: {modelo.description}")
        
        # Actualizar el campo de algoritmo
        modelo.algorithm = algoritmo
        modelo.save()
        
        print(f"\nModelo actualizado correctamente:")
        print(f"  Nombre: {modelo.name}")
        print(f"  Algoritmo: {modelo.algorithm}")
        print(f"  Descripción: {modelo.description}")
        
    except MLModel.DoesNotExist:
        print(f"Error: No existe un modelo con ID {model_id}")
    except Exception as e:
        print(f"Error al actualizar el modelo: {str(e)}")

if __name__ == "__main__":
    # Solicitar los valores al usuario
    model_id = input("Ingrese el ID del modelo a actualizar: ")
    print("\nAlgoritmos disponibles:")
    print("1. random_forest")
    print("2. naive_bayes")
    print("3. neuronal_network")
    algoritmo_opcion = input("\nSeleccione el algoritmo (1, 2 o 3): ")
    
    # Validar y convertir los valores
    try:
        model_id = int(model_id)
        algoritmo_opcion = int(algoritmo_opcion)
        
        if algoritmo_opcion == 1:
            algoritmo = "random_forest"
        elif algoritmo_opcion == 2:
            algoritmo = "naive_bayes"
        elif algoritmo_opcion == 3:
            algoritmo = "neuronal_network"
        else:
            print("Opción de algoritmo no válida. Debe ser 1, 2 o 3.")
            exit(1)
            
        # Actualizar el modelo
        actualizar_algoritmo_modelo(model_id, algoritmo)
        
    except ValueError:
        print("Error: El ID del modelo y la opción del algoritmo deben ser números enteros.")
