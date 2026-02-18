This endpoint enables clients to allow their users to pay with FlowPay using different payment methods.
By default, the client creates a Request To Pay for which they are the creditor. If a debtor isn't specified, the payer will be identified during the payment session.
The client can also specify a different creditor if they are not the intended recipient of the payment.

The methods currently supported are PIS, Card, Wallet

PIS (Payment Initiation Service) is a financial service that allows third-party providers to initiate a payment transaction from a user's bank account. PIS works by using APIs provided to securely connect to the user's bank account and initiate the payment.

FlowPay is an authorized PIS Provider (PISP), meaning it can mediate between the user and their bank to initiate the payment upon the user's authorization.

PIS APIs allow users to initiate various traditional payment types:

- **Simple account-to-account payment**: The user can initiate a SEPA Credit Transfer (SCT) payment from one of their bank accounts.
- **Future-dated payment**: The payer can schedule a payment for a future date.
- **Recurring payment**: The payer can schedule a recurring payment with a fixed frequency.

In addition, FlowPay extends traditional payment methods by providing value-added services, such as:

- **Bulk payment**: The payer can initiate a single payment with a single Strong Customer Authentication (SCA) to pay multiple payment requests or documents at once.
- **Locked payment**: The user can authorize a payment to be executed only if a previous, related payment has been successfully received. The verification of the previous payment's status is performed by the client application that initiated the payment request.

Each of these services uses the FlowPay technical account, but the payment retains the original payer and payee information.

## Locked Payment

If the lockedUntil field is used, the sum will be kept until the date is reached. Until then the client is able to issue a refund of this payment by using the "Refunds" endpoint, or unlock the payment earlier using the "Charge" endpoint.

When a request to pay is locked a paymentMethod is returned that can be used on the "Charge" endpoint, to unlock the payment. When unlocking the payment no other field is necessary but a validation will be carried on in order to mantain data integrity.

## Bulk Payment

You can allow users to pay multiple payees in a single operation using the additionalPayees parameter when creating a payment request.

