# Checklist

Deux parties : **le socle**, à cocher pour toute vidéo, et **le type**, qui ajoute ses propres lignes. Les valeurs entre crochets viennent de la fiche de paramètres ([fiche.md](fiche.md)).

## Socle

### Avant la voix

- [ ] Fiche de paramètres remplie ; type choisi et son fichier lu.
- [ ] Charte écrite (palette, 3 polices et leur rôle, transitions, symboles récurrents).
- [ ] Chaque affirmation relue à sa source primaire ; nuances gardées (« selon », « aligné sur »).
- [ ] Script dans la fourchette de mots [mots] ; chaque phrase dicible à voix haute ; aucun mot de la liste des interdits.
- [ ] Tableau de séquences ([sequences.md](sequences.md)) : chaque ligne a un message en une phrase, une difficulté, une représentation justifiée et ce que fait le spectateur ; puis les mots déclencheurs.
- [ ] Aucune image choisie pour un mot plutôt que pour une idée ; aucun schéma montré avant d'en avoir besoin ; un mème au plus par minute, sur un moment d'émotion.
- [ ] Vidéo de plus de 2 min ou nouveau style : maquette animée avec voix provisoire regardée par l'utilisateur.
- [ ] Validation de l'utilisateur reçue (script + plan), ou mode autonome annoncé.
- [ ] Crédits estimés (≈ 1 par caractère) et solde vérifié.

### Après la voix

- [ ] Durée mesurée dans la cible [durée] ; si elle dépasse, couper le texte, jamais accélérer au-delà de 1,1.
- [ ] Aucun silence involontaire > 0,6 s ; balises absentes de la timeline des mots.
- [ ] Chaque mot horodaté (mots non trouvés interpolés et signalés).

### Avant le rendu complet

- [ ] Vérification automatique des mots déclencheurs : tous trouvés, dans la bonne scène ; plus long trou par scène ≤ [micro-changement].
- [ ] Aucun effet interdit au rendu (`video-remotion`, « Rendu fiable ») dans le code des scènes.
- [ ] Aperçu basse résolution + planche de contrôle regardée image par image :
  - aucun écran vide plus de 1,5 s, caméra jamais figée ;
  - aucun texte coupé ou qui sort du cadre, aucun chevauchement involontaire ;
  - un seul point focal ; tailles lisibles sur téléphone (≥ 20 px en 1080 de large) ;
  - chaque passage du tableau se reconnaît sur la planche (message visible sans le son) ; le repère persistant est à jour ;
  - « ILLUSTRATION » sur tout ce qui est inventé, source sous chaque capture.

### Livraison

- [ ] Images corrompues = 0 sur le fichier final (`video-remotion`, `scripts/deglitch.py check`).
- [ ] Durée du fichier final = somme des scènes (assemblage par ré-encodage, pas par copie).
- [ ] Son : [LUFS] intégrés (±0,5), crête ≤ −1 dBTP ; musique audible dans les pauses, jamais devant la voix ; bruitages sous la voix.
- [ ] Versions de livraison sous leur poids maximum [livraison].
- [ ] Une ligne à l'utilisateur : durée, ce qui est illustratif, crédits utilisés, ce qui n'a pas pu être vérifié (écoute humaine, relecture d'une scène).
- [ ] Leçons et corrections humaines consignées dans le guide du projet.

## Par type

### news-reel

- [ ] Accroche lisible à l'écran dans les 3 premières secondes ; compréhensible sans le son.
- [ ] Sous-titres : 3 mots pris au hasard, écart ≤ 200 ms ; rien dans la zone des sous-titres ni sous y = 1060.
- [ ] Les flashs couvrent tout le cadre (pas de rectangle).
- [ ] Musique coupée sur la leçon ; carton d'offre muet de 5 à 6 s si la vidéo sert une entreprise.
- [ ] Auto-contrôle x/7 de [types/news-reel.md](types/news-reel.md) ; version e-mail ≤ 15 Mo.

### cours

- [ ] Relances : écart maximal ≤ 180 s, pas deux du même type de suite, au moins une prédiction, un incident, un rappel et un piège, chacune avec son silence et son anneau.
- [ ] Question de l'accroche refermée explicitement dans le dernier tiers.
- [ ] Barre de progression sur chaque scène sauf l'accroche ; scène « À toi » avec carton du module suivant.
- [ ] Commandes affichées identiques à celles de la page du cours.
- [ ] Vidéo regardée une fois en entier à vitesse normale, en notant le moment où l'on décroche.
- [ ] Version ≤ 19 Mo en tête de la page du cours, avec sa ligne de durée.

### demo-produit

- [ ] Chaque fonctionnalité apparaît au mot qui la nomme ; zoom sur la zone utile de l'interface.
- [ ] Aucune donnée réelle de client à l'écran.

### pub

- [ ] Accroche validée parmi 2 ou 3 pistes ; une version par ratio, chacune contrôlée sur sa planche.
- [ ] Chaque chiffre affiché a une source.
