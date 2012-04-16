from django.contrib import admin
from models import utility_bill, daily_budget

class UtilityBillAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Service period', {'fields': ['DATE_START', 'DATE_END']}),
        ('Meter reading', {'fields': ['POWER_START', 'POWER_END']}),
        ('Service Cost', {'fields': ['COST']}),
        ]

    list_display = ('DATE_END', 'COST')
    date_hierarchy = 'DATE_END'
    
class DailyBudgetAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date', {'fields': ['date']}),
        ('Daily Budget', {'fields': ['night', 'morning', 'afternoon', 'evening']}),
        ]

    list_display = ('date', 'night', 'morning', 'afternoon', 'evening')
    date_hierarchy = 'date'

admin.site.register(utility_bill, UtilityBillAdmin)
admin.site.register(daily_budget, DailyBudgetAdmin)

