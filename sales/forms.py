from django.db import models
from django.forms import ModelForm
from django import forms
from .models import *


class SaleNovaForm(ModelForm):
    class Meta:
        model = SaleNova
        fields = '__all__'


class FacturaNovaForm(ModelForm):
    class Meta:
        model = FacturaNova
        fields = '__all__'

