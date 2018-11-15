import django
import os
settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AviationSite.settings")
django.setup()

