from django.db import models

class BenddaoBorrow(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	block_number = models.IntegerField()
	loan_id = models.IntegerField()
	user = models.TextField()
	on_behalf_of = models.TextField(blank=True, null=True)
	nft_token_id = models.CharField(max_length=20)
	nft_asset = models.CharField(max_length=100)
	transaction_hash = models.TextField(blank=True, null=True)
	reserve = models.TextField(blank=True, null=True)
	referral = models.IntegerField(blank=True, null=True)
	borrow_rate = models.TextField(blank=True, null=True)
	block_timestamp = models.DateTimeField(blank=True, null=True)
	amount = models.TextField()


class BenddaoLiquidate(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	block_number = models.IntegerField()
	block_timestamp = models.DateTimeField(blank=True, null=True)
	borrower = models.TextField()
	loan_id = models.IntegerField()
	nft_asset = models.CharField(max_length=100)
	nft_token_id = models.CharField(max_length=20)
	remain_amount = models.TextField()
	repay_amount = models.TextField()
	reserve = models.TextField(blank=True, null=True)
	transaction_hash = models.TextField(blank=True, null=True)
	user = models.TextField()


class BenddaoRedeem(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	block_number = models.IntegerField()
	block_timestamp = models.DateTimeField(blank=True, null=True)
	borrow_amount = models.TextField()
	borrower = models.TextField()
	fine_amount = models.TextField()
	loan_id = models.IntegerField()
	nft_asset = models.CharField(max_length=100)
	nft_token_id = models.CharField(max_length=20)
	reserve = models.TextField(blank=True, null=True)
	transaction_hash = models.TextField(blank=True, null=True)
	user = models.TextField()