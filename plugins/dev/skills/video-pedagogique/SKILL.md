---
name: video-pedagogique
description: "Vidéo en motion design avec voix off (Remotion + ElevenLabs) : news ou reel explicatif, cours long, démo produit, pub. Socle commun à toutes les vidéos (message d'abord : tableau de séquences et maquette validés avant la voix, tout calé au mot sur la voix, lisibilité avant effets, musique et bruitages sous la voix, planches et images corrompues contrôlées) + paramètres par type de vidéo et checklist. Use for any explainer, course or tutorial video, product demo, ad, reel or short with voice-over, or to improve a video's rhythm, music or visual quality. FR : « vidéo pédagogique », « vidéo explicative », « vidéo de cours », « motion design », « vidéo de la veille », « démo produit », « pub vidéo », « reel », « musique de fond », « rends la vidéo plus dynamique », « effet waouh »."
---

# Vidéo en motion design avec voix off

Une vidéo = **le socle** (ce fichier, identique pour toutes) + **une fiche de paramètres** (ce qui change selon le type). `video-remotion` couvre la mécanique (projet, rendu fiable, B-roll, licences) ; cette skill couvre le contenu, le rythme, le son et la qualité. Si le projet a son propre guide de style, il prime pour le ton, la voix et la charte ; cette skill prime pour la méthode.

Méthode tirée de vidéos réellement livrées : une news de 52 s refusée puis validée (« excellente »), un cours de 9 min puis une série de cours de 6 à 7 min (« c'est excellent »), puis un prototype de cours refusé (« c'est le bordel, foire du slip ») et refait message d'abord (« beaucoup mieux »). Les types non encore produits sont marqués comme tels dans leur fiche.

## Le socle : 9 règles pour toutes les vidéos

0. **Le message d'abord.** Pour chaque passage, se demander dans l'ordre : quel message je fais passer, est-il difficile, quelle est la meilleure façon de le montrer, que fait le spectateur, depuis quand rien de neuf n'est arrivé. Le visuel découle de ces réponses, jamais l'inverse ([sequences.md](references/sequences.md)).
1. **Montrer l'idée, dite au même moment.** Chaque élément apparaît quand la voix le prononce, et montre l'idée, pas le mot : « un port » n'est pas une photo de porte mais le programme relié à la porte réseau où il écoute.
2. **Tout se cale sur un mot**, jamais sur une seconde (`cue(scene, "mot")`, `tl.at("mot", n)`), et un mot introuvable fait échouer le rendu. On change la voix, tout reste synchronisé.
3. **Rythme mesuré** : un micro-changement et un changement de scène à des intervalles fixés par la fiche ; la caméra ne reste jamais figée.
4. **Lisibilité avant complexité** : un seul point focal par image, aucun texte coupé, aucun chevauchement involontaire, peu d'effets et seulement sur les mots forts. Un effet qui n'aide pas à comprendre est retiré.
5. **Une charte unique** : mêmes couleurs, polices, espacements, transitions et symboles d'une scène et d'une vidéo à l'autre ([motion-design.md](references/motion-design.md)).
6. **Vrais visuels, qui montrent la chose elle-même** : vraie page d'erreur, vraie sortie de commande, vrai terminal, logos réels ; schémas construits élément par élément au moment où le récit en a besoin, jamais montrés d'avance. Un mème ou un GIF : un par minute au plus, seulement sur un moment d'émotion (frustration, danger, chute), jamais pendant une première explication. Ce qui est inventé porte « ILLUSTRATION ». Jamais d'image ou de clip générés par IA.
6 bis. **Un repère qui reste** : ce qui a été construit (la chaîne, la carte) reste en petit à l'écran et évolue (étape en cours, ✓), pour relier les passages entre eux.
7. **Son en couches** : voix naturelle devant, bruitages synthétisés sur les mots forts, musique de fond discrète sous la voix ([son.md](references/son.md)).
8. **Rien n'est livré sans contrôle** : checklist du socle + celle du type ([checklist.md](references/checklist.md)).

