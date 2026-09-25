---
name: viability-audit
description: "Qualifie par elimination si un projet peut rapporter de l'argent, et departage plusieurs projets candidats. Triggers FR: audit de viabilite, ce projet est-il viable, lequel de mes projets je garde, faut-il continuer ce projet. Triggers EN: viability audit, is this project viable, should I kill this project, which project should I build."
---

<!-- Provenance: base and references/ adapted from the author's private skill "audit-viabilite" (elimination gates, French freelance/SASU context).
Optional modules (references/module-*.md) adapted from anthropics/knowledge-work-plugins, private skill "product-viability-audit"
(same author, unreleased) — code-truth extraction, market recon fan-out, weighted scoring, red team. All examples below are fictional. -->

# Audit de viabilite

## Ce que fait ce skill

Repond a une seule question : **ce projet peut-il rapporter de l'argent, et si plusieurs, lequel garder ?**

Par **elimination**, pas par notation. Un projet ne « marque pas des points » : il franchit des portes, ou il
meurt a l'une d'elles. Un zero a une porte n'est jamais rattrapable par un excellent score ailleurs. Un scorecard
pondere laisse un defaut fatal se compenser par une force sans rapport — trois degres de liberte (criteres, poids,
notes) suffisent a obtenir n'importe quel resultat sous apparence quantitative. **Les portes sont conjonctives.**
Une note n'apparait qu'a la toute fin, et seulement pour departager des survivants (Phase 5, `references/module-scoring.md`).

S'arrete sur un verdict, l'objection la plus forte contre ce verdict, et une condition de mort. **Ne produit ni
business plan, ni PRD, ni roadmap, ni code.** Doit passer par les skills `writing-voice` et `language-strategy`
pour toute sortie destinee a un humain.

## Regles dures — non negociables

1. **DECLARE != OBSERVE.** Ce qui vient des fichiers, du porteur ou d'un tiers entre comme DECLARE. N'entre comme
   OBSERVE que ce que tu as verifie toi-meme (domaine qui resout, service qui repond, commit qui existe, comptes
   deposes). Chaque ligne « fait » porte une source ou une commande en clair, datee.
2. **Aucun verbatim resume.** Les paroles de prospects vont brutes dans `verbatims.md`, jamais reformulees.
3. **« Ca pourrait etre utile » est un non.** Seul compte un engagement qui coute quelque chose a celui qui le donne.
4. **Une hypothese portante non verifiee bloque l'aval.**
5. **Jamais la meme conversation pour generer une hypothese et l'evaluer.** Delegue la refutation a un sous-agent.
6. **Ne jamais poser une question dont la reponse est dans le dossier.**
7. **Une porte franchie « de justesse » est une porte echouee.**

Si le porteur propose un cadre classique (SWOT, Business Model Canvas, Porter, personas, RICE...), ou si tu es
toi-meme tente d'en produire un : charge `references/theatre.md` avant de repondre.

## Resolution des chemins

Chemins nus = depuis la racine du skill. `references/*.md` se chargent a la demande, jamais toutes d'un coup.
`{doc_workspace}` par defaut : `{project-root}/_audit/audit-<projet-slug>-<date>/`.

## Phase 0 — Avant de regarder quoi que ce soit

Trois ecrits avant toute lecture du projet, sinon l'audit s'auto-annule :
- **0.a Budget de l'audit** — plafond en heures et euros, ecrit et date. Defaut : ~10h pour trier N projets, +20h
  sur le survivant jusqu'au premier euro demande.
- **0.b Classement de preference, date** — s'il y a plusieurs projets, faire ecrire le classement intuitif
  maintenant. Si le classement final est identique, l'audit est **non concluant**.
- **0.c Perte acceptable** — mois et euros acceptes en perte, ecrit avant.

Cree ensuite `{doc_workspace}/.memlog.md` (frontmatter `topic`, `mode`, `status: en_cours`), une ligne horodatee
par entree, append seul.

## Phase 1 — Decouverte automatique

Charge `references/decouverte.md`. Lis ce que tu trouves, **n'exige rien**. README, historique git, decks,
sorties anterieures entrent en DECLARE ; ce qui est verifiable (DNS, services, commits) entre en OBSERVE.
Deduis l'archetype (B2C, B2B, marketplace, outil interne...) du contenu, jamais d'une case a cocher.
Produis la table des affirmations portantes (3-5 lignes) : DECLARE/OBSERVE, source datee, cout de verification.

**Module optionnel — verite code.** Si le projet a un depot de code, charge `references/module-code-truth.md` :
un sous-agent extrait ce qui est REEL / PARTIEL / FACTICE depuis le code, pas depuis le pitch.

## Phase 2 — Les questions

Une question par message, jamais de mur. Ordre : heures disponibles/semaine (disponibles, pas souhaitees) ;
seul ou accompagne ; est-il lui-meme la cible et qui connait-il nominativement dans l'audience ; a quoi ressemble
le revenu « reussi ».

## Phase 3 — Les portes

Charge `references/portes.md`. Deux axes gouvernent l'ordre : **qui execute** (agent seul, quasi gratuit, sur
tous les projets · porteur seul · exige un tiers humain, ressource rare) et **la latence** (ce qui prend du temps
a recruter se lance jour 1, en parallele).

- **P0 — Joignabilite x logique d'achat** (~2h, porteur) : audience non joignable gratuitement des demain = mort.
- **P0 bis — Operabilite a temps partiel** : presence quotidienne requise = structurellement mort sous ~10h/semaine.
- **P1 — Recensement nominatif, vivants ET morts** (~45min/projet) : zero nom = recherche incomplete ; que des
  morts = maillon sans argent ; vivants et rentables = seule configuration exploitable.
- **P2 — Rentabilite inverse** (~30min/projet) : N clients au point mort (remuneration incluse) / audience
  joignable. Au-dela de 1-2% de penetration implicite, mort.
- **P3 — L'argent d'un inconnu** (survivant unique, lance jour 1) : `references/entretien.md`, protocole anti-politesse.

**Module optionnel — recon marche.** Pour un axe concurrentiel/acquereurs plus large qu'un simple recensement
P1, charge `references/module-market-recon.md` (fan-out de sous-agents sources, pare-feu strict).

## Phase 4 — Viabilite operationnelle

Uniquement pour les projets ayant franchi P0 a P3. Charge `references/operationnel.md` : budget d'heures,
plafond de revenu, cycle vs runway, canal repetable (3 clients hors reseau), saisonnalite, solvabilite, cout de l'arret.

## Phase 5 — Verdict (et scoring optionnel)

Un verdict par projet :
```
PROJET · <nom>
Verdict     : POURSUIVRE | VERIFIER | REORIENTER | ABANDONNER
Mort a      : <porte echouee, ou "aucune">
Preuve      : <fait OBSERVE, avec source>
Objection   : <argument le plus fort CONTRE, non attenue>
Hypotheses  : <encore SUPPOSEES, cout de verification>
Condition de mort : <falsifiable, datee, < 2 semaines, < 500 EUR>
Peremption  : <date de reaudit>
```
Departage entre survivants seulement : `references/comparaison.md`. Pour un departage chiffre plus formel
(matrice ponderee ancree, test de mort le moins cher) ou une **contre-expertise adverse** avant de conclure,
charge `references/module-scoring.md` et `references/module-red-team.md`. Compare enfin au classement date de 0.b.

## Phase 6 — Cloture

`status: complete` dans le memlog, puis `verdict.md`. Pour chaque projet abandonne : date d'archivage et ce qui
devrait devenir vrai pour le rouvrir. Sans cet ecrit, le tri est a refaire dans six semaines.
