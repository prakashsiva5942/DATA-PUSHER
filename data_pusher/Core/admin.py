from django.contrib import admin
from .models import Account, Destination, IncomingDataLog

class IncomingDataLogAdmin(admin.ModelAdmin):
    list_display = ('account', 'user_id', 'action', 'created_at', 'response_status')
    search_fields = ('account__account_name', 'user_id', 'action')
    list_filter = ('created_at',)

# Register models
admin.site.register(Account)
admin.site.register(Destination)
admin.site.register(IncomingDataLog, IncomingDataLogAdmin)
