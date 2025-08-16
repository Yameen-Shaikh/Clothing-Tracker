# Project State Summary

This document summarizes the current state of the `Clothes-Production-Tracker` Django project.

## Project Setup
- **Project Name:** `clothing_factory`
- **App Name:** `production_tracker`
- **Virtual Environment:** `.venv` (activated using `source .venv/bin/activate`)
- **Dependencies:** `requirements.txt` (Django, psycopg2-binary, gunicorn, djangorestframework, djangorestframework-simplejwt)

## Database Schema (`production_tracker/models.py`)

### Customer
- `id`: AutoField (Primary Key)
- `name`: CharField (max_length=100)
- `email`: EmailField
- `phone`: BigIntegerField (null=True, blank=True)
- `address`: TextField (blank=True)

### Measurement
- `id`: AutoField (Primary Key)
- `customer`: ForeignKey to `Customer` (on_delete=models.CASCADE)
- `measurement_type`: CharField (max_length=20, choices=[('Pant', 'Pant'), ('Shirt', 'Shirt'), ('Suite', 'Suite'), ('Jacket', 'Jacket'), ('Trouser', 'Trouser'), ('Blouse', 'Blouse'), ('Skirt', 'Skirt'), ('Dress', 'Dress'), ('Coat', 'Coat'), ('Vest', 'Vest'), ('Kurta', 'Kurta'), ('Pajama', 'Pajama'), ('Sherwani', 'Sherwani'), ('Lehenga', 'Lehenga'), ('Saree Blouse', 'Saree Blouse'), ('Salwar Kameez', 'Salwar Kameez')])
- `height`: FloatField (null=True, blank=True)
- `weight`: FloatField (null=True, blank=True)
- `chest`: FloatField (null=True, blank=True)
- `waist`: FloatField (null=True, blank=True)
- `hips`: FloatField (null=True, blank=True)
- `neck`: FloatField (null=True, blank=True)
- `sleeve_length`: FloatField (null=True, blank=True)
- `bicep`: FloatField (null=True, blank=True)
- `wrist`: FloatField (null=True, blank=True)
- `shoulder_width`: FloatField (null=True, blank=True)
- `shirt_length`: FloatField (null=True, blank=True)
- `inseam`: FloatField (null=True, blank=True)
- `outseam`: FloatField (null=True, blank=True)
- `thigh`: FloatField (null=True, blank=True)
- `knee`: FloatField (null=True, blank=True)
- `ankle`: FloatField (null=True, blank=True)
- `pant_length`: FloatField (null=True, blank=True)
- `jacket_length`: FloatField (null=True, blank=True)
- `dress_length`: FloatField (null=True, blank=True)

### VendorRole
- `id`: SmallAutoField (Primary Key)
- `name`: CharField (max_length=10)

### Vendor
- `id`: SmallAutoField (Primary Key)
- `name`: CharField (max_length=100)
- `role`: ForeignKey to `VendorRole` (on_delete=models.CASCADE)
- `phone_numbers`: ArrayField(BigIntegerField) (blank=True, null=True, default=list, help_text="List of contact phone numbers for the vendor.")
- `address`: TextField (blank=True)
- `remark`: TextField (blank=True, help_text="Any additional remarks about the vendor.")

### PipelineStage
- `id`: SmallAutoField (Primary Key)
- `name`: CharField (max_length=20)

