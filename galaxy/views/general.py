from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.http import JsonResponse
from django.core import serializers

from galaxy.models import *
from galaxy.views.renderers import *

from rest_framework import viewsets, permissions
from galaxy.serializers import SystemSerializer

from rest_framework.exceptions import ValidationError, ParseError
import json
import sys

def index(request):
	context = {}
	return render(request, 'galaxy/index.html', context)

def galaxyMapView(request):
	context = {
		'systems': System.objects.all(),
	}
	return render(request, 'galaxy/galaxy.html', context)

def systemView(request, system_id):
	context = {
		'systems': System.objects.all(),
	}
	return render(request, 'galaxy/system.html', context)

def bodyView(request):
	context = {
		'systems': System.objects.all(),
	}
	return render(request, 'galaxy/body.html', context)

def apiBodies(request, system_id):
	system = get_object_or_404(System, pk=system_id)
	response = []
	for body in StellarBody.objects.filter(system=system):
		deposits = []
		for deposit in body.resource_deposits.all():
			deposits.append({
				'resource': deposit.resource.key,
				'amount': deposit.amount,
			})
		response.append({
			'id': body.id,
			'name': body.name,
			'body_type': body.body_type,
			'position_x': body.position_x,
			'position_y': body.position_y,
			'deposits': deposits,
		})
	return JsonResponse(response, safe=False)

def apiFactions(request):
	response = []
	for faction in Faction.objects.all():
		faction_renderer = FactionRenderer(faction)
		response.append(faction_renderer.toJson())
	return JsonResponse(response, safe=False)

def apiHoldings(request, faction_id):
	response = []
	faction = get_object_or_404(Faction, pk=faction_id)
	for holding in faction.holdings.all():
		resources = []
		for stockpile in holding.resource_stockpiles.all():
			resources.append({
				'key': stockpile.resource.key,
				'amount': stockpile.amount,
			})

		buildings = []
		for building in holding.buildings.all():
			buildings.append({
				'name': building.building_type.name,
				'count': building.count,
			})
		response.append({
			'id': holding.id,
			'on': holding.colony.stellar_body.name,
			'resources': resources,
			'buildings': buildings,
		})
	return JsonResponse(response, safe=False)

def apiBuildingTypes(request):
	response = []
	for building_type in BuildingType.objects.all():
		required_resources = []
		for required_resource in building_type.required_resources.all():
			required_resources.append({
				'resource': required_resource.resource.name,
				'amount': required_resource.amount,
			})

		response.append({
			'id': building_type.id,
			'key': building_type.key,
			'name': building_type.name,
			'required_progress': building_type.required_progress,
			'required_resources': required_resources,
		})
	return JsonResponse(response, safe=False)

class Cheat(View):
	def post(self, request):
		body = json.loads(request.body)

		if body["cheat"] == 'add_resource':
			holding_id = body["holding_id"]
			resource_key = body["resource_key"]
			amount = body["amount"]

			holding = get_object_or_404(Holding, pk=holding_id)
			resource = get_object_or_404(Resource, key=resource_key)

			resource_stockpile = ResourceStockpile.objects.filter(holding=holding, resource=resource).first()
			if not resource_stockpile:
				resource_stockpile = ResourceStockpile(
					holding=holding,
					resource=resource,
				)

			resource_stockpile.amount = max(resource_stockpile.amount + amount, 0)
			resource_stockpile.save()

			response = JsonResponse({
				'holding': holding.colony.stellar_body.name,
				'resource': resource.name,
				'amount': resource_stockpile.amount,
			})
			response.status_code = 205
			return response
		return JsonResponse({}, 400)

class ConstructionProjectView(View):
	def get(self, request, construction_project_id):
		construction_project = get_object_or_404(ConstructionProject, pk=construction_project_id)

		construction_project_renderer = ConstructionProjectRenderer(construction_project)
		render = construction_project_renderer.toJson()

		response = JsonResponse(render)
		response.status_code = 200
		return response

class ConstructionProjectList(View):
	def get(self, request):
		response = []
		for project in ConstructionProject.objects.all():
			construction_project_renderer = ConstructionProjectRenderer(project)
			project_render = construction_project_renderer.toJson()
			response.append(project_render)

		response = JsonResponse(response, safe=False)
		return response

	def put(self, request):
		body = json.loads(request.body)
		faction_id = body['faction_id']
		stellar_body_id = body['stellar_body_id']
		building_key = body['building_key']

		faction = get_object_or_404(Faction, pk=faction_id)
		stellar_body = get_object_or_404(StellarBody, pk=stellar_body_id)

		holding = Holding.objects.filter(owner=faction, colony__stellar_body=stellar_body).first()
		building_type = BuildingType.objects.filter(key=building_key).first()

		project = ConstructionProject(
			holding=holding,
			building_type=building_type
		)
		project.save()

		renderer = ConstructionProjectRenderer(project)
		response = JsonResponse(renderer.toJson())
		response.status_code = 201
		response.headers["Location"] = renderer.route()
		return response

class ShipConstructionProjectList(View):
	def get(self, request):
		response = []
		for project in ShipConstructionProject.objects.all():
			ship_construction_project_renderer = ShipConstructionProjectRenderer(project)
			project_render = ship_construction_project_renderer.toJson()
			response.append(project_render)

		response = JsonResponse(response, safe=False)
		return response

	def put(self, request):
		body = json.loads(request.body)
		faction_id = body['faction_id']
		stellar_body_id = body['stellar_body_id']
		ship_key = body['ship_key']

		faction = get_object_or_404(Faction, pk=faction_id)
		stellar_body = get_object_or_404(StellarBody, pk=stellar_body_id)

		holding = Holding.objects.filter(owner=faction, colony__stellar_body=stellar_body).first()

		project = ShipConstructionProject(
			holding=holding,
			ship_type=ship_key
		)
		project.save()

		if not ship_key in ["construction", "corvette"]:
			raise ParseError

		renderer = ShipConstructionProjectRenderer(project)
		response = JsonResponse(renderer.toJson())
		response.status_code = 201
		response.headers["Location"] = renderer.route()
		return response

class ShipConstructionProjectView(View):
	def get(self, request, project_id):
		project = get_object_or_404(ShipConstructionProject, pk=project_id)

		renderer = ShipConstructionProjectRenderer(project)
		render = renderer.toJson()

		response = JsonResponse(render)
		response.status_code = 200
		return response

class SystemViewSet(viewsets.ModelViewSet):
	queryset = System.objects.all().order_by('id')
	serializer_class = SystemSerializer
	permission_classes = [permissions.IsAuthenticated]