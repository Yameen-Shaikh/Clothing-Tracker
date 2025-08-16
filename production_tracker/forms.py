from django import forms
from .models import OrderStage, Vendor, Order, Customer, Measurement, PipelineStage, Invoice

class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES),
        }

class OrderStageUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['status', 'assigned_vendor', 'note']
        widgets = {
            'status': forms.Select(choices=OrderStage.STATUS_CHOICES),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_placed_on', 'completion_date', 'specifications', 'amount']
        widgets = {
            'order_placed_on': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None:
            return int(amount * 100) # Convert to paise
        return amount

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'gender']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Check if a customer with this phone number already exists
            # Exclude the current instance if it's an update
            if self.instance and self.instance.pk:
                if Customer.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError("This phone number is already registered to another customer.")
            else:
                if Customer.objects.filter(phone=phone).exists():
                    raise forms.ValidationError("This phone number is already registered.")
        return phone

class MeasurementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)
        if self.read_only:
            for field_name, field in self.fields.items():
                field.widget.attrs['readonly'] = 'readonly'
                field.widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Measurement
        fields = ['measurement_type', 'height', 'weight', 'chest', 'waist', 'hips', 'neck', 'sleeve_length', 'bicep', 'wrist', 'shoulder_width', 'shirt_length', 'inseam', 'outseam', 'thigh', 'knee', 'ankle', 'pant_length', 'jacket_length', 'dress_length']

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'role', 'phone_numbers', 'address', 'remark']

class PipelineStageForm(forms.ModelForm):
    class Meta:
        model = PipelineStage
        fields = ['name']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['total_amount', 'paid_on_date', 'paid_amount']
        widgets = {
            'paid_on_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk: # If editing an existing invoice
            self.fields['total_amount'].initial = self.instance.total_amount / 100
            self.fields['paid_amount'].initial = self.instance.paid_amount / 100

    def clean_total_amount(self):
        total_amount = self.cleaned_data.get('total_amount')
        if total_amount is not None:
            return int(total_amount * 100) # Convert to paise
        return total_amount

    def clean_paid_amount(self):
        paid_amount = self.cleaned_data.get('paid_amount')
        if paid_amount is not None:
            return int(paid_amount * 100) # Convert to paise
        return paid_amount


class OrderStageCreateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['stage', 'assigned_vendor', 'start_date', 'end_date', 'note']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }