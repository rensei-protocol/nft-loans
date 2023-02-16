from django.db import models


# Create your models here.
class ArcadeLoan(models.Model):
    loan_id = models.IntegerField(primary_key=True)
    block_time = models.DateTimeField(blank=True, null=True)
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    borrower = models.TextField(blank=True, null=True)
    lender = models.TextField(blank=True, null=True)
    borrow_amount = models.TextField(blank=True, null=True)
    borrow_asset = models.TextField(blank=True, null=True)
    loan_duration = models.TextField(blank=True, null=True)
    loan_start = models.DateTimeField(blank=True, null=True)
    loan_end = models.DateTimeField(blank=True, null=True)
    loan_repay_amount = models.TextField(blank=True, null=True)
    nft_asset = models.TextField(blank=True, null=True)
    nft_token_id = models.TextField(blank=True, null=True)
    txhash = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    num_installments = models.IntegerField(blank=True, null=True)
    num_installments_paid = models.IntegerField(blank=True, null=True)
    balance = models.TextField(blank=True, null=True)
    balance_paid = models.TextField(blank=True, null=True)
    late_fees_accrued = models.TextField(blank=True, null=True)
    interest_rate = models.TextField(blank=True, null=True)

    # class Meta:
    # 	managed = False
    # 	db_table = 'arcade_loans'
