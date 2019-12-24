from .base import *

ALLOWED_HOSTS = ['127.0.0.1','192.168.1.200']

# you cannot have "APP_DIRS" setting simultaneously with 'loaders' option set in "Templates".
# make sure include 'django.template.loaders.app_directories.Loader' in the 'loaders' option under 'Templates'. These two settings are one in the same.
TEMPLATES[0]['APP_DIRS'] = None
TEMPLATES[0]['OPTIONS']['loaders'] =  [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ]


try:
    from .local import *
except ImportError:
    pass
