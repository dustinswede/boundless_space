from django.shortcuts import render, redirect
from django.views import View

from galaxy.models import *
from django.http import JsonResponse
import json

class Galaxy(View):
	def get(self, request):
		round = GalaxyData.objects.filter(key='round').first()
		response = JsonResponse({
			'round': round.value,
		})
		response.status_code = 200
		return response

	def put(self, request):
		body = json.loads(request.body)

		if 'template' in body:
			galaxy_templates = GalaxyTemplates()
			class_method = getattr(galaxy_templates, body['template'])
			if class_method:
				class_method()

		response = JsonResponse({})
		response.status_code = 205
		return response

	def post(self, request):
		body = json.loads(request.body)

		# TODO Go to next turn

		response = JsonResponse({})
		response.status_code = 205
		return response

# These functions can be called dynamically. Any function can be called as a template name.
class GalaxyTemplates:
	def tutorial_galaxy(self):
		self.delete_galaxy()

		tutorial_galaxy = TutorialGalaxy()
		tutorial_galaxy.generate()

	def delete_galaxy(self):
		# Delete the old galaxy, everything else cascades off these deletes.
		System.objects.all().delete()
		Faction.objects.all().delete()
		Species.objects.all().delete()
		GalaxyData.objects.all().delete()
		Resource.objects.all().delete()
		BuildingType.objects.all().delete()

# Generate the default "Earth Tutorial" start.
class TutorialGalaxy:
	# A lot of the ids are set to make debugging easier.
	def generate(self):
		galaxy_round = GalaxyData(
			key='round',
			value=0
		)
		galaxy_round.save()

		self.createResources()
		self.createBuildings()

		civilian_faction = Faction(
			id = "a5d3fb41-7157-4991-8bdd-a2a503d48cdb",
			name="Civilian",
		)
		civilian_faction.save()

		self.humans = Species(
			name="Humans",
		)
		self.humans.save()

		self.createSolSystem()
		self.createUEGFaction()

	def createBuildings(self):
		mine = BuildingType(
			key="mine",
			name="Mine",
			required_progress=1,
		)
		mine.save()

		factory = BuildingType(
			key="factory",
			name="Factory",
			required_progress=1,
		)
		factory.save()
		factory_metals = BuidingTypeRequiredResource(
			building_type=factory,
			resource=self.metal,
			amount=10,
		)
		factory_metals.save()

		launch_platform = BuildingType(
			key="launch_platform",
			name="Launch Platform",
			required_progress=5,
		)
		launch_platform.save()
		launch_platform_metals = BuidingTypeRequiredResource(
			building_type=launch_platform,
			resource=self.metal,
			amount=100,
		)
		launch_platform_metals.save()
		launch_platform_ss_parts = BuidingTypeRequiredResource(
			building_type=launch_platform,
			resource=self.spaceship_part,
			amount=50,
		)
		launch_platform_ss_parts.save()

		fuel_refinery = BuildingType(
			key="fuel_refinery",
			name="Fuel Refinery",
			required_progress=5,
		)
		fuel_refinery.save()
		fuel_refinery_metals = BuidingTypeRequiredResource(
			building_type=fuel_refinery,
			resource=self.metal,
			amount=100,
		)
		fuel_refinery_metals.save()

		
	def createResources(self):
		self.metal = Resource(
			key='metal',
			name='Metal',
		)
		self.metal.save()

		self.water = Resource(
			key='water',
			name='Water',
		)
		self.water.save()

		self.spaceship_part = Resource(
			key='spaceship_part',
			name='Spaceship Part',
		)
		self.spaceship_part.save()

		self.hydrogen_fuel = Resource(
			key='liquid_hydrogen_fuel',
			name='Liquid Hydrogen Fuel',
		)
		self.hydrogen_fuel.save()

	def createSolSystem(self):
		sol = System(
			id="6d131270-ac25-4bbe-9fb1-54619e1736c6",
			name="Sol",
			position_x=0,
			position_y=0,
		)
		sol.save()

		sun = StellarBody(
			id="5a0f8f5a-083b-4b48-b8be-db1794337f25",
			system=sol,
			name="Sol",
			body_type="star",
			position_x=0,
			position_y=0,
		)
		sun.save()

		earth = StellarBody(
			id="3cacee75-9cc2-4ecb-bd11-2b1f78b8a775",
			system=sol,
			name="Earth",
			body_type="planet",
			position_x=5,
			position_y=5,
		)
		earth.save()

		earth_metals = ResourceDeposit(
			stellar_body=earth,
			resource=self.metal,
			amount = 5000,
		)
		earth_metals.save()

		earth_water = ResourceDeposit(
			stellar_body=earth,
			resource=self.water,
			amount=1234044241584000000, # In kiloliters # 326000000000000000000 gallons on earth # there is a limit to the size of numbers in sqlite
		)
		earth_water.save()

		self.earth_colony = Colony(
			stellar_body=earth
		)
		self.earth_colony.save()

		earth_population = Demographic(
			colony=self.earth_colony,
			species=self.humans,
			count=10000000000,
		)
		earth_population.save()

		mars = StellarBody(
			id="9fac7389-512d-4893-9624-d64818c61951",
			system=sol,
			name="Mars",
			body_type="planet",
			position_x=-5,
			position_y=5,
		)
		mars.save()

	def createUEGFaction(self):
		faction = Faction(
			id="f792a9bb-d1b6-4290-aa59-6e5e09487db0",
			name="Unified Earth Government",
		)
		faction.save()
		
		earth_holding = Holding(
			id="8bea9a74-5ebc-4fde-abbb-a8fec3a16be1",
			colony=self.earth_colony,
			owner=faction,
		)
		earth_holding.save()