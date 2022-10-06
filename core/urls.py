from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.galaxy_map, name='index'),
    path('map', views.galaxy_map, name='galaxy_map'),
    path('map/<uuid:system_id>', views.system_map, name='system_map'),
    path('map/<uuid:system_id>/body/<uuid:body_id>', views.body_details, name='body_details'),
    path('map/<uuid:system_id>/fleet/<uuid:fleet_id>', views.fleet_details, name='fleet_details'),
    path('culture', views.culture, name='culture'),
    path('technology', views.technology, name='technology'),
    path('projects', views.projects_view, name='projects'),
    path('menu', views.menu, name='menu'),
    path('options', views.options, name='options'),
    path('end_turn', views.EndTurn.as_view(), name='end_turn')
]