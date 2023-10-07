from rest_framework import serializers
from .models import User, Restaurant, Bonuses


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'name', 'surname', 'password', 'activated', 'otp', 'status']
        extra_kwargs = {'password': {'write_only': True}}


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['url', 'id', 'name', 'address', 'user']
        
        
class BonusesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bonuses
        fields = ['ur', 'id', 'amount', 'user', 'restaurant']