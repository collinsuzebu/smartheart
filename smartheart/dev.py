from .settings import LOGGING, INSTALLED_APPS, MIDDLEWARE

LOGGING['handlers']['file']['backupCount'] = 1

INSTALLED_APPS += ['corsheaders']
CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication',],
}