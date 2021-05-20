from django.urls import path, include


from . import views

# TODO - eventually find a better securty
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('systems', views.api.SystemListApiView.as_view(), name='api-systems'),
    path('system/<str:system_id>', views.api.SystemApiView.as_view(), name='api-system'),
    path('system/<str:system_id>/bodies', views.apiBodies, name='api bodies'),

    path('factions', views.apiFactions, name='api factions'),
    path('faction/<str:faction_id>/holdings', views.apiHoldings, name='api faction holdings'),
    path('building_types', views.apiBuildingTypes, name='api-building_types'),

    path('construction_projects', csrf_exempt(views.ConstructionProjectList.as_view()), name='api-construction_projects'),
    path('construction_project/<str:construction_project_id>', views.ConstructionProjectView.as_view(), name='api-construction_project'),

    path('ship_construction_projects', csrf_exempt(views.ShipConstructionProjectList.as_view()), name='api-ship-construction_projects'),
    path('ship_construction_project/<str:project_id>', views.ShipConstructionProjectView.as_view(), name='api-ship-construction_project'),

    path('galaxy', csrf_exempt(views.Galaxy.as_view()), name='api galaxy'),
    path('galaxy/end_round', csrf_exempt(views.EndRound.as_view()), name='api end round'),
    path('cheat', csrf_exempt(views.Cheat.as_view()), name='api cheat'),
]