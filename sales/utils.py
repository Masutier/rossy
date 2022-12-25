from .models import *


def allVentas(allventas):
    venmeses = []
    allventas = allventas
    for ven in allventas:
        if ven.month not in venmeses:
            venmeses.append(ven.month)
    return venmeses


def allFacturas(allfacturas):
    factmeses = []
    allfacturas = allfacturas
    for fact in allfacturas:
        if fact.month not in factmeses:
            factmeses.append(fact.month)
    return factmeses


def meses():
    venmesesNova = []
    venmesesLeo = []
    venmesesModa = []
    facmesesNova = []
    facmesesLeo = []
    facmesesModa = []

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

    return venmesesNova, venmesesLeo, venmesesModa, facmesesNova, facmesesLeo, facmesesModa


def ventasYfacturas(ventas, facturas):
    ventascodes = []
    facturascodes = []
    sillego = []
    nollego = []
    noEsta = []
    olvidos = []
    olvidofac = []
    siVenta = []
    siFact = []
    
    # EXTRACT CODIGOS
    for venta in ventas:
        ventascodes.append(venta.codigo)
    for factura in facturas:
        facturascodes.append(factura.codigo)

    # SEPARA LOS CODIGOS DE LAS VENTAS QUE LLEGARON EN LA FACTURA Y CUALES NO LLEGARON
    for ventacode in ventascodes:
        if ventacode in facturascodes:
            sillego.append(ventacode)
        if ventacode not in facturascodes:
            nollego.append(ventacode)

    # EXTRAE LAS VENTAS Y LAS FACTURAS QUE SI CONCUERDAN
    for vent in sillego:
        for venta in ventas:
            if vent == venta.codigo:
                if venta not in siVenta:
                    siVenta.append(venta)
        for fact in facturas:
            if vent == fact.codigo:
                if fact not in siFact:
                    siFact.append(fact)

    # EXTRAE LAS VENTAS QUE NO ESTAN EN LA FACTURA
    for vent in nollego:
        for venta in ventas:
            if vent == venta.codigo:
                if venta not in noEsta:
                    noEsta.append(venta)

    # SEPARA LOS CODIGOS DE LAS VENTAS QUE NO ESTAN EN LA RELACION PERO SI EN FACTURA
    for facturacode in facturascodes:
        if facturacode not in ventascodes:
            olvidos.append(facturacode)
    for factura in facturas:
        for nofac in olvidos:
            if factura.codigo == nofac:
                olvidofac.append(factura)

    return siVenta, noEsta, olvidofac, siFact