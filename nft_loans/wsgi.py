"""
WSGI config for nft_loans project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nft_loans.settings')

settings.configure(default_settings='nft_loans.settings')

application = get_wsgi_application()
