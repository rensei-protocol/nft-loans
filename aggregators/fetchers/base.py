import string

from django.db import models

from nft_loans.configs.logger import logger


class BaseFetcher:
    model: models.Model
    SUBGRAPH_URL: str
    BATCH_SIZE = 500
    QUERY_BATCH_SIZE = BATCH_SIZE * 2
    IGNORE_CONFLICTS = True

    def __init__(self):
        pass

    def get_common_conditions(self, model) -> string:
        last = model.objects.all().order_by("block_number").last()
        common_cond = f"""
                orderBy: blockNumber
	            orderDirection: asc
	            first: {self.QUERY_BATCH_SIZE}
	            """
        if last:
            common_cond += "where: {blockNumber_gt:" + f'"{last.block_number}"' + "}"
        # print(model, common_cond)
        return common_cond

    def save(self, data: dict):
        try:
            obj = self.model.save(data)
        except Exception as e:
            logger.error(e)
        obj = None
        return obj
