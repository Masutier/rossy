from .models import *
from datetime import datetime, timedelta


def allVentas(ventas):
    venmeses = []
    for ven in ventas:
        if ven.month not in venmeses:
            venmeses.append(ven.month)
    return venmeses


def allFacturas(facturas):
    factmeses = []
    for fact in facturas:
        if fact.month not in factmeses:
            factmeses.append(fact.month)
    return factmeses


def allCobros(revista):
    cobmeses = []
    allcobros = Cobros.objects.all()
    for cobro in allcobros:
        if cobro.revista == revista:
            if cobro.month not in cobmeses:
                cobmeses.append(cobro.month)
    return cobmeses


def meses():
    venmesesNova = []
    venmesesLeo = []
    venmesesModa = []
    facmesesNova = []
    facmesesLeo = []
    facmesesModa = []
    cobmesesNova = []
    cobmesesLeo = []
    cobmesesModa = []

    allventas = SaleNova.objects.all()
    venmesesNova = allVentas(allventas)
    allventas = SaleLeonisa.objects.all()
    venmesesLeo = allVentas(allventas)
    allventas = SaleModa.objects.all()
    venmesesModa = allVentas(allventas)

    allfacturas = FacturaNova.objects.all()
    facmesesNova = allFacturas(allfacturas)
    allfacturas = FacturaLeonisa.objects.all()
    facmesesLeo = allFacturas(allfacturas)
    allfacturas = FacturaModa.objects.all()
    facmesesModa = allFacturas(allfacturas)

    revista = "novaventa"
    cobmesesNova = allCobros(revista)
    revista = "leonisa"
    cobmesesLeo = allCobros(revista)
    revista = "moda"
    cobmesesModa = allCobros(revista)

    return venmesesNova, venmesesLeo, venmesesModa, facmesesNova, facmesesLeo, facmesesModa, cobmesesNova, cobmesesLeo, cobmesesModa


def myFunc(e):
    return e['comprador']


def createCuentaCobro(salesName, month):
    if salesName == "novaventa":
        ventas = SaleNova.objects.filter(month=month)
        facturas = FacturaNova.objects.filter(month=month)
    elif salesName == "leonisa":
        ventas = SaleLeonisa.objects.filter(month=month)
        facturas = FacturaLeonisa.objects.filter(month=month)
    elif salesName == "moda":
        ventas = SaleModa.objects.filter(month=month)
        facturas = FacturaModa.objects.filter(month=month)
    
    revista = salesName
    month = month
    fechaLimite = (datetime.now() + timedelta(days = 15))

    for venta in ventas:
        for factura in facturas:
            if venta.codigo == factura.codigo:
                codigo = factura.codigo
                comprador = venta.comprador
                cantidad = venta.cantidad
                descripcion = factura.descripcion
                catalogo = factura.catalogo

                Cobros.objects.create (
                    revista = salesName
                    , month = month
                    , codigo = codigo
                    , descripcion = codigo
                    , comprador = comprador
                    , cantidad = cantidad
                    , catalogo = catalogo
                    , fechaLimite = fechaLimite
                )

    return


def selection(revista, month):
    factSele = []
    ventSele = []
    selected = []
    selectedII = []
    if revista == "novaventa":
        ventas = SaleNova.objects.filter(month=month)
        facturas = FacturaNova.objects.filter(month=month)


        for fact in facturas:
            if fact.codigo not in factSele:
                factSele.append(fact.codigo)
                
        for venta in ventas:
            if venta.codigo not in ventSele:
                ventSele.append(venta.codigo)
                
        for vent in ventSele:

            if vent not in factSele and vent not in selected:
                selected.append(vent)

            else:
                if vent not in selectedII:
                    selectedII.append(vent)

        print('sele', selected)
        print('seII', selectedII)


    elif revista == "leonisa":
        ventas = SaleLeonisa.objects.filter(month=month)
        facturas = FacturaLeonisa.objects.filter(month=month)
    elif revista == "moda":
        ventas = SaleModa.objects.filter(month=month)
        facturas = FacturaModa.objects.filter(month=month)



