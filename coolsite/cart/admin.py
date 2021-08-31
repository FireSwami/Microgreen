from django.contrib import admin

from .models import Order, OrderLineItem

class OrderLineItemAdmin(admin.TabularInline):
    model = OrderLineItem
    

   

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "final_price")
    list_filter = ['user']
    inlines = [OrderLineItemAdmin, ]
