from django.urls import path
from .views import (
    DashboardView,
    OrderListView, OrderDetailView, UpdateOrderStageView, OrderCreateView, UpdateOrderStatusView, OrderStageManageView,
    CustomerListView, CustomerCreateView, CustomerSearchView, CustomerDetailUpdateView,
    MeasurementListView, MeasurementDetailView, MeasurementSearchView,
    VendorListView, VendorCreateView, VendorUpdateView,
    PipelineStageListView, PipelineStageCreateView, PipelineStageUpdateView, InvoiceListView,
    CustomLoginView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/new/', OrderCreateView.as_view(), name='order_new'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/manage-stages/', OrderStageManageView.as_view(), name='order_stage_manage'),
    path('order-stage/<int:pk>/update/', UpdateOrderStageView.as_view(), name='update_order_stage'),
    path('orders/<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/new/', CustomerCreateView.as_view(), name='customer_new'),
    path('customers/search-detail/', CustomerDetailUpdateView.as_view(), name='customer_search_detail'),
    path('api/customer-search/', CustomerSearchView.as_view(), name='customer_search'),
    path('api/measurement-search/', MeasurementSearchView.as_view(), name='measurement_search'),
    
    path('measurements/', MeasurementListView.as_view(), name='measurement_list'),
    path('measurements/create/', MeasurementDetailView.as_view(), name='measurement_create'),
    path('measurements/<int:pk>/', MeasurementDetailView.as_view(), name='measurement_detail'),
    
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/create/', VendorCreateView.as_view(), name='vendor_create'),
    path('vendors/<int:pk>/update/', VendorUpdateView.as_view(), name='vendor_update'),
    path('pipeline-stages/', PipelineStageListView.as_view(), name='pipelinestage_list'),
    path('pipeline-stages/create/', PipelineStageCreateView.as_view(), name='pipelinestage_create'),
    path('pipeline-stages/<int:pk>/update/', PipelineStageUpdateView.as_view(), name='pipelinestage_update'),
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
]