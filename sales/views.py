import os
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from openpyxl import Workbook, load_workbook
from datetime import datetime, timedelta
from .models import *
from .utils import allVentas, allFacturas, ventasYfacturas, meses

destiny_path = "/home/gabriel/Documents/catalogRossy/registros/ccobro/"
origen_path = "/home/gabriel/Downloads/"
endDir = ""


def cuentas(request):
    venmesesNova, venmesesLeo, venmesesModa, facmesesNova, facmesesLeo, facmesesModa, = meses()

    if request.method == 'POST':
        docNova = request.POST.get('docNova')
        docLeo = request.POST.get('docLeo')
        docModa = request.POST.get('docModa')

        if docNova:
            salesName = "NovaVenta"
            month = docNova
            ventas = SaleNova.objects.filter(month=docNova).order_by('codigo')
            facturas = FacturaNova.objects.filter(month=docNova).order_by('codigo')
        elif docLeo:
            salesName = "Leonisa"
            month = docLeo
            ventas = SaleLeonisa.objects.filter(month=docLeo).order_by('codigo')
            facturas = FacturaLeonisa.objects.filter(month=docLeo).order_by('codigo')
        elif docModa:
            salesName = "Moda Internacional"
            month = docModa
            ventas = SaleModa.objects.filter(month=docModa).order_by('codigo')
            facturas = FacturaModa.objects.filter(month=docModa).order_by('codigo')
        else:
            messages.info(request, 'No se encontro data')
            return redirect('cuentas')

        context = {"title": "Ventas y Facturas", 'ventas':ventas, 'facturas':facturas, 'salesName':salesName, 'month':month}
        return render(request, "sales/venFac.html", context)

    context = {"title": "Cuentas", 'venmesesNova':venmesesNova, 'facmesesNova':facmesesNova, 'venmesesLeo':venmesesLeo, 'facmesesLeo':facmesesLeo, 'venmesesModa':venmesesModa, 'facmesesModa':facmesesModa}
    return render(request, "sales/cuentas.html", context)


def loadXlsxSales(request):
    if request.method == 'POST':
        mysales = request.POST['mysales']
        month = request.POST['month']

        if mysales == "novaventa":
            allventas = SaleNova.objects.all()
            venmeses = allVentas(allventas)
        elif mysales == "leonisa":
            allventas = SaleLeonisa.objects.all()
            venmeses = allVentas(allventas)
        elif mysales == "moda":
            allventas = SaleModa.objects.all()
            venmeses = allVentas(allventas)
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
                oneData = {'codigo': data[0], 'cantidad': data[1], 'precio': data[2], 'comprador': data[3]}
                if mysales == "novaventa":
                    SaleNova.objects.create (codigo=oneData['codigo'], cantidad=oneData['cantidad'], precio=oneData['precio'], comprador=oneData['comprador'], month=month)
                if mysales == "leonisa":
                    SaleLeonisa.objects.create (codigo=oneData['codigo'], cantidad=oneData['cantidad'], precio=oneData['precio'], comprador=oneData['comprador'], month=month)
                if mysales == "moda":
                    SaleModa.objects.create (codigo=oneData['codigo'], cantidad=oneData['cantidad'], precio=oneData['precio'], comprador=oneData['comprador'], month=month)

            context={'title': "xlsx Home", 'mysales':mysales, 'month':month, 'column_names':column_names, 'row_data':row_data, 'records':records}
            return render(request, "sales/excelTable.html", context)

    context = {"title": "Registro Ventas"}
    return render(request, "sales/registroSales.html", context)


def loadXlsxFactura(request):
    if request.method == 'POST':
        myFacturas = request.POST['mysales']
        month = request.POST['month']

        if myFacturas == "novaventa":
            allfacturas = FacturaNova.objects.all()
            factmeses = allFacturas(allfacturas)
        elif myFacturas == "leonisa":
            allfacturas = FacturaLeonisa.objects.all()
            factmeses = allFacturas(allfacturas)
        elif myFacturas == "moda":
            allfacturas = FacturaModa.objects.all()
            factmeses = allFacturas(allfacturas)
        else:
            messages.info(request, 'No se encontro data')
            return redirect('cuentas')

        if month in factmeses:
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
                    , 'iva': data[2]
                    , 'cantidad': data[3]
                    , 'valorUn':data[4]
                    , 'valorIva':data[5]
                    , 'subTotal':data[6]
                    , 'total': data[7]
                }
                if myFacturas == "novaventa":
                    FacturaNova.objects.create (
                        codigo=oneData['codigo']
                        , descripcion=oneData['descripcion']
                        , iva=oneData['iva']
                        , cantidad=oneData['cantidad']
                        , valorUn=oneData['valorUn']
                        , valorIva=oneData['valorIva']
                        , subTotal=oneData['subTotal']
                        , total=oneData['total']
                        , month=month
                    )
                if myFacturas == "leonisa":
                    FacturaLeonisa.objects.create (
                        codigo=oneData['codigo']
                        , descripcion=oneData['descripcion']
                        , iva=oneData['iva']
                        , cantidad=oneData['cantidad']
                        , valorUn=oneData['valorUn']
                        , valorIva=oneData['valorIva']
                        , subTotal=oneData['subTotal']
                        , total=oneData['total']
                        , month=month
                    )
                if myFacturas == "moda":
                    FacturaModa.objects.create (
                        codigo=oneData['codigo']
                        , descripcion=oneData['descripcion']
                        , iva=oneData['iva']
                        , cantidad=oneData['cantidad']
                        , valorUn=oneData['valorUn']
                        , valorIva=oneData['valorIva']
                        , subTotal=oneData['subTotal']
                        , total=oneData['total']
                        , month=month
                    )

            context={'title': "Factura Home", 'month':month, 'myFacturas':myFacturas, 'column_names':column_names, 'row_data':row_data, 'records':records}
            return render(request, "sales/excelTable.html", context)

    context = {"title": "Factura Ventas"}
    return render(request, "sales/facturaSales.html", context)


