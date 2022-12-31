from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .forms import *


def adicionarVenta(request):
    revista = "novaventa"
    form = SaleNovaForm()
    if request.method == 'POST':
        form = SaleNovaForm(request.POST)
        if form.is_valid():
            SForm = form.save(commit=False)

            codigo = form.cleaned_data.get('codigo')
            cantidad = form.cleaned_data.get('cantidad')
            comprador = form.cleaned_data.get('comprador')
            month = form.cleaned_data.get('month')

            facturas = FacturaNova.objects.filter(codigo=codigo, month=month)
            cobros = Cobros.objects.filter(codigo=codigo, month=month)
            for cobro in cobros:
                if cobro.codigo == codigo:
                    fechaLimite = cobro.fechaLimite

            for factura in facturas:
                if factura.codigo == codigo:
                    descripcion = factura.descripcion
                    catalogo = factura.catalogo
                    qty = factura.cantidad
            
            catalogo = catalogo / qty

            SForm.save()
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

            messages.success(request, f'La Venta ya quedo modificada y El Cobro creado')
            return redirect('cuentas')

    context = {'title':'Crear Venta', 'form':form}
    return render(request, "sales/editarSales.html", context)


def modificarVenta(request, pk):
    venta = SaleNova.objects.get(id=pk)
    form = SaleNovaForm(instance=venta)
    if request.method == 'POST':
        form = SaleNovaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, f'La Venta ya quedo Modificado!')
            return redirect('cuentas')

    context = {'title':'Editar venta', 'form':form}
    return render(request, "sales/editarSales.html", context)


def modificarRemision(request, pk):
    factura = FacturaNova.objects.get(id=pk)
    form = FacturaNovaForm(instance=factura)
    if request.method == 'POST':
        form = FacturaNovaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            messages.success(request, f'La Remision ya quedo Modificado!')
            return redirect('cuentas')

    context = {'title':'Editar factura', 'form':form}
    return render(request, "sales/editarRemis.html", context)
