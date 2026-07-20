from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from .models import *
from .permissions import *

# Create your views here.

# -----------------------------------------------
# Helper function
# -----------------------------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# -----------------------------------------------
# 1. Register
# -----------------------------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    def post(self , request):
        print(request.FILES.get('profile_picture'))
        serializers = RegisterSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'User created successfully',
                'user':UserSerializer(user).data,
                'token':tokens,
            },status=status.HTTP_201_CREATED)
        return Response(serializers.errors , status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------
# 2. Login
# -----------------------------------------------
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenSerializer


# class LoginView(APIView):
#     permission_classes = [AllowAny]
    
#     def post(self , request):
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         if not email or not password :
#             return Response({'error':'Email and password are required.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(request , username=email , password=password )
        
#         if not user : 
#             return Response({'error':'Invaled Email Or Password.'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         if not user.is_active : 
#             return Response({'error':'Account Is Disable.'})
        
#         tokens = get_tokens_for_user(user)
#         return Response({
#             'message': 'Login successful',
#             'user':UserSerializer(user).data,
#             'tokens':tokens
#         }, status=status.HTTP_200_OK)


# -----------------------------------------------
# 3. Logout
# -----------------------------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'error':'Refresh token is required.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Logged out successfully'},
                status=status.HTTP_200_OK
            )
        
        except Exception:
            return Response(
                {'error': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


# -----------------------------------------------
# 4. Profile (Get & Update)
# -----------------------------------------------
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self , request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def patch(self , request ):
        serializer = UpdateProfileSerializer(
            instance=request.user,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserSerializer(request.user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {'message': 'Account deactivated successfully'},
            status=status.HTTP_200_OK
        )


# -----------------------------------------------
# 5. Change Password
# -----------------------------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self , request):
        serializer = ChangePasswordSerializer(
            data = request.data,
            context = {'request' : request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Password changed successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------
# 6. Refresh Token
# -----------------------------------------------
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self , request):
        try :
            refresh_token = request.data.get('refresh')
            if not refresh_token :
                return Response(
                        {'error': 'Refresh token is required.'},
                        status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            return Response({
                    'access': str(token.access_token)
                }, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {'error': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


# -----------------------------------------------
# 7. Assign Role
# -----------------------------------------------
class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        serializer = AssignRoleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Role updated to {user.role}',
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=400)


# -----------------------------------------------
# 8. All Users
# -----------------------------------------------
class AllUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrHR]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)





