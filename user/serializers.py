from rest_framework import serializers
from .models import User
from .utils import send_otp_phone, generate_otp



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phonenumber', 'activated', 'password', 'otp']
        extra_kwargs = {'password': {'write_only': True}}