# Motion design : grammaire visuelle et catalogue de scènes

## Charte

- Fond sombre persistant (grille qui dérive lentement, halo de couleur) : il bouge toujours un peu, mais ce n'est pas un « changement ».
- Couleurs : cyan `#5ee6ff` pour les idées, ambre pour les chiffres, rouge pour le danger, vert pour ce qui tient ou est juste, blanc pour le reste.
- Trois polices, chacune son rôle : serif italique (Instrument Serif, OFL) pour les grandes idées, sans grasse (Manrope) pour le texte qui accompagne la voix, mono (JetBrains Mono) pour les chiffres et le code.
- Tailles en 1080 px de large : idée 90–180 px, chiffre 130–150 px, texte 40–60 px, mentions 20 px minimum (lisible sur téléphone).
- Un seul point focal par image ; hors sous-titres, 8 mots au maximum à l'écran.
- Pas de rotation, pas de rebond gadget ; entrées en 8–15 frames avec courbe douce ; impacts courts (3 frames d'attaque, 10 de retombée).

## Mise en page 4:5 (1080×1350)

| Zone | y (px) | Contenu |
|---|---|---|
| Bandeau | 0–110 | Marque, chapitre, barre de progression |
| Scène | 130–910 | Le visuel de l'idée |
| Sous-titres | ≈ 930–1060 | Bas des sous-titres à 290 px du bas (hors des 20 % inférieurs) |
| Marge basse | 1060–1350 | Rien d'important (interface des réseaux) |

## Effets (voir `assets/effects.tsx`)

| Effet | Usage | Fréquence |
|---|---|---|
| `punch(f, t)` bosse d'échelle | Le mot qui porte la phrase, un chiffre final | 4 à 8 par vidéo |
| `shake(f, t)` secousse amortie | Un choc (attaque réussie, tampon) | 2 ou 3 |
| `Flash` plein cadre | Révélation (la clé, l'accès admin) | 2 ou 3 ; dimensions explicites 1080×1350 sinon il dessine un rectangle |
| `whip(p)` glisse + flou | Entrée d'un mot ou d'un bloc | Libre |
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

Repères constants : le chapitre en haut à droite, une barre de progression, les mêmes symboles d'une scène et d'une vidéo à l'autre.

## Vrais visuels

- Capture de la source : ouvrir la page dans un navigateur sans compte (Chrome headless `--screenshot`, `--force-device-scale-factor=2`), recadrer le titre et une phrase-clé. Indiquer l'adresse et la date sous la capture.
- Logos : `simple-icons` quand ils existent, sinon le nom en typographie.
- Jamais d'image ou de vidéo générée par IA ; B-roll libre de droits seulement avec crédits (voir `video-remotion`).
