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
- Pas de SSML avec v3/v4 (`<break>` y est ignoré). Avec `eleven_multilingual_v2`, au contraire, `<break time="0.8s" />` est respecté à ±0,1 s et l'alignement le compte comme des caractères : c'est la façon de placer ses pauses dans une prise unique.
- Une seule génération pour tout le texte, avec horodatage par caractère, puis découpe par scène. Sans horodatage (connecteur restreint) : une génération par scène et alignement Whisper ([types/cours.md](types/cours.md)).
- Budget : ≈ 1 crédit par caractère ; estimer et vérifier le solde avant de lancer, ne jamais relancer une génération réussie.
- Après génération : lister les silences > 0,5 s entre deux mots (pauses involontaires) et la durée totale ; si la durée dépasse 60 s, couper le texte.
- Retranscrire l'audio (ElevenLabs `speech-to-text`, `scripts/voice_take.py check`) et comparer au script : aucun mot répété, sauté ou mal prononcé. Générer 2 prises (graines différentes) et faire choisir l'utilisateur à l'oreille.

## Ne jamais recoller des morceaux de voix

Leçon du 07/11/2026 (veille narrée, 3 min) : générer phrase par phrase ou paragraphe par paragraphe, même avec `previous_text`/`next_text`, puis recoller avec des silences donne une voix « hachée » : respiration bizarre aux coupes, début de mot répété quand la découpe tombe juste, et surtout l'intonation ne retombe pas en fin de morceau (le modèle « attend la suite »). Ce qu'il faut faire :

1. Tout le texte en **une seule génération** (jusqu'à 10 000 caractères en v2), pauses écrites dans le texte : `<break time="0.6s" />` entre deux scènes, 0,9 à 1 s entre deux affaires, 0,5 à 0,8 s avant une révélation.
2. Endpoint `with-timestamps` ; découper en mots par scène à partir de l'alignement caractère par caractère (`scripts/voice_take.py words`).
3. Ne rien couper ni insérer au montage dans la voix : les images se calent sur les mots, pas l'inverse.

Réglages validés (voix masculine posée, français) : `eleven_multilingual_v2`, stabilité 0,4, similarité 0,8, style 0,4, speaker boost, vitesse 1,0.

## Timeline des mots

`words.json` : `{ "model", "voice", "duration", "words": [ { "word", "start", "end", "scene" } ] }`.
Les balises (y compris avec virgules) sont masquées caractère par caractère avant de découper les mots, pour qu'elles ne deviennent jamais des mots. Les capitales d'emphase sont corrigées à l'affichage par une table `captionFix` (`{"DÉJÀ": "déjà"}`).
