from rest_framework import serializers

from aggregators.models import ArcadeLoan
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


class OfferFilterSerializer(serializers.Serializer):
    conditions = serializers.JSONField(required=True)
    orderings = serializers.ListSerializer(
        child=serializers.CharField(), allow_empty=True, required=True
    )
    marketplaces = serializers.MultipleChoiceField(
        choices=MARKETPLACES, required=True, allow_empty=False
    )

    def get_queryset(self):
        validated_data = self.validated_data
        validated_data["conditions"]["marketplace__in"] = validated_data["marketplaces"]
        offers = (
            CollectionOffer.objects.filter(**validated_data["conditions"])
            .order_by(*validated_data["orderings"])
            .defer(*CollectionOffer.get_metadata_fieldnames())
        )
        return offers
