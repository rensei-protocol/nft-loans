from rest_framework import serializers


class DesiredTermsSerializer(serializers.Serializer):
    unit = serializers.CharField(allow_null=True, allow_blank=True)
    currency = serializers.CharField(allow_null=True, allow_blank=True)
    duration = serializers.IntegerField(allow_null=True)
    principal = serializers.FloatField(allow_null=True)
    repayment = serializers.FloatField(allow_null=True)


class BorrowerStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField(allow_null=True)
    active = serializers.IntegerField(allow_null=True)
    defaulted = serializers.IntegerField(allow_null=True)


class TokenTraitSerializer(serializers.Serializer):
    value = serializers.CharField(allow_blank=True, allow_null=True)
    trait = serializers.CharField(allow_blank=True, allow_null=True)


class TokenDataSerializer(serializers.Serializer):
    traits = TokenTraitSerializer(many=True, allow_null=True)
    name = serializers.CharField(allow_null=True, allow_blank=True)
    image_url = serializers.URLField(
        allow_null=True, allow_blank=True, source="imageUrl"
    )
