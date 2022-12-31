import os
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from openpyxl import Workbook, load_workbook
from humanize import naturaltime
from datetime import datetime, timedelta, time
from .models import *
from .forms import *
from .utils import *
from .logs import *
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

        impNova = request.POST.get('impNova')

        if docVentNova:
            salesName = "NovaVenta"
            month = docVentNova
            ventas = SaleNova.objects.filter(month=docVentNova).values().order_by('codigo')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)
        elif docVentLeo:
            salesName = "Leonisa"
            month = docVentLeo
            ventas = SaleLeonisa.objects.filter(month=docVentLeo).values().order_by('codigo')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)
        elif docVentModa:
            salesName = "Moda Internacional"
            month = docVentModa
            ventas = SaleModa.objects.filter(month=docVentModa).values().order_by('codigo')
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
            cobros, ventas, facturas = revisarDocumentos(salesName, revista, month)
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros, 'ventas':ventas, 'facturas':facturas}
            return render(request, "sales/showCobros.html", context)
        elif docCreaLeo:
            salesName = "Leonisa"
            revista = 'leonisa'
            month = docCreaLeo
            cobros, ventas, facturas = revisarDocumentos(salesName, revista, month)
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros, 'ventas':ventas, 'facturas':facturas}
            return render(request, "sales/showCobros.html", context)
        elif docCreaModa:
            salesName = "Moda Internacional"
            revista = 'moda'
            month = docCreaModa
            cobros, ventas, facturas = revisarDocumentos(salesName, revista, month)
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros, 'ventas':ventas, 'facturas':facturas}
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
                    SaleNova.objects.create (
                        codigo=oneData['codigo']
                        , cantidad=oneData['cantidad']
                        , precio=oneData['precio']
                        , comprador=oneData['comprador']
                        , month=month
                    )
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

