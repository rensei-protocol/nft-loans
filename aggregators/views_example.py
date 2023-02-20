from rest_framework import viewsets, mixins, generics

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from aggregators.models import X2Y2Loan
from aggregators.serializers import X2Y2LoanSerializer
from nft_loans.configs.logger import logger


# Function -------------------


@api_view(["GET"])
# @permission_classes((IsAuthenticated,)) #
def exampleFunctionView(request):
    """This is function version of view
    sources:
    1. https://www.django-rest-framework.org/tutorial/1-serialization/#writing-regular-django-views-using-our-serializer
    2. https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
    """
    try:
        queryset = X2Y2Loan.objects.all().order_by("block_number")
        return Response(
            X2Y2LoanSerializer(queryset, many=True).data,
            status=HTTP_200_OK,
        )
    except Exception as e:
        logger.exception(str(e))
        return Response("Not found", status=HTTP_404_NOT_FOUND)


# ViewSet -------------------


class ExampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint with class-based views
    sources:
    1. https://www.django-rest-framework.org/tutorial/3-class-based-views/
    """

    queryset = X2Y2Loan.objects.all().order_by("block_number")
    serializer_class = X2Y2LoanSerializer
    # permission_classes = [permissions.IsAuthenticated] # permission


# Generics -------------------


class ExampleGenericMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Generic with mixin example
    sources:
    1. https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-mixins
    """

    queryset = X2Y2Loan.objects.all()
    serializer_class = X2Y2LoanSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# OR


class ExampleGeneric(generics.RetrieveUpdateDestroyAPIView):
    """Generic with generics example
    sources:
    1. https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views
    """

    queryset = X2Y2Loan.objects.all()
    serializer_class = X2Y2LoanSerializer
    lookup_field = "loan_id"
