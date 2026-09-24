# TVA et cloture mensuelle — reperes SASU

Non exhaustif. Seuils et taux a verifier sur impots.gouv.fr avant toute decision — ils sont
revalorises regulierement (generalement chaque annee).

## Franchise en base de TVA
- Une SASU dont le chiffre d'affaires reste sous certains seuils (differents pour les
  prestations de services et les ventes de marchandises) peut etre en franchise en base : pas
  de TVA facturee, pas de TVA deductible, mention obligatoire sur facture ("TVA non applicable,
  art. 293 B du CGI").
- Au-dela du seuil (ou du seuil majore de tolerance), l'assujettissement devient obligatoire,
  generalement des le mois de depassement.
- Un consultant IA qui facture aussi bien du conseil que des abonnements SaaS doit suivre son
  CA cumule sur l'annee glissante et alerter l'utilisateur en approche de seuil plutot que
  d'attendre le depassement.

## Regimes de declaration (si assujetti)
- **Reel simplifie** : declaration annuelle avec acomptes semestriels — regime frequent pour une
  jeune SASU.
- **Reel normal** : declaration mensuelle (ou trimestrielle si TVA due faible) — regime frequent
  des que le CA ou la TVA collectee augmentent.
- Le choix du regime et les seuils de bascule sont a confirmer avec l'expert-comptable ou
  impots.gouv.fr — ne jamais l'affirmer sans verification recente.

## TVA intracommunautaire
- Vente de SaaS a des clients B2B dans l'UE : generalement autoliquidation par le client
  (numero de TVA intracommunautaire du client a collecter et verifier via VIES).
- Vente a des particuliers UE (B2C) pour un service electronique : regles specifiques
  (guichet unique OSS) — a verifier au cas par cas, ne pas presumer.
- Hors UE : generalement hors champ de TVA francaise, conditions a verifier.

## Checklist de cloture mensuelle (rapide, pour une SASU sans comptable interne)

1. **Factures emises** — toutes generees et envoyees pour le mois ? Aucune en attente de
   validation client qui traine.
2. **Factures fournisseurs** — toutes recues et rapprochees avec les transactions bancaires ?
3. **Transactions non categorisees** — lister, presenter, faire trancher l'utilisateur.
4. **Justificatifs manquants** — depenses sans facture/recu attache, au-dela d'un seuil
   raisonnable (ex: 25€) a signaler.
5. **Doublons suspects** — meme montant, meme tiers, sous 5 jours.
6. **Charges sociales du president** (si remunere) — echeance URSSAF du mois verifiee (voir
   skill `payroll`).
7. **TVA** — collectee vs deductible, echeance de declaration si applicable ce mois-ci.
8. **Tresorerie** — solde de fin de mois, comparaison au mois precedent, ecart de plus de 10%
   explique.
9. **Export pour l'expert-comptable** — factures, releves, justificatifs rassembles dans un
   dossier ou fichier, pret a transmettre.

## Rappel
Ce skill ne remplace pas un expert-comptable. Il prepare, categorise et signale — la
declaration fiscale et sociale reste sous la responsabilite du dirigeant, verifiee avec un
professionnel. En cas de doute sur un seuil, un taux ou une echeance : le dire explicitement et
renvoyer vers impots.gouv.fr, urssaf.fr, ou l'expert-comptable.
