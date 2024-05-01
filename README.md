Start the Django development server:py manage.py runserver


API Endpoints



Vendor Management



Create a Vendor






POST http://localhost:8000/api/vendors/




Create a new vendor.

Headers:

Content-Type: application/json

Body (example):

json

{
    "name": "Vendor Name",
    "contact": "Vendor Contact",
    "address": "Vendor Address",
    "code": "V001"
}

List All Vendors

GET http://localhost:8000/api/vendors/

Retrieve a list of all vendors.

Retrieve a Vendor

GET http://localhost:8000/api/vendors/{vendor_id}/

Retrieve details of a specific vendor.

Update a Vendor

PUT http://localhost:8000/api/vendors/{vendor_id}/

Update a vendor's details.

Delete a Vendor

DELETE http://localhost:8000/api/vendors/{vendor_id}/

Delete a vendor.

Purchase Order Tracking

Create a Purchase Order

POST http://localhost:8000/api/purchase_orders/

Create a new purchase order.

Headers:

Content-Type: application/json

Body (example):

json
{
    "po_number": "PO001",
    "vendor": 1,
    "order_date": "2024-05-10",
    "items": [
        {
            "name": "Item 1",
            "quantity": 5
        },
        {
            "name": "Item 2",
            "quantity": 10
        }
    ]
}

List All Purchase Orders

GET http://localhost:8000/api/purchase_orders/


Retrieve a list of all purchase orders with optional vendor filtering.


Retrieve a Purchase Order


GET http://localhost:8000/api/purchase_orders/{po_id}/


Retrieve details of a specific purchase order.


Update a Purchase Order


PUT http://localhost:8000/api/purchase_orders/{po_id}/


Update a purchase order.


Delete a Purchase Order


DELETE http://localhost:8000/api/purchase_orders/{po_id}/


Delete a purchase order.


Vendor Performance Evaluation


Retrieve Vendor Performance Metrics


GET http://localhost:8000/api/vendors/{vendor_id}/performance/


Retrieve performance metrics for a specific vendor.

###Logic Overview


On-Time Delivery Rate


Calculation: Count of completed POs delivered on or before delivery date divided by the total number of completed POs for the vendor.


Endpoint: Automatically updated when PO status changes to 'completed'.


Quality Rating Average


Calculation: Average of all quality_rating values for completed POs of the vendor.


Endpoint: Updated upon completion of each PO where a quality_rating is provided.
Average Response Time


Calculation: Time difference between issue_date and acknowledgment_date for each PO, averaged across all POs of the vendor.


Endpoint: Updated each time a PO is acknowledged by the vendor.
Fulfilment Rate


Calculation: Percentage of successfully fulfilled POs (status 'completed' without issues) divided by the total number of POs issued to the vendor.


Endpoint: Calculated upon any change in PO status.
Please ensure that you have Postman installed and configured correctly to interact with these APIs.





