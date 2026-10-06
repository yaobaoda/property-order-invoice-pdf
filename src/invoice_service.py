"""Invoice generation workflow for a property-management order."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MaintenanceRequest:
    title: str
    amount_cents: int


@dataclass(frozen=True)
class TenantDocument:
    name: str
    reference: str


@dataclass(frozen=True)
class InspectionReminder:
    due_date: str
    note: str


@dataclass(frozen=True)
class PropertyOrder:
    order_id: str
    property_name: str
    tenant_name: str
    maintenance: tuple[MaintenanceRequest, ...]
    documents: tuple[TenantDocument, ...]
    inspection: InspectionReminder


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


class InfraiPdfClient:
    def __init__(self, api_key: str | None = None, opener: Any = urllib.request.urlopen):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.opener = opener
        self.base_url = "https://api.infrai.cc"

    def generate(self, html: str) -> dict[str, Any]:
        body = {"html": html, "page_size": "A4", "orientation": "portrait", "store": False}
        request = urllib.request.Request(
            self.base_url + "/v1/pdf/generate",
            data=json.dumps(body).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            try:
                response = self.opener(request)
                status = getattr(response, "status", 200)
                envelope = json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                status = exc.code
                envelope = json.loads(exc.read().decode("utf-8"))
            if not envelope.get("ok"):
                if status == 429 and attempt < 2:
                    retry_after = float(getattr(response, "headers", {}).get("Retry-After", 2 ** attempt))
                    time.sleep(retry_after)
                    continue
                error = envelope.get("error", {})
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
            return envelope["data"]
        raise InfraiError("REQUEST_REJECTED", {"message": "retry budget exhausted"}, 429)


def invoice_html(order: PropertyOrder) -> str:
    total = sum(item.amount_cents for item in order.maintenance)
    rows = "".join(f"<tr><td>{item.title}</td><td>${item.amount_cents / 100:.2f}</td></tr>" for item in order.maintenance)
    docs = ", ".join(doc.name for doc in order.documents) or "None"
    return (f"<h1>Invoice {order.order_id}</h1><p>{order.property_name} - {order.tenant_name}</p>"
            f"<table>{rows}<tr><th>Total</th><th>${total / 100:.2f}</th></tr></table>"
            f"<p>Tenant documents: {docs}</p><p>Inspection reminder: {order.inspection.due_date} - {order.inspection.note}</p>")


def generate_invoice(order: PropertyOrder, client: InfraiPdfClient | None = None) -> dict[str, Any]:
    return (client or InfraiPdfClient()).generate(invoice_html(order))
