from django.urls import path, include
from . import views
from rest_framework import routers
from django.contrib import admin

# TODO - eventually find a better securty
from django.views.decorators.csrf import csrf_exempt

#router = routers.DefaultRouter()
#router.register(r'systems', views.SystemViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('galaxy_map', csrf_exempt(views.galaxyMapView), name='galaxy_map'),
    path('api/v1/', include('galaxy.urls_api_1')),

    #path('api/v2/', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]