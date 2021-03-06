"""smartheart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from courses.views import CourseListView
from deployer.views import deploy_view


api_urls = [
    path('auth/', include('users.api.urls', namespace='users')),
    path('', include('courses.api.urls', namespace='courses')),
]


urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('admin/', admin.site.urls),
    path("update_server/", deploy_view, name="update"),
	path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
	path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('course/', include('courses.urls')),
    path('students/', include('students.urls')),
    path('api/', include(api_urls)),

    # path('api/', include('courses.api.urls', namespace='api')),
    # path('authentication/', include('authentication.urls', namespace='authentication')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)