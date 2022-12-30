import os
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from openpyxl import Workbook, load_workbook
from humanize import naturaltime
from datetime import datetime, timedelta, time
from .models import *
from .utils import *
from .pdf import render_to_pdf

destiny_path = "/home/gabriel/Documents/catalogRossy/registros/ccobro/"
origen_path = "/home/gabriel/Documents/catalogRossy/registros/"
endDir = ""


def cuentas(request):
    venmesesNova, venmesesLeo, venmesesModa, facmesesNova, facmesesLeo, facmesesModa, cobmesesNova, cobmesesLeo, cobmesesModa = meses()

    if request.method == 'POST':
        docVentNova = request.POST.get('docVentNova')
        docVentLeo = request.POST.get('docVentLeo')
        docVentModa = request.POST.get('docVentModa')
        docFactNova = request.POST.get('docFactNova')
        docFactLeo = request.POST.get('docFactLeo')
        docFactModa = request.POST.get('docFactModa')
        docCreaNova = request.POST.get('docCreaNova')
        docCreaLeo = request.POST.get('docCreaLeo')
        docCreaModa = request.POST.get('docCreaModa')

        cobNova = request.POST.get('cobNova')

        if docVentNova:
            salesName = "NovaVenta"
            month = docVentNova
            ventas = SaleNova.objects.filter(month=docVentNova).values().order_by('comprador')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)
        elif docVentLeo:
            salesName = "Leonisa"
            month = docVentLeo
            ventas = SaleLeonisa.objects.filter(month=docVentLeo).values().order_by('comprador')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)
        elif docVentModa:
            salesName = "Moda Internacional"
            month = docVentModa
            ventas = SaleModa.objects.filter(month=docVentModa).values().order_by('comprador')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)

        if docFactNova:
            salesName = "NovaVenta"
            month = docFactNova
            facturas = FacturaNova.objects.filter(month=docFactNova).values().order_by('codigo')
            context = {"title":"Facturas", 'salesName':salesName, 'month':month, 'facturas':facturas}
            return render(request, "sales/showRemis.html", context)
        elif docFactLeo:
            salesName = "Leonisa"
            month = docFactLeo
            facturas = FacturaLeonisa.objects.filter(month=docFactLeo).values().order_by('codigo')
            context = {"title":"Facturas", 'salesName':salesName, 'month':month, 'facturas':facturas}
            return render(request, "sales/showRemis.html", context)
        elif docFactModa:
            salesName = "Moda Internacional"
            month = docFactModa
            facturas = FacturaModa.objects.filter(month=docFactModa).values().order_by('codigo')
            context = {"title":"Facturas", 'salesName':salesName, 'month':month, 'facturas':facturas}
            return render(request, "sales/showRemis.html", context)

        if docCreaNova:
            salesName = "NovaVenta"
            revista = 'novaventa'
            month = docCreaNova
            selection(revista, month)
            cobros = Cobros.objects.filter(revista=revista, month=month).values().order_by('comprador')
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros}
            return render(request, "sales/showCobros.html", context)
        elif docCreaLeo:
            salesName = "Leonisa"
            revista = 'leonisa'
            month = docCreaLeo
            cobros = Cobros.objects.filter(revista=revista, month=month).values().order_by('comprador')
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros}
            return render(request, "sales/showCobros.html", context)
        elif docCreaModa:
            salesName = "Moda Internacional"
            revista = 'moda'
            month = docCreaModa
            cobros = Cobros.objects.filter(revista=revista, month=month).values().order_by('comprador')
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros}
            return render(request, "sales/showCobros.html", context)

    context = {"title": "Cuentas", 'venmesesNova':venmesesNova, 'facmesesNova':facmesesNova, 'venmesesLeo':venmesesLeo, 'facmesesLeo':facmesesLeo, 'venmesesModa':venmesesModa, 'facmesesModa':facmesesModa, 'cobmesesNova':cobmesesNova, 'cobmesesLeo':cobmesesLeo, 'cobmesesModa':cobmesesModa}
    return render(request, "sales/cuentas.html", context)


