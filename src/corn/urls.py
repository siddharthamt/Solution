from django.urls import path

from corn.views import CornListView


urlpatterns = [
    path("yield", CornListView.as_view(), name="corn_list"),
]