### Order
- `id`: AutoField (Primary Key)
- `customer`: ForeignKey to `Customer` (on_delete=models.CASCADE)
- `order_placed_on`: DateField
- `status`: CharField (max_length=10)
- `completion_date`: DateField (null=True, blank=True, help_text="Date when the order was completed.")
- `specifications`: TextField (blank=True)
- `crocky`: BinaryField (null=True, blank=True)
- `crocky_mimetype`: CharField (max_length=50, null=True, blank=True)
- `amount`: IntegerField (default=0, help_text="Total calculated amount for the order. Stored as integer, e.g., in cents/paise.")
- `invoice`: ForeignKey to `Invoice` (on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

### OrderStage
- `id`: AutoField (Primary Key)
- `order`: ForeignKey to `Order` (on_delete=models.CASCADE)
- `stage`: ForeignKey to `PipelineStage` (on_delete=models.CASCADE)
- `assigned_vendor`: ForeignKey to `Vendor` (on_delete=models.SET_NULL, null=True, blank=True)
- `start_date`: DateField
- `end_date`: DateField (null=True, blank=True)
- `status`: CharField (max_length=10)
- `remark`: TextField (blank=True)

### Invoice
- `id`: AutoField (Primary Key)
- `total_amount`: IntegerField (default=0, help_text="Total amount of the invoice. Stored as integer, e.g., in cents/paise.")
- `paid_on_date`: DateField (null=True, blank=True)
- `paid`: BooleanField (default=False)

### Particulars
- `id`: AutoField (Primary Key)
- `order`: ForeignKey to `Order` (on_delete=models.CASCADE, related_name='particulars')
- `name`: CharField (max_length=20, help_text="Name or description of the particular item.")
- `details`: CharField (max_length=100, blank=True, help_text="Additional details about the particular item.")
- `amount`: IntegerField (help_text="Amount for this particular item. Stored as integer, e.g., in cents/paise.")

## Django Admin Configuration
- All models are registered with the Django admin (`production_tracker/admin.py`).
- `OrderAdmin` uses `OrderStageInline` and `ParticularsInline` for direct editing of `OrderStage` and `Particulars` records.
- Custom `list_display` is configured for `Order`, `Customer`, and `Vendor` models.

## Django Rest Framework (DRF) & Simple JWT
- DRF and `djangorestframework-simplejwt` are installed and configured in `clothing_factory/settings.py`.
- `JWTAuthentication` is set as the default authentication class for DRF.
- JWT token endpoints (`api/token/`, `api/token/refresh/`) are configured in `clothing_factory/urls.py`.

## Routes (`production_tracker/urls.py`)
- `/login/`: `CustomLoginView` (Login page)
- `/logout/`: `LogoutView` (Logout functionality)
- `/`: `DashboardView` (Dashboard with analytics)
- `/orders/`: `OrderListView` (List all orders, with status filtering)
- `/orders/new/`: `OrderCreateView` (Create new order)
- `/orders/<int:pk>/`: `OrderDetailView` (View single order details, update OrderStage, add new OrderStage)
- `/order-stage/<int:pk>/update/`: `UpdateOrderStageView` (Update OrderStage status/vendor)
- `/customers/`: `CustomerListView` (List all customers)
- `/customers/new/`: `CustomerCreateView` (Create new customer)
- `/customers/search-detail/`: `CustomerDetailUpdateView` (Search and edit customer)
- `/measurements/`: `MeasurementListView` (List all measurements)
- `/measurements/new/`: `MeasurementCreateView` (Create new measurement, with customer search).
- `/measurements/<int:pk>/`: `MeasurementDetailView` (View single measurement details).
- `/measurements/<int:pk>/edit/`: `MeasurementUpdateView` (Edit single measurement details).
- `/vendor-roles/`: `VendorRoleListView` (List all vendor roles)
- `/vendors/`: `VendorListView` (List all vendors)
- `/pipeline-stages/`: `PipelineStageListView` (List all pipeline stages)
- `/invoices/`: `InvoiceListView` (List all invoices)

## Server-Side Rendered Views & Templates
All views are protected by `LoginRequiredMixin`.
- **Dashboard:** `DashboardView` (`dashboard.html`) displays analytics (order status, invoices, recent orders, vendor/customer counts, stages in progress) with Chart.js graphs.
- **Orders:**
    - `OrderListView` (`order_list.html`): Lists all orders with status and customer filtering (Pending, In Progress, Completed).
    - `OrderDetailView` (`order_detail.html`): Displays single order details, including associated `OrderStage` and `Particulars` records. Allows updating existing `OrderStage` status/vendor and adding new `OrderStage` records via forms.
    - `OrderCreateView` (`order_form.html`): Form for creating new orders with customer search.
- **Customers:**
    - `CustomerListView` (`customer_list.html`): Lists all customers.
    - `CustomerCreateView` (`customer_form.html`): Form for creating new customers.
    - `CustomerDetailUpdateView` (`customer_search_detail.html`): Search for and edit existing customers.
- **Measurements:**
    - `MeasurementListView` (`measurement_list.html`): Lists all measurements.
    - `MeasurementCreateView` (`measurement_form.html`): Form for creating new measurements with customer search.
    - `MeasurementDetailView` (`measurement_form.html`): View for displaying a single measurement's details.
    - `MeasurementUpdateView` (`measurement_form.html`): Form for updating an existing measurement.
- **Other List Views:** `VendorRoleListView`, `VendorListView`, `PipelineStageListView`, `InvoiceListView` with corresponding templates.

## UI/UX Theme
- **Theme:** Mughal cultural theme (reinstated).
- **Layout:** Full width and height application layout.
- **Framework:** Bootstrap is used for styling and layout.
- **Color Scheme:** Deep blues, golds, rich reds, and creams.
- **Typography:** `Roboto` for body text, `Playfair Display` for headings.
- **Icons:** Font Awesome icons used in the sidebar menu.
- **Animations:** Hover and transform animations are present on interactive elements.
- **Gradients:** Used in sidebar and some buttons.
- **Chart Colors:** Aligned with the Mughal theme.

## Authentication
- Custom login page (`production_tracker/login.html`) handled by `CustomLoginView`.
- Upon successful login, JWT access and refresh tokens are generated and stored in the user's session.
- All server-side rendered views require authentication via `LoginRequiredMixin`.
- Logout functionality is available.

## Recent Changes
- **Dashboard:**
    - Fixed JavaScript errors that were preventing the charts from rendering.
    - Refactored the dashboard to use the `json_script` template tag for safely passing data to the frontend.
    - Corrected the calculation of the total invoice amount.
- **Measurements:**
    - Fixed `NoReverseMatch` errors in the measurement list and pipeline stage list pages.
    - Refactored the measurement views to have separate views for creating, updating, and viewing measurements.
    - Updated the measurement form to use Bootstrap for styling.
- **General:**
    - Added Bootstrap to the base template for consistent styling across the application.

## Next Steps/Pending Actions
- User needs to run `python3 manage.py createsuperuser` manually to create an admin user for testing.
