from rest_framework import serializers

INIT_CHOICES = (
    ('k-means++', 'k-means++'), 
    ('random', 'random')
    )

class KmeansSerializer(serializers.Serializer):
    n_clusters = serializers.IntegerField()
    init = serializers.ChoiceField(choices=INIT_CHOICES, default='k-means++')
    max_iter = serializers.IntegerField(default=300)
    n_init = serializers.IntegerField(default=10)
    random_state = serializers.IntegerField(required=False, default=0)

    