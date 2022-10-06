from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from core.models.Galaxy import System, Fleet
from core.models.body import Body
from core.models.project import Project


def galaxy_map(request):
    systems = System.objects.all()
    context = {
        'systems': systems
    }
    return render(request, 'core/map/galaxy_map.html', context)


def system_map(request, system_id):
    system = get_object_or_404(System, pk=system_id)
    context = {
        'system': system
    }
    return render(request, 'core/map/system_map.html', context)


def body_details(request, system_id, body_id):
    system = get_object_or_404(System, pk=system_id)
    body = get_object_or_404(Body, pk=body_id)
    context = {
        'system': system,
        'body': body
    }
    return render(request, 'core/map/body_map.html', context)


def fleet_details(request, system_id, fleet_id):
    system = get_object_or_404(System, pk=system_id)
    fleet = get_object_or_404(Fleet, pk=fleet_id)
    context = {
        'system': system,
        'fleet': fleet
    }
    return render(request, 'core/map/fleet_map.html', context)


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


def projects_view(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'core/projects.html', context)


def end_turn(request):
    context = {}
    return render(request, 'core/menu.html', context)


class EndTurn(View):
    def get(self, request):
        return redirect('galaxy_map')

    def post(self, request):
        return redirect('galaxy_map')