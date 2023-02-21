from django.db import models
from django.db.models import JSONField

from aggregators.models import Collection


class NftfiLoan(models.Model):
    loan_id = models.IntegerField(primary_key=True)
    block_time = models.DateTimeField(blank=True, null=True)
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    borrower = models.TextField(blank=True, null=True)
    lender = models.TextField(blank=True, null=True)
    loan_principal_amount = models.TextField(blank=True, null=True)
    maximum_repayment_amount = models.TextField(blank=True, null=True)
    nft_collateral_id = models.TextField(blank=True, null=True)
    loan_erc20_denomination = models.TextField(blank=True, null=True)
    loan_duration = models.TextField(blank=True, null=True)
    loan_interest_rate_for_duration_in_basis_points = models.IntegerField(
        blank=True, null=True
    )
    loan_admin_fee_in_basic_points = models.IntegerField(blank=True, null=True)
    loan_start_time = models.DateTimeField(blank=True, null=True)
    nft_collateral_contract = models.TextField(blank=True, null=True)
    revenue_share_partner = models.TextField(blank=True, null=True)
    revenue_share_in_basis_points = models.TextField(blank=True, null=True)
    referral_fee_in_basis_points = models.TextField(blank=True, null=True)
    transaction_hash = models.TextField(blank=True, null=True)

    # class Meta:
    # 	managed = False
    # 	db_table = 'nftfi_loans'


class NftfiLiquidated(models.Model):
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    block_time = models.DateTimeField(blank=True, null=True)
    borrower = models.TextField(blank=True, null=True)
    lender = models.CharField(max_length=100, blank=True, null=True)
    loan_id = models.IntegerField(primary_key=True)
    loan_liquidation_date = models.DateTimeField(blank=True, null=True)
    loan_maturity_date = models.DateTimeField(blank=True, null=True)
    loan_principal_amount = models.TextField(blank=True, null=True)
    nft_collateral_contract = models.TextField(blank=True, null=True)
    nft_collateral_id = models.TextField(blank=True, null=True)
    transaction_hash = models.TextField(blank=True, null=True)


class NftfiRepaid(models.Model):
    admin_fee = models.TextField(blank=True, null=True)
    amount_paid_to_lender = models.TextField(blank=True, null=True)
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    block_time = models.DateTimeField(blank=True, null=True)
    borrower = models.TextField(blank=True, null=True)
    lender = models.CharField(max_length=100, blank=True, null=True)
    loan_erc20_denomination = models.TextField(blank=True, null=True)
    loan_id = models.IntegerField(primary_key=True)
    loan_principal_amount = models.TextField(blank=True, null=True)
    nft_collateral_contract = models.TextField(blank=True, null=True)
    nft_collateral_id = models.TextField(blank=True, null=True)
    revenue_share = models.CharField(max_length=30, blank=True, null=True)
    revenue_share_partner = models.TextField(blank=True, null=True)
    transaction_hash = models.TextField(blank=True, null=True)


class NftfiRenegotiated(models.Model):
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    block_time = models.DateTimeField(blank=True, null=True)
    borrower = models.TextField(blank=True, null=True)
    lender = models.CharField(max_length=100, blank=True, null=True)
    loan_id = models.IntegerField(primary_key=True)
    new_loan_duration = models.TextField(blank=True, null=True)
    new_maximum_repayment_amount = models.TextField(blank=True, null=True)
    renegotiation_admin_fee = models.TextField(blank=True, null=True)
    renegotiation_fee = models.TextField(blank=True, null=True)
    transaction_hash = models.TextField(blank=True, null=True)


class NftfiOffer(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    date = models.DateTimeField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    lender = models.CharField(max_length=100)
    lender_nonce = models.TextField(blank=True, null=True)
    borrower = models.TextField(blank=True, null=True)
    referrer = models.TextField(blank=True, null=True)
    loan = JSONField()
    signature = models.TextField(blank=True, null=True)
    nftfi = JSONField(blank=True, null=True)
