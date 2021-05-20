from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.http import JsonResponse
from django.core import serializers

from galaxy.models import *
import json

class EndRound(View):
	def post(self, request):
		buildingProcess = BuildingProcess()
		buildingProcess.runMines()
		buildingProcess.runFactories()
		buildingProcess.runFuelRefineries()

		constructionProcess = ConstructionProcess()
		constructionProcess.build()

		# Update the round
		round = GalaxyData.objects.filter(key='round').first()
		round.value += 1
		round.save()

		return JsonResponse({
			'round': round.value
		})

class ConstructionProcess:
	def build(self):
		projects = ConstructionProject.objects.all()
		for project in projects:
			# ? - Move Construction Ships Around

			# 1 - Allocate local resources (purchase if available)
			fully_allocated_count = 0
			for required_resource in project.building_type.required_resources.all():
				allocated_resource = project.allocated_resources.filter(resource=required_resource.resource).first()
				if not allocated_resource:
					allocated_resource = ConstructionProjectAllocatedResource(
						construction_project=project,
						resource=required_resource.resource
					)

				additional_required = required_resource.amount - allocated_resource.amount
				if additional_required == 0:
					fully_allocated_count += 1
					continue

				faction_stockpile = ResourceStockpile.objects.filter(holding=project.holding, resource=required_resource.resource).first()
				if faction_stockpile and faction_stockpile.amount > 0:
					allocated_resource.amount += min(additional_required, faction_stockpile.amount)
					faction_stockpile.amount = max(faction_stockpile.amount - additional_required, 0)
					faction_stockpile.save()

				# TODO - right now civilian is disabled until other things work
				#civilian_stockpile = ResourceStockpile.objects.filter(holding__stellar_body=project.holding.stellar_body, holding__owner__name="Civilian", resource=required_resource.resource).first()
				#if civilian_stockpile and civilian_stockpile.count > 0:
				#	allocated_resource.value += min(additional_required, civilian_stockpile.count)
				#	civilian_stockpile.value = max(civilian_stockpile.count - additional_required, 0)
				#	civilian_stockpile.save()
				#	# TODO - pay the civilians

				if allocated_resource.amount == required_resource.amount:
					fully_allocated_count += 1
				allocated_resource.save()

			if fully_allocated_count < len(project.building_type.required_resources.all()):
				continue # Not fully allocated

			# 2 - Make process on the construction (based off the workforce?)
			project.progress += 1
			project.save()

			# 3 - Finish construction.
			if project.progress >= project.building_type.required_progress:
				building = Building.objects.filter(holding=project.holding, building_type=project.building_type).first()
				if not building:
					building = Building(
						holding=project.holding,
						building_type=project.building_type,
					)
				else:
					building.count += 1
				building.save()
				project.delete()


class BuildingProcess:
	def runMines(self):
		metal_resource = Resource.objects.filter(key="metal").first()

		mines = Building.objects.filter(building_type__key="mine")
		for mine in mines:
			metal_deposit = mine.holding.colony.stellar_body.resource_deposits.filter(resource=metal_resource).first()
			if metal_deposit:
				stockpile = mine.holding.resource_stockpiles.filter(resource=metal_resource).first()
				if not stockpile:
					stockpile = ResourceStockpile(
						holding = mine.holding,
						resource = metal_resource
					)

				mine_amount = 5 * mine.count
				amount_moved = min(mine_amount, metal_deposit.amount)
				stockpile.amount += amount_moved
				metal_deposit.amount -= amount_moved

				stockpile.save()
				metal_deposit.save()

	def runFactories(self):
		metal_resource = Resource.objects.filter(key="metal").first()
		spaceship_part_resource = Resource.objects.filter(key="spaceship_part").first()
		
		factories = Building.objects.filter(building_type__key="factory")
		for factory in factories:
			metal_stockpile = factory.holding.resource_stockpiles.filter(resource=metal_resource).first()
			if not metal_stockpile:
				continue

			spaceship_part_stockpile = factory.holding.resource_stockpiles.filter(resource=spaceship_part_resource).first()
			if not spaceship_part_stockpile:
				spaceship_part_stockpile = ResourceStockpile(
					holding = factory.holding,
					resource = spaceship_part_resource
				)

			work = min(5 * factory.count, metal_stockpile.amount)
			metal_stockpile.amount -= work
			spaceship_part_stockpile.amount += work

			metal_stockpile.save()
			spaceship_part_stockpile.save()

	def runFuelRefineries(self):
		water = Resource.objects.filter(key="water").first()
		fuel = Resource.objects.filter(key="liquid_hydrogen_fuel").first()

		fuel_refineries = Building.objects.filter(building_type__key="fuel_refinery")

		for fuel_refinery in fuel_refineries:
			water_deposit = fuel_refinery.holding.colony.stellar_body.resource_deposits.filter(resource=water).first()
			if not water_deposit:
				continue

			fuel_stockpile = fuel_refinery.holding.resource_stockpiles.filter(resource=fuel).first()
			if not fuel_stockpile:
				fuel_stockpile = ResourceStockpile(
					holding = fuel_refinery.holding,
					resource = fuel
				)

			work = min(5 * fuel_refinery.count, water_deposit.amount)
			water_deposit.amount -= work
			fuel_stockpile.amount += work

			fuel_stockpile.save()
			water_deposit.save()
