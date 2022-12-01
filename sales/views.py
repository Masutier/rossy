import os
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from openpyxl import Workbook, load_workbook
from .models import *

destiny_path = "/home/gabriel/Downloads/catalogRossy/registros/ccobro/"
origen_path = "/home/gabriel/Downloads/catalogRossy/registros/"
endDir = ""


def xlsTool(request):
    meses = []
    ventas = Sale.objects.all()
    for venta in ventas:
        if venta.month not in meses:
            meses.append(venta.month)

    context = {"title": "Cuentas de Cobro", 'meses':meses}
    return render(request, "sales/cuentasCobro.html", context)


def loadXlsxSales(request):
    if request.method == 'POST':
        xlsFile = request.FILES['inputxlsx']
        sheet = request.POST['sheet']
        month = request.POST['month']
        nameFile = xlsFile.name
        fileNamex = nameFile.split('.')
        file_tp_pross = origen_path + nameFile
        xlsxFile = pd.read_excel(io=file_tp_pross, engine='openpyxl', sheet_name=sheet, skiprows=0)
        records = len(xlsxFile)
        column_names=xlsxFile.columns.values
        row_data=list(xlsxFile.values.tolist())

        for data in row_data:
            oneData = {'codigo': data[0], 'cantidad': data[1], 'precio': data[2], 'comprador': data[3]}
            Sale.objects.create (codigo=oneData['codigo'], cantidad=oneData['cantidad'], precio=oneData['precio'], comprador=oneData['comprador'], month=month)

        context={'title': "xlsx Home", 'column_names':column_names, 'row_data':row_data, 'records':records}
        return render(request, "sales/excelTable.html", context)

    context = {"title": "Registro Ventas"}
    return render(request, "sales/registroSales.html", context)


def loadXlsxFactura(request):
    if request.method == 'POST':
        xlsFile = request.FILES['inputFactura']
        sheet = request.POST['sheet']
        month = request.POST['month']
        nameFile = xlsFile.name
        fileNamex = nameFile.split('.')
        file_tp_pross = origen_path + nameFile
        xlsxFile = pd.read_excel(io=file_tp_pross, engine='openpyxl', sheet_name=sheet, skiprows=0)
        records = len(xlsxFile)
        column_names=xlsxFile.columns.values
        row_data=list(xlsxFile.values.tolist())

        for data in row_data:
            oneData = {'codigo': data[0], 'descripción': data[1], 'cantidad': data[2], 'iva': data[3], 'valor': data[4]}
            Factura.objects.create (codigo=oneData['codigo'], descripción=oneData['descripción'], cantidad=oneData['cantidad'], iva=oneData['iva'], valor=oneData['valor'], month=month)

        context={'title': "xlsx Home", 'column_names':column_names, 'row_data':row_data, 'records':records}
        return render(request, "sales/excelTable.html", context)

    context = {"title": "Factura Ventas"}
    return render(request, "sales/facturaSales.html", context)
