from django.contrib import admin
from .models import Message, CallLog

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__username', 'recipient__username', 'content']

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ['caller', 'receiver', 'call_type', 'status', 'duration', 'started_at']
    list_filter = ['call_type', 'status', 'started_at']
    search_fields = ['caller__username', 'receiver__username']
    readonly_fields = ['started_at', 'ended_at']


# Register your models here.
