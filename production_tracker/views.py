from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import Order, OrderStage, Customer, Measurement, Vendor, PipelineStage, Invoice
from .forms import OrderStageUpdateForm, OrderForm, CustomerForm, MeasurementForm, OrderStageCreateForm, OrderStatusUpdateForm, VendorForm, PipelineStageForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import date
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum, Count, Q
from django.http import JsonResponse


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class CustomerDetailUpdateView(LoginRequiredMixin, View):
    template_name = 'production_tracker/customer_search_detail.html'
    form_class = CustomerForm

    def get(self, request, *args, **kwargs):
        customer_id = request.GET.get('customer_id')
        search_name = request.GET.get('search_name', '')
        search_gender = request.GET.get('search_gender', '')
        search_address = request.GET.get('search_address', '')

        customer = None
        form = self.form_class()
        customers = Customer.objects.none() # Start with an empty queryset

        if search_name or search_gender or search_address:
            customers = Customer.objects.all()
            if search_name:
                customers = customers.filter(Q(name__icontains=search_name) | Q(phone__icontains=search_name))
            if search_gender:
                customers = customers.filter(gender=search_gender)
            if search_address:
                customers = customers.filter(address__icontains=search_address)

        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
            form = self.form_class(instance=customer)
        
        # Check for success message
        success_message = request.session.pop('success_message', None)
        
        return render(request, self.template_name, {
            'form': form, 
            'customer': customer,
            'success_message': success_message,
            'customers': customers, # Pass filtered customers to the template
            'search_name': search_name,
            'search_gender': search_gender,
            'search_address': search_address,
            'gender_choices': Customer.GENDER_CHOICES,
        })

    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get('customer_id')
        customer = None
        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
            form = self.form_class(request.POST, instance=customer)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            request.session['success_message'] = 'Customer details updated successfully!'
            return redirect(request.path_info + f"?customer_id={customer.id if customer else ''}")
        else:
            # Re-render the page with existing search parameters if form is invalid
            search_name = request.POST.get('search_name', '')
            search_gender = request.POST.get('search_gender', '')
            search_address = request.POST.get('search_address', '')
            customers = Customer.objects.none()
            if search_name or search_gender or search_address:
                customers = Customer.objects.all()
                if search_name:
                    customers = customers.filter(name__icontains=search_name)
                if search_gender:
                    customers = customers.filter(gender=search_gender)
                if search_address:
                    customers = customers.filter(address__icontains=search_address)

            return render(request, self.template_name, {
                'form': form, 
                'customer': customer,
                'customers': customers,
                'search_name': search_name,
                'search_gender': search_gender,
                'search_address': search_address,
                'gender_choices': Customer.GENDER_CHOICES,
            })

class CustomerSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        customers = Customer.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )
        results = [{'id': customer.id, 'name': customer.name, 'phone': customer.phone} for customer in customers]
        return JsonResponse(results, safe=False)

class MeasurementSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        customer_id = request.GET.get('customer_id', None)

        measurements = Measurement.objects.all()

        if customer_id:
            measurements = measurements.filter(customer__id=customer_id)

        if query:
            measurements = measurements.filter(
                Q(customer__name__icontains=query) | Q(customer__phone__icontains=query) | Q(measurement_type__icontains=query)
            )
        
        measurements = measurements.select_related('customer')
        results = [{'id': m.id, 'customer_name': m.customer.name, 'type': m.measurement_type} for m in measurements]
        return JsonResponse(results, safe=False)

