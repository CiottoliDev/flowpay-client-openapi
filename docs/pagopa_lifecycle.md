FlowPay is a Payment Service Provider (PSP) that enables seamless payment of PagoPA notices through its API. PagoPA is an Italian payment system designed to simplify and standardize the payment of public administration services and other entities. It ensures that payments are made securely and that funds are transferred directly to the respective government or public entity.

As a direct PSP participant in the PagoPA network, FlowPay is fully integrated with the PagoPA system, ensuring real-time updates and secure processing of payments. Notably, FlowPay is also the first open banking PSP to join the PagoPA network, pioneering a new approach to public service payments through open banking technologies.

FlowPay allows users to pay PagoPA notices by providing the taxpayer identification number (codice fiscale) of the creditor entity and the notice number. Given the dynamic nature of the amounts due, which may change over time, FlowPay automatically updates the payable amount daily and each time a payment session is initiated.

When a payment session for a PagoPA document is started, FlowPay communicates the activation of the notice to the PagoPA system. This notice becomes payable exclusively through the specific session until it is unlocked by FlowPay, which can last up to 30 minutes. Upon successful authorization of the payment, FlowPay releases the payer from the debt and issues a receipt. If an email address is provided via the document upload API, FlowPay sends the receipt by email; otherwise, the partner can retrieve it from the API using `GET /payment-requests/{requestId}` with header `Accept: application/pdf`.

Additionally, if the partner prefers, they can generate their own receipt to send to the payer by utilizing the data retrievable from FlowPay's API. This allows the partner to have full control over the customer experience and the format of the receipt.

Once the payment is authorized, neither the partner using the API nor the debtor has any further obligations. FlowPay autonomously handles the reconciliation and the transfer of funds to the creditor entities, streamlining the entire process and ensuring compliance with the PagoPA framework.

<a target="_blank" href="https://flowpay.s3.eu-west-3.amazonaws.com/files/5DE00DFD-E422-4A65-96B1-CCDF29F65197.pdf">
  <button style="background-color: #263238; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;">
  Receipt preview</button>
</a>
