# Carton d'offre muet (fin de vidéo)

Demande de Julian (xSOM, 23/10/2026) : transformer la news en accroche commerciale, sans le dire à l'oral. Le carton est affiché 5 à 6 s après la question finale, voix terminée, musique qui continue puis s'éteint.

## Contenu

- Badge en haut : « OFFRE <MARQUE> » (il doit être clair que c'est une offre).
- Titre serif : « Ce que <marque> peut faire pour vous ».
- 2 ou 3 offres, numérotées : **nom de l'offre tel qu'il figure sur le site** + une ligne qui la relie au problème de la news (« sauvegarde et reprise, même si un prestataire tombe »).
- Adresse du site et appel court (« xsom.fr · Parlons-en »), logo.

## Règles

- Uniquement des offres publiées sur le site de l'entreprise, avec le nom exact du site (on peut préciser le pôle : « Audit réseaux & cybersécurité »). Ne jamais inventer une offre, un prix, un client ou un chiffre. La ligne sous le nom est rédigée pour la news : elle ne doit rien promettre que la page de l'offre ne dise pas.
- Pour xSOM, il n'existe pas de base « catalogue » dans Notion (vérifié le 23/10/2026 : la base Projects suit des projets, Opportunités des évolutions de produit). La spécification Notion « Système agentique de veille et de produit » § 1 renvoie à l'organisation GitHub `xsom-consulting`, où les sources sont :
  - `infra-xsom_website` (`index.html`, `expertises.html`) → www.xsom.fr : pôle **Réseaux & cybersécurité** (Architecture réseau · DORA · NIS2 · LPM · PCA / PRA · Audit), pôle **Infrastructures IA & cloud HPC**, pôle **Données & MLOps** ;
  - `ai-website` → ai.xsom.fr, fleet.xsom.fr, guard.xsom.fr : **xSOM Fleet** (programme pilote), **Secret Guard** (open source, Apache-2.0), conseil IA sur mesure ;
  - `.github/profile/README.md` : Fleet et Secret Guard comme produits publics.
  - Pas encore proposables : **Model Advisor** (dépôt vide au 23/10/2026), **AI Guard** (remplacé par Fleet), projets internes (personal-agent, xsom-agents, veille-collect).
- Relire ces pages avant chaque carton (elles changent) ; un produit absent du site n'est pas proposé.
- Le lien avec la news doit être direct : l'offre prévient ou résout le problème montré. Si aucune offre ne s'y rattache honnêtement, mettre une seule ligne générale (« Un système critique à faire évoluer ? Parlons-en. ») plutôt que de forcer.
- Un produit en développement est présenté comme tel (« programme pilote »).
- Jamais dit par la voix, jamais dans le corps de la narration.

## Exemples de correspondance (xSOM)

| News | Offres |
|---|---|
| Prestataire ou appli tierce compromise (ConnectWise) | Audit réseaux & cybersécurité · PCA / PRA · DORA · NIS2 · LPM (risque fournisseurs) |
| Faille critique d'un logiciel exposé (PHP, VPN) | Architecture réseau · Audit · PCA / PRA |
| Fuite de secrets par un assistant de code | xSOM Fleet (pilote) · Secret Guard (open source) |
| Réglementation IA ou cyber (AI Act, NIS2) | DORA · NIS2 · LPM · conseil IA sur mesure |
| Coût ou choix des outils IA | xSOM Fleet (FinOps, pilote) · conseil IA |

## Implémentation Remotion

Scène marquée `silentSeconds: 6` dans `edition.json` : la timeline la place après le dernier mot, sans narration ni sous-titres ; la synthèse vocale l'ignore. Composant de référence : `assets/OfferCard.tsx` (props `title`, `items[{name, line}]`, `cta`).
