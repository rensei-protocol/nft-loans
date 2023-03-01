# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from aggregators.models import (
    NftfiLoan,
    NftfiLiquidated,
    NftfiRepaid,
    X2Y2Loan,
    X2Y2Repaid,
    X2Y2Liquidation,
    ArcadeLoan,
    ArcadeLoanRepaid,
    ArcadeLoanRolledOver,
    ArcadeLoanClaimed,
)
from aggregators.serializers import (
    X2Y2LoanSerializer,
    NftFiLoanSerializer,
    OfferFilterSerializer,
    OfferViewSerializer,
    ArcadeLoanSerializer,
)
from nft_loans.configs.logger import logger


@api_view(["GET"])
def fulfilledLoans(request):
    try:
        x2y2QuerySet = (
            X2Y2Loan.objects.all()
            .order_by("loan_id")
            .exclude(
                loan_id__in=X2Y2Liquidation.objects.all().values_list(
                    "loan_id", flat=True
                )
            )
            .exclude(
                loan_id__in=X2Y2Repaid.objects.all().values_list("loan_id", flat=True)
            )
        )
        nftfiQuerySet = (
            NftfiLoan.objects.all()
            .order_by("loan_id")
            .exclude(
                loan_id__in=NftfiLiquidated.objects.all().values_list(
                    "loan_id", flat=True
                )
            )
            .exclude(
                loan_id__in=NftfiRepaid.objects.all().values_list("loan_id", flat=True)
            )
        )
        x2y2loan = []
        nftfiloan = []

        if x2y2QuerySet is not None:
            x2y2loan = X2Y2LoanSerializer(x2y2QuerySet, many=True).data
        if nftfiQuerySet is not None:
            nftfiloan = NftFiLoanSerializer(nftfiQuerySet, many=True).data

        loans = {
            "x2y2": x2y2loan,
            "nftfi": nftfiloan,
        }
        return Response(loans, status=HTTP_200_OK)

    except Exception as e:
        logger.exception(str(e))
        return Response(e, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def activeLoans(request, addr):
    try:
        x2y2QuerySet = (
            X2Y2Loan.objects.filter(borrower__iexact=addr)
            .order_by("loan_id")
            .exclude(
                loan_id__in=X2Y2Liquidation.objects.all().values_list(
                    "loan_id", flat=True
                )
            )
            .exclude(
                loan_id__in=X2Y2Repaid.objects.all().values_list("loan_id", flat=True)
            )
        )
        nftfiQuerySet = (
            NftfiLoan.objects.filter(borrower__iexact=addr)
            .order_by("loan_id")
            .exclude(
                loan_id__in=NftfiLiquidated.objects.all().values_list(
                    "loan_id", flat=True
                )
            )
            .exclude(
                loan_id__in=NftfiRepaid.objects.all().values_list("loan_id", flat=True)
            )
        )
        arcadeQuerySet = (
            ArcadeLoan.objects.filter(borrower__iexact=addr)
            .order_by("loan_id")
            .exclude(
                loan_id__in=ArcadeLoanRepaid.objects.all().values_list(
                    "loan_id", flat=True
                )
            )
            .exclude(
                loan_id__in=ArcadeLoanClaimed.objects.all().values_list(
                    "loan_id", flat=True
                )
            )
            .exclude(
                loan_id__in=ArcadeLoanRolledOver.objects.all().values_list(
                    "old_loan_id", flat=True
                )
            )
        )

        x2y2loan = []
        nftfiloan = []
        arcadeloan = []

        if x2y2QuerySet is not None:
            x2y2loan = X2Y2LoanSerializer(x2y2QuerySet, many=True).data
        if nftfiQuerySet is not None:
            nftfiloan = NftFiLoanSerializer(nftfiQuerySet, many=True).data
        if arcadeQuerySet is not None:
            arcadeloan = ArcadeLoanSerializer(arcadeQuerySet, many=True).data

        loans = {"x2y2": x2y2loan, "nftfi": nftfiloan, "arcade": arcadeloan}
        return Response(loans, status=HTTP_200_OK)

    except Exception as e:
        logger.exception(str(e))
        return Response(e, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_filtered_offers(request):
    serialized = OfferFilterSerializer(data=request.data)
    if not serialized.is_valid():
        return Response(serialized.errors, status=HTTP_400_BAD_REQUEST)

    all_offers = serialized.get_queryset()
    deserialized = OfferViewSerializer(all_offers, many=True).data
    return Response(deserialized, status=HTTP_200_OK)
