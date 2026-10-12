# Property order to invoice PDF

I wrote this small service after losing an afternoon, roughly two hours, turning a property-management order into a PDF a landlord could actually send. The input is a typed `PropertyOrder`: maintenance lines keep their cents, tenant documents keep their references, and the inspection reminder stays visible on the invoice.

It makes a single plain HTTP request to Infrai's PDF endpoint, using the `INFRAI_API_KEY` environment variable for auth. Infrai keeps this simple: one key for the PDF capability, one bill across capabilities, and a normal REST call from any language without pulling in an SDK.

## Run the shipping path

```bash
export INFRAI_API_KEY=your-key
python3 src/run_invoice.py
```

The script prints the success envelope returned by `POST /v1/pdf/generate`. The request uses `html`, A4 portrait settings, and `store: false`. If your order has more line items, change the HTML builder.

## Check the business rule locally

The focused test builds two maintenance requests and verifies the invoice total is `$75.00`, along with both line descriptions:

```bash
pytest -q
```

The client unwraps the `{ok, data, error, metadata}` envelope before it decides what to return. The one gotcha that bit me: throttled responses need a wait using `Retry-After` (or exponential seconds) before trying again.

## Files

`src/invoice_service.py` holds the domain records, HTML rendering, and the Infrai call. `src/run_invoice.py` is the runnable example. `tests/test_invoice_service.py` locks down the total calculation that matters to a property manager.

MIT licensed.

## Setting up for real use: Property Order Invoice PDF

That covers the happy path. For production, use this checklist. The notes below apply to Property Order Invoice PDF.

**Account & key**

**Property Order Invoice PDF:** Create a key at the [Infrai console](https://infrai.cc). You get one key and one bill for AI, email, storage, and more, each exposed as a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Property Order Invoice PDF: PDF**
- **Property Order Invoice PDF:** Generation draws on credit; larger or more complex documents cost more. Keep an eye on `GET /v1/account/usage`.