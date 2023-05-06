from django.urls import path

from apps.service_providers import views

urlpatterns = [
    # path("all/", views.ListServiceProviders.as_view(), name="viewallproviders"),
    path(
        "create-provider/",
        views.CreateServiceProviders.as_view(),
        name="create-provider",
    ),
    # path("create-provider/<str:pk>", views.UpdateServiceRetreiveView.as_view(),),
]
