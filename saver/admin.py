from django.contrib import admin
from .models import Pack


@admin.register(Pack)
class SiteModelAdmin(admin.ModelAdmin):
    pass
