from django.db import models
from django.forms import ModelForm
from django import forms
from .models import *


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'


class FacturaForm(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

