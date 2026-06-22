from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Determine if we're in production based on environment variables
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-z%$5%#--t(sr$bl^uj#+m)5#-u)brj(q!e-1g_=(+sd)m_h142')

# SECURITY WARNING: don't run with debug turned on in production!
# If DEBUG is explicitly set in env, use that value; otherwise use opposite of PRODUCTION
DEBUG_ENV = os.getenv('DEBUG')
if DEBUG_ENV is not None:
    DEBUG = DEBUG_ENV.lower() == 'true'
else:
    DEBUG = not PRODUCTION  # Default: True for development, False for production

# Allowed hosts configuration
if PRODUCTION:
    # Production - use environment variable or empty list for security
    ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',') if host.strip()]
else:
    # Development - allow localhost and 127.0.0.1 for local development
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'django_cleanup.apps.CleanupConfig',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myportfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.latest_resume',  # Add this line

            ],
        },
    },
]

WSGI_APPLICATION = 'myportfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Database configuration - MySQL for production, SQLite for development
if PRODUCTION and os.getenv('DB_NAME'):
    # Production MySQL Database
    try:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.getenv('DB_NAME'),
                'USER': os.getenv('DB_USER'),
                'PASSWORD': os.getenv('DB_PASSWORD'),
                'HOST': os.getenv('DB_HOST', 'localhost'),
                'PORT': os.getenv('DB_PORT', '3306'),
                'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            }
        }
        print("✅ Using MySQL database for production")
    except Exception as e:
        print(f"❌ MySQL configuration error: {e}")
        print("🔄 Falling back to SQLite database")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Development SQLite Database (default)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    if not PRODUCTION:
        print("🔧 Using SQLite database for development")


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Static files configuration based on environment
if PRODUCTION:
    # Production static files configuration
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Use WhiteNoise for static file serving in production
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATICFILES_DIRS = []
    print("📦 Production static files configuration loaded")
else:
    # Development static files configuration
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'app/static'),
    ]
    # Use default static files storage for development
    # STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    print("🔧 Development static files configuration loaded")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Settings for Django
if PRODUCTION and os.getenv('EMAIL_HOST'):
    # Production email configuration
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
    print("📧 Production email configuration loaded")
else:
    # Development email configuration (console backend for testing)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = 'noreply@localhost'
    print("🔧 Development email configuration loaded (console backend)")


TINYMCE_DEFAULT_CONFIG = {
    'height': 500,
    'menubar': True,
    'plugins': 'advlist autolink lists link charmap preview anchor',
    'toolbar': 'undo redo | styleselect | bold italic | bullist numlist outdent indent | link',
    'content_css': '../app/static/css/blogs-detail.css',  # Load your custom CSS
    'valid_elements': '*[*]',  # Allow all elements & attributes
    'forced_root_block': '',  # Prevents adding extra <p> tags
}

X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_BROWSER_XSS_FILTER = True

# Security Settings & CSP
MIDDLEWARE.insert(MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1, 'csp.middleware.CSPMiddleware')

# Strict Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.tiny.cloud")
CSP_IMG_SRC = ("'self'", "data:", "https://*")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_SRC = ("'self'", "https://www.youtube.com", "https://player.vimeo.com")

if PRODUCTION:
    # Production Security Settings
    # HTTPS/SSL Settings
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie Security
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').lower() == 'true'
    
    # Content Security
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    
    # Admin URL Security (optional)
    ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')
    
    print("🔒 Production security settings enabled")
else:
    # Development Security Settings (more relaxed)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    print("🔧 Development security settings (relaxed for local development)")

# Django Jazzmin Settings (Admin Panel UI)
JAZZMIN_SETTINGS = {
    "site_title": "Roshan Admin",
    "site_header": "Portfolio Admin",
    "site_brand": "Roshan's Desk",
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome back, Boss! Time to update the portfolio.",
    "copyright": "Roshan Damor",
    "search_model": ["app.Project", "app.Blog"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Live Site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app.Project": "fas fa-briefcase",
        "app.Blog": "fas fa-pen-nib",
        "app.Skill": "fas fa-star",
        "app.Experience": "fas fa-history",
        "app.FAQ": "fas fa-question-circle",
        "app.ContactMessage": "fas fa-envelope",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}


# Logging Configuration
if PRODUCTION:
    # Production logging to file
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/django.log'),
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
    print("📝 Production logging configured (file-based)")
else:
    # Development logging to console
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    print("🔧 Development logging configured (console-based)")

# Environment Summary
print("\n" + "="*50)
print("🚀 DJANGO PORTFOLIO CONFIGURATION")
print("="*50)
print(f"🎯 Environment: {'Production' if PRODUCTION else 'Development'}")
print(f"🐛 Debug Mode: {'ON' if DEBUG else 'OFF'}")
print(f"💾 Database: {'MySQL' if PRODUCTION and os.getenv('DB_NAME') else 'SQLite'}")
print(f"📧 Email Backend: {'SMTP' if PRODUCTION and os.getenv('EMAIL_HOST') else 'Console'}")
print(f"📦 Static Files: {'Compressed (WhiteNoise)' if PRODUCTION else 'Development'}")
print(f"🔒 Security: {'Enhanced' if PRODUCTION else 'Relaxed'}")
print("="*50 + "\n")
