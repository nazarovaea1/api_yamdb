from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.ApiUserViewSet)

urlpatterns = [
    path('auth/email/', views.SignUpEmail.as_view()),
    path(
        'auth/token/',
        views.MyTokenObtainPairView.as_view()),
    path('users/me/', views.UserProfile.as_view()),
    path('', include(router.urls)),
]
