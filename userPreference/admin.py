from django.contrib import admin
from .models import Categories, userPreference

# Register your models here.
admin.site.register(userPreference)
admin.site.register(Categories)