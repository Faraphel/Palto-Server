"""
Apps for the Palto project.

The app is the configuration for this part of the project.
"""

from django.apps import AppConfig


class PaltoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "Palto.Palto"
    label = "Palto"
