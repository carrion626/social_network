from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating and retrieving user profiles.

    Parameters:
      - id (int): The unique identifier for the user.
      - email (str): The email address of the user.
      - username (str): The username of the user.
      - password (str): The password of the user.

    Extra Parameters:
      - password (write_only): The password field is write-only to ensure security during creation.

    Methods:
      - create(validated_data): Creates a new user with the provided validated data and returns the user instance.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates a new user with the provided validated data.

        Args:
          - validated_data (dict): Validated data containing user information.

        Returns:
          - User: The created user instance.
        """
        user = User.objects.create_user(**validated_data)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with username and password.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates the provided data by authenticating the user with the given credentials.

        Args:
          - data (dict): The data containing username and password.

        Returns:
          - User: The authenticated user instance.

        Raises:
          - serializers.ValidationError: Raised if the provided credentials are incorrect.
        """
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating and retrieving posts.

    Parameters:
      - id (int): The unique identifier for the post.
      - user (int): The user ID associated with the post.
      - content (str): The content of the post.
      - created_at (datetime): The timestamp when the post was created.
    """
    class Meta:
        model = Post
        fields = "__all__"
