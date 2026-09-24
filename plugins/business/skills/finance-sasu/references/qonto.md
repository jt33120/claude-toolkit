# Utiliser le connecteur Qonto

Qonto est un outil bancaire B2B pour PME europeennes. Ce connecteur expose ce que
l'utilisateur peut deja voir dans son compte Qonto. **Aucun outil n'execute de virement.** La
seule action proche d'un paiement (`create_multi_transfer_request`) cree une demande en
attente qu'un membre habilite doit approuver depuis l'app Qonto avec sa propre authentification
forte (2FA) — jamais depuis cette conversation.

## Factures {#factures}

- `list_client_invoices` — filtrer par statut (impayee, en retard) pour la relance.
- `get_client_invoice` — details d'une facture avant redaction de la relance.
- `create_client_invoice` — toujours montrer le brouillon (client, lignes, montant, TVA,
  echeance) avant creation.
- `send_client_invoice` — envoie sur un seul canal (email ou e-facturation selon le mandat
  national d'e-invoicing) ; preciser lequel a l'utilisateur avant d'envoyer. Uniquement apres
  validation explicite.
- `mark_client_invoice_as_paid` — seulement si l'utilisateur confirme le paiement recu hors
  Qonto (ex: virement recu mais pas encore rapproche).
- `list_transactions` (reglements recents) — croiser avant de relancer, pour ne pas relancer un
  client qui a deja paye. Fenetre recommandee : 14 jours.

## Devis

- `list_quotes`, `get_quote`, `create_quote`, `send_quote`, `delete_quote` — meme logique que
  les factures : brouillon montre, validation avant envoi.

## Tresorerie {#tresorerie}

- `list_bank_accounts` — solde actuel, a dater precisement ("solde au [date]").
- `list_transactions` — historique pour estimer les delais de paiement moyens par client.
- `list_supplier_invoices` — decaissements a venir.
- `get_statement` / `list_statements` — releves pour verification si besoin d'un justificatif.

### Construire le previsionnel
1. Solde de depart, date exacte.
2. Encaissements attendus par fenetre (0-30 / 31-60 / 61-90j), ajustes par le delai de paiement
   historique du client (si un client paie a 45j en moyenne, une facture a J+20 ne rentre pas
   dans la fenetre 30 jours).
3. Decaissements connus : factures fournisseurs, charges fixes (loyer, abonnements SaaS,
   charges sociales du president si remunere — voir skill `payroll`), echeance URSSAF/TVA si
   connue.
4. Net par fenetre, avec une fourchette prudente/optimiste plutot qu'un chiffre unique.
5. Risques nommes : quel client, quel montant, quel decalage.

## Transactions et cloture

- `list_transactions` — reperer les non categorisees.
- `list_transaction_attachments` / `get_attachment` — verifier les justificatifs presents.
- `modify_transaction_cash_flow_category` — uniquement apres validation de l'utilisateur sur
  chaque changement propose ; ne jamais recategoriser en masse sans accord.
- Doublons suspects : meme montant + meme tiers + moins de 5 jours d'ecart → signaler, ne pas
  trancher a la place de l'utilisateur.

## Ce que Qonto ne fait jamais depuis cet outil
- Ne deplace pas d'argent (pas de virement execute).
- N'approuve pas une demande de virement (l'approbation se fait dans l'app Qonto avec la 2FA de
  l'utilisateur — au mieux, ce connecteur renvoie un lien vers l'app).
- Ne contourne jamais l'authentification forte.

Si l'utilisateur demande "peux-tu payer ce fournisseur" ou "valide ce virement", la reponse est
toujours : non, mais voici ce qu'il faut faire dans l'app Qonto.
