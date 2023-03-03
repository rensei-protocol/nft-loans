from django.db.models import Max, Min
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from aggregators.fetchers.nft_metadata import NftscanMetadataFetcher
from aggregators.models import CurrencyMetadata, CollectionOffer, Collection
from aggregators.offers.recommendation_helper import RecommendationKnapsack
from aggregators.offers.recommendation_multi_knapsack import RecommendationKnapsackV2
from aggregators.serializers import (
    CurrencyPreloadSerializer,
    OfferFilterSerializer,
)


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


@api_view(["POST"])
def get_recommended_offers_multi_bin(request):
    serialized = OfferFilterSerializer(data=request.data)
    if not serialized.is_valid():
        return Response(serialized.errors, status=HTTP_400_BAD_REQUEST)

    all_offers = serialized.get_queryset()
    validated_data = serialized.validated_data
    recommendation_handler = RecommendationKnapsackV2(
        all_offers,
        validated_data["currency"],
        validated_data["amount"],
        validated_data["threshold"],
    )
    results = recommendation_handler.get_recommendations()
    # deserialized = OfferViewSerializer(all_offers, many=True).data
    return Response(results, status=HTTP_200_OK)


@api_view(["POST"])
def get_recommended_offers_single_bin(request):
    serialized = OfferFilterSerializer(data=request.data)
    if not serialized.is_valid():
        return Response(serialized.errors, status=HTTP_400_BAD_REQUEST)

    all_offers = serialized.get_queryset()
    validated_data = serialized.validated_data
    recommendation_handler = RecommendationKnapsack(
        all_offers,
        validated_data["currency"],
        validated_data["amount"],
        validated_data["threshold"],
    )
    results = recommendation_handler.get_recommendations()
    # deserialized = OfferViewSerializer(all_offers, many=True).data
    return Response(results, status=HTTP_200_OK)
