from django.urls import path
from . import views
from .views import (
    DashboardView,
    OrderListView, OrderDetailView, UpdateOrderStageView, OrderCreateView, UpdateOrderStatusView, OrderStageManageView, OrderDeleteView,
    CustomerListView, CustomerCreateView, CustomerSearchView, CustomerDetailUpdateView,
    MeasurementListView, MeasurementCreateView, MeasurementUpdateView, MeasurementSearchView, MeasurementDetailView, OrderSearchView, VendorSearchView,
    VendorListView, VendorCreateView, VendorUpdateView,
    PipelineStageListView, PipelineStageCreateView, PipelineStageUpdateView, InvoiceListView, PickOrdersView, CreateInvoiceView, InvoiceUpdateView, AddOrdersToInvoiceView, RemoveOrderFromInvoiceView, InvoiceDeleteView,
    CustomLoginView,
    CustomLogoutView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/new/', OrderCreateView.as_view(), name='order_new'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_edit'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/manage-stages/', OrderStageManageView.as_view(), name='order_stage_manage'),
    path('order-stage/<int:pk>/update/', UpdateOrderStageView.as_view(), name='update_order_stage'),
    path('orders/<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/new/', CustomerCreateView.as_view(), name='customer_new'),
    path('customers/search-detail/', CustomerDetailUpdateView.as_view(), name='customer_search_detail'),
    path('api/customer-search/', CustomerSearchView.as_view(), name='customer_search'),
    path('api/measurement-search/', MeasurementSearchView.as_view(), name='measurement_search'),
    path('api/order-search/', OrderSearchView.as_view(), name='order_search'),
    path('api/vendor-search/', VendorSearchView.as_view(), name='vendor_search'),
    
    path('measurements/', MeasurementListView.as_view(), name='measurement_list'),
    path('measurements/new/', MeasurementCreateView.as_view(), name='measurement_new'),
    path('measurements/<int:pk>/edit/', MeasurementUpdateView.as_view(), name='measurement_edit'),
    path('measurements/<int:pk>/', MeasurementDetailView.as_view(), name='measurement_detail'),

    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/create/', VendorCreateView.as_view(), name='vendor_create'),
    path('vendors/<int:pk>/update/', VendorUpdateView.as_view(), name='vendor_update'),
    path('pipeline-stages/', PipelineStageListView.as_view(), name='pipelinestage_list'),
    path('pipeline-stages/create/', PipelineStageCreateView.as_view(), name='pipelinestage_create'),
    path('pipeline-stages/<int:pk>/update/', PipelineStageUpdateView.as_view(), name='pipelinestage_update'),
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/pick-orders/', PickOrdersView.as_view(), name='pick_orders'),
    path('invoices/create/', CreateInvoiceView.as_view(), name='create_invoice'),
    path('invoices/<int:pk>/edit/', InvoiceUpdateView.as_view(), name='invoice_edit'),
    path('invoices/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoices/<int:pk>/add-orders/', AddOrdersToInvoiceView.as_view(), name='add_orders_to_invoice'),
    path('invoices/<int:pk>/remove-order/', RemoveOrderFromInvoiceView.as_view(), name='remove_order_from_invoice'),
    path('vendors/by-stage/<int:stage_id>/', views.get_vendors_by_stage, name='get_vendors_by_stage'),
]