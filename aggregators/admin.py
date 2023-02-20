from django.contrib import admin

# Register your models here.
from .models import (
    ArcadeLoan,
    BenddaoBorrow,
    BenddaoLiquidate,
    BenddaoRedeem,
    NftfiLoan,
    NftfiLiquidated,
    NftfiRepaid,
    NftfiRenegotiated,
    X2Y2Loan,
    X2Y2Liquidation,
    X2Y2NonceCancelled,
    X2Y2Repaid,
)


@admin.register(ArcadeLoan)
class ArcadeLoanAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "txhash")


@admin.register(BenddaoBorrow)
class BenddaoBorrowAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "transaction_hash")


@admin.register(BenddaoLiquidate)
class BenddaoLiquidateAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "transaction_hash")


@admin.register(BenddaoRedeem)
class BenddaoRedeemAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "transaction_hash")


@admin.register(NftfiLoan)
class NftfiLoanmAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "transaction_hash")


@admin.register(NftfiLiquidated)
class NftfiLiquidatedAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "transaction_hash")


@admin.register(NftfiRepaid)
class NftfiRepaidAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "transaction_hash")


@admin.register(NftfiRenegotiated)
class NftfiRenegotiatedAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "transaction_hash")


@admin.register(X2Y2Loan)
class X2Y2LoanAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "txhash")


@admin.register(X2Y2Liquidation)
class X2Y2LiquidationAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "txhash")


@admin.register(X2Y2NonceCancelled)
class X2Y2NonceCancelledAdmin(admin.ModelAdmin):
    list_display = ("nonce", "block_time", "txhash")


@admin.register(X2Y2Repaid)
class X2Y2RepaidAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "block_time", "txhash")
