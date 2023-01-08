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
from .tests import *


destiny_path = "/home/gabriel/Documents/catalogRossy/registros/ccobro/"
origen_path = "/home/gabriel/Documents/catalogRossy/registros/"
endDir = ""


def cuentas(request):
    revista = "novaventa"
    salesMesesNova, invoicesMesesNova, receiptMesesNova = meses(revista)
    revista = "leonisa"
    salesMesesLeo, invoicesMesesLeo, receiptMesesLeo = meses(revista)
    revista = "moda"
    salesMesesModa, invoicesMesesModa, receiptMesesModa = meses(revista)

    if request.method == 'POST':
        if request.POST.get('saleNova'):
            month = request.POST.get('saleNova')
            salesName = "NovaVenta"
            revista = "novaventa"
            ventas = Sale.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)
        elif request.POST.get('saleLeo'):
            month = request.POST.get('saleLeo')
            salesName = "Leonisa"
            revista = "leonisa"
            ventas = Sale.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)
        elif request.POST.get('saleModa'):
            month = request.POST.get('saleModa')
            salesName = "Moda Internacional"
            revista = "moda"
            ventas = Sale.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Ventas", 'salesName':salesName, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)

        elif request.POST.get('invoiceNova'):
            month = request.POST.get('invoiceNova')
            salesName = "NovaVenta"
            revista = "novaventa"
            facturas = Invoice.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Remisiones", 'salesName':salesName, 'month':month, 'facturas':facturas}
            return render(request, "sales/showRemis.html", context)
        elif request.POST.get('invoiceLeo'):
            month = request.POST.get('invoiceLeo')
            salesName = "Leonisa"
            revista = "leonisa"
            facturas = Invoice.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Remisiones", 'salesName':salesName, 'month':month, 'facturas':facturas}
            return render(request, "sales/showRemis.html", context)
        elif request.POST.get('invoiceModa'):
            month = request.POST.get('invoiceModa')
            salesName = "Moda Internacional"
            revista = "moda"
            facturas = Invoice.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Remisiones", 'salesName':salesName, 'month':month, 'facturas':facturas}
            return render(request, "sales/showRemis.html", context)

        elif request.POST.get('receiptNova'):
            month = request.POST.get('receiptNova')
            salesName = "NovaVenta"
            revista = "novaventa"
            cobros = Receipt.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros}
            return render(request, "sales/showCobros.html", context)
        elif request.POST.get('receiptLeo'):
            month = request.POST.get('receiptLeo')
            salesName = "Leonisa"
            revista = "leonisa"
            cobros = Receipt.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros}
            return render(request, "sales/showCobros.html", context)
        elif request.POST.get('receiptModa'):
            month = request.POST.get('receiptModa')
            salesName = "Moda Internacional"
            revista = "moda"
            cobros = Receipt.objects.filter(revista=revista, month=month).values().order_by('codigo')
            context = {"title":"Cobros", 'salesName':salesName, 'month':month, 'cobros':cobros}
            return render(request, "sales/showCobros.html", context)

    context = {
        "title": "Cuentas"
        , 'salesMesesNova':salesMesesNova
        , 'invoicesMesesNova':invoicesMesesNova
        , 'receiptMesesNova':receiptMesesNova
        , 'salesMesesLeo':salesMesesLeo
        , 'invoicesMesesLeo':invoicesMesesLeo
        , 'receiptMesesLeo':receiptMesesLeo
        , 'salesMesesModa':salesMesesModa
        , 'invoicesMesesModa':invoicesMesesModa
        , 'receiptMesesModa':receiptMesesModa
    }
    return render(request, "sales/cuentas.html", context)


def loadXlsxSales(request):
    if request.method == 'POST':
        revista = request.POST['revista']
        month = request.POST['month']

        if revista == "novaventa":
            salesMesesNova, invoicesMesesNova, receiptMesesNova = meses(revista)
            salesMonth = salesMesesNova
            invoicesMonth =invoicesMesesNova
        if revista == "leonisa":
            salesMesesLeo, invoicesMesesLeo, receiptMesesLeo = meses(revista)
            salesMonth = salesMesesLeo
            invoicesMonth = invoicesMesesLeo
        if revista == "moda":
            salesMesesModa, invoicesMesesModa, receiptMesesModa = meses(revista)
            salesMonth = salesMesesModa
            invoicesMonth = invoicesMesesModa

        if month in salesMonth:
            messages.warning(request, 'La Lista de Ventas de este mes ya esta procesada')
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

                Sale.objects.create (
                    revista=revista
                    , codigo=oneData['codigo']
                    , cantidad=oneData['cantidad']
                    , precio=oneData['precio']
                    , comprador=oneData['comprador']
                    , month=month
                )

            if month in invoicesMonth:
                verificaVentas(revista, month)

            ventas = Sale.objects.filter(month=month).values().order_by('codigo')
            context = {"title":"Ventas", 'revista':revista, 'month':month, 'ventas':ventas}
            return render(request, "sales/showSales.html", context)

    context = {"title": "Registro Ventas"}
    return render(request, "sales/registroSales.html", context)


def loadXlsxFactura(request):
    if request.method == 'POST':
        revista = request.POST['revista']
        month = request.POST['month']
        
        if revista == "novaventa":
            salesMesesNova, invoicesMesesNova, receiptMesesNova = meses(revista)
            salesMonth = salesMesesNova
            invoicesMonth = invoicesMesesNova
        elif revista == "leonisa":
            salesMesesLeo, invoicesMesesLeo, receiptMesesLeo = meses(revista)
            salesMonth = salesMesesLeo
            invoicesMonth = invoicesMesesLeo
        elif revista == "moda":
            salesMesesModa, invoicesMesesModa, receiptMesesModa = meses(revista)
            salesMonth = salesMesesModa
            invoicesMonth = invoicesMesesModa

        if month in invoicesMonth:
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
                    , 'precio':data[3]
                    , 'ganancia':data[4]
                }
                Invoice.objects.create (
                    revista=revista
                    , codigo=oneData['codigo']
                    , descripcion=oneData['descripcion']
                    , cantidad=oneData['cantidad']
                    , precio=oneData['precio']
                    , ganancia=oneData['ganancia']
                    , month=month
                )

            if month in salesMonth:
                cobros, facturas, ventas = verificaVentas(revista, month)
                context = {"title":"Facturas", 'revista':revista, 'month':month, 'cobros':cobros, 'facturas':facturas, 'ventas':ventas}
                return render(request, "sales/revisarDocumentos.html", context)

        facturas = Invoice.objects.filter(month=month).values().order_by('codigo')
        context = {"title":"Facturas", 'revista':revista, 'month':month, 'facturas':facturas}
        return render(request, "sales/showRemis.html", context)

    context = {"title": "Factura Ventas"}
    return render(request, "sales/registroRemis.html", context)


def revisarDocumentos(request):
    revista = "novaventa"
    month = 'Nov22'
    cobros, ventas, facturas = verificaVentas(revista, month)
    context = {"title":"Facturas", 'revista':revista, 'month':month, 'cobros':cobros, 'facturas':facturas, 'ventas':ventas}
    return render(request, "sales/revisarDocumentos.html", context)
