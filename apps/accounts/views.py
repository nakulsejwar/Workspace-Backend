from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer, RegisterSerializer
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
