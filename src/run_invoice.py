import json

from invoice_service import (InspectionReminder, MaintenanceRequest, PropertyOrder,
                             TenantDocument, generate_invoice)


def main() -> None:
    order = PropertyOrder(
        order_id="PM-1042", property_name="Harbor View 12B", tenant_name="Mina Chen",
        maintenance=(MaintenanceRequest("Leaking kitchen tap", 12500),),
        documents=(TenantDocument("lease.pdf", "lease-1042"),),
        inspection=InspectionReminder("2026-10-15", "Annual safety check"),
    )
    print(json.dumps(generate_invoice(order), indent=2))


if __name__ == "__main__":
    main()
