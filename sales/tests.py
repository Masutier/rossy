from .models import *
from datetime import datetime, timedelta


def ventasYfacturas(ventas, facturas):
    today = datetime.date(datetime.now())
    cuentasCobro = []
    ventascodes = []
    facturascodes = []
    sillego = []
    nollego = []
    noEsta = []
    noesta = []
    olvidos = []
    olvidofac = []
    cantimore = []
    masdeuna = []
    
    for venta in ventas:
        for factura in facturas:
            if venta.codigo == factura.codigo and venta.cantidad != factura.cantidad:
                oneData = {
                    'codigo': factura.codigo
                    , 'comprador': venta.comprador
                    , 'descripcion': factura.descripcion
                    , 'cantidad': venta.cantidad
                    , 'catalogo': venta.precio
                    , 'fechaLimite': today
                }
                cuentasCobro.append(oneData)
        for factura in facturas:
            if venta.codigo == factura.codigo and venta.cantidad == factura.cantidad:
                oneData = {
                    'codigo': factura.codigo
                    , 'comprador': venta.comprador
                    , 'descripcion': factura.descripcion
                    , 'cantidad': venta.cantidad
                    , 'catalogo': venta.precio
                    , 'fechaLimite': today
                }
                cuentasCobro.append(oneData)

    # EXTRACT CODIGOS
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
    for factura in facturas:
        if factura.cantidad > 1:
            cantimore.append(factura)

    for cm in cantimore:
        for venta in ventas:
            if cm.codigo == venta.codigo and cm.cantidad >= 1:
                cm.cantidad = cm.cantidad - venta.cantidad
                od = {
                    'codigo': cm.codigo
                    , 'comprador': venta.comprador
                    , 'descripcion': cm.descripcion
                    , 'cantidad': venta.cantidad
                    , 'catalogo': venta.precio
                    , 'fechaLimite': today
                }
                masdeuna.append(od)
            elif cm.cantidad == 1:
                if cm.codigo not in noesta:
                    cm.cantidad = cm.cantidad - 1
                    noesta.append(cm)
                    nod = {
                        'codigo': cm.codigo
                        , 'descripcion': cm.descripcion
                        , 'cantidad': 1
                        , 'catalogo': venta.precio
                    }
                    olvidofac.append(nod)

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

    return cuentasCobro, olvidofac, noEsta