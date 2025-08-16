from django.db import models
from django.contrib.postgres.fields import ArrayField

class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField(null=True, blank=True, unique=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    MEASUREMENT_CHOICES = [
        ('Pant', 'Pant'),
        ('Shirt', 'Shirt'),
        ('Suite', 'Suite'),
        ('Jacket', 'Jacket'),
        ('Trouser', 'Trouser'),
        ('Blouse', 'Blouse'),
        ('Skirt', 'Skirt'),
        ('Dress', 'Dress'),
        ('Coat', 'Coat'),
        ('Vest', 'Vest'),
        ('Kurta', 'Kurta'),
        ('Pajama', 'Pajama'),
        ('Sherwani', 'Sherwani'),
        ('Lehenga', 'Lehenga'),
        ('Saree Blouse', 'Saree Blouse'),
        ('Salwar Kameez', 'Salwar Kameez'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    measurement_type = models.CharField(max_length=20, choices=MEASUREMENT_CHOICES)

    # Common measurements
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    hips = models.FloatField(null=True, blank=True)

    # Shirt/Blouse/Kurta etc. measurements
    neck = models.FloatField(null=True, blank=True)
    sleeve_length = models.FloatField(null=True, blank=True)
    bicep = models.FloatField(null=True, blank=True)
    wrist = models.FloatField(null=True, blank=True)
    shoulder_width = models.FloatField(null=True, blank=True)
    shirt_length = models.FloatField(null=True, blank=True)

    # Pant/Trouser/Pajama etc. measurements
    inseam = models.FloatField(null=True, blank=True)
    outseam = models.FloatField(null=True, blank=True)
    thigh = models.FloatField(null=True, blank=True)
    knee = models.FloatField(null=True, blank=True)
    ankle = models.FloatField(null=True, blank=True)
    pant_length = models.FloatField(null=True, blank=True)

    # Suit/Jacket/Coat etc. measurements
    jacket_length = models.FloatField(null=True, blank=True)

    # Dress measurements
    dress_length = models.FloatField(null=True, blank=True)

class VendorRole(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PipelineStage(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    role = models.ForeignKey(VendorRole, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Vendor(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)
    phone_numbers = ArrayField(models.BigIntegerField(), blank=True, null=True, default=list, help_text="List of contact phone numbers for the vendor.")
    address = models.TextField(blank=True)
    remark = models.TextField(blank=True, help_text="Any additional remarks about the vendor.")

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
        ('Cancelled', 'Cancelled'),
        ('Aborted', 'Aborted'),
    ]
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_placed_on = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    specifications = models.TextField(blank=True)
    completion_date = models.DateField(null=True, blank=True, help_text="Date when the order was completed.")
    amount = models.IntegerField(default=0, help_text="Total calculated amount for the order. Stored as integer, e.g., in cents/paise.")
    total_amount = models.IntegerField(default=0)
    invoice = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True, blank=True)

class OrderStage(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
        ('Cancelled', 'Cancelled'),
        ('Aborted', 'Aborted'),
    ]
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)
    assigned_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    note = models.TextField(blank=True, help_text="Any additional notes for this stage.")

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.IntegerField(default=0, help_text="Total amount of the invoice. Stored as integer, e.g., in cents/paise.")
    paid_on_date = models.DateField(null=True, blank=True)
    paid_amount = models.IntegerField(default=0)

