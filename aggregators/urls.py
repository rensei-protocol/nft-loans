from django.urls import path

from . import views
from . import views_example

urlpatterns = [
    # examples
    path("function/", views_example.exampleFunctionView),
    path("viewset/", views_example.ExampleViewSet.as_view({"get": "list"})),
    path("generics/<int:loan_id>/", views_example.ExampleGeneric.as_view()),
    # real apis
    path("loans/active/<str:addr>", views.activeLoans),
    path("loans/fulfilled", views.fulfilledLoans),
    # offers
    path("offers/filter", views.get_filtered_offers),
    path("offers/preload/<str:owner>", views.offer_preload_view),
]
