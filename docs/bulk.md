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
      "remittanceInformation": "Order A-100"
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

The payment request created will have an amount of 250€; the payer can now pay it with a single payment.
The wire transfer allowed with the PIS on a bulk payment is addressed to the FlowPay technical account (TA).
When the TA receives the payment, it splits the amount among the beneficiaries, groups them by their IBANs and names, and sends the payments to them with wire transfers.

In case of a bulk payment to the same beneficiary, the payment initiation effective beneficiary is the beneficiary itself, so the payer can easily recognize the transaction. Otherwise, the payment initiation effective beneficiary is FlowPay.
Wire transfers to beneficiaries are sent with the same original payer, so beneficiaries can easily identify the payer.

<div class="info">
 <div class="title">In case of PagoPA payments</div>
    The bulk service is not natively supported with PagoPA payments; please contact us for more information and workarounds.
</div>
