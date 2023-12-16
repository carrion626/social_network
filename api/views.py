from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import mixins
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, F
from .decorators import update_last_request
from .models import Post
from .serializers import UserProfileSerializer, UserLoginSerializer, PostSerializer



class RegisterUserView(generics.CreateAPIView):
    """
    Register a new user.
    """
    serializer_class = UserProfileSerializer


class UserLoginAPIView(APIView):
    """
    An endpoint to authenticate existing users using their username and password.

     Methods:
      - `post`: Authenticates the user, updates the last login timestamp, and returns JWT tokens.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        user.last_login = timezone.now()
        user.save()

        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)   

    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def all_users_view(request):
    """
    List of all registered users.

    Retrieve a list of all users.

    This endpoint requires authentication using a valid JWT (JSON Web Token).
    """
    users = User.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    


class BasePostView:
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # @update_last_request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(BasePostView, mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for listing posts.

    Inherits from BasePostView and includes mixins for List operations.

    **Endpoint**: `/api/posts/`

    **Methods**:
    - `GET`: List all posts.
    """ 
    pass


class PostListCreateView(BasePostView, generics.ListCreateAPIView):
    """
    View for creating posts.

    Inherits from BasePostView and provides a generic view for handling Create operations.

    **Endpoint**: `/api/create/`

    **Methods**:
    - `GET`: List all posts.
    - `POST`: Create a new post.

    """
    pass


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@update_last_request
def like_post(request, post_id):
    """
    Like or unlike a post.

    This view allows a user to like or unlike a post by providing the post's ID.

    **Endpoint**: `/api/like-post/{post_id}/`

    **Method**: `POST`

    **Authentication**:
    - Requires a valid JWT (JSON Web Token) for authentication.

    **Permissions**:
    - Only authenticated users are allowed.

    **Middleware**:
    - The `update_last_request` middleware is applied to update the user's last request timestamp.

    **Parameters**:
    - `post_id` (int): The ID of the post to like or unlike.

    **Request**:
    - Method: `POST`
    - Endpoint: `/api/like-post/{post_id}/`

    **Response**:
    - Returns the serialized data of the updated post.
    """
    post = get_object_or_404(Post, pk=post_id)

    user = request.user
    if user in post.liked_by.all():
        post.liked_by.remove(user)
        post.likes -= 1
    else:
        post.liked_by.add(user)
        post.likes += 1

    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@update_last_request
def user_activity(request):
    """
    User activity.

    Retrieve user activity information.

    This view returns information about the user's last login and last request timestamp.

    **Endpoint**: `/api/user-activity/`

    **Method**: `GET`

    **Authentication**:
    - Requires a valid JWT (JSON Web Token) for authentication.

    **Permissions**:
    - Only authenticated users are allowed.
    """
    user = request.user
    last_login = user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None
    last_request = user.last_request.strftime('%Y-%m-%d %H:%M:%S') if user.last_request else None

    return Response({'last_login': last_login, 'last_request': last_request})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def likes_analytics(request):
    """
    Analytics for likes.

    Get analytics for post likes.

    Parameters:
    - date_from (string): Start date for analytics (YYYY-MM-DD).
    - date_to (string): End date for analytics (YYYY-MM-DD).

    Returns:
    - list: List of dictionaries with analytics data including date, likes_count, post_id, and user_id.
    """
    date_from_str = request.query_params.get('date_from')
    date_to_str = request.query_params.get('date_to')

    date_from = datetime.strptime(date_from_str, '%Y-%m-%d') if date_from_str else None
    date_to = datetime.strptime(date_to_str, '%Y-%m-%d') if date_to_str else None

    queryset = Post.objects.all()
    if date_from:
        queryset = queryset.filter(created_at__gte=date_from)
    if date_to:
        queryset = queryset.filter(created_at__lte=date_to + timedelta(days=1))

    likes_by_day = (
        queryset
        .annotate(likes_per_day=Count('liked_by', distinct=True), post_id=F('id'), username=F('user'))
        .values('created_at__date', 'likes_per_day', 'post_id', 'username')
    )

    analytics_data = [{'date': like['created_at__date'], 'likes_count': like['likes_per_day'], 'post_id': like['post_id'], 'id of the user who created this post': like['username']} for like in likes_by_day]

    return Response(analytics_data)
