# Script et voix

Commun à tous les types. Le gabarit de script propre à chaque type est dans `types/`.

## Écrire pour l'oreille

- Une idée par phrase ; alterner phrases très courtes (« Ils avaient déjà la clé. ») et phrases plus longues.
- Sujet, verbe, complément ; des verbes plutôt que des noms.
- Les mots du métier tels qu'on les dit en France, expliqués la première fois en quelques mots.
- Pas de parenthèses, pas de sigle non expliqué, nombres en toutes lettres (« deux mille deux cent cinquante »).
- Les deux-points et les virgules en série créent des pauses : les garder seulement là où une pause sert.
- Interdits : « Dans un monde où », « À l'ère de », question rhétorique en ouverture, crucial, essentiel, incontournable, majeur, sans précédent, révolutionnaire, « Ce n'est pas X, c'est Y », « n'est plus une option », conclusions moralisatrices, point d'exclamation.
- Test : chaque phrase pourrait-elle être dite à voix haute à un collègue ? Sinon, réécrire.

## Voix ElevenLabs

| Réglage | Valeur | Effet |
|---|---|---|
| Modèle | `eleven_v4` (repli `eleven_v3`, `eleven_multilingual_v2`) | v4 suit les balises et renvoie l'alignement ; v2 lirait les balises à voix haute : les retirer pour v2 |
| `stability` | 0,35 | Plus bas = plus de relief et de réponse aux balises |
| `similarity_boost` | 0,75 | Fidélité au timbre |
| `speed` | 1,08 (plage 1,0–1,1) | Rythme vif sans voix pressée |
| `language_code` | `fr` | Toujours explicite |

- Balises : 3 ou 4 au total, au plus 2 compatibles ensemble. Utiles en v4 : `[low, steady voice, restrained urgency]`, `[dramatically]`, `[warmly]`, `[excitedly]`, `[impressed]`, `[curious]`. Elles s'appliquent jusqu'à la balise suivante. Pas de balises de bruit (rires, soupirs) dans une news.
- Capitales : un mot par phrase au plus, 2 à 4 sur le script, sur le mot qui porte la phrase (DÉJÀ, TROIS, OUI).
- Points de suspension « … » : 2 ou 3 sur le script, pour une pause qui crée l'attente.
- Pas de SSML (`<break>` est ignoré par v3/v4).
- Une seule génération pour tout le texte, avec horodatage par caractère, puis découpe par scène. Sans horodatage (connecteur restreint) : une génération par scène et alignement Whisper ([types/cours.md](types/cours.md)).
- Budget : ≈ 1 crédit par caractère ; estimer et vérifier le solde avant de lancer, ne jamais relancer une génération réussie.
- Après génération : lister les silences > 0,5 s entre deux mots (pauses involontaires) et la durée totale ; si la durée dépasse 60 s, couper le texte.
- Si un outil de transcription est disponible, retranscrire l'audio et comparer au script pour repérer les mots mal prononcés.

## Timeline des mots

`words.json` : `{ "model", "voice", "duration", "words": [ { "word", "start", "end", "scene" } ] }`.
Les balises (y compris avec virgules) sont masquées caractère par caractère avant de découper les mots, pour qu'elles ne deviennent jamais des mots. Les capitales d'emphase sont corrigées à l'affichage par une table `captionFix` (`{"DÉJÀ": "déjà"}`).