class CustomLoginView(LoginView):
    template_name = 'production_tracker/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        refresh = RefreshToken.for_user(user)
        self.request.session['access_token'] = str(refresh.access_token)
        self.request.session['refresh_token'] = str(refresh)
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'production_tracker/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Order Analytics
        pending_orders = Order.objects.filter(status='Pending').count()
        in_progress_orders = Order.objects.filter(status='In-Progress').count()
        completed_orders = Order.objects.filter(status='Completed').count()
        
        context['total_orders'] = pending_orders + in_progress_orders + completed_orders
        context['pending_orders'] = pending_orders
        context['in_progress_orders'] = in_progress_orders
        context['completed_orders'] = completed_orders
        context['recent_orders'] = Order.objects.order_by('-order_placed_on')[:5]

        # Vendor Analytics
        context['total_vendors'] = Vendor.objects.count()

        # Customer Analytics
        context['total_customers'] = Customer.objects.count()

        # Invoice Analytics
        total_invoice_amount = Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        paid_invoices = Invoice.objects.filter(paid=True).count()
        unpaid_invoices = Invoice.objects.filter(paid=False).count()

        context['total_invoice_amount'] = total_invoice_amount / 100
        context['paid_invoices'] = paid_invoices
        context['unpaid_invoices'] = unpaid_invoices

        # Order Stage Analytics
        context['stages_in_progress'] = OrderStage.objects.filter(status='In-Progress').count()

        # Chart data
        context['order_status_data'] = {
            'labels': ['Pending', 'In Progress', 'Completed'],
            'data': [pending_orders, in_progress_orders, completed_orders],
        }
        context['invoice_status_data'] = {
            'labels': ['Paid', 'Unpaid'],
            'data': [paid_invoices, unpaid_invoices],
        }

        return context

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'production_tracker/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('customer')
        status = self.request.GET.get('status')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        customer_id = self.request.GET.get('customer')

        if status and status != 'All':
            queryset = queryset.filter(status=status)
        if start_date:
            queryset = queryset.filter(order_placed_on__gte=start_date)
        if end_date:
            queryset = queryset.filter(order_placed_on__lte=end_date)
        if customer_id:
            queryset = queryset.filter(customer__id=customer_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', 'All')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        
        selected_customer_id = self.request.GET.get('customer')
        if selected_customer_id:
            try:
                selected_customer = Customer.objects.get(id=selected_customer_id)
                context['selected_customer_id'] = selected_customer.id
                context['selected_customer_name'] = selected_customer.name
            except Customer.DoesNotExist:
                context['selected_customer_id'] = ""
                context['selected_customer_name'] = ""
        else:
            context['selected_customer_id'] = ""
            context['selected_customer_name'] = ""
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'production_tracker/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_status_form'] = OrderStatusUpdateForm(instance=self.object)
        context['current_stage'] = self.object.orderstage_set.filter(status='In-Progress').first()
        return context

class OrderStageManageView(LoginRequiredMixin, View):
    template_name = 'production_tracker/order_stage_manage.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order_stages = order.orderstage_set.all().order_by('stage__id')
        form = OrderStageCreateForm(initial={'order': order})
        return render(request, self.template_name, {
            'order': order,
            'order_stages': order_stages,
            'form': form,
            'vendors': Vendor.objects.all(),
            'pipeline_stages': PipelineStage.objects.all()
        })

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderStageCreateForm(request.POST)
        if form.is_valid():
            order_stage = form.save(commit=False)
            order_stage.order = order
            order_stage.status = 'New'
            order_stage.save()
            messages.success(request, 'Order Stage added successfully!')
            return redirect('order_stage_manage', pk=order.pk)
        else:
            order_stages = order.orderstage_set.all().order_by('stage__id')
            return render(request, self.template_name, {
                'order': order,
                'order_stages': order_stages,
                'form': form,
                'vendors': Vendor.objects.all(),
                'pipeline_stages': PipelineStage.objects.all()
            })

class UpdateOrderStageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order_stage = get_object_or_404(OrderStage, pk=pk)
        form = OrderStageUpdateForm(request.POST, instance=order_stage)
        if form.is_valid():
            updated_stage = form.save(commit=False)
            if updated_stage.status == 'Completed':
                updated_stage.end_date = date.today()
                
                # Get the next stage in the sequence
                next_stage = OrderStage.objects.filter(
                    order=updated_stage.order, 
                    stage__id__gt=updated_stage.stage.id
                ).order_by('stage__id').first()

                if next_stage:
                    next_stage.status = 'In-Progress'
                    next_stage.save()
                else:
                    # This is the last stage, so mark the order as completed
                    order = updated_stage.order
                    order.status = 'Completed'
                    order.save()

            updated_stage.save()
        return redirect('order_stage_manage', pk=order_stage.order.pk)

class UpdateOrderStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('order_detail', pk=order.pk)

