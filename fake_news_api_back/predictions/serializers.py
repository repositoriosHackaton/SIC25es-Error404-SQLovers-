from rest_framework import serializers

class PredictNewsSerializer(serializers.Serializer):
    text = serializers.CharField(
        required=True,
        help_text="Texto de la noticia a analizar"
    )