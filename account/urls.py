from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CommentViewSet, ReviewViewSet
from titles.views import CategoriesViewSet, GenreViewSet, TitleViewSet

from .views import (UserInfo, UserViewSet, get_user_token,
                    send_confirmation_code)


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoriesViewSet)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews')
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='comments')


urlpatterns = [
    path('v1/auth/email/', send_confirmation_code),
    path('v1/auth/token/', get_user_token),
    path('v1/users/me/', UserInfo.as_view()),
    ]

urlpatterns += [
    path('v1/', include(v1_router.urls)),
    ]
