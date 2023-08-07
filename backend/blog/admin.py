from django.contrib import admin
from django.db.models import QuerySet

from .models import *


class ReportAdmin(admin.ModelAdmin):
    list_display = ['text', 'creation_date', 'responded']
    search_fields = ['text']
    list_filter = ['creation_date', 'responded']
    actions = ['set_responded_true']

    @admin.action(description="Отметить как выполнены")
    def set_responded_true(self, request, qs: QuerySet):
        qs.update(responded = True)


admin.site.register(Article)
admin.site.register(Report, ReportAdmin)
