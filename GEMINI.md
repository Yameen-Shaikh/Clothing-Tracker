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
- `hips`: FloatField(null=True, blank=True)
- `neck`: FloatField(null=True, blank=True)
- `sleeve_length`: FloatField(null=True, blank=True)
- `bicep`: FloatField(null=True, blank=True)
- `wrist`: FloatField(null=True, blank=True)
- `shoulder_width`: FloatField(null=True, blank=True)
- `shirt_length`: FloatField(null=True, blank=True)
- `inseam`: FloatField(null=True, blank=True)
- `outseam`: FloatField(null=True, blank=True)
- `thigh`: FloatField(null=True, blank=True)
- `knee`: FloatField(null=True, blank=True)
- `ankle`: FloatField(null=True, blank=True)
- `pant_length`: FloatField(null=True, blank=True)
- `jacket_length`: FloatField(null=True, blank=True)
- `dress_length`: FloatField(null=True, blank=True)

### VendorRole
- `id`: SmallAutoField (Primary Key)
- `name`: CharField (max_length=100)

### Vendor
- `id`: SmallAutoField (Primary Key)
- `name`: CharField (max_length=100)
- `role`: ForeignKey to `PipelineStage` (on_delete=models.CASCADE)
- `phone_numbers`: ArrayField(BigIntegerField) (blank=True, null=True, default=list, help_text="List of contact phone numbers for the vendor.")
- `address`: TextField (blank=True)
- `remark`: TextField (blank=True, help_text="Any additional remarks about the vendor.")

### PipelineStage
- `id`: SmallAutoField (Primary Key)
- `name`: CharField (max_length=20)
- `role`: ForeignKey to `VendorRole` (on_delete=models.SET_NULL, null=True, blank=True)

### Order
- `id`: AutoField (Primary Key)
- `customer`: ForeignKey to `Customer` (on_delete=models.CASCADE)
- `order_placed_on`: DateField
- `status`: CharField (max_length=20)
- `completion_date`: DateField (null=True, blank=True, help_text="Date when the order was completed.")
- `specifications`: TextField (blank=True)
- `crocky`: BinaryField (null=True, blank=True)
- `crocky_mimetype`: CharField (max_length=50, null=True, blank=True)
- `amount`: IntegerField (default=0, help_text="Total calculated amount for the order. Stored as integer, e.g., in cents/paise.")
- `total_amount`: IntegerField (default=0)
- `invoice`: ForeignKey to `Invoice` (on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
- `measurement`: ForeignKey to `Measurement` (on_delete=models.SET_NULL, null=True, blank=True)

### OrderStage
- `id`: AutoField (Primary Key)
- `order`: ForeignKey to `Order` (on_delete=models.CASCADE)
- `stage`: ForeignKey to `PipelineStage` (on_delete=models.CASCADE)
- `assigned_vendor`: ForeignKey to `Vendor` (on_delete=models.SET_NULL, null=True, blank=True)
- `start_date`: DateField
- `end_date`: DateField (null=True, blank=True)
- `status`: CharField (max_length=20)
- `note`: TextField (blank=True, help_text="Any additional notes for this stage.")

### Invoice
- `id`: AutoField (Primary Key)
- `total_amount`: IntegerField (default=0, help_text="Total amount of the invoice. Stored as integer, e.g., in cents/paise.")
- `paid_on_date`: DateField (null=True, blank=True)
- `paid_amount`: IntegerField (default=0)

### Particulars
- `id`: AutoField (Primary Key)
- `order`: ForeignKey to `Order` (on_delete=models.CASCADE, related_name='particulars')
- `name`: CharField (max_length=20, help_text="Name or description of the particular item.")
- `details`: CharField (max_length=100, blank=True, help_text="Additional details about the particular item.")
- `amount`: IntegerField (help_text="Amount for this particular item. Stored as integer, e.g., in cents/paise.")

## Django Admin Configuration
- All models are registered with the Django admin (`production_tracker/admin.py`).
- `OrderAdmin` uses `OrderStageInline` for direct editing of `OrderStage` records.
- Custom `list_display` is configured for `Order`, `Customer`, and `Vendor` models.
- `VendorAdmin` now uses a default form that displays `PipelineStage` objects for the `role` field.

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
- **Model Changes:**
    - `Vendor` model's `role` field now directly links to `PipelineStage`.
    - `VendorRole` model was introduced and then its relationship with `Vendor` was removed.
    - `OrderStage` model's `remark` field was replaced with `note`.
- **Admin Interface:**
    - The "role" field in the Django admin for `Vendor` now displays `PipelineStage` objects.
    - All admin buttons are styled consistently with the main application's dark gold theme.
- **Order Management Logic:**
    - Order status now dynamically updates based on the status of its associated `OrderStage`s (In-Progress, Completed, Pending).
    - Prevention of duplicate `OrderStage` entries for the same `Order` and `PipelineStage`.
    - Prevention of creating new `Order`s with `Measurement`s already linked to another `Order`.
    - Automatic progression of `OrderStage` status (next stage becomes "In-Progress" when current is "Completed").
- **Dynamic Vendor Filtering:**
    - The "Assigned Vendor" dropdown in the "Add New Stage" form now dynamically displays vendors related to the selected `PipelineStage` via an AJAX call.
- **Bug Fixes:**
    - Fixed `NoReverseMatch` error for `invoice_detail` by changing the URL name in `order_detail.html` to `invoice_edit` and updating the displayed field to `invoice.id`.
    - Fixed CSRF token missing error in `customer_form.html`.
    - Fixed `FieldError` due to `remark` field removal in `OrderStage` and `Vendor` models.
- **Button Styling (Frontend):**
    - All buttons in the main application are styled consistently with the dark gold theme.
    - "Filter" button changed to "Search" in `measurement_list.html` and `order_list.html`.
    - "View" and "Edit" actions in `measurement_list.html` are now styled as buttons with spacing.
    - Button text changes in `customer_form.html`, `measurement_form.html`, `create_invoice.html`, `invoice_edit.html`, and `order_list.html`.
- **Agent-Made Changes:**
    - **Dynamic Vendor Filtering in Order Stages:**
        - Added `get_vendors_by_stage` view and URL (`/vendors/by-stage/<int:stage_id>/`).
        - Updated `order_detail.html` and `order_stage_manage.html` to dynamically filter vendors based on selected stage using AJAX.
    - **Order Creation Validation:**
        - Reverted `measurement` field from `OrderForm` in `production_tracker/forms.py`.
        - Modified `OrderCreateView` in `production_tracker/views.py` to prevent duplicate orders for the same measurement, displaying a popup message (`messages.error`) and clearing the form fields.
    - **Invoice Functionality Enhancements:**
        - Added search by order ID to `InvoiceListView` (`invoice_list.html` and `production_tracker/views.py`).
        - Implemented validation in `CreateInvoiceView` to prevent creating invoices with already-invoiced orders, displaying a popup message (`messages.error`).
        - Improved `CreateInvoiceView` and `PickOrdersView` to retain state (search query and selected orders) on `pick_orders.html` after validation errors.
    - **Order Edit Functionality:**
        - Added "Edit" button to `OrderListView` (`order_list.html`).
        - Added `order_edit` URL pattern (`/orders/<int:pk>/update/`).
        - Created `OrderUpdateView` in `production_tracker/views.py` to handle order editing.

## Next Steps/Pending Actions
- User needs to run `python3 manage.py createsuperuser` manually to create an admin user for testing.