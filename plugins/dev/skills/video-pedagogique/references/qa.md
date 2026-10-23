# Contrôle qualité

## Avant la voix

- [ ] Chaque affirmation du script relue à sa source primaire (chiffres, dates, qui a fait quoi, qualification : attaque observée, démonstration, étude, annonce).
- [ ] Nuances gardées (« selon », « aligné sur », « la plupart des cibles »).
- [ ] 130 à 150 mots, aucun tic interdit, chaque phrase dicible à voix haute.

## Après la voix

- [ ] Durée 45 à 60 s (avec le carton d'offre muet : 50 à 65 s au total).
- [ ] Aucun silence involontaire > 0,6 s ; les balises n'apparaissent pas dans `words.json`.

## Avant le rendu complet

- [ ] `scripts/check_cues.py` : tous les mots déclencheurs trouvés, dans la bonne scène ; plus long trou par scène ≤ 2,5 s.
- [ ] Aperçu à `--scale=0.5` puis planche `scripts/contact_sheet.py` regardée image par image :
  - aucun écran vide plus de 1,5 s ;
  - rien dans la zone des sous-titres (y ≈ 930–1060) ni sous 1060 ;
  - aucun texte coupé ou qui déborde ;
  - les flashs couvrent tout le cadre (pas de rectangle) ;
  - mots-clés lisibles sur un téléphone (≥ 20 px pour les mentions) ;
  - « ILLUSTRATION » sur tout ce qui est inventé, source sous chaque capture.

## Auto-contrôle noté (x/7)

1. Le fait est lisible à l'écran dans les 3 premières secondes.
2. Chaque phrase a son visuel, qui apparaît au moment où elle est dite.
3. Sous-titres synchronisés : 3 mots pris au hasard, écart ≤ 200 ms.
4. Aucun plan sans information nouvelle pendant plus de 2,5 s.
5. Durée de la partie parlée entre 45 et 60 s.
6. Compréhensible sans le son : sur 3 images clés, le message passe.
7. Aucun mot de la liste des interdits, ni dans la narration ni à l'écran.

## Son

- [ ] −14 LUFS intégrés (±0,5), crête ≤ −1 dBTP (`ffmpeg -af ebur128=peak=true`).
- [ ] Musique coupée sur la leçon ; bruitages audibles mais sous la voix.

## Livraison

- [ ] Version e-mail ≤ 15 Mo (H.264, CRF 26–28) en plus de la version pleine qualité.
- [ ] Une ligne dite à l'utilisateur sur ce qui n'a pas pu être vérifié (écoute humaine, transcription).
