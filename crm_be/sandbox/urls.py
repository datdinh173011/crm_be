from django.urls import path
from .views import ImportAPIView, ExportAPIView

urlpatterns = [
    path("import/", ImportAPIView.as_view(), name="import-api"),
    path("export/", ExportAPIView.as_view(), name="export-api"),
]