def loadXlsxSales(request):
    if request.method == 'POST':
        salesName = request.POST['salesName']
        month = request.POST['month']

        if salesName == "novaventa":
            ventas = SaleNova.objects.all()
            venmeses = allVentas(ventas)
            allfacturas = FacturaNova.objects.all()
            facmeses = allFacturas(allfacturas)
        elif salesName == "leonisa":
            ventas = SaleLeonisa.objects.all()
            venmeses = allVentas(ventas)
            allfacturas = FacturaLeonisa.objects.all()
            facmeses = allFacturas(allfacturas)
        elif salesName == "moda":
            ventas = SaleModa.objects.all()
            venmeses = allVentas(ventas)
            allfacturas = FacturaModa.objects.all()
            facmeses = allFacturas(allfacturas)
        else:
            messages.info(request, 'No se encontro data')
            return redirect('cuentas')

        if month in venmeses:
            messages.warning(request, 'La lista de Ventas de este mes ya esta procesada')
            return redirect('cuentas')
        else:
            xlsFile = request.FILES['inputxlsx']
            sheet = request.POST['sheet']
            nameFile = xlsFile.name
            fileNamex = nameFile.split('.')
            file_tp_pross = origen_path + nameFile
            xlsxFile = pd.read_excel(io=file_tp_pross, engine='openpyxl', sheet_name=sheet, skiprows=0)
            records = len(xlsxFile)
            column_names=xlsxFile.columns.values
            row_data=list(xlsxFile.values.tolist())

            for data in row_data:
                oneData = {
                    'codigo': data[0]
                    , 'cantidad': data[1]
                    , 'precio': data[2]
                    , 'comprador': data[3]
                }
                if salesName == "novaventa":
                    SaleNova.objects.create (codigo=oneData['codigo'], cantidad=oneData['cantidad'], precio=oneData['precio'], comprador=oneData['comprador'], month=month)
                if salesName == "leonisa":
                    SaleLeonisa.objects.create (codigo=oneData['codigo'], cantidad=oneData['cantidad'], precio=oneData['precio'], comprador=oneData['comprador'], month=month)
                if salesName == "moda":
                    SaleModa.objects.create (codigo=oneData['codigo'], cantidad=oneData['cantidad'], precio=oneData['precio'], comprador=oneData['comprador'], month=month)
            
            if month in facmeses:
                createCuentaCobro(salesName, month)
            
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)

    context = {"title": "Registro Ventas"}
    return render(request, "sales/registroSales.html", context)


