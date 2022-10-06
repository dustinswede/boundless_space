from django.db import models
import uuid


# The population on a planet/station is divided into populations in factions and independents.
# Independents are the "civilians" on a planet. They do not have any particular faction loyalty.

# Faction have an Ideology which is all the parts of their Culture and Social interactions.
# The culture of the faction has dramatic effect on the gameplay and how you interact with other factions.

# Within a faction there is culture support


class System(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.PositiveIntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Faction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Fleet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    faction = models.ForeignKey(Faction, related_name='fleets', on_delete=models.CASCADE)
    system = models.ForeignKey(System, related_name='fleets', on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.faction.name + ' - ' + self.name