[![](https://mermaid.ink/img/pako:eNqFk81um0AQx18FTQ-5kGgxsGAOkUzanqoqcqxWqris2cFZFXbdZYnsWL70efpUeZIuH66hiRVOszO_-c9_PzhArjhCArVhBj8KttGsyqRjPy405kYo6XxZ9pkUJRYiF0zvF8719a2z4Fy0BCvv2R6xThyPkJfff17h6QU8fJO-u0DPwrfoS1aiM_1_setYru77qg26xGrRjjg7WvXK3-052HG26I0kp8V0spVp7W4wDi5stOCQGN2gCxXqirVLOLRdGZhHrDCDxIZrVtvIHeW_MS3YusS6BQ79mAwKJc1nVoly3_ddLdVaGXXlOk-oOZPMddq-ctA6tTyI52GQR7e7UXGrRdWevyqV7oEPnKNf5K-ZVGmOekwG1M-LYkQy-3qeWHvu6c_NmCxmRTzRHJHvyw4GVrgzY84jPglwxNX4q0GZ49emWk8lT3tqyWMmj_Zmtkz-UKo6XY5WzeYRkoKVtV01W37-Of5lNcrOaiMNJPNo1olAcoAdJF4Y3ZCQ0HlMI0r9yPNd2EMyC2KbpkEc0LmtUhIeXXju5pKbICC2jYRhHAbRPPKpC6wx6mEv85Ot3sgn-5iVHnwc_wL-ZjBd?type=png)](https://mermaid.live/edit#pako:eNqFk81um0AQx18FTQ-5kGgxsGAOkUzanqoqcqxWqris2cFZFXbdZYnsWL70efpUeZIuH66hiRVOszO_-c9_PzhArjhCArVhBj8KttGsyqRjPy405kYo6XxZ9pkUJRYiF0zvF8719a2z4Fy0BCvv2R6xThyPkJfff17h6QU8fJO-u0DPwrfoS1aiM_1_setYru77qg26xGrRjjg7WvXK3-052HG26I0kp8V0spVp7W4wDi5stOCQGN2gCxXqirVLOLRdGZhHrDCDxIZrVtvIHeW_MS3YusS6BQ79mAwKJc1nVoly3_ddLdVaGXXlOk-oOZPMddq-ctA6tTyI52GQR7e7UXGrRdWevyqV7oEPnKNf5K-ZVGmOekwG1M-LYkQy-3qeWHvu6c_NmCxmRTzRHJHvyw4GVrgzY84jPglwxNX4q0GZ49emWk8lT3tqyWMmj_Zmtkz-UKo6XY5WzeYRkoKVtV01W37-Of5lNcrOaiMNJPNo1olAcoAdJF4Y3ZCQ0HlMI0r9yPNd2EMyC2KbpkEc0LmtUhIeXXju5pKbICC2jYRhHAbRPPKpC6wx6mEv85Ot3sgn-5iVHnwc_wL-ZjBd)

The above diagram shows how bulk works.
We assume the case in which a user wants to pay Beneficiary A for 100€, Beneficiary B for 50€ and Beneficiary C for 25€ and again Beneficiary A for 75€.
The additionalPayees parameter will be populated like this (you can also specify a per-payee `remittanceInformation`; if omitted, the main request `remittanceInformation` is used):

```json
{
  "additionalPayees": [
    {
      "iban": "IT79Q0300203280941591243326",
      "name": "Beneficiary A",
      "amount": 100,
      "remittanceInformation": "Order #A-100"
    },
    {
      "iban": "IT79Q0300203280941591243327",
      "name": "Beneficiary B",
      "amount": 50
    },
    {
      "iban": "IT79Q0300203280941591243328",
      "name": "Beneficiary C",
      "amount": 25,
      "remittanceInformation": "Service fee C"
    },
    {
      "iban": "IT79Q0300203280941591243326",
      "name": "Beneficiary A",
      "amount": 75
    }
  ]
}
```

The payment request created will have an amount of 250€, payer can now pay it with a single payments.
The wire transfer allowed with the PIS on a bulk payment is addressed to the FlowPay technical account (TA).
When the TA receives the payment, it splits the amount among the beneficiaries, groups them by their IBANs and names, and sends the payments to them with wire transfers.

In case of a bulk payment to the same beneficiary, the payment initiation effective beneficiary is the beneficiary itself, so the payer can easily recognize the transaction. Otherwise, the payment initiation effective beneficiary is FlowPay.
Wire transfers to beneficiaries are sent with the same original payer, so beneficiaries can easily identify the payer.

<div class="info">
 <div class="title">In case of pagoPA payments</div>
    The bulk service is not natively supported with pagoPA payment, please contact us for more information and workarounds.
</div>

## Split Payment

[![](https://mermaid.ink/img/pako:eNqFk82OmzAQx18FTQ97YSM7QAIcKoV-nNpqlY1aqeLi4CFrFezUmFXYKJc-T5-qT1Jjwi50D-Vg2TO_-c8ff5yhUBwhhcYwg-8FO2hW59KzHxcaCyOU9D5th0iGEktRCKa7jXd7-9a7Yx1i6lFC_vz6_YrJHLPhXPQqrHJ0k3rRM_xvzhVsd3dD1sXmITtxgd2m7_oitBv8fLOWrYHN3NI8mY0GwIeDFhxSo1v0oUZds34J574sB_OANeaQ2umeNXbmT-JfmRZsX2HTA-ehTw6lkuYjq0XVDXU3W7VXRt343iNqziTzvb6uumqNJffi6dqIro6nSfKoRW038p2qlB6AN5xjUBavmUxpjnpKhqugKMsJyexpPrJ-v7MfhylZLst4pjkh_y97NbDDk5lylAQkxAnX4M8WZYFf2no_lxz_qScvubzYkzky-V2pejwcrdrDA6Qlqxq7ao_85bI-RzVKZ7WVBlJKAycC6RlOkK6TRZgkNIlCQqPlivrQWSYOF5QkwZoQe11WQRhcfHhyXckijgIax2s7LmMS0dgHtHdV6c_Dc3GvxgfWGnXfyWL0OTj74Mirsctf7aUOvw?type=png)](https://mermaid.live/edit#pako:eNqFk82OmzAQx18FTQ97YSM7QAIcKoV-nNpqlY1aqeLi4CFrFezUmFXYKJc-T5-qT1Jjwi50D-Vg2TO_-c8ff5yhUBwhhcYwg-8FO2hW59KzHxcaCyOU9D5th0iGEktRCKa7jXd7-9a7Yx1i6lFC_vz6_YrJHLPhXPQqrHJ0k3rRM_xvzhVsd3dD1sXmITtxgd2m7_oitBv8fLOWrYHN3NI8mY0GwIeDFhxSo1v0oUZds34J574sB_OANeaQ2umeNXbmT-JfmRZsX2HTA-ehTw6lkuYjq0XVDXU3W7VXRt343iNqziTzvb6uumqNJffi6dqIro6nSfKoRW038p2qlB6AN5xjUBavmUxpjnpKhqugKMsJyexpPrJ-v7MfhylZLst4pjkh_y97NbDDk5lylAQkxAnX4M8WZYFf2no_lxz_qScvubzYkzky-V2pejwcrdrDA6Qlqxq7ao_85bI-RzVKZ7WVBlJKAycC6RlOkK6TRZgkNIlCQqPlivrQWSYOF5QkwZoQe11WQRhcfHhyXckijgIax2s7LmMS0dgHtHdV6c_Dc3GvxgfWGnXfyWL0OTj74Mirsctf7aUOvw)

The above diagram shows how split works.
In case we want to pay beneficiary A 100€ and beneficiary B takes a 5€ commission on that payment, all that is needed is to add the beneficiary B to the additional Payees array.

```json
{
  "amount": 105,
  "currency": "EUR",
  "remittanceInformation": "Order #12345", 
  "payee": {
    "iban": "IT79Q0300203280941591243326",
    "name": "Beneficiary A"
  },
  "additionalPayees": [
    {
      "iban": "IT79Q0300203280941591243327",
      "name": "Beneficiary B",
      "amount": 5,
      "remittanceInformation": "Fee for #12345" 
    }
  ]
}
```

The total amount of the payment request must be specified, and the payee will receive the remaining amount after the split.
The wire transfer allowed with the PIS on a split payment is addressed to the FlowPay technical account (TA).
When the TA receives the payment, it splits the amount among the beneficiaries, groups them by their IBANs and names, and sends the payments to them with wire transfers.

The Wire transfer to the payee is sent with the original payer, the additional Payees receive the commission as a wire transfer with the payee as the payer.

### Split with customer payee

You can also direct a part of the payment to a registered customer by providing an object with the `customerId` and optional `remittanceInformation`.

```json
{
  "amount": 130,
  "currency": "EUR",
  "remittanceInformation": "Invoice #7890",
  "payee": {
    "iban": "IT79Q0300203280941591243326",
    "name": "Beneficiary A"
  },
  "additionalPayees": [
    {
      "customerId": "f1a56c5b-6e2a-4af9-8f77-4c9b1f0c2a22",
      "amount": 25,
      "remittanceInformation": "Commission for #7890"
    }
  ]
}
```
