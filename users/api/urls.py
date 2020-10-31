from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = 'users'

urlpatterns = [

    path('signup/', views.user_create, name='sign-up'),
    path('login/', views.user_login, name='login'),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token-create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('protected/', views.protected, name='protected'),

]