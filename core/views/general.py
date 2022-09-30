from django.shortcuts import render
from core.models import System


def mapView(request):
    systems = System.objects.all()
    context = {
        'systems': systems
    }
    return render(request, 'core/index.html', context)


def menu(request):
    context = {}
    return render(request, 'core/menu.html', context)


def options(request):
    context = {}
    return render(request, 'core/options.html', context)


def technology(request):
    context = {}
    return render(request, 'core/technology.html', context)


def culture(request):
    context = {}
    return render(request, 'core/culture.html', context)