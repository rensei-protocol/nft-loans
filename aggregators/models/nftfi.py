from django.db import models

class NftfiLoan(models.Model):
	loan_id = models.IntegerField(primary_key=True)
	block_time = models.DateTimeField(blank=True, null=True)
	block_number = models.TextField(blank=True, null=True)
	borrower = models.TextField(blank=True, null=True)
	lender = models.TextField(blank=True, null=True)
	loan_principal_amount = models.TextField(blank=True, null=True)
	maximum_repayment_amount = models.TextField(blank=True, null=True)
	nft_collateral_id = models.TextField(blank=True, null=True)
	loan_erc20_denomination = models.TextField(blank=True, null=True)
	loan_duration = models.TextField(blank=True, null=True)
	loan_interest_rate_for_duration_in_basis_points = models.IntegerField(blank=True, null=True)
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