from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('users/<username>', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('/auth/email/', views.),
    # path('/auth/token/'),
]