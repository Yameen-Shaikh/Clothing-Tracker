from django.contrib import admin
from .models import (
    Customer, Measurement, Vendor, PipelineStage, Order, OrderStage, Invoice, Particulars
)

class OrderStageInline(admin.TabularInline):
    model = OrderStage
    extra = 1
    fields = ('stage', 'assigned_vendor', 'start_date', 'end_date', 'status', 'note')

class ParticularsInline(admin.TabularInline):
    model = Particulars
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_placed_on', 'status')
    inlines = [OrderStageInline, ParticularsInline]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'note')

admin.site.register(Measurement)

admin.site.register(PipelineStage)
admin.site.register(OrderStage)
admin.site.register(Invoice)
admin.site.register(Particulars)