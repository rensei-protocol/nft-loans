from django.db import models


class X2Y2Loan(models.Model):
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
    nft_is_collection = models.IntegerField(blank=True, null=True)
    txhash = models.TextField(blank=True, null=True)
    fee = models.TextField(blank=True, null=True)
    nonce = models.TextField(blank=True, null=True)

    # class Meta:
    # 	managed = False
    # 	db_table = 'x2y2_loans'


class X2Y2Liquidation(models.Model):
    loan_id = models.IntegerField(primary_key=True)
    block_time = models.DateTimeField(blank=True, null=True)
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    borrower = models.TextField(blank=True, null=True)
    lender = models.TextField(blank=True, null=True)
    borrow_amount = models.TextField(blank=True, null=True)
    nft_asset = models.TextField(blank=True, null=True)
    nft_token_id = models.TextField(blank=True, null=True)
    loan_liquidation_time = models.DateTimeField(blank=True, null=True)
    loan_maturity_time = models.DateTimeField(blank=True, null=True)
    txhash = models.TextField(blank=True, null=True)


# class Meta:
# 	managed = False
# 	db_table = 'x2y2_liquidations'


class X2Y2NonceCancelled(models.Model):
    nonce = models.TextField(blank=True, null=True)
    block_time = models.DateTimeField(blank=True, null=True)
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    lender = models.TextField(blank=True, null=True)
    txhash = models.TextField(blank=True, null=True)

    # class Meta:
    # 	managed = False
    # 	db_table = 'x2y2_nonce_cancelled'


class X2Y2Repaid(models.Model):
    loan_id = models.IntegerField(primary_key=True)
    block_time = models.DateTimeField(blank=True, null=True)
    block_number = models.IntegerField(blank=True, null=True, db_index=True)
    borrower = models.TextField(blank=True, null=True)
    lender = models.TextField(blank=True, null=True)
    borrow_amount = models.TextField(blank=True, null=True)
    borrow_asset = models.TextField(blank=True, null=True)
    loan_repay_amount = models.TextField(blank=True, null=True)
    nft_asset = models.TextField(blank=True, null=True)
    nft_token_id = models.TextField(blank=True, null=True)
    txhash = models.TextField(blank=True, null=True)
    fee = models.TextField(blank=True, null=True)

    # class Meta:
    # 	managed = False
    # 	db_table = 'x2y2_repaids'


class X2Y2Offer(models.Model):
    offer_id = models.TextField(primary_key=True)
    token_id = models.TextField(blank=True, null=True)
    nft_address = models.TextField(blank=True, null=True)
    amount = models.TextField(blank=True, null=True)
    repayment = models.TextField(blank=True, null=True)
    apr = models.IntegerField(blank=True, null=True)
    lender = models.TextField(blank=True, null=True)
    expire_time = models.IntegerField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    erc20_address = models.TextField(blank=True, null=True)
    nonce = models.TextField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)

    # class Meta:
    # 	managed = False
    # 	db_table = 'x2y2_offer'
