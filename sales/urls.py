from django.urls import path, include
from .views import *

urlpatterns = [
    path('xlsTool', xlsTool, name="xlsTool"),

    path('loadXlsxSales', loadXlsxSales, name="loadXlsxSales"),
    path('loadXlsxFactura', loadXlsxFactura, name="loadXlsxFactura"),


]

