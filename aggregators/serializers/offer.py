import json

from rest_framework import serializers

from aggregators.models import CurrencyMetadata


class CurrencyPreloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyMetadata
        fields = "__all__"


class NFTScanAssetSerializer(serializers.Serializer):
    token_id = serializers.CharField()
    name = serializers.CharField()
    erc_type = serializers.CharField(allow_null=True)
    metadata_json = serializers.JSONField(allow_null=True)

    def to_representation(self, instance):
        core_repr = super().to_representation(instance)
        core_repr["metadata_json"] = (
            json.loads(core_repr["metadata_json"])
            if core_repr["metadata_json"]
            else None
        )

        return core_repr


class NFTScanMetadataSerializer(serializers.Serializer):
    contract_name = serializers.CharField()
    # logo_url = serializers.URLField()
    owns_total = serializers.IntegerField()
    symbol = serializers.CharField()
    assets = NFTScanAssetSerializer(many=True)
