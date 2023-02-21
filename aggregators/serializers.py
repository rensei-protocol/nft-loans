from rest_framework import serializers

from aggregators.models import X2Y2Loan, NftfiLoan


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
