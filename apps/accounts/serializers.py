from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    username_field = "email"

    def validate(self, attrs):
        # Map email -> username internally
        attrs["username"] = attrs.get("email")
        return super().validate(attrs)
