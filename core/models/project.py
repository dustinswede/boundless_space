from django.db import models
import uuid

from core.models.Galaxy import Faction, Fleet
from core.models.body import Body


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=50)
    faction = models.ForeignKey(Faction, related_name='projects', on_delete=models.CASCADE)
    data = models.TextField(null=True)

    def description(self):
        return self.key


class ProjectAssignedFleet(models.Model):
    project = models.ForeignKey(Project, related_name='project_assigned_fleets', on_delete=models.CASCADE)
    fleet = models.ForeignKey(Fleet, related_name='project_assigned_fleets', on_delete=models.CASCADE)
    use_key = models.CharField(max_length=50)


class ProjectAssignedBody(models.Model):
    project = models.ForeignKey(Project, related_name='project_assigned_bodies', on_delete=models.CASCADE)
    body = models.ForeignKey(Body, related_name='project_assigned_bodies', on_delete=models.CASCADE)
    use_key = models.CharField(max_length=50)
