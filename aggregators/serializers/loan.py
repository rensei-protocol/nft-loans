from rest_framework import serializers

from aggregators.models import ArcadeLoan, CurrencyMetadata
from aggregators.models import X2Y2Loan, NftfiLoan, CollectionOffer
from aggregators.models.helper import MARKETPLACES


class X2Y2LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = X2Y2Loan
        fields = [
            "loan_id",
            "block_number",
            "borrower",
            "lender",
            "borrow_amount",
            "borrow_asset",
            "loan_start",
            "loan_end",
            "nft_asset",
            "nft_token_id",
            "loan_repay_amount",
        ]


class NftFiLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = NftfiLoan
        fields = [
            "loan_id",
            "block_number",
            "borrower",
            "lender",
            "loan_principal_amount",
            "maximum_repayment_amount",
            "nft_collateral_contract",
            "nft_collateral_id",
            "loan_start_time",
            "loan_duration",
        ]


class ArcadeLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArcadeLoan
        fields = [
            "loan_id",
            "block_time",
            "block_number",
            "borrower",
            "lender",
            "borrow_amount",
            "borrow_asset",
            "loan_duration",
            "loan_start",
            "loan_end",
            "loan_repay_amount",
            "nft_asset",
            "nft_token_id",
            "txhash",
            "state",
            "num_installments",
            "num_installments_paid",
            "balance",
            "balance_paid",
            "late_fees_accrued",
            "interest_rate",
        ]


class OfferViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionOffer
        exclude = CollectionOffer.get_metadata_fieldnames()


class CollectionThresholdSerializer(serializers.Serializer):
    collection = serializers.CharField(required=True)
    count = serializers.IntegerField(required=True)

    def validate(self, data):
        if data["count"] <= 0:
            raise serializers.ValidationError("count cannot be <= 0!")
        if data["collection"][:2] != "0x":
            raise serializers.ValidationError("address must be valid!")
        return {i["collection"]: i["count"]}


class OfferFilterSerializer(serializers.Serializer):
    conditions = serializers.JSONField(required=True)
    orderings = serializers.ListSerializer(
        child=serializers.CharField(), allow_empty=True, required=True
    )
    marketplaces = serializers.MultipleChoiceField(
        choices=MARKETPLACES, required=True, allow_empty=False
    )
    currency = serializers.CharField(
        required=True,
    )
    amount = serializers.FloatField(required=True)
    threshold = serializers.DictField(required=True, child=serializers.IntegerField())

    def get_queryset(self):
        validated_data = self.validated_data
        validated_data["conditions"]["marketplace__in"] = validated_data["marketplaces"]
        validated_data["conditions"]["currency"] = validated_data["currency"]
        validated_data["conditions"]["collection__in"] = validated_data[
            "threshold"
        ].keys()
        offers = (
            CollectionOffer.objects.filter(**validated_data["conditions"])
            .order_by(*validated_data["orderings"])
            .defer(*CollectionOffer.get_metadata_fieldnames())
        )
        return offers

    def validate_threshold(self, threshold):
        threshold_lowered = {}
        for collection, count in threshold.items():
            if count <= 0:
                raise serializers.ValidationError("count cannot be <= 0!")
            if collection[:2] != "0x":
                raise serializers.ValidationError("address must be valid!")
            threshold_lowered[collection.lower()] = count
        return threshold_lowered

    def validate_currency(self, value):
        try:
            return CurrencyMetadata.objects.get(address__iexact=value)
        except Exception as e:
            raise serializers.ValidationError(e)
