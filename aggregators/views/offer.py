from django.db.models import Max, Min
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from aggregators.fetchers.nft_metadata import NftscanMetadataFetcher
from aggregators.models import CurrencyMetadata, CollectionOffer, Collection
from aggregators.serializers import CurrencyPreloadSerializer


@api_view(["GET"])
def offer_preload_view(request, owner):
    if owner[:2] != "0x":
        return Response("owner format is not correct!", HTTP_400_BAD_REQUEST)
    existing_currencies = (
        CollectionOffer.objects.all()
        .distinct("erc20_address")
        .values_list("erc20_address", flat=True)
    )
    min_max_fields = CollectionOffer.objects.all().aggregate(
        Max("apr"), Min("apr"), Max("duration"), Min("duration")
    )
    nfts = NftscanMetadataFetcher.fetch_nfts_by_owner(owner)
    preload_obj = {
        "currencies": CurrencyPreloadSerializer(
            CurrencyMetadata.objects.filter(address__in=existing_currencies), many=True
        ).data,
        "nfts": nfts,
        "supported_collections": Collection.get_all_collections(),
        **min_max_fields,
    }
    return Response(preload_obj, status=HTTP_200_OK)
