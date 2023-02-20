from django.urls import path

from . import views_example

urlpatterns = [
    path("function/", views_example.exampleFunctionView),
    path("viewset/", views_example.ExampleViewSet.as_view({"get": "list"})),
    path("generics/<int:loan_id>/", views_example.ExampleGeneric.as_view()),
]
