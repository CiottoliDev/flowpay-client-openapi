<!-- include css file -->
<link rel="stylesheet" href="./theme/messages.css">
<link rel="stylesheet" href="./theme/darkmode.css">
<link rel="stylesheet" href="./theme/beta.css">

# API Support

If you have any questions or need help with the APIs, you can open a ticket on our support portal. Click on the button below to open a ticket.

<!-- redoc breaks the script embed, we need to make it work differently -->
<script src=https://youtrack.flowpay.it/static/simplified/form/form-entry.js?auto=true></script>
<div id=form-button style="">
    <button> Do you need help? Open a ticket! </button>
</div>
<script>
    YTFeedbackForm.renderFeedbackButton(
        document.currentScript.previousElementSibling,
        {
            backendURL: 'https://youtrack.flowpay.it',
            formUUID: '5365c66c-6295-4631-9a5e-7afc2d5b7abf',
            theme: 'auto',
            language: 'en'
        }
    );
</script>

# FlowPay's commitment to the payments ecosystem

As a Payment Service Provider (PSP), FlowPay is regulated by the Bank of Italy and we are authorised to provide payment services to our customers.

We believe that the best API a payment institution can provide is one that is tailored to the payment use case, **allowing customers to focus on their business and not the payment process**.

On the end user side, FlowPay ensures that **users own their data, can access it at any time and fully manage it**. They can choose which data to share with third parties in the most transparent way possible.

## Contributions

FlowPay welcomes contributions from partners. The OpenAPI file is publicly available on GitHub: [FlowPay/client-openapi](https://github.com/FlowPay/client-openapi).

Partners can propose changes by forking the repository and submitting a pull request.

# Introduction

The APIs are REST over HTTPS. Some endpoints are restricted; partners must register their application and obtain an API key from the developer portal to access them. API keys can be rotated, scoped, and revoked at any time from the backoffice.

## Account Information Service (AIS)

FlowPay is authorised to provide AIS. In the Simplified Flow model, consents are collected directly by FlowPay via a hosted flow to minimise partner burden.

Endpoints:

- `POST /ais/consents`: create a consent session; returns a `link` to complete SCA with the bank.
- `GET /ais/consents/{consentId}`: retrieve consent status (`pending`, `active`, `expired`, ...).
- `GET /ais/accounts`: list available bank accounts under active consents.
- `GET /ais/accounts/{accountId}/balances`: current and available balances.
- `GET /ais/accounts/{accountId}/transactions`: list transactions, filterable by date.

If no active consent exists, AIS endpoints return `403` and partners can create a new consent using the consent endpoint.

## Payment Initiation Service (PIS)

FlowPay is an authorised PIS Provider (PISP). In the Simplified Flow, partners create Request To Pay objects and direct users to a hosted checkout to perform Strong Customer Authentication with their bank and authorise the payment.

APIs allow users to initiate traditional payment types:

- Simple account-to-account payment: user can initiate a SEPA Credit Transfer (SCT) payment from one of its bank accounts.
- Future date payment: the payer can schedule a payment for a future date.

In addition, FlowPay extends traditional payment methods by providing value-added services such as

- **Bulk payment**: payer can initiate a single payment with a single Strong Customer Authentication (SCA) to pay multiple payment requests or documents at once.
- **Payment chain**: user can authorise a payment to be executed when a previous payment has been successfully received.
- **Locked payment**: the user can authorise a payment to be executed if a previous payment has been successfully received. The check is performed by the client application that initiated the payment request.

Each of these services may route funds via a FlowPay technical account when required by business rules, while preserving original payer/payee information in remittance data.

## Hosted Checkout

See checkout behavior, redirects, callbacks, and branding in `docs/checkout.md`.

# Onboarding

Partners register their application in the developer portal (<https://developer.flowpay.it>) and obtain one or more API keys with configurable scopes. Keys can be rotated or revoked at any time. Access to the portal requires a company account enabled for FlowPay services.

# Sandbox environment

FlowPay provides a sandbox environment to allow partners to test the APIs before going into production. The sandbox is a safe space where you can experiment with the APIs without affecting real accounts or transactions.

<!-- # Mock environment

FlowPay provides a mock environment designed to help developers quickly prototype and validate their integration without connecting to real systems. This environment is built using [Prism](https://github.com/stoplightio/prism), which serves the OpenAPI specification as live endpoints, and uses [faker.js](https://fakerjs.dev/) to generate random but realistic data.

## How it works

The mock server validates all requests against the OpenAPI specification and returns mocked responses that match the expected output schema. Each field in the response is populated with context-aware fake data, such as realistic names, IBANs, dates, or UUIDs.
The mock environment is available at: `https://api.mock-flowpay.it/v3`; all endpoints mirror those defined in the OpenAPI specification.

The mock server automatically checks:

- required query parameters and headers
- request body structure and content
- response conformance to schema

This allows you to focus on building your application without worrying about backend logic or data consistency.

You can use the mock environment to:

- Test your application's integration with FlowPay APIs
- Front-end integration without backend logic
- Early validation of request formats
- Automated tests with predictable structure

Example request to list payment requests:

```
GET https://api.mock-flowpay.it/v3/payment-requests
X-API-Key: test_key
```

Response:

```json
{
  "data": [
    {
      "id": "req_82ae0947",
      "amount": 1250,
      "currency": "EUR",
      "created_at": "2024-06-01T14:30:00Z",
      "description": "Mocked request",
      "status": "created"
    }
  ],
  "next_cursor": "abc123",
  "has_more": false
}
```

## Validating your requests

You can deliberately send incorrect requests (e.g. missing required fields) to confirm how the system returns validation errors. This helps ensure that your integration meets the expected structure before switching to a real sandbox or production environment.

Example invalid request (missing `X-API-Key` header):

```
GET https://api.mock-flowpay.it/v3/payment-requests
```

Response:

```json
{
  "type": "https://stoplight.io/prism/errors#MISSING_HEADER",
  "title": "Authorization header is required",
  "status": 400,
  "detail": "Missing required header: Authorization"
}
``` -->

# Pagination

FlowPay APIs implement offset-based pagination on all list endpoints, following a standard response structure.

## Query parameters

When requesting a paginated resource, the following query parameters are supported:

- `limit` (integer): the maximum number of items to return. Default is 50, maximum is 100.
- `offset` (integer): the number of items to skip before starting to return results.

## Response structure

Each paginated response follows the `PaginatedResult` format:

- `total`: total number of available items.
- `limit`: maximum number of items returned in this page (as requested).
- `offset`: number of items skipped from the beginning of the collection.
- `count`: number of items actually returned in this response.
- `items`: array of objects representing the current page results.

## Example

### Request

```markdown
### Request
GET /payment-requests?limit=20&offset=0
X-API-Key: {api_key}
```

### Response

```json
{
  "total": 147,
  "limit": 20,
  "offset": 0,
  "count": 20,
  "items": [
    {
      "id": "req_12345",
      "amount": 1000,
      "currency": "EUR",
      "created_at": "2024-06-01T10:00:00Z",
      "status": "created"
    }
  ]
}
```

This structure allows clients to calculate pagination UI and control navigation across multiple pages using `offset` and `limit`.

# Rate limits

Requests are limited to 100 requests per minute per source IP; exceeding this limit results in 429 responses. A burst limit of 10 requests per second also applies. Production limits can be customised per partner on request.
