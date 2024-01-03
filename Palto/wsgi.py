"""
WSGI config for Palto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""


import dotenv
from django.core.wsgi import get_wsgi_application

from utils import env


dotenv.load_dotenv(env.create_dotenv())
application = get_wsgi_application()
