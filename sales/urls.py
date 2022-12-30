from django.urls import path, include
from .views import *


urlpatterns = [
    path('cuentas', cuentas, name="cuentas"),

    path('loadXlsxSales', loadXlsxSales, name="loadXlsxSales"),
    path('loadXlsxFactura', loadXlsxFactura, name="loadXlsxFactura"),
    path('createCuentaCobro', createCuentaCobro, name="createCuentaCobro"),

    path('test', test, name="test"),

]

