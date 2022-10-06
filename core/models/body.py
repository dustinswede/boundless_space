from django.db import models
import uuid

from core.models.Galaxy import System, Faction

class Body(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System, related_name='bodies', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    x = models.IntegerField()
    y = models.IntegerField()

    def type_text(self):
        return self.type.capitalize()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "bodies"


class Colony(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    population = models.PositiveIntegerField() # TODO - This should eventually cover different species (Demographics)
    body = models.ForeignKey(Body, related_name='colonies', on_delete=models.CASCADE)
    faction = models.ForeignKey(Faction, related_name='colonies', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "colonies"

    def __str__(self):
        return f'{self.faction.name}\'s colony on {self.body.name} '


class Building(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    colony = models.ForeignKey(Colony, related_name='buildings', on_delete=models.CASCADE)