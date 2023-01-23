from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .forms import *


def adicionarVenta(request):
    revista = "novaventa"
    form = SaleForm()
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            SForm = form.save(commit=False)

            codigo = form.cleaned_data.get('codigo')
            cantidad = form.cleaned_data.get('cantidad')
            comprador = form.cleaned_data.get('comprador')
            month = form.cleaned_data.get('month')

            facturas = Invoice.objects.filter(revista=revista, codigo=codigo, month=month)
            cobros = Receipt.objects.filter(revista=revista, codigo=codigo, month=month)
            for cobro in cobros:
                if cobro.codigo == codigo:
                    fechaLimite = cobro.fechaLimite

            for factura in facturas:
                if factura.codigo == codigo:
                    descripcion = factura.descripcion
                    precio = factura.precio
                    qty = factura.cantidad
            
            precio = precio / qty

            SForm.save()
            Cobros.objects.create (
                revista = revista
                , month = month
                , codigo = codigo
                , descripcion = descripcion
                , comprador = comprador
                , cantidad = cantidad
                , precio = precio
                , fechaLimite = fechaLimite
            )

            messages.success(request, f'La Venta ya quedo modificada y El Cobro creado')
            return redirect('cuentas')

    context = {'title':'Crear Venta', 'form':form}
    return render(request, "sales/editarSales.html", context)


def modificarVenta(request, pk):
    venta = Sale.objects.get(id=pk)
    form = SaleForm(instance=venta)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, f'La Venta ya quedo Modificada!')
            return redirect('cuentas')

    context = {'title':'Editar venta', 'form':form}
    return render(request, "sales/editarSales.html", context)


def modificarRemision(request, pk):
    factura = Invoice.objects.get(id=pk)
    form = FacturaForm(instance=factura)
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            messages.success(request, f'La Remision ya quedo Modificada!')
            return redirect('cuentas')

    context = {'title':'Editar factura', 'form':form}
    return render(request, "sales/editarRemis.html", context)
