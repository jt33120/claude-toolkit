# Grille de revue contractuelle (France)

Non exhaustif, non un avis juridique. A verifier contre service-public.fr / Code civil / Code
de commerce a jour, ou un avocat.

## Categories de risque

### Paiement et delais
- Delai de paiement legal B2B : 30 jours a compter de la reception (60 jours si convenu par
  contrat, plafond legal). Au-dela : anormal, a questionner.
- Penalites de retard : taux legal minimum (3x taux d'interet legal) + indemnite forfaitaire de
  recouvrement de 40€ (obligatoire meme si non mentionnee, mais mieux vaut l'ecrire).
- Clause de reserve de propriete : le bien/service reste la propriete du prestataire jusqu'au
  paiement complet — utile a inclure cote prestataire.
- Acompte : usage courant 30% a la commande pour du conseil/dev sur mesure.

### Responsabilite et assurance
- Responsabilite illimitee = rouge, quasi systematique a plafonner (ex: montant du contrat,
  ou X mois de facturation).
- Assurance RC Pro : verifier que le contrat n'exige pas une couverture disproportionnee par
  rapport a la taille de la SASU.
- Clause abusive (art. L212-1 Code de la consommation, applicable B2C, et par analogie
  jurisprudentielle a certains B2B avec asymetrie forte) : desequilibre significatif entre
  droits et obligations.

### Resiliation
- Preavis raisonnable (30-90 jours usuels).
- Reconduction tacite : loi Chatel impose d'informer le client de la possibilite de ne pas
  reconduire, avec un delai avant echeance — sinon reconduction contestable.
- Sortie : restitution des donnees/livrables, assistance a la transition, ce qui reste du.

### Propriete intellectuelle
- Par defaut en droit francais, le prestataire (freelance/SASU) reste titulaire des droits
  d'auteur sur ses creations sauf cession expresse ecrite (art. L131-3 CPI — la cession doit
  etre explicite, delimitee en etendue, destination, lieu, duree).
- Attention aux clauses de cession large "tout ce qui est produit dans le cadre de la mission"
  — verifier que ca ne capture pas vos outils/frameworks reutilisables (background IP).
- Si vous utilisez de l'IA generative pour produire des livrables, clarifier qui est titulaire
  des sorties et si le client en est informe.

### Confidentialite
- Duree standard 2-5 ans apres la fin du contrat. Perpetuelle = a discuter sauf secrets
  d'affaires reels.
- Exclusions standards : information publique, deja connue, developpee independamment,
  requise par la loi.

### Non-concurrence / non-sollicitation
- Une clause de non-concurrence imposee a un prestataire independant doit etre limitee dans le
  temps, l'espace et l'activite, et proportionnee — sinon contestable.
- Non-sollicitation de salaries : usage courant, 12-24 mois, limitee aux personnes
  effectivement impliquees dans la mission.

### Droit applicable et litiges
- Droit francais + tribunal competent (siege du defendeur par defaut, ou clause attributive
  de competence si B2B).
- Clause compromissoire (arbitrage) : rare et couteux pour une SASU, generalement a eviter sauf
  contrat international a fort enjeu.

## NDA — triage rapide {#nda}

**VERT** — approbation standard :
- Mutuelle (ou unilaterale coherente avec le sens du partage d'info).
- Duree 2-3 ans (jusqu'a 5 ans si secrets industriels).
- Exclusions standards presentes (info publique, deja connue, developpement independant,
  obligation legale de divulguer).
- Pas de non-concurrence, pas de non-sollicitation, pas de clause d'exclusivite.
- Droit francais, tribunal raisonnable.

**ORANGE** — a ajuster :
- Champ de la confidentialite tres large mais pas deraisonnable.
- Duree plus longue que standard mais dans la norme du marche.
- Une exclusion manquante, facile a ajouter.
- Clause de non-sollicitation etroite et limitee dans le temps.

**ROUGE** — a retravailler avant signature :
- Unilaterale dans le mauvais sens (vous engagez sans reciprocite alors que le partage est
  mutuel).
- Exclusions essentielles absentes (developpement independant, obligation legale).
- Non-concurrence ou exclusivite cachee dans une NDA.
- Duree perpetuelle sans justification de secret industriel.
- Clause de residuals large (droit d'utiliser ce qui reste "en memoire" sans limite) —
  equivaut a une licence deguisee.
- Le document n'est pas vraiment une NDA (contient des clauses commerciales substantielles).

## Format de synthese suggere

```
## Revue — [nom du document]
Parties : [X] / Vous etes : [prestataire/client/editeur]
Verdict : [Signer / Negocier / Consulter un avocat]

### Points rouges
- [Clause citee] — [risque] — [reformulation proposee]

### Points orange
- [Clause citee] — [risque] — [reformulation proposee]

### A connaitre
- [echeances, renouvellement, etc.]

### Rappel
Ceci n'est pas un avis juridique. Points a faire verifier par un avocat : [liste].
```
