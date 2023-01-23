from .models import *
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.db.models import Count
import pandas as pd


def testing(request):
    revista = "novaventa"
    month = "Nov22"
    faccode = []
    vencode = []
    ventas2 = []
    ventas3 = []
    sillego = []
    sillego2 = []
    sillego3 = []
    sillego4 = []
    sillego5 = []
    nollego = []
    nollego2 = []
    olvidocode = []
    olvidos = []
    olvidos2 = []

    ventas = Sale.objects.filter(revista=revista, month=month)
    for venta in ventas:
        vencode.append(venta.codigo)
    facturas = Invoice.objects.filter(revista=revista, month=month)
    for factura in facturas:
        faccode.append(factura.codigo)

    # CUENTA DUPLICADOS EN VENTAS
    salesDuplicates = Sale.objects.values('codigo').annotate(codigo_count=Count('codigo')).filter(revista=revista, month=month, codigo_count__gt=0)

    # LISTA DE TODO LO QUE SI LLEGO ASI FALTEN DUPLICADOS
    for sd in salesDuplicates:
        qty = 0
        for venta in ventas:
            if sd['codigo'] == venta.codigo:
                qty = qty + venta.cantidad
                precio = venta.precio
                comprador = 'varios'
        ventas2.append({
            'codigo':sd['codigo']
            , 'cantidad':qty
            , 'precio':precio
            })

    # sillego2 == VENTAS LLEGARON COMPLETAS, SOLO CODIGO
    # ventas2 == VENTAS LLEGARON INCOMPLETAS O NO LLEGARON SOLO CODIGO
    # sillego3 == LA INFO DE VENTAS COMPLETA
    # ventas3 == VENTAS QUE NO LLEGARON
    for factura in facturas:
        for venta2 in ventas2:
            if factura.codigo == venta2['codigo'] and factura.cantidad == venta2['cantidad']:
                sillego2.append(venta2)
                ventas2.remove(venta2)
            if factura.codigo == venta2['codigo'] and factura.cantidad > venta2['cantidad']:
                sillego4.append(venta2)
                noEsta = factura.cantidad - venta2['cantidad']
                venta2['cantidad'] = noEsta
                ventas3.append(venta2)
                ventas2.remove(venta2)
                olvidos2.append(venta2)
            if factura.codigo == venta2['codigo'] and factura.cantidad < venta2['cantidad']:
                noEsta = venta2['cantidad'] - factura.cantidad
                venta2['cantidad'] = noEsta
                sillego5.append(venta2)
                ventas3.append(venta2)
    for venta in ventas:
        for sill2 in sillego2:
            if venta.codigo == sill2['codigo']:
                if venta not in sillego3:
                    sillego3.append(venta)
        for sill4 in sillego4:
            if venta.codigo == sill4['codigo']:
                if venta not in sillego3:
                    sillego3.append(venta)
        for sill5 in sillego5:
            if venta.codigo == sill5['codigo']:
                if venta not in sillego3:
                    venta.cantidad = sill5['cantidad']
                    sillego3.append(venta)
        # NO LLEGO
        for venta2 in ventas2:
            if venta.codigo == venta2['codigo']:
                if venta not in nollego:
                    nollego.append(venta)

    # sillego == UNION DE sillego2 CON FACTURA Y FECHA == db --> Receipt
    for factura in facturas:
        for sill3 in sillego3:
            if factura.codigo == sill3.codigo:
                today = date.today()
                fechaLimite = today + timedelta(days=15)
                sillego.append({
                    'revista':revista
                    , 'month':month
                    , 'codigo':sill3.codigo
                    , 'comprador':sill3.comprador
                    , 'descripcion':factura.descripcion
                    , 'cantidad':sill3.cantidad
                    , 'precio':sill3.precio
                    , 'fechaLimite':fechaLimite
                    })
    
    ############     createCuentaCobro(sillego)

    # SE OLVIDO
    for fcode in faccode:
        if fcode not in vencode:
            olvidocode.append(fcode)
    for factura in facturas:
        for code in olvidocode:
            if factura.codigo == code:
                olvidos.append(factura)
        for olvido in olvidos2:
            if factura.codigo == olvido['codigo']:
                factura.cantidad = olvido['cantidad']
                olvidos.append(factura)


    context = {"title": "Testing", 'sillego':sillego, 'nollego':nollego, 'olvidos':olvidos}
    return render(request, "sales/test.html", context)
