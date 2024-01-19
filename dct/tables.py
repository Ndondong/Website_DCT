import django_tables2 as tables

from .models import *

class TabelPenyisipan(tables.Table):
    class Meta:
        model = ModelPenyisipan
        template_name = 'django_tables2/bootstrap4-responsive.html'

class TabelPengekstrakan(tables.Table):
    class Meta:
        model = ModelPengekstrakan
        template_name = 'django_tables2/bootstrap4-responsive.html'
    