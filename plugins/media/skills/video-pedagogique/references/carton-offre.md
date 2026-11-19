# Carton d'offre muet (fin de vidéo)

Demande de l'utilisateur (23/10/2026) : transformer la news en accroche commerciale, sans le dire à l'oral. Le carton est affiché 5 à 6 s après la question finale, voix terminée, musique qui continue puis s'éteint.

## Contenu

- Badge en haut : « OFFRE <MARQUE> » (il doit être clair que c'est une offre).
- Titre serif : « Ce que <marque> peut faire pour vous ».
- 2 ou 3 offres, numérotées : **nom de l'offre tel qu'il figure sur le site** + une ligne qui la relie au problème de la news (« sauvegarde et reprise, même si un prestataire tombe »).
- Adresse du site et appel court (« xsom.fr · Parlons-en »), logo.

## Règles

- Uniquement des offres publiées sur le site de l'entreprise. Pour xSOM : www.xsom.fr (pôles Réseaux & cybersécurité : architecture réseau, DORA · NIS2 · LPM, PCA / PRA, audit ; Infrastructures IA & cloud HPC ; Données & MLOps) et ai.xsom.fr (xSOM Fleet, programme pilote 2026 ; Secret Guard, open source ; prestations de conseil IA sur mesure). Ne jamais inventer une offre, un prix, un client ou un chiffre.
- Le lien avec la news doit être direct : l'offre prévient ou résout le problème montré. Si aucune offre ne s'y rattache honnêtement, mettre une seule ligne générale (« Un système critique à faire évoluer ? Parlons-en. ») plutôt que de forcer.
- Un produit en développement est présenté comme tel (« programme pilote »).
- Jamais dit par la voix, jamais dans le corps de la narration.

## Exemples de correspondance (xSOM)

| News | Offres |
|---|---|
| Prestataire ou appli tierce compromise (ConnectWise) | Audit cybersécurité · PCA / PRA · NIS2 · DORA (risque fournisseurs) |
| Faille critique d'un logiciel exposé (PHP, VPN) | Architecture réseau · Audit · PCA / PRA |
| Fuite de secrets par un assistant de code | xSOM Fleet (pilote) · Secret Guard (open source) |
| Réglementation IA ou cyber (AI Act, NIS2) | NIS2 · DORA · conseil IA sur mesure |
| Coût ou choix des outils IA | xSOM Fleet (FinOps, pilote) · conseil IA |

## Implémentation Remotion

Scène marquée `silentSeconds: 6` dans `edition.json` : la timeline la place après le dernier mot, sans narration ni sous-titres ; la synthèse vocale l'ignore. Composant de référence : `assets/OfferCard.tsx` (props `badge`, `title`, `items[{name, line}]`, `cta`).
