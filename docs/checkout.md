# Hosted Checkout

The hosted checkout page handles the user experience to select a payment method, perform Strong Customer Authentication (SCA) with the bank (for PIS), and complete the payment.

- Link: use the `link` returned by `POST /payment-requests`.
- Redirect: set `redirectUrl` at creation time to receive the user back with `?status=success|error|cancel`.
- Callback: set `callbackUrl` to receive server-to-server notifications of status changes.

## Redirect parameters

When the checkout completes or the user cancels, the user is redirected to `redirectUrl` with a `status` query parameter:

- `success`: the payment has been authorised.
- `error`: the payment failed or an unrecoverable error occurred.
- `cancel`: the user exited the flow.

Optionally, `requestId` and `sessionId` can be included for convenience. Always use the API to retrieve the authoritative status.

## Callback notifications

If `callbackUrl` is provided, FlowPay sends server-to-server notifications when the payment status changes via a single event type `payment.status_change`. Inspect the `status` field in the payload (enum `PaymentRequestStatus`: `created`, `inProgress`, `authorized`, `rejected`, `onHold`, `locked`, `forwarded`, `refunded`, `deleted`).

- Method: POST
- Headers: `Content-Type: application/json`
- Payload: includes `requestId`, optional `sessionId`, `status`, and timestamps.

Note: ensure idempotency on your endpoint; the same event may be retried.

## Theming and branding

Branding (logo, primary color, legal info) is configured per partner in the FlowPay backoffice. Contact support to enable custom themes or environment-specific branding.

## Mobile and PWA behavior

The checkout behaves as a mobile-friendly web app and supports handoff between desktop and mobile via QR code in the PDF returned by `GET /payment-requests/{requestId}` with `Accept: application/pdf`.
