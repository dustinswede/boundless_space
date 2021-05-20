from django.views import View
from django.shortcuts import get_object_or_404, render, redirect

from galaxy.models import System
from django.http import JsonResponse
from galaxy.views.renderers import SystemRenderer

class SystemListApiView(View):
	def get(self, request):
		response = []
		for system in System.objects.all():
			renderer = SystemRenderer(system, show_bodies=False)
			response.append(renderer.toJson())
		response = JsonResponse(response, safe=False)
		response.status_code = 200
		return response

class SystemApiView(View):
	def get(self, request, system_id):
		system = get_object_or_404(System, pk=system_id)
		renderer = SystemRenderer(system)

		response = JsonResponse(renderer.toJson(), safe=False)
		response.status_code = 200
		return response
