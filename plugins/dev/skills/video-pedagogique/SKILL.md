---
name: video-pedagogique
description: "Vidéo pédagogique courte en motion design (Remotion + voix ElevenLabs) qui explique une news, un concept ou un cours à un public non spécialiste, avec un vrai effet « waouh » : accroche choc en 1 s, typographie cinétique plein écran, un changement visuel toutes les 1,5 à 2,5 s calé au mot près sur la voix, impacts et bruitages synthétisés, vraie capture de la source, voix naturelle modulée, carton d'offre muet en fin. Méthode complète : script, voix, timeline des mots, scènes, son, contrôle qualité (planches, vérification des mots déclencheurs), rendu. Use for any explainer, news recap, course or teaching video, reel or short with voice-over. FR : « vidéo pédagogique », « vidéo explicative », « motion design », « vidéo de la veille », « vidéo de la news », « reel pédagogique », « rends la vidéo plus dynamique », « effet waouh »."
---

# Vidéo pédagogique en motion design

Objectif : qu'un dirigeant non technique, sur son téléphone, sans le son, comprenne la news en 45 à 60 s et ait envie de regarder jusqu'au bout. Cette skill complète `video-remotion` (mécanique Remotion, B-roll, licences) : elle fixe **le contenu, le rythme, le son et la qualité**. Elle est née d'une vidéo refusée (« ennuyeuse, pas dynamique, que des encadrés ») puis refaite et validée (« excellente ») le 23/10/2026 : tout ce qui suit vient de cet écart.

Si le projet a son propre guide de style (ex. `tasks/guide-style.md` de xsom-agents), il prime pour le ton, la voix et la charte ; cette skill prime pour la méthode.

## Ce qui rend une vidéo ennuyeuse (à ne jamais refaire)

- Des **cartes encadrées** (boîtes à bordure) remplies de texte, qui apparaissent puis restent.
- Un plan qui ne bouge pas pendant plus de 2,5 s, ou une moitié d'écran vide.
- Une voix plate (stabilité haute), lue sans relief, à vitesse 1.0.
- Un récit en liste (« contexte, puis 3 actions ») sans tension ni retournement.
- Des animations calées sur des secondes fixes, qui se décalent dès que la voix change.

## Les 8 règles

