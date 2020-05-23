from rest_framework import serializers

from stories.models import Grapher, Asset


class GrapherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grapher
        fields = ["id"]


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["asset_file"]

    def create(self, validated_data):
        data = {
            'asset_file': validated_data['asset_file'],
            'asset_name': validated_data['asset_file']._name,
            'is_asset_image': True if validated_data['asset_file'].content_type.startswith('image') else False
        }
        return Asset.objects.create(**data)
