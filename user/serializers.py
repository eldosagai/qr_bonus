from rest_framework import serializers
from .models import History, User, Restaurant, Bonuses


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'name', 'surname', 
                  'password', 'activated', 'otp', 'status']
        extra_kwargs = {'password': {'write_only': True}}


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['url', 'id', 'name', 'address', 'user']
        
        
class BonusesSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    restaurant_name = serializers.SerializerMethodField()
    restaurant_id = serializers.SerializerMethodField()

    class Meta:
        model = Bonuses
        fields = ['url', 'id', 'amount', 'user', 'username', 'user_id', 'restaurant', 'restaurant_name', 'restaurant_id']
        
    def get_username(self, obj):
        return obj.user.username
    
    def get_user_id(self, obj):
        return obj.user.id
    
    def get_restaurant_name(self, obj):
        return obj.restaurant.name
    
    def get_restaurant_id(self, obj):
        return obj.restaurant.id


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    restaurant_name = serializers.SerializerMethodField()
    restaurant_id = serializers.SerializerMethodField()
    
    class Meta:
        model = History
        fields = ['url', 'id', 'amount', 'user', 'username', 'user_id', 
                  'restaurant', 'restaurant_name', 'restaurant_id']
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_user_id(self, obj):
        return obj.user.id
    
    def get_restaurant_name(self, obj):
        return obj.restaurant.name
    
    def get_restaurant_id(self, obj):
        return obj.restaurant.id