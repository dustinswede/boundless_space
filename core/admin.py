from django.contrib import admin

from core.models import System, Body, Colony


# Register your models here.

class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'id')


admin.site.register(System, SystemAdmin)
admin.site.register(Body)
admin.site.register(Colony)
