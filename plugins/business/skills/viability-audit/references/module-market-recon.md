# Module optionnel — Recon marche et concurrence

Va au-dela du simple recensement nominatif de P1 quand l'enjeu le justifie (survivant unique de P3, ou
demande explicite d'un panorama concurrentiel plus large). Seule phase couteuse : **presenter les axes a
l'utilisateur et obtenir son accord avant de lancer le fan-out.**

Les sous-agents recoivent leur brief **seul** — jamais les fichiers du projet, jamais l'opinion du porteur sur
son marche. Pare-feu : le contexte oriente ce qu'on cherche, jamais ce qui est vrai.

## Axes (3 a 4, un sous-agent par axe)

- **A. Paysage concurrentiel** — qui vend deja une solution, y compris les substituts et le "ne rien faire" ;
  pour chacun : offre, financement, derniere levee datee, clients nommes. Chercher aussi ce qui a disparu.
- **B. Consolidation et acquereurs** — acquisitions sur 24 mois avec montants publics. Si tous les acquereurs
  plausibles ont deja acquis dans les 12 derniers mois, la fenetre se referme, pas s'ouvre — le dire.
- **C. Preuve de solvabilite** — pages tarifaires lues chez l'editeur (jamais un comparatif), offres d'emploi,
  documents financiers publics, tailles de contrats.
- **D. Douleur reelle des utilisateurs** — avis 1-3 etoiles, forums, issues GitHub. Une plainte qui persiste
  plusieurs annees est un resultat plus fort, pas perime : personne ne l'a resolue.
- **E. Absorption par la plateforme** (si archetype = outil dev ou infra) — ce que les plateformes dominantes
  livrent deja en natif sur 12 mois.

## Brief type par sous-agent

> Deux regles absolues : (1) aucune conclusion depuis ta memoire d'entrainement — sert uniquement a formuler
> des requetes ; (2) une affirmation est une phrase avec une source (editeur, date, URL), jamais de chiffre nu.
> Barres de fraicheur : taille de marche <= 18 mois, pricing <= 3 mois (page tarif de l'editeur), comportement
> <= 2 ans, levees/acquisitions <= 6 mois. Double source obligatoire pour toute taille de marche, prix, ou
> traction concurrente.
> Sujet : `{axe}`. Ecris dans `{doc_workspace}/digests/{axe}.md`.
> Retour (600 mots max) : 8-12 faits decisifs sources et dates, plus ce qui n'a pas pu etre verifie.

## Lecture par le parent

Trois concurrents finances ne tue pas le projet en soi, mais deplace la question de "le marche existe-t-il"
a "pourquoi toi" — si aucune reponse ne survit, KILL. Zero concurrent est un signal negatif par defaut : chercher
pourquoi avant de s'en rejouir. Absence de donnees publiques se rapporte comme absence, jamais comblee par une
inference presentee comme un fait.
