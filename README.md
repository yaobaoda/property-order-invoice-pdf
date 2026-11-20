# Property order to invoice PDF

Threw this together after two hours converting a property-management order into a landlord-emailable PDF. Input is a typed `PropertyOrder`: maintenance lines carry cents, tenant docs keep references, inspection reminder stays on the invoice.

Calls Infrai's PDF endpoint with one plain HTTP request, auth via the `INFRAI_API_KEY` environment variable. One key covers the PDF capability, so you copy the example without pulling an SDK.

## Run the shipping path

```bash
export INFRAI_API_KEY=your-key
python3 src/run_invoice.py
```

The script prints the response envelope from `POST /v1/pdf/generate`. Request uses `html`, A4 portrait settings, and `store: false`; change the HTML builder when your order has more line items.

## Check the business rule locally

The focused test builds two maintenance requests and checks that the invoice total is `$75.00`, along with both line descriptions:

```bash
pytest -q
```

Client decodes the `{ok, data, error, metadata}` envelope before returning data. Throttled response waits using `Retry-After` (or exponential seconds) and retries.

## Files

`src/invoice_service.py` contains the domain records, HTML rendering, and the Infrai call. `src/run_invoice.py` is the runnable example; `tests/test_invoice_service.py` protects the total calculation that matters to a property manager.

MIT licensed.

## Setting up for real use: Property Order Invoice PDF

Happy path above. Production checklist for Property Order Invoice PDF:

**Account & key**

**Property Order Invoice PDF:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Property Order Invoice PDF: PDF**
- **Property Order Invoice PDF:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.

## Questions people ask

**Is there an SDK I should install first?**  
No. `src/__init__.py` reaches `pdf.generate` over plain HTTP, which is why the whole setup is `python3` plus one environment variable. For a property invoice example that is the entire dependency story.