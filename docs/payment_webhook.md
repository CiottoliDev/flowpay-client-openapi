## Overview

FlowPay delivers real-time, server-to-server notifications whenever a payment request changes state. Notifications are sent as HTTP POST requests to your configured `callbackUrl` and include the authoritative status you should use to advance your business flow. When in doubt, you can always query the latest state via `GET /payment-requests/{requestId}`.

## Event Semantics

There is a single, stable event for Request-to-Pay: `payment.status_change`. The current state is provided in the `status` field and reuses the API enum `PaymentRequestStatus` (`created`, `inProgress`, `authorized`, `rejected`, `onHold`, `locked`, `forwarded`, `refunded`, `deleted`). If the change originates from a specific checkout attempt, the event includes a `sessionId`. Multiple attempts may occur during a request’s lifecycle, and events may be delivered more than once; your handler must therefore be idempotent and tolerant of out-of-order delivery within the same `requestId`.

## Request Details

Deliveries use HTTPS POST with a JSON payload encoded in UTF‑8. The request carries headers that establish identity, integrity and replay protection. In particular, `X-FlowPay-Event-Id` uniquely identifies the delivery, `X-FlowPay-Event-Type` is always `payment.status_change`, `X-FlowPay-Timestamp` contains Unix epoch seconds, `X-FlowPay-Signature` holds a detached Ed25519 signature, `X-FlowPay-Key-Id` identifies the public key to use for verification, and `X-FlowPay-Retry-Count` indicates the attempt number starting at zero. Any HTTP 2xx response acknowledges the event.

## Security and Verification

Every delivery is signed by FlowPay with a platform private key. The signature covers the exact bytes of the HTTP body prefixed by the timestamp. Specifically, construct `payload = "{timestamp}.{rawBody}"` and verify the Base64URL‑encoded Ed25519 signature from `X-FlowPay-Signature` using the public key indicated by `X-FlowPay-Key-Id`.

To validate a notification, read `X-FlowPay-Timestamp`, `X-FlowPay-Signature` and `X-FlowPay-Key-Id`; fetch the matching key from our well‑known JWKS; rebuild the payload from the raw HTTP body; and verify the signature using a constant‑time comparison. Reject messages older than five minutes to mitigate replay attacks.

Well‑known JWKS is published at `/.well-known/jwks.json`:

Implementation notes: we use Ed25519 (EdDSA on Curve25519). The `X-FlowPay-Signature` header is Base64URL without padding. In Ed25519 JWKs, the public key is carried in the `x` parameter (also Base64URL without padding).

### Verification examples

Below are compact examples of signature verification using JWKS and Ed25519. Always use the raw HTTP request body, not a re‑serialized JSON string.

#### Java (Java 17+, Nimbus JOSE for JWK)

```java
// Maven deps:
// <dependency>
//   <groupId>com.nimbusds</groupId>
//   <artifactId>nimbus-jose-jwt</artifactId>
//   <version>9.37.3</version>
// </dependency>

import com.nimbusds.jose.jwk.*;
import com.nimbusds.jose.util.Base64URL;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.PublicKey;
import java.security.Signature;

public class FlowPayWebhookVerifier {
  public static boolean verify(
      String jwksUrl,
      String kid,
      String timestamp,
      String signatureB64Url,
      byte[] rawBody
  ) throws Exception {
    JWKSet jwkSet = JWKSet.load(new URL(jwksUrl));
    JWK jwk = jwkSet.getKeyByKeyId(kid);
    if (!(jwk instanceof OctetKeyPair) || !"Ed25519".equals(((OctetKeyPair) jwk).getCurve().getName())) {
      throw new IllegalArgumentException("Unsupported JWK or curve");
    }
    PublicKey publicKey = ((OctetKeyPair) jwk).toPublicKey();

    byte[] message = (timestamp + ".").getBytes(StandardCharsets.UTF_8);
    byte[] payload = new byte[message.length + rawBody.length];
    System.arraycopy(message, 0, payload, 0, message.length);
    System.arraycopy(rawBody, 0, payload, message.length, rawBody.length);

    byte[] signature = Base64URL.from(signatureB64Url).decode();

    Signature verifier = Signature.getInstance("Ed25519");
    verifier.initVerify(publicKey);
    verifier.update(payload);
    return verifier.verify(signature);
  }
}
```

