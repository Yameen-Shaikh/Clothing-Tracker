from django import forms
from .models import OrderStage, Vendor, Order, Customer, Measurement, PipelineStage, Particulars

COMMON_MEASUREMENTS = [
    "Chest", "Waist", "Hip", "Shoulder", "Sleeve Length", "Inseam", "Outseam",
    "Neck", "Front Length", "Back Length", "Thigh", "Calf", "Ankle"
]

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
        fields = ['status', 'assigned_vendor']
        widgets = {
            'status': forms.Select(choices=OrderStage.STATUS_CHOICES),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_placed_on']
        widgets = {
            'order_placed_on': forms.DateInput(attrs={'type': 'date'})
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
        fields = ['measurement_type']

    def __init__(self, *args, **kwargs):
        self.read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        # Ensure self.instance.value is a dictionary, even if it's None from DB
        measurement_data = self.instance.value if self.instance and self.instance.value else {}

        # Dynamically add fields for common measurements
        for measure in COMMON_MEASUREMENTS:
            field_name = measure.lower().replace(" ", "_")
            self.fields[field_name] = forms.CharField(
                label=measure,
                required=False,
                widget=forms.TextInput(attrs={'placeholder': f'{measure} in inches'})
            )
            # Populate dynamic fields from measurement_data
            self.fields[field_name].initial = measurement_data.get(measure)
        
        if self.read_only:
            for field in self.fields.values():
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['disabled'] = 'disabled'
                else:
                    field.widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = super().clean()
        # Serialize dynamic fields into the 'value' JSONField
        measurement_values = {}
        for measure in COMMON_MEASUREMENTS:
            field_name = measure.lower().replace(" ", "_")
            if field_name in cleaned_data and cleaned_data[field_name]:
                measurement_values[measure] = cleaned_data[field_name]
                # Remove the dynamic field from cleaned_data to prevent ModelForm from trying to save it directly
                del cleaned_data[field_name]
        cleaned_data['value'] = measurement_values
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # The 'value' field is already populated in clean()
        if commit:
            instance.save()
        return instance

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'role', 'phone_numbers', 'address', 'remark']

class PipelineStageForm(forms.ModelForm):
    class Meta:
        model = PipelineStage
        fields = ['name']

class OrderStageCreateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['stage', 'assigned_vendor', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }