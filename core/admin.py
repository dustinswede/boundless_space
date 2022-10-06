from django.contrib import admin

from core.models.Galaxy import Faction, Fleet, System
from core.models.body import Body, Colony, Building
from core.models.project import Project, ProjectAssignedFleet, ProjectAssignedBody


# Register your models here.
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'id')


class BodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'id')


class ColonyAdmin(admin.ModelAdmin):
    list_display = ('id', 'faction', 'body')


class ProjectAssignedFleetInline(admin.StackedInline):
    model = ProjectAssignedFleet
    extra = 0


class ProjectAssignedBodyInline(admin.StackedInline):
    model = ProjectAssignedBody
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('key', 'faction')
    inlines = [ProjectAssignedFleetInline, ProjectAssignedBodyInline]


admin.site.register(System, SystemAdmin)
admin.site.register(Body, BodyAdmin)
admin.site.register(Colony, ColonyAdmin)
admin.site.register(Faction)
admin.site.register(Fleet)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Building)