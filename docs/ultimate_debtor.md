Determines who appears as the originator on the account statement or on the receipt.

<!-- <br>
It can take the following values:
- `debtor`
- `payee`
- `payer`
- `tenant`
- `anonymous` -->

In the case of a PagoPA payment, this value is used to generate the receipt.

<div class="critical">
    <div class="title"> <span>&#9888;&#65039;</span>Warning</div>
    <div>If different from <code>debtor</code>, the payment is routed to a technical account and re-issued after the funds are received.</div>
</div>
