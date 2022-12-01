from django.urls import path, include
from .views import *

urlpatterns = [
    path('pdfTool', pdfTool, name="pdfTool"),
    path('pdfLoad', pdfLoad, name="pdfLoad"),

    path('xxx', xxx, name="xxx"),

    
    path('pdfExport', pdfExport, name="pdfExport"),

]
