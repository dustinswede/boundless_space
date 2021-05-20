from django.db import models
import uuid

# Tutorial Goals

# Build a ship
	# Build a factory to make more ships
# Create a new colony on mars
# Research hyperlane travel
# Build some buildings to handle issues. (Food, etc) 
# Learn about the civilian faction and their needs.
# Learn to handle factions as they are created. 
	# Gain advisors if you choose not to create factions.

class GalaxyData(models.Model):
	key = models.CharField(max_length=200, primary_key=True, editable=False)
	value = models.IntegerField()

class System(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	position_x = models.IntegerField()
	position_y = models.IntegerField()

class Hyperlane(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	system1 = models.ForeignKey(System, related_name='+', on_delete=models.CASCADE)
	system2 = models.ForeignKey(System, related_name='+', on_delete=models.CASCADE)

class StellarBody(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	system = models.ForeignKey(System, related_name='stellar_bodies', on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	body_type = models.CharField(max_length=200)

	position_x = models.IntegerField()
	position_y = models.IntegerField()

class Faction(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)

class Fleet(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	owner = models.ForeignKey(Faction, related_name='fleets', on_delete=models.CASCADE)

class Species(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)

class Colony(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	stellar_body = models.ForeignKey(StellarBody, related_name='colonies', on_delete=models.CASCADE)

class Holding(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	colony = models.ForeignKey(Colony, related_name='holdings', on_delete=models.CASCADE)
	owner = models.ForeignKey(Faction, related_name='holdings', on_delete=models.CASCADE)

class Demographic(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	colony = models.ForeignKey(Colony, related_name='populations', on_delete=models.CASCADE)
	species = models.ForeignKey(Species, related_name='+', on_delete=models.CASCADE)
	count = models.IntegerField()

class Resource(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	key = models.CharField(max_length=200, unique=True)
	name = models.CharField(max_length=200)

class ResourceDeposit(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	stellar_body = models.ForeignKey(StellarBody, related_name='resource_deposits', on_delete=models.CASCADE)
	resource = models.ForeignKey(Resource, related_name='+', on_delete=models.CASCADE)
	amount = models.PositiveBigIntegerField()

class ResourceStockpile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	holding = models.ForeignKey(Holding, related_name='resource_stockpiles', on_delete=models.CASCADE)
	resource = models.ForeignKey(Resource, related_name='+', on_delete=models.CASCADE)
	amount = models.PositiveBigIntegerField(default=0)

class BuildingType(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	key = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	required_progress = models.PositiveIntegerField(default=0)

class BuidingTypeRequiredResource(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	building_type = models.ForeignKey(BuildingType, related_name='required_resources', on_delete=models.CASCADE)
	resource = models.ForeignKey(Resource, related_name='+', on_delete=models.CASCADE)
	amount = models.PositiveIntegerField()

class ConstructionProject(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	holding = models.ForeignKey(Holding, related_name='construction_projects', on_delete=models.CASCADE)
	building_type = models.ForeignKey(BuildingType, related_name='+', on_delete=models.CASCADE)
	progress = models.PositiveIntegerField(default=0)

class ConstructionProjectAllocatedResource(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	construction_project = models.ForeignKey(ConstructionProject, related_name='allocated_resources', on_delete=models.CASCADE)
	resource = models.ForeignKey(Resource, related_name='+', on_delete=models.CASCADE)
	amount = models.PositiveIntegerField(default=0)

class Building(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	building_type = models.ForeignKey(BuildingType, related_name='+', on_delete=models.CASCADE)
	holding = models.ForeignKey(Holding, related_name='buildings', on_delete=models.CASCADE)
	count = models.PositiveIntegerField(default=1)

class ShipConstructionProject(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	holding = models.ForeignKey(Holding, related_name='ship_construction_projects', on_delete=models.CASCADE)
	ship_type = models.CharField(max_length=200)
	progress = models.PositiveIntegerField(default=0)