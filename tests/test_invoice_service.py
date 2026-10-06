import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.invoice_service import InspectionReminder, MaintenanceRequest, PropertyOrder, TenantDocument, invoice_html


def test_invoice_total_reflects_maintenance_lines():
    order = PropertyOrder("PM-1", "Oak House", "Lee", (MaintenanceRequest("Boiler", 5000), MaintenanceRequest("Lock", 2500)),
                          (TenantDocument("lease.pdf", "r1"),), InspectionReminder("2026-11-01", "Check"))
    html = invoice_html(order)
    assert "$75.00" in html
    assert "Boiler" in html and "Lock" in html
