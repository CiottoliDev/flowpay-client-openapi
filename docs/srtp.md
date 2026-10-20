# SRTP payees registry

This is a **proposed API contract** for the client gateway. This documentation-only change does not implement the route or confirm its availability in any environment.

`GET /srtp/payees` exposes the creditor registry defined by the official [pagoPA SRTP Payees API](https://developer.pagopa.it/it/srtp/api/srtp-payees) within the FlowPay `/v2` API. It is separate from the Request To Pay payment-request lifecycle.

## Source and compatibility

The reference is [`payees_registry.yaml`](https://github.com/pagopa/cstar-securehub-infra-api-spec/blob/dfa4d72eda8edbcbec2ccb7c794fbdd89646221e/src/srtp/api/pagopa/payees_registry.yaml), API version `1.0.0`, OpenAPI `3.0.3`, last changed in commit `dfa4d72eda8edbcbec2ccb7c794fbdd89646221e` on 4 June 2026. Verified on 20 October 2026 against the file linked from the official portal. SHA-256: `b5fe5ea5c49272b33d79e83bdaa8789053b8bbd306d9185fc72d26ddf37fce31`.

The FlowPay document uses OpenAPI `3.1.0`. The imported schemas use keywords compatible with both versions, so no validation constraints need to change. Components are prefixed with `Srtp` to avoid collisions. The upstream `payeeId` pattern is preserved literally (`\d{11}|\d{16}`), including its numeric-only definition; the prose reference to a fiscal code does not justify broadening it to an alphanumeric pattern. The example page is corrected to contain two entries with `size: 2`, `page: 0` and `totalPages: 1`; the original example contained two entries with `size: 1`.

## Gateway adaptations

- The resource path is `/srtp/payees`, under the existing FlowPay server URLs.
- Callers authenticate using the existing `X-API-Key` / `ApiKeyAuth` scheme. The upstream OAuth2 token endpoint and `read_rtp_payees` scope belong to the provider integration and are not exposed as FlowPay authentication.
- The required `RequestId` UUID and `Version` headers retain their upstream names, constraints and meaning. `Version` selects the SRTP provider API version (for example `v1`), independently of the FlowPay `/v2` base URL.
- Error bodies use the existing gateway `BadRequest` and `DefaultError` responses (`code`, `message`). The HTTP statuses remain `400`, `401`, `403`, `429`, `500` and `default`. Provider application/APIM/framework error formats are not exposed to gateway clients.
- Provider-specific CORS and rate-limit response headers, including their numeric limits, are not advertised as FlowPay guarantees.

## Pagination and payload

This endpoint preserves the upstream page-based interface. It is an exception to the generic offset-based pagination described in the general guide and does not use the AIS one-based `page` / `per` convention.

Both query parameters are required, with no defaults:

| Parameter | Meaning | Range |
| --- | --- | --- |
| `page` | Zero-based page number | 0–2147483647 |
| `size` | Entries per page | 1–128 |

The success body is returned directly, without an additional gateway envelope:

```json
{
  "payees": [
    { "payeeId": "02438750586", "name": "Roma Capitale" },
    { "payeeId": "80015010723", "name": "Comune di Bari" }
  ],
  "page": { "totalElements": 2, "totalPages": 1, "page": 0, "size": 2 }
}
```

Each entry contains only the required `payeeId` and `name`. The upstream required fields, patterns, lengths, numeric bounds, array bound and `additionalProperties: false` constraints are preserved. There are no search parameters, name/payeeId filters, detail route, timestamps, synchronization job or pagination guarantees beyond the upstream specification.

## Standalone document

`docs/srtp-openapi.json` contains only SRTP paths, their transitive component dependencies and the existing API-key security scheme. It has no external `$ref` dependencies. Regenerate it from the main contract with:

```sh
python3 scripts/export-srtp-openapi.py
```
