from django.urls import path, include
from .views import *


urlpatterns = [
    path('cuentas', cuentas, name="cuentas"),

    path('loadXlsxSales', loadXlsxSales, name="loadXlsxSales"),
    path('loadXlsxFactura', loadXlsxFactura, name="loadXlsxFactura"),
    path('createCuentaCobro', createCuentaCobro, name="createCuentaCobro"),

    path('revisarDocumentos', revisarDocumentos, name="revisarDocumentos"),
    path('adicionarVenta', adicionarVenta, name="adicionarVenta"),
    path('modificarVenta/<int:pk>', modificarVenta, name="modificarVenta"),
    path('modificarRemision/<int:pk>', modificarRemision, name="modificarRemision"),

]