1. **Une idée par écran**, dite et montrée au même moment. Chaque nom propre, chiffre ou objet cité apparaît quand la voix le prononce.
2. **Tout se cale sur un mot**, jamais sur une seconde : `cue(scene, "connectwise")`. On change la voix, tout reste synchronisé.
3. **Rythme** : micro-changement (zoom, pastille, mot qui s'allume) toutes les 1,5 à 2,5 s ; grand changement (nouvelle scène) toutes les 6 à 10 s. Jamais plus de 2,5 s sans information nouvelle à l'écran.
4. **Typographie cinétique plein écran** plutôt que des encadrés : serif italique géante pour l'idée, mono ambre pour les chiffres, sans grasse pour le reste. Un seul point focal.
5. **Récit en retournement** : accroche choc → qui / quoi → échelle → « mais… » → leçon (écran noir, musique coupée) → un seul réflexe → question → carton d'offre muet.
6. **Vrais visuels** : capture réelle de la source (titre de l'article, communiqué), logos réels, schémas qui se construisent. Jamais d'image ou de clip générés par IA. Ce qui est inventé (applis génériques, exemple) porte « ILLUSTRATION ».
7. **Son** : voix naturelle et modulée (voir § 3), bruitages synthétisés discrets sur les mots forts, musique 20 à 24 dB sous la voix, coupée sur la phrase clé ; −14 LUFS en sortie.
8. **Rien n'est livré sans contrôle** : vérification automatique des mots déclencheurs, calcul des trous, planche de captures regardée pour de vrai (§ 6).

## 1. Script (texte d'abord, image ensuite)

Écrire le script complet avant toute animation. 130 à 150 mots pour 45 à 60 s (≈ 2,8 mots/s à vitesse 1.08). Détail, modèles et exemples : [script-et-voix.md](references/script-et-voix.md).

- **Accroche (0 à 2 s)** : le fait le plus surprenant, formulé comme une perte ou un paradoxe (« Pas besoin de votre mot de passe. Ils avaient déjà la clé. »). Écrite en entier à l'écran dès la première image.
- **Qui / quoi** en une ou deux phrases, avec la source dite (« Selon Microsoft… »).
- **Échelle** : un chiffre qui parle, montré (compteur, grille de points).
- **Retournement** : « Mais… » + la conséquence concrète.
- **Leçon** en une phrase mémorisable, sans morale (« Ils visent les applis à qui vous avez déjà dit oui. »).
- **Un seul réflexe**, qui fait quoi, faisable cette semaine.
- **Question finale** qui renvoie au spectateur.
- Phrases courtes parlées, une idée par phrase ; les mots du métier tels qu'on les dit (phishing, patch, sandbox) ; nombres écrits en toutes lettres pour la voix.
- Faits : chaque affirmation vient d'une source primaire vérifiée **avant** de générer la voix (sinon la voix est à refaire). Garder les nuances (« selon Microsoft », « aligné sur » et non « lié à »).

## 2. Découpage en scènes

Une scène par temps du récit (7 à 9 scènes). Pour chaque scène, écrire une ligne de plan : mots déclencheurs → ce qui apparaît. Catalogue de scènes qui fonctionnent et code des effets : [motion-design.md](references/motion-design.md).

## 3. Voix (ElevenLabs, une seule génération)

- Modèle `eleven_v4` (repli `eleven_v3` puis `eleven_multilingual_v2`), langue explicite, **une seule génération** pour toute la narration (intonation continue), endpoint `with-timestamps` (repli `forced-alignment`).
- Réglages vivants : `stability` 0,35, `similarity_boost` 0,75, `speed` 1,08. Si la voix sonne plate, baisser la stabilité vers 0,3 ; si elle part dans tous les sens, remonter vers 0,5.
- Relief : 3 ou 4 balises au total, aux bascules (`[low, steady voice, restrained urgency]` en ouverture, `[dramatically]` sur l'échelle, `[warmly]` sur le réflexe) ; 2 à 4 mots en CAPITALES sur tout le script (un par phrase au plus) ; points de suspension « … » une ou deux fois pour une vraie pause. La ponctuation avant les balises.
- Les balises et les capitales ne s'affichent jamais : retirer les balises de la timeline des mots, et corriger l'affichage des capitales (`captionFix`).
- Sortie : `voice.mp3` + `words.json` (mot, début, fin, scène). Mesurer la durée (`ffprobe`) ; au-delà de 60 s, couper le texte, pas la vitesse.
- Une génération coûte des crédits : générer une fois le script validé et vérifié.

## 4. Animations (Remotion)

- Format 4:5 (1080×1350) ou 9:16 selon le canal, 30 i/s. Zone utile : sous le bandeau (y ≥ 130) et au-dessus des sous-titres, qui restent hors des 20 % du bas.
- Chaque élément cherche son mot dans la timeline (`cue`) ; les scènes démarrent au premier mot de leur phrase ; transitions courtes (8 frames).
- Les éléments à venir peuvent être affichés en transparence (20 à 25 %) pour éviter les écrans vides, puis s'allumer sur leur mot.
- Effets d'impact (bosse d'échelle, secousse amortie, flash plein cadre, entrée « whip » avec flou) réservés aux mots forts : 4 à 8 par vidéo. Code prêt à copier : [effects.tsx](assets/effects.tsx).
- Sous-titres mot à mot : le mot dit passe à l'accent, mots-clés colorés en permanence (cyan idées, ambre chiffres, rouge danger), 3 à 6 mots par ligne, 2 lignes max, affichés ~130 ms avant la voix, contour + ombre, sans encadré.
- Un écran noir, musique coupée, pour la leçon : c'est la rupture la plus forte de la vidéo.

## 5. Son

- Bruitages **synthétisés** (aucun échantillon externe) et placés sur des mots : impact (choc, chiffre final), whoosh (entrée d'un élément), riser (montée vers l'échelle), ticks (compteur, cases cochées), pop (on débranche), click (interrupteur). Générateur : `scripts/sfx.py`.
- Musique de fond discrète (≈ 0,08 de gain, compresseur latéral sur la voix), coupée sur la scène de la leçon.
- Mixage final normalisé à −14 LUFS, crête ≤ −1 dBTP.

## 6. Contrôle qualité (obligatoire avant le rendu complet)

Checklist complète : [qa.md](references/qa.md).

1. `python3 scripts/check_cues.py <scenes.tsx> <edition.json> <words.json>` : chaque mot déclencheur existe dans la bonne scène et l'ordre est cohérent ; le script affiche aussi le plus long trou entre deux déclencheurs de chaque scène. Tout trou > 2,5 s est à combler (pastille, mot qui s'allume, zoom), sauf s'il est couvert par une cascade programmée (lignes qui entrent une à une après un mot) : la vérifier alors sur la planche.
2. Rendu d'aperçu rapide : `npx remotion render … --scale=0.5 --crf=28` (≈ 1 min 30), puis `python3 scripts/contact_sheet.py preview.mp4 out/sheet.png --every 1.6` : regarder la planche pour de vrai. Chercher : écran vide, chevauchement avec les sous-titres, texte coupé, flash qui dessine un rectangle, élément illisible sur téléphone.
3. Corriger, refaire l'aperçu, puis seulement le rendu complet (CRF 18), le mixage, et une version compressée (CRF 26 à 28) sous 15 Mo pour l'e-mail.
4. Auto-contrôle noté x/7 (fait lisible en 3 s ; chaque phrase a son visuel ; sous-titres à ±200 ms ; aucun plan figé > 2,5 s ; durée 45 à 60 s ; compréhensible sans le son ; aucun tic d'écriture interdit).

## 7. Carton d'offre (fin, muet)

Quand la vidéo sert une entreprise, un carton muet de 5 à 6 s après la question finale relie le problème aux offres qui le préviennent ou le résolvent : badge « OFFRE », titre « Ce que <marque> peut faire pour vous », 2 ou 3 offres (nom + une ligne liée à la news), adresse du site. Jamais dit par la voix, jamais d'offre inventée : uniquement ce qui est publié sur le site de l'entreprise. Règles et exemple : [carton-offre.md](references/carton-offre.md).

## 8. Livraison

- Fichiers : vidéo pleine qualité, version e-mail ≤ 15 Mo, `words.json`, la planche de contrôle.
- Dire en une ligne : durée, score d'auto-contrôle, ce qui est illustratif, crédits utilisés, ce qui n'a pas pu être vérifié à l'oreille.
- Consigner toute correction humaine dans le carnet ou le guide du projet pour la prochaine vidéo.
