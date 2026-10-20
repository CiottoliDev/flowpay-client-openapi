# SRTP payees registry

This is a **proposed API contract** for the client gateway. This documentation-only change does not implement the route or confirm its availability in any environment.

`GET /srtp/payees` exposes the creditor registry defined by the official [pagoPA SRTP Payees API](https://developer.pagopa.it/it/srtp/api/srtp-payees) within the FlowPay `/v2` API. It is separate from the Request To Pay payment-request lifecycle.

## Source and compatibility

The reference is [`payees_registry.yaml`](https://github.com/pagopa/cstar-securehub-infra-api-spec/blob/dfa4d72eda8edbcbec2ccb7c794fbdd89646221e/src/srtp/api/pagopa/payees_registry.yaml), API version `1.0.0`, OpenAPI `3.0.3`, last changed in commit `dfa4d72eda8edbcbec2ccb7c794fbdd89646221e` on 4 June 2026. Verified on 20 October 2026 against the file linked from the official portal. SHA-256: `b5fe5ea5c49272b33d79e83bdaa8789053b8bbd306d9185fc72d26ddf37fce31`.

The FlowPay document uses OpenAPI `3.1.0`. The imported payee and technical-header schemas use keywords compatible with both versions, so their validation constraints do not change. Components are prefixed with `Srtp` to avoid collisions. The upstream `payeeId` pattern is preserved literally (`\d{11}|\d{16}`), including its numeric-only definition; the prose reference to a fiscal code does not justify broadening it to an alphanumeric pattern. Pagination uses the existing gateway contract instead of importing the upstream pagination schemas.

## Gateway adaptations

- The resource path is `/srtp/payees`, under the existing FlowPay server URLs.
- Callers authenticate using the existing `X-API-Key` / `ApiKeyAuth` scheme. The upstream OAuth2 token endpoint and `read_rtp_payees` scope belong to the provider integration and are not exposed as FlowPay authentication.
- The required `RequestId` UUID and `Version` headers retain their upstream names, constraints and meaning. `Version` selects the SRTP provider API version (for example `v1`), independently of the FlowPay `/v2` base URL.
- Error bodies use the existing gateway `BadRequest` and `DefaultError` responses (`code`, `message`). The HTTP statuses remain `400`, `401`, `403`, `429`, `500` and `default`. Provider application/APIM/framework error formats are not exposed to gateway clients.
- Provider-specific CORS and rate-limit response headers, including their numeric limits, are not advertised as FlowPay guarantees.

## Pagination and payload

This endpoint uses exactly the standard gateway pagination of `GET /customers` (`listCustomers`) and `GET /refunds` (`listRefunds`) in `openapi.json`. It references the same `LimitParam`, `OffsetParam` and `PaginatedResult` components. The response specializes `items` with `SrtpPayee` using the same `allOf` structure as those operations. `GET /payment-requests` also uses the same response structure and equivalent inline pagination parameters. It does not use the separate AIS `page` / `per` convention.

The public query parameters are optional:

| Parameter | Meaning | Default | Schema constraints |
| --- | --- | --- | --- |
| `limit` | Maximum number of items per page | 20 | Integer; no declared minimum or maximum |
| `offset` | Number of items to skip | 0 | Integer; no declared minimum or maximum |

No SRTP-specific bounds or required flags are added to those shared parameters. The existing `PaginatedResult` requires `total`, `limit`, `offset`, `count` and `items` and disallows additional top-level properties. Example response to `GET /srtp/payees?limit=20&offset=0`:

```json
{
  "total": 2,
  "limit": 20,
  "offset": 0,
  "count": 2,
  "items": [
    { "payeeId": "02438750586", "name": "Roma Capitale" },
    { "payeeId": "80015010723", "name": "Comune di Bari" }
  ]
}
```

Each entry contains only the required `payeeId` and `name`. Their upstream patterns, lengths and `additionalProperties: false` constraints are preserved. There are no search parameters, name/payeeId filters, detail route, timestamps or synchronization job.

### Mapping to the provider contract

The provider uses required zero-based `page` and `size` (1–128) and responds with `{payees, page: {totalElements, totalPages, page, size}}`. Those query parameters and metadata are not part of the public gateway contract:

| Gateway field | Provider mapping |
| --- | --- |
| `total` | Provider `page.totalElements` |
| `limit` | Effective gateway `limit`, default 20 |
| `offset` | Effective gateway `offset`, default 0 |
| `count` | Number of entries actually returned in `items` |
| `items` | Requested offset window of provider `payees`, retaining each payee unchanged |

An adapter must translate the offset window into provider page requests while respecting the provider's `size` bound of 128. An offset need not align with a provider page boundary, and a gateway limit may require several provider pages. Consequently a simple `page = offset / limit` conversion is insufficient: page results must be sliced and, when needed, combined to produce the requested window. For example, `limit=20&offset=25` spans provider pages 1 and 2 at `size=20`, discarding the first five entries before returning up to twenty. The provider's page-size bound must not become a new public gateway constraint. This describes the contract mapping only; no adapter runtime is implemented here.

## Standalone document

`docs/srtp-openapi.json` contains only SRTP paths, their transitive component dependencies and the existing API-key security scheme. It has no external `$ref` dependencies. Regenerate it from the main contract with:

```sh
python3 scripts/export-srtp-openapi.py
```
