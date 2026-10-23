# Script et voix

## Gabarit (≈ 145 mots, 50 à 55 s)

| Temps | Durée | Rôle | Contrainte |
|---|---|---|---|
| Accroche | 0–3 s | Le paradoxe ou la perte | 8 à 12 mots, écrit en entier à l'écran dès l'image 1 |
| Qui / quoi | 3–13 s | Les acteurs, la source dite | « Selon <source>, … » ; un nom propre par phrase |
| Échelle | 13–19 s | Un chiffre qui parle | Nombre en toutes lettres pour la voix ; compteur à l'écran |
| Retournement | 19–28 s | « La plupart… Mais… » | La conséquence concrète, avec une durée ou un montant |
| Leçon | 28–34 s | Une phrase à retenir | « Retenez ça. » + la phrase ; écran noir, musique coupée |
| Réflexe | 34–49 s | Qui fait quoi, cette semaine | Une action principale, deux précisions au plus |
| Question | 49–52 s | Renvoyer au spectateur | Concrète, sans morale |
| Offre (muette) | +5–6 s | Ce que l'entreprise propose | Voir carton-offre.md |

## Écrire pour l'oreille

- Une idée par phrase ; alterner phrases très courtes (« Ils avaient déjà la clé. ») et phrases plus longues.
- Sujet, verbe, complément ; des verbes plutôt que des noms.
- Les mots du métier tels qu'on les dit en France, expliqués la première fois en quelques mots.
- Pas de parenthèses, pas de sigle non expliqué, nombres en toutes lettres (« deux mille deux cent cinquante »).
- Les deux-points et les virgules en série créent des pauses : les garder seulement là où une pause sert.
- Interdits : « Dans un monde où », « À l'ère de », question rhétorique en ouverture, crucial, essentiel, incontournable, majeur, sans précédent, révolutionnaire, « Ce n'est pas X, c'est Y », « n'est plus une option », conclusions moralisatrices, point d'exclamation.
- Test : chaque phrase pourrait-elle être dite à voix haute à un collègue ? Sinon, réécrire.

## Exemple validé (23/10/2026, Storm-0940 / ConnectWise, 150 mots, 52 s)

```
[low, steady voice, restrained urgency] Pas besoin de votre mot de passe. Ils avaient DÉJÀ la clé.
Selon Microsoft, des pirates alignés sur l'État chinois prennent la main sur des applis de ConnectWise. Un outil de sauvegarde… déjà autorisé chez ses clients.
[dramatically] Et là, ils lâchent des agents IA. Presque sans humain. Plus de deux mille deux cent cinquante clients visés.
La plupart ont tenu. Mais chez certains… en moins de TROIS heures, les agents étaient administrateurs. Sans taper un seul mot de passe.
Retenez ça. Les pirates ne visent plus seulement vos mots de passe. Ils visent les applis à qui vous avez déjà dit OUI.
[warmly] Votre réflexe : demandez à votre prestataire la liste des applis branchées sur votre Microsoft 365. Ce qui ne sert plus, on débranche. Le reste garde juste les droits nécessaires. Client ConnectWise ? Connexions coupées, jusqu'aux consignes de l'éditeur.
Alors… qui a les clés de votre messagerie ?
```

La version refusée le même jour disait la même chose en liste (« Selon Microsoft… Ce service sauvegarde… Alors, que faire ? Demandez… ») : même information, aucune tension.

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
- Une seule génération pour tout le texte, avec horodatage par caractère, puis découpe par scène.
- Après génération : lister les silences > 0,5 s entre deux mots (pauses involontaires) et la durée totale ; si la durée dépasse 60 s, couper le texte.
- Si un outil de transcription est disponible, retranscrire l'audio et comparer au script pour repérer les mots mal prononcés.

## Timeline des mots

`words.json` : `{ "model", "voice", "duration", "words": [ { "word", "start", "end", "scene" } ] }`.
Les balises (y compris avec virgules) sont masquées caractère par caractère avant de découper les mots, pour qu'elles ne deviennent jamais des mots. Les capitales d'emphase sont corrigées à l'affichage par une table `captionFix` (`{"DÉJÀ": "déjà"}`).
