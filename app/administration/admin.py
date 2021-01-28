from django.contrib import admin
from django.apps import apps
for model in apps.get_app_config('administration').models.values():
    admin.site.register(model)