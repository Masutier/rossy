from django.db import models
from django.urls import reverse


class Sale(models.Model):
    codigo = models.CharField(max_length=7)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    comprador = models.CharField(max_length=100)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.title


    def get_sale_absolute_url(self):
        return reverse("saleDetail", kwargs={"pk": self.pk})


class Factura(models.Model):
    codigo = models.CharField(max_length=7)
    descripción = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    valor = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    iva = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.codigo


    def get_factura_absolute_url(self):
        return reverse("FacturaDetail", kwargs={"pk": self.pk})
