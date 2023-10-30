# serializers.py
from rest_framework import serializers
from backendapp.models.likes import Likes
from backendapp.serializers.cacheserializer import CachedSerializer


class LikesSerializer(CachedSerializer):

    class Meta:
        name = "likes"
        model = Likes
        fields = '__all__'
