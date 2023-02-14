from django.db import models

from nft_loans.configs.logger import logger


class BaseFetcher:
	model: models.Model
	SUBGRAPH_URL: str
	BATCH_SIZE = 500
	IGNORE_CONFLICTS = True

	def __init__(self):
		pass

	def fetch(self):
		raise NotImplemented

	def save(self, data: dict):
		try:
			obj = self.model.save(data)
		except Exception as e:
			logger.error(e)
		obj = None
		return obj