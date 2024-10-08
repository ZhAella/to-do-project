from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('token/', views.JwtPairAPIView.as_view(), name='token_obtain_pair'),
]