class CustomerListView(SuperuserRequiredMixin, ListView):
    model = Customer
    template_name = 'production_tracker/customer_list.html'
    context_object_name = 'customers'

class MeasurementListView(LoginRequiredMixin, ListView):
    model = Measurement
    template_name = 'production_tracker/measurement_list.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        customer_id = self.request.GET.get('customer')
        if customer_id:
            queryset = super().get_queryset().select_related('customer')
            queryset = queryset.filter(customer__id=customer_id)
            return queryset
        return Measurement.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_customer_id = self.request.GET.get('customer')
        if selected_customer_id:
            try:
                selected_customer = Customer.objects.get(id=selected_customer_id)
                context['selected_customer_id'] = selected_customer.id
                context['selected_customer_name'] = selected_customer.name
            except Customer.DoesNotExist:
                context['selected_customer_id'] = ""
                context['selected_customer_name'] = ""
        else:
            context['selected_customer_id'] = ""
            context['selected_customer_name'] = ""
        return context

class VendorCreateView(SuperuserRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'production_tracker/vendor_form.html'
    success_url = reverse_lazy('vendor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Vendor'
        return context

class VendorUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'production_tracker/vendor_form.html'
    success_url = reverse_lazy('vendor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Vendor'
        return context

class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'production_tracker/vendor_list.html'
    context_object_name = 'vendors'

class PipelineStageCreateView(SuperuserRequiredMixin, CreateView):
    model = PipelineStage
    form_class = PipelineStageForm
    template_name = 'production_tracker/pipelinestage_form.html'
    success_url = reverse_lazy('pipelinestage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Pipeline Stage'
        return context

class PipelineStageUpdateView(SuperuserRequiredMixin, UpdateView):
    model = PipelineStage
    form_class = PipelineStageForm
    template_name = 'production_tracker/pipelinestage_form.html'
    success_url = reverse_lazy('pipelinestage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Pipeline Stage'
        return context

class PipelineStageListView(LoginRequiredMixin, ListView):
    model = PipelineStage
    template_name = 'production_tracker/pipelinestage_list.html'
    context_object_name = 'pipeline_stages'

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'production_tracker/invoice_list.html'
    context_object_name = 'invoices'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'production_tracker/order_form.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        customer_id = self.request.POST.get('customer')
        measurement_id = self.request.POST.get('measurement')

        if not customer_id:
            form.add_error(None, 'Please select a customer.')
            return self.form_invalid(form)
        
        customer = get_object_or_404(Customer, pk=customer_id)
        form.instance.customer = customer

        if measurement_id:
            measurement = get_object_or_404(Measurement, pk=measurement_id)
            form.instance.measurement = measurement

        return super().form_valid(form)

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'production_tracker/customer_form.html'
    success_url = reverse_lazy('customer_new') # Redirect back to the same page

    def form_valid(self, form):
        customer = form.save()
        messages.success(self.request, f'Customer {customer.name} added successfully.')
        self.request.session['success_message'] = f'Customer {customer.name} added successfully.'
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = self.request.session.pop('success_message', None)
        return context

class MeasurementCreateView(LoginRequiredMixin, CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'production_tracker/measurement_form.html'
    
    def get_success_url(self):
        return reverse('measurement_new')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create New Measurement"
        return context

    def form_valid(self, form):
        customer_id = self.request.POST.get('customer')
        if not customer_id:
            form.add_error('customer', 'Please select a customer.')
            return self.form_invalid(form)

        customer = get_object_or_404(Customer, pk=customer_id)
        measurement = form.save(commit=False)
        measurement.customer = customer
        measurement.save()
        messages.success(self.request, f'Measurement for {customer.name} saved successfully.')
        return redirect(self.get_success_url())

class MeasurementUpdateView(LoginRequiredMixin, UpdateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'production_tracker/measurement_form.html'
    
    def get_success_url(self):
        return reverse('measurement_edit', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Measurement"
        return context

class MeasurementDetailView(LoginRequiredMixin, DetailView):
    model = Measurement
    template_name = 'production_tracker/measurement_form.html'
    context_object_name = 'measurement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "View Measurement"
        context['read_only'] = True
        form = MeasurementForm(instance=self.object)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True
        context['form'] = form
        return context