from django.contrib import admin
from .models import (
    Customer, Measurement, Vendor, PipelineStage, Order, OrderStage, Invoice
)

class OrderStageInline(admin.TabularInline):
    model = OrderStage
    extra = 1
    fields = ('stage', 'assigned_vendor', 'start_date', 'end_date', 'status', 'remark', 'note')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_placed_on', 'status')
    inlines = [OrderStageInline]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'note')

@admin.register(OrderStage)
class OrderStageAdmin(admin.ModelAdmin):
    list_display = ('order', 'stage', 'assigned_vendor', 'status', 'remark', 'note')
    fields = ('order', 'stage', 'assigned_vendor', 'start_date', 'end_date', 'status', 'remark', 'note')

admin.site.register(Measurement)

admin.site.register(PipelineStage)
admin.site.register(Invoice)