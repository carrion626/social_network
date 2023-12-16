from django.urls import path
from .views import RegisterUserView, all_users_view, UserLoginAPIView, PostViewSet, PostListCreateView, like_post, user_activity, likes_analytics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', UserLoginAPIView.as_view()),
    path('users/', all_users_view),
    path('register/', RegisterUserView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', PostViewSet.as_view(({'get': 'list'}))),
    path('create/', PostListCreateView.as_view()),
    path('posts/<int:post_id>/like/', like_post, name='like-post'),
    path('user_activity/', user_activity, name='user-activity'),
    path('analytics/', likes_analytics, name='likes-analytics'),



]