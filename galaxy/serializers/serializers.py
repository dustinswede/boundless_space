
from galaxy.models import System
from rest_framework import serializers

class SystemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = System
		fields = ['id', 'name', 'position_x', 'position_y']