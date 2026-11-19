# Type : cours long (validé)

Vidéo de 6 à 8 min qui accompagne un module de cours (page Notion, LMS). Validée sur une série de modules DevOps (octobre 2026) : 16:9, 18 à 24 scènes, une relance toutes les 2 min environ.

## Ce que disent les données sur l'attention

- L'attention décroche par cycles, et les décrochages se rapprochent au fil d'un cours (Bunce et al., 2010).
- Dans les MOOC, l'engagement plafonne autour de 6 min de vidéo (Guo, Kim & Rubin, 2014) : viser 6 à 8 min, découper au-delà.
- Des mini-tests intercalés réduisent la rêverie et améliorent la mémorisation (Szpunar, Khan & Schacter, 2013).
- Prédire avant de voir aide, même quand la prédiction est fausse (Richland et al., 2009).
- Une question laissée ouverte retient l'attention jusqu'à la réponse (Loewenstein, 1994).

## Structure

- **Accroche (scène 0)** : une situation concrète et une question laissée ouverte (« trois heures du matin, le site ne répond plus »), refermée explicitement dans le dernier tiers. Pas de barre de progression sur l'accroche.
- **Étapes** : celles du module, une barre « étape n/N » sur chaque scène.
- **Relances** : une scène entière toutes les 1,5 à 3 min, jamais plus de 3 min sans relance, jamais deux du même type de suite.
- **Fin « À toi »** : la liste « c'est bon si », ce qu'il faut consigner, puis un carton « module suivant » et un fondu au noir.
- **Casser les séries** : après trois éléments de même forme, le quatrième change de forme (prédiction, raccourci, piège).

## Relances (10 à 25 s chacune)

Une relance fait agir le spectateur (prédire, se rappeler, choisir, taper) et change au moins deux canaux sur trois : la tâche mentale, le mode visuel (palette, cadrage), la voix ou le son.

| Type | Ce que fait le spectateur | Forme |
|---|---|---|
| Prédiction | Devine avant la réponse | Question plein écran, anneau de compte à rebours, silence, révélation |
| Rappel éclair | Ressort ce qu'il a vu 2 à 3 min plus tôt | Carte question, silence, réponse |
| Mini-incident | Se projette dans une situation | Palette plus chaude, notification, horloge, enjeu |
| Piège | Repère l'erreur | Le mauvais geste montré, puis barré |
| Analogie | Relie à du connu | Autre style d'illustration |
| Mise en action | Fait le geste | Carton « Pause : ouvre ton terminal » + commande |
| Teaser | Garde une question en tête | Phrase courte avec un indice visuel qui reviendra |

Silence d'une relance : dans la narration, séparer la question de la réponse par ` ‖ `. La question et la réponse sont générées à part, puis collées avec 2,7 s de silence. Pendant le silence : la question en grand et un anneau de compte à rebours, calés sur la fin du dernier mot de la question et le début du premier mot de la réponse.

## Narration

- Fichier `narration.txt`, une ligne par scène : `index|type|texte` (types : `hook`, `step`, `relance-prediction`, `relance-incident`, `relance-rappel`, `relance-piege`, `relance-analogie`, `relance-action`, `action`).
- 40 à 65 mots par scène, tutoiement, un fil rouge (un même projet exemple tout le long).
- Tout ce qui est prononcé s'écrit en toutes lettres : nombres, commandes lues (« tiret tiret now »), aucun symbole. Les commandes exactes vont dans les visuels.
- Avant la voix, vérifier automatiquement : écart entre deux relances ≤ 180 s, pas deux relances du même type consécutives.

## Voix (par scène)

Quand l'outil ElevenLabs ne renvoie pas d'horodatage (connecteur MCP restreint), générer une piste par scène, puis aligner les mots avec Whisper :

- Whisper `small`, `--word_timestamps True`, `--initial_prompt` = le texte de la scène ; si moins de 80 % des mots s'apparient, refaire sans prompt (`--no_speech_threshold 1.0 --compression_ratio_threshold 10 --logprob_threshold -5`) et garder le meilleur ; interpoler les mots non trouvés.
- Accélérer de 10 % (`atempo=1.1`) et normaliser chaque piste (`loudnorm=I=-16`) avant l'alignement.
- Budget : ≈ 1 crédit par caractère, soit 6 000 à 7 000 crédits par cours de 7 min. Vérifier le solde avant de lancer plusieurs cours ; deux générations de cours en parallèle au plus.
- Les liens de téléchargement des générations expirent (≈ 2 h) : télécharger juste après la génération.

## Images

- Contenu entre y = 230 et y = 960 sur 1080 ; caméra qui bouge toujours (une clé toutes les 2 à 4 s, zoom 0,95 à 1,2) ; quelque chose apparaît au moins toutes les 3 s.
- Une seule légende courte visible à la fois (8 mots au plus), en haut, qui apparaît au mot dit. Pas de sous-titres.
- Terminaux : 10 lignes au plus, commandes exactes de la page du cours.
- Relance : bandeau de type (« PRÉDICTION », « INCIDENT ») et mode visuel distinct.

## Production en série

Pour une série de modules, un brief unique remis à des sous-agents d'écriture (narration + scènes + voix), le rendu et la publication restant à l'agent principal. Le brief contient : ce qu'il faut lire, les fichiers à écrire, les règles de narration et de code, les effets interdits au rendu, les vérifications à lancer, le tableau des modules (page source, titre, module suivant).

## Livraison

- Une vidéo pleine qualité (CRF 19, −16 LUFS) et une version ≤ 19 Mo pour la page du cours (960×540, débit calculé depuis la durée).
- Dans la page : la vidéo en tête, puis une ligne grise « Vidéo du module · durée · une relance toutes les 2 minutes environ ».
