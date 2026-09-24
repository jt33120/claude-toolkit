# Triage, priorisation, escalade

## Categories {#triage}
| Categorie | Description | Signaux |
|---|---|---|
| Bug | Le produit se comporte mal | erreur, plante, ne fonctionne pas |
| Comment faire | Besoin d'aide pour utiliser le produit | comment je, ou est, configurer |
| Demande de fonctionnalite | Capacite qui n'existe pas | serait bien si, envisagez-vous |
| Facturation | Paiement, abonnement, facture | facture, prelevement, rembourser |
| Compte | Acces, permissions, parametres | connexion, mot de passe, acces |
| Integration | Connexion a un outil tiers | API, webhook, synchronisation |
| Securite | Donnees, acces non autorise | fuite, non autorise, RGPD |
| Performance | Lenteur, indisponibilite | lent, timeout, indisponible |

Regle : si le client ne peut pas se connecter a cause d'un bug, c'est un Bug, pas un probleme de
Compte — la cause racine determine la categorie.

## Priorites
- **P1 — Critique** : produit inutilisable, perte/corruption de donnees, incident de securite.
  Reponse immediate, mise a jour reguliere jusqu'a resolution.
- **P2 — Elevee** : fonctionnalite majeure cassee, plusieurs clients touches, pas de
  contournement. Reponse le jour meme.
- **P3 — Moyenne** : contournement disponible, un seul client touche. Reponse sous 1-2 jours
  ouvres.
- **P4 — Basse** : cosmetique, demande de fonctionnalite, question generale. Reponse sous
  quelques jours.

## Escalade {#escalade}

Format de brief, utile meme en solo pour prioriser son propre backlog ou briefer un prestataire :

```
## ESCALADE : [resume en une ligne]

Severite : [Critique/Elevee/Moyenne]
Client(s) touche(s) : [qui, combien]
Impact : [ce qui est bloque]
Depuis : [date/duree]

### Ce qui a ete tente
[liste]

### Etapes de reproduction (si bug)
1. [etape]
2. [etape]
Attendu : [X]
Observe : [Y]

### Ce qu'il faut
[investiguer / corriger / decider X]
Echeance : [date]
```

Pour une panne touchant plusieurs clients : preparer un message de statut clair (ce qui se
passe, impact, statut, ETA si connue) plutot que de repondre a chacun separement de facon
incoherente.
