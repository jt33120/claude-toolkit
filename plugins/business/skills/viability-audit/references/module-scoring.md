# Module optionnel — Matrice ponderee et test de mort

A charger seulement en Phase 5, entre survivants ayant tous franchi les portes de `portes.md`. Ne remplace
jamais les portes : un scoring n'intervient qu'apres elimination, jamais a la place.

## La matrice

Une ligne par critere, une colonne par projet survivant. **Chaque cellule porte sa justification et sa
source** — un total sans detail est incontestable et donc inutilisable.

Echelle 0-5, ancree :

| Note | Signification |
|---:|---|
| 0 | Preuve du contraire trouvee pendant ce run |
| 1 | Rien trouve qui soutienne le critere |
| 2 | Soutenu par du declaratif porteur uniquement |
| 3 | Source indirecte ou raisonnement analogique |
| 4 | Source directe et datee |
| 5 | Plusieurs sources directes convergentes, ou code lu |

Score = note x poids / 5. Total sur 100. Criteres par defaut (a re-ponderer selon l'objectif du porteur —
revente, revenu exploite soi-meme, ou actif de credibilite) : avantage injuste (25), vitesse jusqu'a la
premiere preuve externe (20), marche adressable reel et solvable (15), defensabilite a 24 mois (15), acquereurs
actifs identifies (15), cout du kill (10).

**Regle anti-illusion de precision.** Deux projets separes de moins de 8 points sont a egalite. Le dire, et
trancher sur le cout du kill ou la conviction du porteur, jamais sur le total.

## Le test de mort le moins cher

Pour chaque projet : l'experience la plus rapide et la moins chere qui **prouverait que le projet est mort**
(charge de la preuve inversee expres). Quatre proprietes : falsifiable (resultat precis, decide d'avance),
court (<= 2 semaines), externe (implique quelqu'un sans raison d'etre gentil), sans construction.

Forme : *« Si `{action}` ne produit pas `{resultat mesurable}` avant `{date}`, le projet est mort. »*

Exemples fictifs : B2B — « Si sur 5 conversations avec des responsables ayant le budget, aucun ne decrit ce
probleme spontanement, mort. » Marketplace — « Si je ne peux pas recruter 20 vendeurs du cote difficile en
2 semaines sans depenser un euro, mort. »