def consultas(request):
    venmesesNova, venmesesLeo, venmesesModa, facmesesNova, facmesesLeo, facmesesModa, = meses()
    if request.method == 'POST':
        docNova = request.POST.get('docNova')
        docLeo = request.POST.get('docLeo')
        docModa = request.POST.get('docModa')

        if docNova:
            salesName = "NovaVenta"
            month = docNova
            ventas = SaleNova.objects.filter(month=docNova).order_by('codigo')
            facturas = FacturaNova.objects.filter(month=docNova).order_by('codigo')
            siVenta, noEsta, olvidofac, siFact = ventasYfacturas(ventas, facturas)
        elif docLeo:
            salesName = "Leonisa"
            month = docLeo
            ventas = SaleLeonisa.objects.filter(month=docLeo).order_by('codigo')
            facturas = FacturaLeonisa.objects.filter(month=docLeo).order_by('codigo')
            siVenta, noEsta, olvidofac, siFact = ventasYfacturas(ventas, facturas)
        elif docModa:
            salesName = "Moda Internacional"
            month = docModa
            ventas = SaleLeonisa.objects.filter(month=docModa).order_by('codigo')
            facturas = FacturaLeonisa.objects.filter(month=docModa).order_by('codigo')
            siVenta, noEsta, olvidofac, siFact = ventasYfacturas(ventas, facturas)

        context = {"title":"Ventas", 'month':month, 'salesName':salesName, 'siVenta':siVenta, 'noEsta':noEsta, 'olvidofac':olvidofac, 'siFact':siFact}
        return render(request, "sales/xx1.html", context)

    context = {"title":"Cuentas de Cobro", 'venmesesNova':venmesesNova, 'facmesesNova':facmesesNova, 'venmesesLeo':venmesesLeo, 'facmesesLeo':facmesesLeo, 'venmesesModa':venmesesModa, 'facmesesModa':facmesesModa}
    return render(request, "sales/xxx.html", context)


def cuentaCobro(request):
    today = datetime.date(datetime.now())
    venmesesNova, venmesesLeo, venmesesModa, facmesesNova, facmesesLeo, facmesesModa, = meses()
    total = 0

    if request.method == 'POST':
        cuentasCobro = []
        docNova = request.POST.get('docNova')
        docLeo = request.POST.get('docLeo')
        docModa = request.POST.get('docModa')

        if docNova:
            salesName = "NovaVenta"
            month = docNova
            ventas = SaleNova.objects.filter(month=docNova).order_by('codigo')
            facturas = FacturaNova.objects.filter(month=docNova).order_by('codigo')
            siVenta, noEsta, olvidofac, siFact = ventasYfacturas(ventas, facturas)

            for sive in siVenta:
                for sifa in siFact:
                    if sive.codigo == sifa.codigo:
                        subTotal = sifa.valorUn * sive.cantidad
                        valorIva = float(subTotal) * (float(sifa.iva) *.01)
                        subTotIva = float(subTotal) + valorIva
                        total = total + valorIva

                        oneData = {
                            'codigo': sifa.codigo
                            , 'comprador': sive.comprador
                            , 'descripcion': sifa.descripcion
                            , 'cantidad': sive.cantidad
                            , 'valorUn': sifa.valorUn
                            , 'subTotal': subTotal
                            , 'iva': sifa.iva
                            , 'valorIva': valorIva
                            , 'subTotIva': subTotIva
                            , 'fechaLimite': today
                        }

                        cuentasCobro.append(oneData)

            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'cuentasCobro':cuentasCobro, 'total':total}
            return render(request, "sales/cuentasCobro.html", context)

        elif docLeo:
            salesName = "Leonisa"
            month = docLeo
            ventas = SaleLeonisa.objects.filter(month=docLeo).order_by('codigo')
            facturas = FacturaLeonisa.objects.filter(month=docLeo).order_by('codigo')
            siVenta, noEsta, olvidofac, siFact = ventasYfacturas(ventas, facturas)

        elif docModa:
            salesName = "Moda Internacional"
            month = docModa
            ventas = SaleLeonisa.objects.filter(month=docModa).order_by('codigo')
            facturas = FacturaLeonisa.objects.filter(month=docModa).order_by('codigo')
            siVenta, noEsta, olvidofac, siFact = ventasYfacturas(ventas, facturas)

    context = {"title":"Cuentas de Cobro", 'venmesesNova':venmesesNova, 'facmesesNova':facmesesNova, 'venmesesLeo':venmesesLeo, 'facmesesLeo':facmesesLeo, 'venmesesModa':venmesesModa, 'facmesesModa':facmesesModa}
    return render(request, "sales/xxx.html", context)
