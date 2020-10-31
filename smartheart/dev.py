from .settings import LOGGING, INSTALLED_APPS, MIDDLEWARE, REST_FRAMEWORK

LOGGING['handlers']['file']['backupCount'] = 1

INSTALLED_APPS += ['corsheaders']
CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')


REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny',]