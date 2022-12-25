from django.urls import path, include
from .views import *

urlpatterns = [
    path('cuentas', cuentas, name="cuentas"),

    # NOVAVENTA

    # LEONISA

    # MODA

    path('consultas', consultas, name="consultas"),
    path('cuentaCobro', cuentaCobro, name="cuentaCobro"),
    path('loadXlsxSales', loadXlsxSales, name="loadXlsxSales"),
    path('loadXlsxFactura', loadXlsxFactura, name="loadXlsxFactura"),

]

