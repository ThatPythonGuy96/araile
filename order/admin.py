from django.contrib import admin
from .models import *

class OrdeItemInline(admin.TabularInline):
    model = OrderItem
    extra = 3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'status', 'total')
    readonly_fields = ['total',]
    # inlines = [OrdeItemInline]
