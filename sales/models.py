from django.db import models
from django.urls import reverse


class SaleNova(models.Model):
    codigo = models.CharField(max_length=7)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    comprador = models.CharField(max_length=100)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.codigo


    def get_salenova_absolute_url(self):
        return reverse("saleNovaDetail", kwargs={"pk": self.pk})


class FacturaNova(models.Model):
    codigo = models.CharField(max_length=7)
    descripcion = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    catalogo = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    ganancia = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.codigo


    def get_facturanova_absolute_url(self):
        return reverse("FacturaNovaDetail", kwargs={"pk": self.pk})


class SaleLeonisa(models.Model):
    codigo = models.CharField(max_length=7)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    comprador = models.CharField(max_length=100)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.codigo


    def get_saleLeo_absolute_url(self):
        return reverse("saleLeonisaDetail", kwargs={"pk": self.pk})


class FacturaLeonisa(models.Model):
    codigo = models.CharField(max_length=7)
    descripcion = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    catalogo = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    ganancia = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.codigo


    def get_facturaLeo_absolute_url(self):
        return reverse("FacturaLeonisaDetail", kwargs={"pk": self.pk})


class SaleModa(models.Model):
    codigo = models.CharField(max_length=7)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    comprador = models.CharField(max_length=100)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.codigo


    def get_saleModa_absolute_url(self):
        return reverse("saleModaDetail", kwargs={"pk": self.pk})


class FacturaModa(models.Model):
    codigo = models.CharField(max_length=7)
    descripcion = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    catalogo = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    ganancia = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    month = models.CharField(max_length=30)


    def __str__(self):
        return self.codigo


    def get_facturaModa_absolute_url(self):
        return reverse("FacturaModaDetail", kwargs={"pk": self.pk})


class Cobros(models.Model):
    revista = models.CharField(max_length=150)
    month = models.CharField(max_length=30)
    codigo = models.CharField(max_length=7)
    comprador = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    catalogo = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    fechaLimite = models.DateField()

    def __str__(self):
        return self.comprador


    def get_cobros_absolute_url(self):
        return reverse("CobrosaDetail", kwargs={"pk": self.pk})
