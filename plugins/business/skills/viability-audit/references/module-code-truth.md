# Module optionnel — Verite terrain (code)

Le pitch decrit l'intention. Le code decrit l'etat. A charger en Phase 1 quand le projet a un depot de code
et que le porteur ou l'audit veut une base plus dure que la simple decouverte documentaire.

Lance **un sous-agent par projet**. Le sous-agent lit, le parent ne lit pas le code en detail.

## Brief a donner au sous-agent

> Tu es un sous-agent d'extraction. Tu ne juges pas le projet, tu etablis des faits.
> **Regle absolue : le code est la source de verite.** Un README, un nom de fichier, un commentaire ou un
> ticket ne prouvent rien. Une fonctionnalite n'est REELLE que si tu as lu le code qui l'implemente.
>
> Depot : `{repo}`.
>
> 1. **Activite reelle** — date du dernier commit, commits sur 90j et 12 mois, contributeurs, plus longue
>    inactivite. Dernier commit > 6 mois = projet a l'arret, le dire.
> 2. **Ce qui tourne vraiment** — classe chaque fonctionnalite majeure : REEL (implemente et atteignable),
>    PARTIEL (chemin nominal existe, erreurs/auth/persistance manquent), FACTICE (mock, valeur en dur, TODO,
>    donnees de demo, fonction jamais appelee). Chemin de fichier a l'appui.
> 3. **Point d'entree et parcours utilisateur** — le chemin reel de bout en bout. S'il n'existe pas, c'est le
>    fait le plus important du rapport.
> 4. **Stack et dependances** — langages, frameworks, services externes, modeles IA, hebergement.
> 5. **Signaux de maturite** — tests, CI, secrets, auth, migrations, logs, gestion d'erreurs : present / absent / decoratif.
> 6. **Volume** — lignes de code ecrites, hors dependances et genere.
> 7. **Ce que le code ne peut pas dire** — utilisateurs, revenu, IP, engagements tiers. Ne rien inventer.
> 8. **Archetype produit** — d'apres le code seul : marketplace, B2B, grand public, outil dev, SaaS vertical, autre.
>
> Retour (500 mots max) : archetype ; 5 faits les plus decisifs ; ratio REEL/PARTIEL/FACTICE ; l'ecart le plus
> important entre ce que le projet annonce et ce qu'il fait ; ce que le code ne peut pas dire. Pas de conseil.

## Lecture par le parent

- L'archetype oriente la porte P1/P0 specifique (`portes.md`).
- Le ratio REEL/PARTIEL/FACTICE alimente P0 bis (vitesse jusqu'a la premiere preuve).
- **L'ecart annonce/realite est le signal le plus important de tout l'audit** — s'il etait inconnu du porteur,
  tout ce qu'il croit savoir sur son projet est a revitrifier ; le dire directement en tete de rapport.
- La liste « ce que le code ne peut pas dire » devient le questionnaire groupe de la Phase 2.

Depot inaccessible : ne pas contourner, ne pas deviner depuis le README seul. Marquer l'audit
`[non verifie — code non lu]` en tete de rapport plutot que de continuer sans le dire.
