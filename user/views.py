from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_otp, send_otp_phone
from .models import User
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            phonenumber = serializer.validated_data['phonenumber']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=username, phonenumber=phonenumber)
                if user.activated:
                    return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
                otp = generate_otp()
                send_otp_phone(phonenumber, otp)
                user.otp = otp
                user.save()
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                otp = generate_otp()
                send_otp_phone(phonenumber, otp)
                user = User.objects.create_user(
                    username=username,
                    phonenumber=phonenumber,
                    password=password,
                    otp=otp
                )
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def validate_registration_otp(self, request):
        username = request.data.get('username', '')
        phonenumber = request.data.get('phonenumber', '')
        otp = request.data.get('otp', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(username=username, phonenumber=phonenumber)
        except User.DoesNotExist:
            return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None
            user.activated = True
            user.save()

            authenticated_user = authenticate(request=request, username=username, password=password)
            if authenticated_user is not None:
                token, _ = Token.objects.get_or_create(user=authenticated_user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def login_with_otp(self, request):
        phonenumber = request.data.get('phonenumber', '')
        try:
            user = User.objects.get(phonenumber=phonenumber)
        except User.DoesNotExist:
            return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_phone(phonenumber, otp)

        return Response({'message': 'OTP has been sent to your phone number.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def validate_login_otp(self, request):
        username = request.data.get('username', '')
        phonenumber = request.data.get('phonenumber', '')
        otp = request.data.get('otp', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(phonenumber=phonenumber)
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
    def user_logout(self, request):
        try:
            # Delete the user's token to logout
            request.auth.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def register_user(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterOTP(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         username=serializer.validated_data['username'],
#         phonenumber=serializer.validated_data['phonenumber'],
#         password=serializer.validated_data['password'],
#         try:
#             user = User.objects.get(username=username, phonenumber=phonenumber)
#             if user.activated == True:
#                 return Response({'message': 'User already exist'}, status = status.HTTP_400_BAD_REQUEST)
#             otp = generate_otp()
#             send_otp_phone(phonenumber, otp)
#             user.otp = otp
#             user.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         except User.DoesNotExist:
#             if serializer.is_valid():
#                 otp = generate_otp()
#                 send_otp_phone(phonenumber, otp)
#                 user = User.objects.create_user(
#                     username=serializer.validated_data['username'],
#                     phonenumber=serializer.validated_data['phonenumber'],
#                     password=serializer.validated_data['password'],
#                     otp = serializer.validated_data['otp']
#                 )
#                 return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ValidateRegistrationOTP(APIView):
#     def post(self, request):
#         username = request.data.get('username', '')
#         phonenumber = request.data.get('phonenumber', '')
#         otp = request.data.get('otp', '')
#         password = request.data.get('password', '')
        
#         try:
#             user = User.objects.get(username=username, phonenumber=phonenumber)
#         except User.DoesNotExist:
#             return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         if user.otp==otp:
#             user.otp = None
#             user.activated = True
#             user.save()
            
#             authenticate(request=request, username=username, password=password)
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            

# class ValidateLoginOTP(APIView):
#     def post(self, request):
#         username = request.data.get('username', '')
#         phonenumber = request.data.get('phonenumber', '')
#         otp = request.data.get('otp', '')
#         password = request.data.get('password', '')

#         try:
#             user = User.objects.get(phonenumber=phonenumber)
#         except User.DoesNotExist:
#             return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         if user.otp == otp:
#             user.otp = None  # Reset the OTP field after successful validation
#             user.save()

#             authenticate(username=username, password=password)
#             token, _ = Token.objects.get_or_create(user=user)

#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


# class LoginWithOTP(APIView):
#     def post(self, request):
#         phonenumber = request.data.get('phonenumber', '')
#         try:
#             user = User.objects.get(phonenumber=phonenumber)
#         except User.DoesNotExist:
#             return Response({'error': 'User with this phonenumber does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         otp = generate_otp()
#         user.otp = otp
#         user.save()

#         send_otp_phone(phonenumber, otp)

#         return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def user_logout(request):
#     if request.method == 'POST':
#         try:
#             # Delete the user's token to logout
#             request.user.auth_token.delete()
#             return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
