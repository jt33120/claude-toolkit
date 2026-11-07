# Type : veille narrée (validé)

Objectif : qu'un public technique (développeurs, RSSI, DSI) comprenne en 3 minutes **comment** plusieurs attaques de la semaine ont fonctionné, ce qu'elles ont en commun et quoi faire, en regardant une histoire racontée par des personnages plutôt que des graphiques. Validé le 07/11/2026 après 13 versions (veille cyber d'un cabinet de conseil : Binance, Arkéa, vol de clés d'IA).

## Ce qui a été refusé en chemin (ne pas refaire)

| Refusé | Pourquoi | Retenu |
|---|---|---|
| Graphes, cartes encadrées, « slides animés » | ennuyeux, rien ne se passe | des **scènes narrées** : des personnages font l'action dite par la voix |
| Personnages ronds, avec visage | « enfantin » | silhouettes **corporate sans visage** (costume, cravate, badge) |
| Attaquants en ninja | cliché | attaquants en **chapeau noir** (black hat), défenseurs en **chapeau blanc** ; un attaquant déguisé paraît normal et son chapeau noir **tombe** quand le piège est révélé |
| « Bonjour, ici <marque> » en ouverture, logo deux fois | inutile | accroche directe sur l'enjeu, le logo une seule fois à la fin |
| Ouverture lente, titre qui traîne 3 s | ennuyeux | **dossier** : 3 chiffres-chocs en 10 s, une question, la promesse de la révélation à la fin |
| Serif italique + mono ambre, 5 couleurs | « trop Claude », « hyper coloré » | **une police** (Inter variable, esprit Apple), blanc + **un seul accent** ; rouge seulement pour un tampon d'alerte |
| Voix générée phrase par phrase puis recollée | respiration bizarre, mots répétés aux coupes, la voix ne retombe pas | **une seule prise** de tout le texte, pauses écrites dans le texte (voir [script-et-voix.md](../script-et-voix.md)) |
| Bruitages synthétisés, nappe grave | inaudibles sur téléphone : « il manque musique et bruitages » | bruitages et musique **générés** (ElevenLabs), musique nivelée, ≈ 13 dB sous la voix ([son.md](../son.md)) |
| Compteur ou chiffre sans source (« requêtes / s ») | invention | tout chiffre à l'écran vient d'une source citée |
| Panneau « à retenir » de 20 lignes avec étiquettes | illisible en 720p | 1 ligne courte par affaire, puis le principe, les réflexes, la conclusion ; il reste jusqu'au carton final |
| Phrase de fin « Construisons ensemble… » | creuse | finir sur la conviction, puis carton muet ultra sobre |

## Structure (≈ 3 min, 16:9 1920×1080)

| Bloc | Durée | Contenu |
|---|---|---|
| Accroche « dossier » | 12–14 s | « Trois attaques, un seul problème. » ; un chiffre par affaire (photo/clip réel derrière) ; les 3 cartes se rangent ; « On pourrait croire à trois failles différentes. Pourtant… même biais… on vous l'explique en fin de vidéo. » |
| Par affaire (× 3) | 35–60 s | **ce qui s'est passé** (chiffre, faille en une phrase, source dite) → **comment** (mots techniques assumés : token, repo, container, EIP-7702) → **la vraie question** (le point de bascule) |
| Révélation | 15 s | « Quel point commun ? » → « La confiance. » ; « Aucune porte n'a été forcée » ; les intermédiaires de confiance en personnages ; « pas dans la technologie : dans les liens humains » |
| Réflexes | 15 s | 3 réflexes concrets, chacun relié aux affaires qu'il aurait évitées |
| Conviction | 20–25 s | demain : la confiance accordée aux IA, attaques à la vitesse des machines ; « notre conviction » en 3 ou 4 piliers |
| Carton final (muet) | 6–7 s | logo au centre, URL dessous, 3 offres en tout petit avec icônes ; rien d'autre |

## Images

- Panneau « À retenir » à gauche (≈ 470 px), visible dès la 1re affaire et jusqu'au carton ; une ligne s'allume quand la voix la dit.
- Scènes pleine largeur restantes ; quand une scène dessinée pour 1776 px doit tenir à côté du panneau, la mettre à l'échelle **exacte** (1322/1776), sans la décaler sous le panneau.
- Chaque scène s'ouvre avec son visuel déjà à l'écran (titre, logo) : jamais 1–2 s de fond vide.
- Vrais logos, vraie photo du siège, clips de stock libres (Mixkit, Pexels) ; ce qui est reconstitué porte « ILLUSTRATION ».
- Sous-titres mot à mot : blanc, seul le mot prononcé passe à l'accent (pas de mots-clés colorés en permanence) ; une ligne ne finit jamais sur un mot-outil (le, de, ne, qu'une…).
- Transitions « traversée » (la scène sortante avance et floute, l'entrante émerge) entre scènes ; caméra qui bouge lentement dans les scènes.

## Contrôle avant envoi

- Planche toutes les 2 s sur la vidéo entière, lue en entier : chevauchements (deux textes visibles en même temps pendant un fondu), éléments coupés aux bords ou sous le panneau, écrans vides, couleurs hors charte.
- Transcription de la voix comparée au script (aucun mot répété, sauté ou mal prononcé).
- Niveaux : voix ≈ −16 LUFS, musique seule ≈ −29 dB moyen (mesurée sur le carton final), bruitages audibles.
- Retouches : re-rendre seulement les plages d'images touchées puis recoller (parties ré-encodées avec `-video_track_timescale 90000`, sinon le collage s'arrête en silence au premier segment de base de temps différente).
