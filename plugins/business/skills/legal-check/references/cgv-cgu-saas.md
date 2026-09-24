# CGV / CGU pour un SaaS francais

Non exhaustif, non un avis juridique. A faire relire par un avocat avant publication,
surtout si vente B2C.

## CGV vs CGU
- **CGV (conditions generales de vente)** : regissent l'acte de vente — prix, paiement, duree,
  resiliation, garanties. Obligatoires des qu'il y a une transaction commerciale.
- **CGU (conditions generales d'utilisation)** : regissent l'usage du service — comportement,
  contenu, propriete intellectuelle, disponibilite. Utiles meme sur une offre gratuite (freemium).
- Un SaaS payant a generalement les deux, parfois fusionnees en un seul document.

## Mentions obligatoires (B2B et B2C)
- Identification de l'editeur : denomination sociale, forme (SASU), capital, siege social,
  RCS/SIREN, TVA intracommunautaire, directeur de publication, hebergeur.
- Description du service, prix TTC (et HT si B2B), modalites de paiement, duree d'engagement.
- Conditions de resiliation, y compris la reconduction tacite (loi Chatel — informer le client
  de la possibilite de ne pas reconduire, avec un delai avant echeance).
- Disponibilite / SLA si engage contractuellement (sinon, formuler en moyens, pas en resultat).
- Traitement des donnees personnelles (renvoi vers la politique de confidentialite RGPD).
- Droit applicable et juridiction competente.
- Modalites de reclamation / mediation (obligatoire en B2C — mediateur de la consommation).

## Specifique B2C
- **Droit de retractation** : 14 jours, MAIS exception classique pour le contenu numerique
  fourni immediatement (abonnement SaaS actif des la souscription) si le client a renonce
  expressement a son droit de retractation en cochant une case dediee avant paiement — sans
  cette renonciation explicite et documentee, le droit de retractation s'applique.
- Information precontractuelle claire (art. L221-5 Code conso) : prix total, duree, modalites
  de resiliation, existence de la retractation ou de son exclusion.
- Clauses abusives interdites (art. L212-1 et R212-1/R212-2 Code conso) : ex. modification
  unilaterale du prix sans preavis, exoneration totale de responsabilite de l'editeur, clause
  compromissoire imposee.

## Specifique B2B
- Plus de liberte contractuelle, mais delais de paiement legaux (30-60 jours) et penalites de
  retard s'appliquent quand meme.
- Si le client est une TPE/PME, certaines protections du Code de commerce sur le desequilibre
  significatif (art. L442-1) peuvent s'appliquer par analogie — eviter les clauses trop
  asymetriques meme en B2B.

## Points frequents a couvrir pour un SaaS IA
- Qui est proprietaire des donnees entrees par l'utilisateur, et des sorties generees par l'IA.
- Limitation de responsabilite sur les sorties d'un systeme d'IA generative (le service est
  fourni "en l'etat", pas de garantie d'exactitude — a formuler clairement sans etre abusif).
- Politique d'usage acceptable (pas de contenu illegal, pas d'usage pour entrainer un systeme
  concurrent, etc.).
- Sous-traitance a des fournisseurs d'IA tiers, mentionnee en transparence (recoupe le RGPD, cf.
  `rgpd-ai-act.md`).
- Portabilite / export des donnees a la resiliation.

## Structure suggeree
```
1. Objet et acceptation
2. Description du service et acces (compte, identifiants)
3. Prix, facturation, paiement
4. Duree, resiliation, reconduction
5. Propriete intellectuelle (editeur, contenu utilisateur, sorties IA)
6. Donnees personnelles (renvoi politique de confidentialite)
7. Disponibilite, maintenance, support
8. Responsabilite et garanties
9. Droit de retractation (B2C) ou son exclusion documentee
10. Droit applicable, litiges, mediation
11. Mentions legales de l'editeur
```

A verifier avant publication : service-public.fr (fiches CGV/CGU), economie.gouv.fr (DGCCRF),
et idealement un avocat specialise numerique pour la version finale.
