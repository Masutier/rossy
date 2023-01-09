from django.db import models
from django.urls import reverse


class Sale(models.Model):
    revista = models.CharField(max_length=150)
    codigo = models.CharField(max_length=7)
    comprador = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    month = models.CharField(max_length=30)
    arrive = models.BooleanField(blank=True, null=True, default=False)


    def __str__(self):
        return self.codigo


    def get_sales_absolute_url(self):
        return reverse("SalesDetail", kwargs={"pk": self.pk})


class Invoice(models.Model):
    revista = models.CharField(max_length=150)
    codigo = models.CharField(max_length=7)
    descripcion = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    ganancia = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    month = models.CharField(max_length=30)
    forget = models.BooleanField(blank=True, null=True, default=False)


    def __str__(self):
        return self.codigo


    def get_invoice_absolute_url(self):
        return reverse("InvoiceDetail", kwargs={"pk": self.pk})


class Receipt(models.Model):
    revista = models.CharField(max_length=150)
    month = models.CharField(max_length=30)
    codigo = models.CharField(max_length=7)
    comprador = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    fechaLimite = models.DateField()

    def __str__(self):
        return self.comprador


    def get_receipts_absolute_url(self):
        return reverse("ReceiptsDetail", kwargs={"pk": self.pk})
