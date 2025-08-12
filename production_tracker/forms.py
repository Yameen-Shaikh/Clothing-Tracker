from django import forms
from .models import OrderStage, Vendor, Order, Customer, Measurement, PipelineStage, Particulars

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
        fields = ['order_placed_on', 'completion_date', 'specifications']
        widgets = {
            'order_placed_on': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']

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
    class Meta:
        model = Measurement
        fields = ['measurement_type', 'height', 'weight', 'chest', 'waist', 'hips', 'neck', 'sleeve_length', 'bicep', 'wrist', 'shoulder_width', 'shirt_length', 'inseam', 'outseam', 'thigh', 'knee', 'ankle', 'pant_length', 'jacket_length', 'dress_length']

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'role', 'phone_numbers', 'address', 'note']

class PipelineStageForm(forms.ModelForm):
    class Meta:
        model = PipelineStage
        fields = ['name']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_placed_on', 'completion_date', 'specifications']
        widgets = {
            'order_placed_on': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }

class OrderStageCreateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['stage', 'assigned_vendor', 'start_date', 'end_date', 'remark']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }