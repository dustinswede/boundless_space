from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.mapView, name='map'),
    path('culture', views.culture, name='culture'),
    path('technology', views.technology, name='technology'),
    path('menu', views.menu, name='menu'),
    path('options', views.options, name='options'),
]