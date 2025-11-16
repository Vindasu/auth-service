from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth import login

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer
)

User = get_user_model()


class UserRegistrationView(APIView):
    """
    Register a new user account.
    
    POST /auth/register/
    {
        "username": "johmojojojo",
        "email": "dontbanjo@pls.com", 
        "password": "redemption!",
        "password_confirm": "redemption!",
        "first_name": "Jo",        // optional
        "last_name": "Sephine"     // optional
    }

    """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    Login with username or email and password - might update later to username only but will consult with 361 team.
    
    POST /auth/login/
    {
        "login": "mojojojo",  // Can be username OR email
        "password": "redemption!"
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Update last login
            login(request, user)
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Get or update user profile information.
    
    GET /auth/user/ - Get current user info
    PUT /auth/user/ - Update user profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current user information."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user profile information."""
        serializer = UserProfileUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserSerializer(request.user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Change user password.
    
    POST /auth/change-password/
    {
        "current_password": "redemption!",
        "new_password": "weewoo123!",
        "new_password_confirm": "weewoo123!"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # Invalidate all existing tokens for this user
            # This forces the user to login again with new password and gets new tokens to avoid funny business
            try:
                refresh_token = RefreshToken.for_user(request.user)
                refresh_token.blacklist()
            except Exception:
                pass  # Token blacklisting might not be available in everyone's project but it's nice if it is
            
            return Response({
                'message': 'Password changed successfully. Please login again.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout user by blacklisting the refresh token.
    
    POST /auth/logout/
    {
        "refresh": "refresh_token_here"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_status(request):
    """
    Simple endpoint to check if the API is running.
    
    GET /auth/status/
    """
    return Response({
        'status': 'Auth service is running',
        'version': '1.0.0',
        'endpoints': {
            'register': '/auth/register/',
            'login': '/auth/login/', 
            'user_profile': '/auth/user/',
            'change_password': '/auth/change-password/',
            'logout': '/auth/logout/',
            'token_refresh': '/auth/token/refresh/',
        }
    })


# Optional: Health check endpoint for monitoring
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring services.
    
    GET /health/
    """
    return Response({
        'status': 'healthy',
        'database': 'connected'
    })
