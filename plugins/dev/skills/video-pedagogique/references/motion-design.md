# Motion design : grammaire visuelle et catalogue de scènes

## Charte par défaut

À utiliser quand le projet n'a pas sa propre charte ; une charte de marque la remplace entièrement.

- Fond sombre persistant (grille qui dérive lentement, halo de couleur) : il bouge toujours un peu, mais ce n'est pas un « changement ».
- Couleurs : fond `#04070e`, cyan `#5ee6ff` pour les idées, ambre `#ffb547` pour les chiffres, rouge `#ff5a6e` pour le danger, vert `#7cffb2` pour ce qui tient ou est juste, violet `#b79cff` en accent rare, blanc `#f2f5fa` pour le reste, gris `#8a93a6` pour le secondaire.
- Trois polices, chacune son rôle : serif italique (Instrument Serif, OFL) pour les grandes idées, sans grasse (Manrope) pour le texte qui accompagne la voix, mono (JetBrains Mono) pour les chiffres et le code.
- Tailles en 1080 px de large : idée 90–180 px, chiffre 130–150 px, texte 40–60 px, mentions 20 px minimum (lisible sur téléphone). En 1920×1080 (cours) : légende 44–60 px, texte de schéma ≥ 26 px, terminal ≥ 24 px.
- Halos et reliefs en `boxShadow` ou dégradés, jamais en `filter` (images corrompues au rendu, voir `video-remotion`).
- Un seul point focal par image ; hors sous-titres, 8 mots au maximum à l'écran.
- Pas de rotation, pas de rebond gadget ; entrées en 8–15 frames avec courbe douce ; impacts courts (3 frames d'attaque, 10 de retombée).

## Mises en page

### 4:5 (1080×1350), news et réseaux

| Zone | y (px) | Contenu |
|---|---|---|
| Bandeau | 0–110 | Marque, chapitre, barre de progression |
| Scène | 130–910 | Le visuel de l'idée |
| Sous-titres | ≈ 930–1060 | Bas des sous-titres à 290 px du bas (hors des 20 % inférieurs) |
| Marge basse | 1060–1350 | Rien d'important (interface des réseaux) |

### 16:9 (1920×1080), cours et démo

| Zone | y (px) | Contenu |
|---|---|---|
| Légende | 44–150 | Une légende courte, au mot dit |
| Monde | 230–960 | Schémas, terminaux, interface ; la caméra (zoom 0,95 à 1,2) le parcourt |
| Bas | 960–1080 | Barre de progression des étapes, bandeau de relance |

Position à l'écran d'un point du monde : 960 + (x − cx) × zoom (idem en y avec 540). Vérifier pour chaque clé de caméra que ce qui compte reste entièrement dans le cadre.

### 9:16 (1080×1920)

Comme le 4:5 en gardant libres les 250 px du haut et les 20 % du bas, ainsi que le bord droit (interface des réseaux).

## Effets (voir `assets/effects.tsx`)

| Effet | Usage | Fréquence |
|---|---|---|
| `punch(f, t)` bosse d'échelle | Le mot qui porte la phrase, un chiffre final | 4 à 8 par vidéo |
| `shake(f, t)` secousse amortie | Un choc (attaque réussie, tampon) | 2 ou 3 |
| `Flash` plein cadre | Révélation (la clé, l'accès admin) | 2 ou 3 ; dimensions explicites 1080×1350 sinon il dessine un rectangle |
| `whip(p)` glisse rapide | Entrée d'un mot ou d'un bloc (flou optionnel, vidéos courtes seulement) | Libre |
| `between(f, a, b)` | Faire vivre un élément entre deux mots | Libre |
| Fantômes à 20–25 % | Annoncer ce qui va s'allumer, éviter le vide | Une fois par scène à éléments multiples |

## Catalogue de scènes qui fonctionnent

| Scène | Ce qu'on voit | Déclencheurs typiques |
|---|---|---|
| Champ barré | Un champ « mot de passe » rempli de points, barré en rouge avec secousse | le mot « passe » |
| Objet qui entre en force | Grande icône (clé, cadenas) qui arrive en « whip » + phrase serif géante + flash | le mot-objet |
| Capture de la source | Vraie capture du titre de l'article, surlignée par un trait ambre qui court | le nom de la source |
| Tampon | Nom de l'acteur en mono rouge dans un cadre qui tombe (échelle 1,8 → 1) avec secousse | le nom de l'acteur |
| Nom géant + pictogramme | Nom de l'outil en 110 px, pictogramme qui monte, sous-ligne serif | nom, puis fonction |
| Grille de clients cochés | 12 bâtiments qui reçoivent un badge vert l'un après l'autre (2 frames d'écart) | « autorisé » |
| Essaim | 40 à 50 icônes de robots en spirale (angle d'or) qui se déploient depuis le centre | « agents » |
| Grille de points | Autant de points que le chiffre (50 × 45 = 2 250) qui s'allument en vague + compteur mono | « plus », jusqu'au mot final |
| Grille qui tient / qui cède | Les mêmes points deviennent verts, quelques-uns rouges et grossissent ; zoom avant | « plupart », « mais », le mot du danger |
| Chrono | Mono ambre 00:00 → 02:59 qui défile pendant « en moins de trois heures » | « moins » → « heures » |
| Rupture noire | Fond noir, musique coupée, une phrase serif de 170 px qui monte | « Retenez » |
| Boutons « Autoriser » | Applis génériques avec un bouton vert pressé tour à tour, puis « oui. » géant | « applis », « dit », « oui » |
| Liste qui se nettoie | Liste illustrative d'applis : une ligne se débranche (prise qui s'ouvre) et se replie ; les barres de droits rétrécissent | « débranche », « droits » |
| Interrupteur | Interrupteur vert → coupé, avec la consigne | « coupées », « consignes » |
| Question finale | Grande clé qui se balance + question serif | « qui », dernier mot |
| Schéma qui se construit (cours) | Boîtes reliées qui apparaissent une à une, un paquet qui circule sur les liens | le nom de chaque maillon |
| Terminal (cours) | Commande tapée lettre à lettre, puis sortie ligne à ligne | le verbe de l'action (« tape », « vérifie ») |
| Question à silence (cours) | Question en grand, anneau de compte à rebours pendant le silence, révélation | fin de la question → début de la réponse |
| Mini-incident (cours) | Palette plus chaude, notification, horloge qui tourne | l'heure, le symptôme |
| Barré (piège) | Le mauvais geste affiché puis barré en rouge, le bon geste dessous | le mot du piège |

Repères constants : le chapitre en haut à droite, une barre de progression, les mêmes symboles d'une scène et d'une vidéo à l'autre.

## Vrais visuels

- Capture de la source : ouvrir la page dans un navigateur sans compte (Chrome headless `--screenshot`, `--force-device-scale-factor=2`), recadrer le titre et une phrase-clé. Indiquer l'adresse et la date sous la capture.
- Logos : `simple-icons` quand ils existent, sinon le nom en typographie.
- Jamais d'image ou de vidéo générée par IA ; B-roll libre de droits seulement avec crédits (voir `video-remotion`).
