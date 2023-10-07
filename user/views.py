from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_otp, send_otp_phone
from .models import User, Restaurant, Bonuses
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from .serializers import UserSerializer, RestaurantSerializer, BonusesSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class BonusesViewsSet(viewsets.ModelViewSet):
    queryset = Bonuses.objects.all()
    serializer_class = BonusesSerializer
    permission_classes = [permissions.AllowAny]


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            name = serializer.validated_data['name']
            surname = serializer.validated_data['surname']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=username)
                if user.activated:
                    return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
                otp = generate_otp()
                send_otp_phone(username, otp)
                user.otp = otp
                user.save()
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                otp = generate_otp()
                send_otp_phone(username, otp)
                user = User.objects.create_user(
                    username=username,
                    name = name,
                    surname = surname,
                    password=password,
                    otp=otp
                )
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def validate_registration_otp(self, request):
        username = request.data.get('username', '')
        otp = request.data.get('otp', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None
            user.activated = True
            user.save()

            authenticated_user = authenticate(request=request, username=username, password=password)
            if authenticated_user is not None:
                tokens = RefreshToken.for_user(user)
                return Response({'Access_Token': str(tokens.access_token),
                                'Refresh_Token': str(tokens)}, 
                                status=status.HTTP_200_OK)

        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def login_with_otp(self, request):
        username = request.data.get('username', '')
        otp = request.data.get('otp', '')
        password = request.data.get('password', '')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_phone(username, otp)

        return Response({'message': 'OTP has been sent to your phone number.'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def validate_login_otp(self, request):
        username = request.data.get('username', '')
        otp = request.data.get('otp', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None
            user.save()
# U8JFGGZZWF7LW2HXPAZPKFKT
            authenticated_user = authenticate(request=request, username=username, password=password)
            if authenticated_user is not None:
                tokens = RefreshToken.for_user(user)
                return Response({'Access_Token': str(tokens.access_token),
                                'Refresh_Token': str(tokens)}, 
                                status=status.HTTP_200_OK)

        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def refresh_access_token(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False, methods=['post'])
    def user_logout(self, request):
        try:
            # Delete the user's token to logout
            request.auth.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)