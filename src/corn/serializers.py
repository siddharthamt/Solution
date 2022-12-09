from rest_framework import serializers

from corn.models import Corn


class CornSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corn
        fields = ["year", "corn_yield", "created_at", "updated_at"]