#### Node.js (Node 18+, tweetnacl)

```js
// npm i tweetnacl
import nacl from "tweetnacl";

function b64urlToUint8(b64url) {
  const b64 =
    b64url.replace(/-/g, "+").replace(/_/g, "/") +
    "=".repeat((4 - (b64url.length % 4)) % 4);
  return new Uint8Array(Buffer.from(b64, "base64"));
}

export async function verifyFlowPay({
  jwksUrl,
  kid,
  timestamp,
  signatureB64Url,
  rawBodyBytes,
}) {
  const res = await fetch(jwksUrl);
  const { keys } = await res.json();
  const jwk = keys.find(
    (k) => k.kid === kid && k.kty === "OKP" && k.crv === "Ed25519"
  );
  if (!jwk) throw new Error("Key not found");

  const publicKey = b64urlToUint8(jwk.x);
  const signature = b64urlToUint8(signatureB64Url);

  const prefix = new TextEncoder().encode(`${timestamp}.`);
  const msg = new Uint8Array(prefix.length + rawBodyBytes.length);
  msg.set(prefix);
  msg.set(rawBodyBytes, prefix.length);

  return nacl.sign.detached.verify(msg, signature, publicKey);
}
```

#### Swift (CryptoKit)

```swift
import Foundation
import CryptoKit

func base64URLDecode(_ s: String) -> Data? {
  var str = s.replacingOccurrences(of: "-", with: "+").replacingOccurrences(of: "_", with: "/")
  let padLen = 4 - (str.count % 4)
  if padLen < 4 { str += String(repeating: "=", count: padLen) }
  return Data(base64Encoded: str)
}

func verifyFlowPay(jwksJson: Data, kid: String, timestamp: String, signatureB64Url: String, rawBody: Data) throws -> Bool {
  let jwks = try JSONSerialization.jsonObject(with: jwksJson) as! [String: Any]
  guard let keys = jwks["keys"] as? [[String: Any]],
        let key = keys.first(where: { ($0["kid"] as? String) == kid && ($0["kty"] as? String) == "OKP" && ($0["crv"] as? String) == "Ed25519" }),
        let xStr = key["x"] as? String,
        let x = base64URLDecode(xStr),
        let sig = base64URLDecode(signatureB64Url) else {
    return false
  }

  let publicKey = try Curve25519.Signing.PublicKey(rawRepresentation: x)
  var message = Data((timestamp + ".").utf8)
  message.append(rawBody)
  return publicKey.isValidSignature(sig, for: message)
}
```

## Delivery and Reliability

FlowPay uses at‑least‑once delivery with exponential backoff and jitter over a multi‑hour window. Retries occur on network errors, timeouts and non‑2xx responses; the current attempt is provided in `X-FlowPay-Retry-Count` starting from zero. Ordering within the same `requestId` is best‑effort and not strictly guaranteed. As soon as you persist the event safely, reply with any HTTP 2xx; redirects are not followed.

## Idempotency and Responses

Use `X-FlowPay-Event-Id` as the natural idempotency key. Keep a record of processed IDs for at least seven days and return 2xx for already‑applied deliveries. Respond as soon as the event is durably stored; keep the response body empty or return a small acknowledgment such as `{ "ok": true }`.

## Operational Guidance

Prefer a dedicated, unguessable `callbackUrl` and, where possible, additional controls such as IP allow‑listing or mutual TLS. Keep your handler lean—enqueue downstream work and acknowledge quickly. Log the event headers and `id` to correlate deliveries with your internal processing during troubleshooting.
