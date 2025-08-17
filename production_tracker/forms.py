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
            'paid_on_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # --- CHANGE 1: More robust check and added safety for None values ---
        # Check if we are editing an existing instance
        if self.instance and self.instance.pk:
            # Convert total_amount from paise to rupees for display, if it exists
            if self.instance.total_amount is not None:
                self.initial['total_amount'] = self.instance.total_amount / 100

            # Convert paid_amount from paise to rupees for display, if it exists
            if self.instance.paid_amount is not None:
                self.initial['paid_amount'] = self.instance.paid_amount / 100

    def save(self, commit=True):
        """
        Override the save method to handle currency conversion.
        """
        # Get the form's instance (the invoice object) but don't save it to the DB yet.
        instance = super().save(commit=False)

        # --- CHANGE 2: Convert submitted rupee values back to paise before saving ---
        # Get the values from the cleaned_data dictionary
        total_amount_rupees = self.cleaned_data.get('total_amount')
        paid_amount_rupees = self.cleaned_data.get('paid_amount')

        if total_amount_rupees is not None:
            instance.total_amount = int(total_amount_rupees * 100)

        if paid_amount_rupees is not None:
            instance.paid_amount = int(paid_amount_rupees * 100)

        # If commit is True, save the instance to the database.
        if commit:
            instance.save()
            
        return instance
class OrderStageCreateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['stage', 'assigned_vendor', 'start_date', 'end_date', 'note']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }