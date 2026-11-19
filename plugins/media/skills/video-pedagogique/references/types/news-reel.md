# Type : news ou reel explicatif (validé)

Objectif : qu'un dirigeant non technique, sur son téléphone, sans le son, comprenne la news en 45 à 60 s et regarde jusqu'au bout. Né d'une vidéo refusée (« ennuyeuse, pas dynamique, que des encadrés ») puis refaite et validée le 23/10/2026.

## Ce qui a rendu la première version ennuyeuse

- Des cartes encadrées remplies de texte, qui apparaissent puis restent.
- Un plan sans changement pendant plus de 2,5 s, ou une moitié d'écran vide.
- Une voix plate (stabilité haute), lue à vitesse 1,0.
- Un récit en liste (« contexte, puis 3 actions ») sans tension ni retournement.

La version validée : typographie cinétique plein écran (serif italique géante pour l'idée, mono ambre pour les chiffres, sans grasse pour le reste), un changement toutes les 1,5 à 2,5 s, récit en retournement.

## Script (≈ 145 mots, 50 à 55 s)

| Temps | Durée | Rôle | Contrainte |
|---|---|---|---|
| Accroche | 0–3 s | Le paradoxe ou la perte | 8 à 12 mots, écrit en entier à l'écran dès l'image 1 |
| Qui / quoi | 3–13 s | Les acteurs, la source dite | « Selon <source>, … » ; un nom propre par phrase |
| Échelle | 13–19 s | Un chiffre qui parle | Nombre en toutes lettres pour la voix ; compteur à l'écran |
| Retournement | 19–28 s | « La plupart… Mais… » | La conséquence concrète, avec une durée ou un montant |
| Leçon | 28–34 s | Une phrase à retenir | « Retenez ça. » + la phrase ; écran noir, musique coupée |
| Réflexe | 34–49 s | Qui fait quoi, cette semaine | Une action principale, deux précisions au plus |
| Question | 49–52 s | Renvoyer au spectateur | Concrète, sans morale |
| Offre (muette) | +5–6 s | Ce que l'entreprise propose | Voir [carton-offre.md](../carton-offre.md) |

Faits : chaque affirmation vient d'une source primaire vérifiée **avant** la voix ; garder les nuances (« selon Microsoft », « aligné sur » et non « lié à »).

### Exemple validé (Storm-0940 / ConnectWise, 150 mots, 52 s)

```
[low, steady voice, restrained urgency] Pas besoin de votre mot de passe. Ils avaient DÉJÀ la clé.
Selon Microsoft, des pirates alignés sur l'État chinois prennent la main sur des applis de ConnectWise. Un outil de sauvegarde… déjà autorisé chez ses clients.
[dramatically] Et là, ils lâchent des agents IA. Presque sans humain. Plus de deux mille deux cent cinquante clients visés.
La plupart ont tenu. Mais chez certains… en moins de TROIS heures, les agents étaient administrateurs. Sans taper un seul mot de passe.
Retenez ça. Les pirates ne visent plus seulement vos mots de passe. Ils visent les applis à qui vous avez déjà dit OUI.
[warmly] Votre réflexe : demandez à votre prestataire la liste des applis branchées sur votre Microsoft 365. Ce qui ne sert plus, on débranche. Le reste garde juste les droits nécessaires. Client ConnectWise ? Connexions coupées, jusqu'aux consignes de l'éditeur.
Alors… qui a les clés de votre messagerie ?
```

La version refusée disait la même chose en liste : même information, aucune tension.

## Voix

Une seule génération pour toute la narration (intonation continue), `eleven_v4`, stabilité 0,35, similarité 0,75, vitesse 1,08, 3 ou 4 balises aux bascules, 2 à 4 mots en CAPITALES, 2 ou 3 « … ». Réglages détaillés : [script-et-voix.md](../script-et-voix.md).

## Images

- Mise en page 4:5 : bandeau 0–110, scène 130–910, sous-titres ≈ 930–1060, rien d'important sous 1060 (interface des réseaux).
- Sous-titres mot à mot : le mot dit passe à l'accent, mots-clés colorés en permanence, 3 à 6 mots par ligne, 2 lignes au plus, affichés ≈ 130 ms avant la voix, contour + ombre portée par `text-shadow`, sans encadré.
- Éléments à venir en transparence (20 à 25 %) pour éviter les écrans vides, qui s'allument sur leur mot.
- Effets d'impact (bosse, secousse, flash, entrée « whip ») réservés aux mots forts : 4 à 8 par vidéo ([effects.tsx](../../assets/effects.tsx)).
- La leçon sur écran noir, musique coupée : la rupture la plus forte de la vidéo.

## Auto-contrôle noté (x/7)

1. Le fait est lisible à l'écran dans les 3 premières secondes.
2. Chaque phrase a son visuel, qui apparaît au moment où elle est dite.
3. Sous-titres synchronisés : 3 mots pris au hasard, écart ≤ 200 ms.
4. Aucun plan sans information nouvelle pendant plus de 2,5 s.
5. Durée de la partie parlée entre 45 et 60 s.
6. Compréhensible sans le son : sur 3 images clés, le message passe.
7. Aucun mot de la liste des interdits ([script-et-voix.md](../script-et-voix.md)), ni dans la narration ni à l'écran.
