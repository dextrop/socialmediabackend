from rest_framework import serializers
from backendapp.middlewares.caching import get_model_object

class CachedSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        instance = get_model_object(instance.id, self.Meta.name)  # Get the object from cache
        return super(CachedSerializer, self).to_representation(instance)