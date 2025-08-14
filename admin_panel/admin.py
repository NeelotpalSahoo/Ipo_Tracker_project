from django.contrib import admin
from .models import IPO

@admin.register(IPO)
class IPOAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'status', 'open_date', 'close_date', 'listing_date')
    search_fields = ('company_name',)
    list_filter = ('status', 'issue_type')
