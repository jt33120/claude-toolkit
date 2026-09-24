---
name: finance-sasu
description: "Runs invoicing, quotes, transaction review, overdue-payment reminders, TVA tracking, and a 30/60/90-day cash forecast for a French SASU, using the Qonto connector when present. Triggers (EN): who owes me money, cash flow forecast, will I make it this month, TVA, invoice this client, chase this invoice, month-end close, bank transactions. Triggers (FR): qui me doit de l'argent, previsionnel de tresorerie, est-ce que je passe le mois, TVA, facturer ce client, relancer cette facture, cloture du mois, transactions bancaires, devis."
model: claude-opus-5-5
effort: medium
---

<!--
Provenance: merged and adapted for France from Anthropic knowledge-work-plugins
(Apache-2.0, https://github.com/anthropics/knowledge-work-plugins):
- small-business/skills/invoice-chase
- small-business/skills/cash-flow-snapshot
- small-business/skills/month-end-prep
Adaptation: French SASU, Qonto MCP as primary connector, TVA regime, no direct money movement.
-->

# Finance SASU

Facturation, relances, tresorerie et cloture mensuelle pour une SASU freelance/consultant.
Utilise le connecteur **Qonto** quand il est present pour les factures, devis, transactions et
relances. **Qonto ne peut jamais deplacer d'argent depuis cet outil** — toute action sensible
(virement, validation de paiement) demande l'authentification forte (2FA) de l'utilisateur dans
l'app Qonto elle-meme. Ici, on prepare, on relance, on projette — l'humain valide et paie.

## Quand l'utiliser
- "Qui me doit de l'argent" / relance de factures impayees.
- "Est-ce que je passe le mois" / previsionnel de tresorerie.
- Cloture mensuelle : rapprochement, TVA, ce qu'il reste a faire avant l'expert-comptable.
- Creer un devis ou une facture pour un client.

## Workflow

### 1. Relances de factures impayees (`references/qonto.md#factures`)
Avec Qonto connecte : lister les factures clients en retard (`list_client_invoices`, statut
impaye), croiser avec les transactions recentes pour eviter de relancer un paiement deja recu,
et rediger une relance adaptee au ton (premiere relance courtoise, relance ferme au-dela de
30 jours). **Rien n'est envoye sans validation explicite.** Sans Qonto, demander un export ou
la liste des factures en retard.

### 2. Devis et factures
Creer un devis (`create_quote`) ou une facture (`create_client_invoice`) sur demande, a partir
des informations client et des prestations. Toujours montrer le brouillon avant creation.
Envoi (`send_client_invoice`, `send_quote`) uniquement apres validation. TVA a appliquer selon
le regime de l'utilisateur (voir `references/tva-cloture.md`) — demander le regime si inconnu,
ne jamais le presumer.

### 3. Previsionnel de tresorerie 30/60/90 jours (`references/qonto.md#tresorerie`)
Solde bancaire actuel (`list_bank_accounts`), factures clients en attente (encaissements
prevus), factures fournisseurs (`list_supplier_invoices`, decaissements prevus), charges fixes
connues (loyer, abonnements, URSSAF/charges sociales si president remunere — voir skill
`payroll`). Construire trois fenetres (0-30, 31-60, 61-90 jours) avec un scenario prudent et un
scenario optimiste. Toujours dater le solde de depart ("solde au [date]").

Signaler les risques nommement : "facture Client X, 3200€, historiquement payee a 45 jours,
sort de la fenetre 30 jours" plutot qu'un chiffre generique.

### 4. Rapprochement et preparation de cloture (`references/tva-cloture.md`)
Lister les transactions non categorisees, les depenses sans justificatif attache
(`list_transaction_attachments`), les doublons suspects (meme montant, meme tiers, moins de
5 jours d'ecart). Presenter la liste a l'utilisateur avant toute conclusion — ne jamais
modifier une transaction ou sa categorie sans validation.

### 5. TVA
Suivre le chiffre d'affaires cumule vs seuils de franchise en base de TVA, ou, si assujetti,
rappeler l'echeance de declaration (mensuelle, trimestrielle, ou annuelle selon le regime
choisi). Ne jamais affirmer un seuil ou un taux sans le signaler comme "a verifier sur
impots.gouv.fr" — ces seuils sont revises regulierement.

## Garde-fous

- **Aucune action ne deplace d'argent.** Qonto ne le permet pas depuis cet outil ; toute demande
  de virement ou de paiement s'arrete a "voici ce qu'il faudrait faire dans l'app Qonto avec
  votre 2FA."
- Rien n'est envoye (facture, relance, devis) sans validation explicite de l'utilisateur.
- Ne jamais inventer un solde, une echeance ou un montant — s'il manque une donnee, le dire et
  demander.
- TVA, seuils, taux et delais : toujours signaler qu'ils doivent etre verifies contre
  impots.gouv.fr, urssaf.fr ou l'expert-comptable — ces chiffres changent.
- Sans Qonto connecte : fonctionne quand meme a partir d'un export CSV ou de chiffres donnes a
  la main. Le dire clairement plutot que bloquer.
- Textes adresses a des clients (relances) passent par les skills coeur `writing-voice` et
  `language-strategy`.

## References

- `references/qonto.md` — usage du connecteur Qonto : factures, devis, transactions, relances
- `references/tva-cloture.md` — TVA (franchise en base, regimes), checklist de cloture mensuelle
