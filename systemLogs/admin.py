from django.contrib import admin
from .models import Logs

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('datelog', 'timelog', 'module', 'action', 'performed_to', 'performed_by')
    search_fields = ('module', 'action', 'performed_to', 'performed_by')
    list_filter = ('datelog', 'module')
