from django.contrib import admin
from .models import PlantCheck


@admin.register(PlantCheck)
class PlantCheckAdmin(admin.ModelAdmin):
    list_display = ['user', 'check_type', 'severity', 'confidence_score', 'created_at']
    list_filter = ['check_type', 'severity', 'created_at']
    search_fields = ['user__username', 'result_title', 'result_summary']
    readonly_fields = ['created_at']
