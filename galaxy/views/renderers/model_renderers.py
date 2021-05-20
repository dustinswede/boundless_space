from django.urls import reverse

class SystemRenderer:
	def __init__(self, system, show_bodies = True):  
		self.system = system  
		self.show_bodies = show_bodies

	def toJson(self):
		render = {
			'id': self.system.id,
			'location': self.route(),
			'name': self.system.name,
			'position_x': self.system.position_x,
			'position_y': self.system.position_y,
		}

		if self.show_bodies:
			render['bodies'] = []
			for body in self.system.stellar_bodies.all():
				body_renderer = StellarBodyRenderer(body)
				render['bodies'].append(body_renderer.toJson())

		return render

	def route(self):
		return 'system/' + str(self.system.id)

class FactionRenderer:
	def __init__(self, faction, style='full'):
		self.faction = faction

	def toJson(self):
		render = {
			'id': self.faction.id,
			'location': self.route(),
			'name': self.faction.name,
		}
		return render

	def route(self):
		return 'faction/' + str(self.faction.id)

class StellarBodyRenderer:
	def __init__(self, stellar_body):
		self.stellar_body = stellar_body

	def toJson(self):
		render = {
			'id': self.stellar_body.id,
			'location': self.route(),
			'name': self.stellar_body.name,
			'body_type': self.stellar_body.body_type,
			'position_x': self.stellar_body.position_x,
			'position_y': self.stellar_body.position_y,
			'deposits': [],
		}

		for deposit in self.stellar_body.resource_deposits.all():
			render['deposits'].append({
				'resource': deposit.resource.key,
				'amount': deposit.amount,
			})

		return render

	def route(self):
		return None # TODO Body route

class ConstructionProjectRenderer:
	def __init__(self, construction_project):  
		self.construction_project = construction_project  

	def toJson(self):
		project = self.construction_project

		faction_renderer = FactionRenderer(project.holding.owner)
		render = {
			'id': project.id,
			'location': self.route(),
			'building': project.building_type.key,
			'progress': project.progress,
			'required_progress': project.building_type.required_progress,
			'faction': faction_renderer.toJson(),
			'allocated_resources': [],
			'required_resources': [],
		}
		for allocated_resource in project.allocated_resources.all():
			render['allocated_resources'].append({
				'resource': allocated_resource.resource.name,
				'amount': allocated_resource.amount,
			})

		for required_resource in project.building_type.required_resources.all():
			render['required_resources'].append({
				'resource': required_resource.resource.name,
				'amount': required_resource.amount,
			})
		return render

	def route(self):
		return 'construction_project/' + str(self.construction_project.id)

class ShipConstructionProjectRenderer:
	def __init__(self, project):  
		self.project = project  

	def toJson(self):
		faction_renderer = FactionRenderer(self.project.holding.owner)
		render = {
			'id': self.project.id,
			'location': self.route(),
			'ship_type': self.project.ship_type,
			'progress': self.project.progress,
			'required_progress': 10,
			'faction': faction_renderer.toJson(),
		}
		return render

	def route(self):
		return 'ship_construction_project/' + str(self.project.id)