## Déroulé

Chaque étape se termine sur son critère de fin.

1. **Fiche de paramètres.** Choisir le type et copier la fiche de [fiche.md](references/fiche.md) : public, objectif, format, durée, structure, rythme, voix, musique, livraison, budget de crédits. Lire le fichier du type, lié depuis la fiche. *Fin : fiche remplie, chaque valeur venant du type ou d'une demande de l'utilisateur.*
2. **Références et direction artistique.** 3 à 5 références (vidéos, captures, charte de la marque) ; en extraire les principes (couleurs, compositions, rythme, transitions) sans copier. Sans référence, la charte par défaut de [motion-design.md](references/motion-design.md). *Fin : charte écrite en 5 lignes (palette, 3 polices et leur rôle, transitions, symboles récurrents).*
3. **Script et tableau de séquences.** Script ([script-et-voix.md](references/script-et-voix.md)) et tableau de séquences ([sequences.md](references/sequences.md)) s'écrivent ensemble : une ligne par passage de 5 à 15 s (message, difficulté, meilleure représentation et pourquoi, ce que fait le spectateur, temps depuis la dernière nouveauté), puis les mots déclencheurs. Pour un format long, la carte des relances. **Faire valider le tableau par l'utilisateur avant la voix** dès que la voix coûte des crédits ou que la vidéo dépasse 2 min. *Fin : chaque ligne a un message en une phrase et une représentation justifiée ; validation reçue, ou mode autonome annoncé en tête.*
3 bis. **Maquette animée (vidéo de plus de 2 min ou nouveau style).** Voix provisoire gratuite (macOS : `say -v Thomas -o tmp.aiff "<texte>"`, puis alignement Whisper comme pour la vraie voix), animation simplifiée, rendu `--scale=0.5`. L'utilisateur la regarde à vitesse normale et note en minutage où il décroche ou ne comprend pas. *Fin : retours intégrés au tableau ; rien n'a encore coûté de crédits.*
4. **Voix et timeline des mots.** Estimer les crédits (≈ 1 par caractère) et vérifier le solde avant de lancer ; générer une seule fois ; produire la timeline mot par mot. *Fin : durée mesurée dans la cible de la fiche, chaque mot horodaté.*
5. **Scènes.** Écrire les compositions (mécanique et effets interdits au rendu : `video-remotion`, section « Rendu fiable »). *Fin : vérification automatique des mots déclencheurs propre (`scripts/check_cues.py` pour une timeline `words.json` ; sinon un script du projet qui lit chaque `tl.at("mot", n)` et le cherche dans le texte de sa scène) et trous ≤ au maximum de la fiche.*
6. **Aperçu et planches.** Rendu basse résolution, planche de contrôle (`scripts/contact_sheet.py`) regardée image par image, corrections scène par scène. *Fin : checklist « avant le rendu complet » entièrement cochée.*
7. **Rendu, son, assemblage.** Rendu complet par scène, remplacement des images corrompues, bruitages (`scripts/sfx.py`), musique (`scripts/music_bed.py`), texture CRT éventuelle après le rendu (`scripts/crt.py`), assemblage, versions de livraison. *Fin : checklist « livraison » cochée, mesures (durée, LUFS, crête, images corrompues = 0, poids) relevées sur le fichier final.*
8. **Retours et leçons.** Les retours se donnent en minutage (« 2:14, texte coupé ») ; ne corriger que la ou les scènes concernées, puis ré-assembler. Consigner chaque correction humaine dans le guide du projet pour la vidéo suivante.

## Carton d'offre (vidéo au service d'une entreprise)

Carton muet de 5 à 6 s en fin de vidéo, qui relie le sujet aux offres publiées par l'entreprise : [carton-offre.md](references/carton-offre.md).
