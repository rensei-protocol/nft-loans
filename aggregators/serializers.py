from rest_framework import serializers

from aggregators.models import X2Y2Loan


class X2Y2LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = X2Y2Loan
        fields = ["loan_id", "block_number"]
