# Fee structure

FlowPay provides a fully automated fee management system that simplifies the process for partners, eliminating the need to integrate specific APIs for fee collection.

Fees calculation rules are determined during the initial system setup, tailored to the specific contractual requirements of each partner. These fees can be charged either to the creditor or the debtor, depending on the case. When the creditor is responsible for the fee, a split payment is automatically generated. Conversely, if the debtor bears the cost, a bulk payment is triggered.

The fee calculation rules are flexible and can be customized to suit various payment scenarios. Rules can be defined based on the type of payment (e.g., bulk, split, locked, PagoPA) and the payment method used (e.g., PIS, SDD, card). Also, minimum amounts can be set, below which fees are not applied, allowing for exceptions to the general rule or progressive fee structures.
Rules also determine which party will be responsible for the fees, ensuring a clear and transparent process.
Every fee rule is composed of a fixed component and a variable one based on the amount of the transaction.
For bulk and split payments, the fee includes an additional fixed component for each beneficiary; this covers the costs of payments from the technical account to the beneficiaries.

In case of partial payments, the system automatically calculates the fee based on the amount of the single payment, ensuring that the fee is applied consistently across all payments. If the fee rule changes, the system automatically applies the new rules to all future payments, ensuring that the most up-to-date fee structure is always in effect.

# Lifecycle

When the payer selects the payment method to be used, the fee calculation is done automatically by the payment gateway retrieving the most up-to-date rule applicable to that specific payment. Once the calculation is performed, the gateway automatically inserts the fee amount into the payment request.
