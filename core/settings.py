############ Padrão do projeto  #########################
# Obs: Recomendado a leitura e conhecimentos prévios da arquitetura MVT: https://www.djangoproject.com/start/

################# IMPORTANTE ############################

#
#                Recomendado a visualizaçãao do video para setar o ambiente corretamente:
#                           https://youtu.be/TlrWduZC4Ko

#########################################################

# Aqui está todas as configurações globais do projeto e para isso é preciso conhecimentos da arquitetura do Django como um todo.
# Doc: https://docs.djangoproject.com/en/4.0/topics/settings/
# Lista de varíaveiis e mais configurações: https://docs.djangoproject.com/en/4.0/ref/settings/


#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################
from datetime import timedelta
import os

# Solução utilizada para a implementação do postGIS, serve para indicar onde as dlls da biblioteca estão inseridas. (Visualizar '#importante' no cabeçalho)
if os.name == 'nt':
    OSGEO4W = r"C:\OSGeo4W"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
    GEOS_LIBRARY_PATH = 'C:\\OSGeo4W\\bin\\geos_c.dll'
    GDAL_LIBRARY_PATH = 'C:\\OSGeo4W\\bin\\gdal304.dll'

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!+^9zqq*!1-u*@f_zi4&%2@7$+#p3id4%xwqxf*u^5k6-f9i$1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # Jazzmin app for new template
    'jazzmin',
    #Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Third party Apps
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_simplejwt',
    'djgeojson',
    'corsheaders',
    'drf_yasg',
    #Project Apps
    'api',
    'map',
    'authentication',
]


# Classe de usuário
AUTH_USER_MODEL = 'authentication.Usuario'
LOGIN_URL = '/auth/login/'

# Doc settings
SWAGGER_SETTINGS = {
    'LOGIN_URL': 'auth:login',
    'LOGOUT_URL': 'auth:sair',
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}

# Rest framwork autenticação configurações
REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
	)
}


# Jwt Token configuração
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'UPDATE_LAST_LOGIN': True,

    'AUTH_HEADER_TYPES': ('Bearer','Token',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'pk',
    'USER_ID_CLAIM': 'user_id',

}

# Configurações do APP map
MAP_SETTINGS = {
    "ENDPOINT":"http://localhost:8000/api/",  # Endpoint da aplicação
    "LOADING_INTERVAL":10,                    # Intervalo em milisegundos para renderizar os objetos
}


# Tela de Admin
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": 'Admin',

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": 'Admin',

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": 'Admin',

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "assets/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "assets/logo.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": 'assets/favicon.png',

    # Welcome text on the login screen
    "welcome_sign": 'Painel de Administrador',

    # Copyright on the footer
    "copyright": "Policia Militar da Paraíba",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "authentication.Usuario",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        {"name": "Mapa",  "url": "map:index"},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Doc", "url": "schema-swagger-ui"},

        {"name": "Redoc", "url": "schema-redoc"},
        # model admin to link to (Permissions checked against model)
        {"model": "authentication.Usuario"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "api"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "authentication.Usuario"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ['auth'],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["authentication", 'api'],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        # "books": [{
        #     "name": "Make Messages", 
        #     "url": "make_messages", 
        #     "icon": "fas fa-comments",
        #     "permissions": ["books.view_book"]
        # }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-light",
    "accent": "accent-info",
    "navbar": "navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cerulean",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# Banco de dados postgres local, é necessário setar o ambiente previamente. Ler aviso '#importante' no cabeçalho.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'webgis',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Arquivos estáticos do django estarão na seguinte pasta: 
STATIC_URL = 'static/'

# Após a aplicação ter sido dada deploy é necessário utilizar o middleware whitenoise
if DEBUG:
        STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static')]
else:
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
