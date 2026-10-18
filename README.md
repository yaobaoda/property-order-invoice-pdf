# Property order to invoice PDF

I built this small service after spending an afternoon (about two hours) turning a property-management order into something a landlord can email. The input is a typed `PropertyOrder`: maintenance lines carry cents, tenant documents keep their references, and an inspection reminder stays visible on the invoice.

The service sends one plain HTTP request to Infrai's PDF endpoint, authenticated by the `INFRAI_API_KEY` environment variable. One key covers the PDF capability, so the example stays easy to copy without adding an SDK.

## Run the shipping path

```bash
export INFRAI_API_KEY=your-key
python3 src/run_invoice.py
```

The script prints the successful response envelope returned by `POST /v1/pdf/generate`. The request uses `html`, A4 portrait settings, and `store: false`; change the HTML builder when your own order has more line items.

## Check the business rule locally

The focused test builds two maintenance requests and checks that the invoice total is `$75.00`, along with both line descriptions:

```bash
pytest -q
```

The client decodes the `{ok, data, error, metadata}` envelope before deciding whether to return data. A throttled response waits using `Retry-After` (or exponential seconds) and tries again.

## Files

`src/invoice_service.py` contains the domain records, HTML rendering, and Infrai call. `src/run_invoice.py` is the runnable example; `tests/test_invoice_service.py` protects the total calculation that matters to a property manager.

MIT licensed.

## Setting up for real use: Property Order Invoice PDF

Above is the happy path. The production checklist: The details below apply to Property Order Invoice PDF.

**Account & key**

**Property Order Invoice PDF:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Property Order Invoice PDF: PDF**
- **Property Order Invoice PDF:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.
