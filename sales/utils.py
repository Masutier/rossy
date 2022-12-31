from .models import *
from datetime import datetime, timedelta, date


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


def crearCobro(venta, factura, revista, month, fechaLimite):
    if venta.codigo == factura.codigo:
        codigo = factura.codigo
        comprador = venta.comprador
        cantidad = venta.cantidad
        descripcion = factura.descripcion
        catalogo = factura.catalogo

        Cobros.objects.create (
            revista = revista
            , month = month
            , codigo = codigo
            , descripcion = descripcion
            , comprador = comprador
            , cantidad = cantidad
            , catalogo = catalogo
            , fechaLimite = fechaLimite
        )


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
            crearCobro(venta, factura, revista, month, fechaLimite)


def revisarDocumentos(salesName, revista, month):
    if revista == "novaventa":
        ventas = SaleNova.objects.filter(month=month).values()
        facturas = FacturaNova.objects.filter(month=month).values()
        cobros, ventas, facturas = processCobro(revista, ventas, facturas, month)
    elif revista == "leonisa":
        ventas = SaleLeonisa.objects.filter(month=month).values()
        facturas = FacturaLeonisa.objects.filter(month=month).values()
        cobros, ventas, facturas = processCobro(revista, ventas, facturas, month)
    elif revista == "moda":
        ventas = SaleModa.objects.filter(month=month).values()
        facturas = FacturaModa.objects.filter(month=month).values()
        cobros, ventas, facturas = processCobro(revista, ventas, facturas, month)

    return cobros, ventas, facturas


def processCobro(revista, ventas, facturas, month):
    today = date.today()
    fechaLimite = today + timedelta(days=15)
    cobros = Cobros.objects.filter(revista=revista, month=month).values().order_by('comprador')

    facturascodes = []
    ventascodes = []
    sillego = []
    nollego = []
    noEsta = []
    noesta = []
    olvidos = []
    cantimore = []
    masdeuna = []
    olvidofac = []
    cuentasCobro = []

    for factura in facturas:
        facturascodes.append(factura['codigo'])
    for venta in ventas:
        ventascodes.append(venta['codigo'])
    
    # EXTRAE LAS VENTAS QUE NO ESTAN EN LA FACTURA
    for ventacode in ventascodes:
        if ventacode not in facturascodes:
            nollego.append(ventacode)
    for vent in nollego:
        for venta in ventas:
            if vent == venta['codigo']:
                if venta not in noEsta:
                    noEsta.append(venta)

    # EXTRAE LAS VENTAS Y LAS FACTURAS QUE SI CONCUERDAN
    for factura in facturas:
        if factura['cantidad'] > 1:
            cantimore.append(factura)

    for cm in cantimore:
        cm['catalogo'] = cm['catalogo'] / cm['cantidad']
        for venta in ventas:
            if cm['codigo'] == venta['codigo'] and cm['cantidad'] >= 1:
                cm['cantidad'] = cm['cantidad'] - venta['cantidad']

                od = {
                    'codigo': cm['codigo']
                    , 'comprador': venta['comprador']
                    , 'descripcion': cm['descripcion']
                    , 'cantidad': venta['cantidad']
                    , 'catalogo': cm['catalogo']
                    , 'fechaLimite': fechaLimite
                }
                masdeuna.append(od)
            elif cm['cantidad'] == 1:
                if cm['codigo'] not in noesta:
                    cm['cantidad'] = cm['cantidad'] - 1
                    noesta.append(cm)
                    nod = {
                        'id': cm['id']
                        , 'codigo': cm['codigo']
                        , 'descripcion': cm['descripcion']
                        , 'cantidad': 1
                        , 'catalogo': cm['catalogo']
                        , 'month': month
                    }
                    olvidofac.append(nod)

    # SEPARA LOS CODIGOS DE LAS VENTAS QUE NO ESTAN EN LA RELACION PERO SI EN FACTURA
    for facturacode in facturascodes:
        if facturacode not in ventascodes:
            olvidos.append(facturacode)
    for factura in facturas:
        for nofac in olvidos:
            if factura['codigo'] == nofac:
                olvidofac.append(factura)

    ventas = noEsta
    facturas = olvidofac

    return cobros, ventas, facturas
