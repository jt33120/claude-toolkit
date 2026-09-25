---
name: inventory
description: "Works out what to reorder and when, from actual sales/usage velocity — physical goods or SaaS resources like licenses, seats, or API quotas. Triggers (EN): what do I need to reorder, am I going to run out, restock, how much stock is left, draft a purchase order, we're running low on licenses. Triggers (FR): que dois-je reapprovisionner, je vais bientot manquer de stock, reappro, combien de stock reste-t-il, bon de commande, on manque de licences."
---

<!--
Provenance: adapted from Anthropic knowledge-work-plugins (Apache-2.0,
https://github.com/anthropics/knowledge-work-plugins):
- small-business/skills/inventory-planner
- small-business/skills/restock
Kept generic: applies to physical products or SaaS resources (licenses, seats, API quotas).
-->

# Inventory

Calcule ce qu'il faut reapprovisionner et quand, a partir de ce qui se consomme vraiment. Fait
pour du stock physique (materiel, fournitures) ou des ressources SaaS (licences tierces, sieges,
quotas d'API a renouveler).

## Quand l'utiliser
- "Qu'est-ce que je dois recommander" / risque de rupture.
- Suivre la consommation d'un quota ou d'un pool de licences.
- Preparer un bon de commande ou un email fournisseur.

## Workflow

### 1. Recuperer la consommation
Historique de vente ou de consommation par article/ressource, stock actuel (ou quota restant),
cout unitaire, fournisseur, delai de reapprovisionnement si connu. A partir d'un export ou de
chiffres donnes directement — aucun connecteur requis.

### 2. Calculer la vitesse
Vitesse sur 7 jours (tendance recente) et sur 28 jours (base stable) — les deux, la divergence
est un signal (pic ponctuel vs tendance reelle). Une periode de rupture n'est pas une demande
nulle — ne pas la compter comme telle.

### 3. Projeter la date de rupture, prudemment
Stock actuel / vitesse la plus elevee des deux fenetres. Comparer au delai de
reapprovisionnement pour savoir s'il reste le temps de commander. Ne jamais donner de date de
rupture pour un article sans historique suffisant — le dire explicitement.

### 4. Dimensionner la commande
Cible par defaut : 60 jours de couverture + delai de reapprovisionnement, base sur la vitesse
28 jours (pas la plus rapide). Soustraire ce qui est deja en commande. Arrondir au conditionnement
du fournisseur en le signalant.

### 5. Signaler ce qui ne bouge pas
Articles a vitesse nulle : jamais une commande candidate — signaler comme stock dormant avec le
montant immobilise, ne pas calculer de date de rupture (ca n'a pas de sens sur du zero).

### 6. Presenter et faire valider
Total en euros et nombre d'articles urgents en tete. Rediger le bon de commande et l'email
fournisseur **sans les envoyer** — validation explicite requise avant tout envoi ou engagement
de depense.

## Garde-fous

- Ne jamais inventer une vitesse, un delai, ou une date de rupture — signaler l'historique
  insuffisant par article.
- Ne jamais recommander un article a vitesse nulle.
- Ne jamais envoyer un bon de commande ou un email fournisseur sans validation explicite.
- Toujours donner les montants en euros, pas seulement en unites — la decision porte sur de
  l'argent.
- Textes adresses a un fournisseur passent par les skills coeur `writing-voice` et
  `language-strategy`.
