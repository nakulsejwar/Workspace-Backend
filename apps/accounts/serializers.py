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


from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
