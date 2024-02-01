from django.contrib import admin

# Register your models here.
from .models import Customer
from import_export.admin import ImportExportModelAdmin

admin.site.register(Customer, ImportExportModelAdmin)
