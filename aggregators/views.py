from django.shortcuts import render
from django.http import JsonResponse

from .models import ArcadeLoan, BenddaoBorrow, BenddaoLiquidate, BenddaoRedeem, NftfiLoan, NftfiLiquidated, NftfiRepaid, NftfiRenegotiated, X2Y2Loan, X2Y2Liquidation, X2Y2NonceCancelled, X2Y2Repaid


def loans(request):
    x2 = list(X2Y2Loan.objects.values().order_by('-loan_id'))
    res = {
        'data': x2,
    }
    return JsonResponse(res)
