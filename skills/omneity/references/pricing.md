# Pricing and billing

Read [the generated API contract](contracts/pricing.md) for request fields, defaults, auth, and response types.

Use the current published account price in the [Sawalni portal](https://api.sawalni.com/).
Confirm currency, units, included allowances, and model access before quoting a
budget. Do not infer the active price from backend configuration or development
rate cards.

The public pricing artifact contains no unverified prices or plan allowances.
Read [the generated pricing status](pricing-rates.md). Public release of the
new rates has not been independently confirmed. Do not substitute an estimate
for a published price.

Use `GET /v1/billing/balance` to read the current credit balance.
For combined workflows, estimate each model and function call separately.
Account for retries and repeated retrieval. Preserve an existing alignment job
ID when polling. A network timeout does not prove a paid call was rejected.
