"""
WSGI config for giw project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import locale


from django.core.wsgi import get_wsgi_application

"""
Agregamos setLocale para que se vea en Español
la fecha
"""
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giw.settings')

application = get_wsgi_application()