def loadXlsxFactura(request):
    if request.method == 'POST':
        salesName = request.POST['salesName']
        month = request.POST['month']

        if salesName == "novaventa":
            allventas = SaleNova.objects.all()
            venmeses = allVentas(allventas)
            facturas = FacturaNova.objects.all()
            facmeses = allFacturas(facturas)
        elif salesName == "leonisa":
            allventas = SaleLeonisa.objects.all()
            venmeses = allVentas(allventas)
            facturas = FacturaLeonisa.objects.all()
            facmeses = allFacturas(facturas)
        elif salesName == "moda":
            allventas = SaleModa.objects.all()
            venmeses = allVentas(allventas)
            facturas = FacturaModa.objects.all()
            facmeses = allFacturas(facturas)
        else:
            messages.info(request, 'No se encontro data')
            return redirect('cuentas')

        if month in facmeses:
            messages.warning(request, 'La Factura de ese mes ya esta procesada')
            return redirect('cuentas')
        else:
            xlsFile = request.FILES['inputFactura']
            sheet = request.POST['sheet']
            nameFile = xlsFile.name
            fileNamex = nameFile.split('.')
            file_tp_pross = origen_path + nameFile
            xlsxFile = pd.read_excel(io=file_tp_pross, engine='openpyxl', sheet_name=sheet, skiprows=0)
            records = len(xlsxFile)
            column_names=xlsxFile.columns.values
            row_data=list(xlsxFile.values.tolist())

            for data in row_data:
                oneData = {
                    'codigo': data[0]
                    , 'descripcion': data[1]
                    , 'cantidad': data[2]
                    , 'catalogo':data[3]
                    , 'ganancia':data[4]
                }
                if salesName == "novaventa":
                    FacturaNova.objects.create (
                        codigo=oneData['codigo']
                        , descripcion=oneData['descripcion']
                        , cantidad=oneData['cantidad']
                        , catalogo=oneData['catalogo']
                        , ganancia=oneData['ganancia']
                        , month=month
                    )
                if salesName == "leonisa":
                    FacturaLeonisa.objects.create (
                        codigo=oneData['codigo']
                        , descripcion=oneData['descripcion']
                        , cantidad=oneData['cantidad']
                        , catalogo=oneData['catalogo']
                        , ganancia=oneData['ganancia']
                        , month=month
                    )
                if salesName == "moda":
                    FacturaModa.objects.create (
                        codigo=oneData['codigo']
                        , descripcion=oneData['descripcion']
                        , cantidad=oneData['cantidad']
                        , catalogo=oneData['catalogo']
                        , ganancia=oneData['ganancia']
                        , month=month
                    )

            if month in venmeses:
                print(salesName)
                createCuentaCobro(salesName, month)
            
        if salesName == "novaventa":
            facturas = FacturaNova.objects.all()
        elif salesName == "leonisa":
            facturas = FacturaLeonisa.objects.all()
        elif salesName == "moda":
            facturas = FacturaModa.objects.all()

        context = {"title":"Facturas", 'salesName':salesName, 'month':month, 'facturas':facturas}
        return render(request, "sales/showRemis.html", context)

    context = {"title": "Factura Ventas"}
    return render(request, "sales/registroRemis.html", context)


def test(request):
    revista = "novaventa"
    month = 'Nov22'
    today = datetime.date(datetime.now())
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

    if revista == "novaventa":
        ventas = SaleNova.objects.filter(month=month).values()
        facturas = FacturaNova.objects.filter(month=month).values()

    for venta in ventas:
        for factura in facturas:
            if venta['codigo'] == factura['codigo'] and venta['cantidad'] != factura['cantidad']:
                oneData = {
                    'codigo': factura['codigo']
                    , 'comprador': venta['comprador']
                    , 'descripcion': factura['descripcion']
                    , 'cantidad': venta['cantidad']
                    , 'catalogo': venta['precio']
                    , 'fechaLimite': today
                }
                cuentasCobro.append(oneData)
        for factura in facturas:
            if venta['codigo'] == factura['codigo'] and venta['cantidad'] == factura['cantidad']:
                oneData = {
                    'codigo': factura['codigo']
                    , 'comprador': venta['comprador']
                    , 'descripcion': factura['descripcion']
                    , 'cantidad': venta['cantidad']
                    , 'catalogo': venta['precio']
                    , 'fechaLimite': today
                }
                cuentasCobro.append(oneData)

    
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
            for venta in ventas:
                if cm['codigo'] == venta['codigo'] and cm['cantidad'] >= 1:
                    cm['cantidad'] = cm['cantidad'] - venta['cantidad']
                    od = {
                        'codigo': cm['codigo']
                        , 'comprador': venta['comprador']
                        , 'descripcion': cm['descripcion']
                        , 'cantidad': venta['cantidad']
                        , 'catalogo': venta['precio']
                        , 'fechaLimite': today
                    }
                    masdeuna.append(od)
                elif cm['cantidad'] == 1:
                    if cm['codigo'] not in noesta:
                        cm['cantidad'] = cm['cantidad'] - 1
                        noesta.append(cm)
                        nod = {
                            'codigo': cm['codigo']
                            , 'descripcion': cm['descripcion']
                            , 'cantidad': 1
                            , 'catalogo': venta['precio']
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

        cobros = cuentasCobro
        ventas = noEsta
        facturas = olvidofac

    context = {"title": "Cuentas", 'cobros':cobros, 'ventas':ventas, 'facturas':facturas}
    return render(request, "sales/test.html", context)
