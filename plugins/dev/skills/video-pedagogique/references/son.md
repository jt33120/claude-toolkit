# Son : voix, bruitages, musique

Trois couches, dans cet ordre d'importance : la voix, les bruitages, la musique. Tout est synthétisé ou généré pour la vidéo : aucun échantillon ni morceau externe, donc aucune licence à suivre.

## Musique de fond

Pourquoi discrète : une musique trop présente fait baisser ce qu'on retient d'une explication, parce qu'elle prend une part de l'attention (principe de cohérence de Mayer ; Moreno & Mayer, 2000). Une nappe calme, sans paroles ni mélodie qui accroche, maintient l'ambiance et remplit les silences sans entrer en concurrence avec la voix.

`scripts/music_bed.py` (numpy + ffmpeg) :

```bash
# 1. nappe de la durée de la vidéo, au niveau de loudness du programme moins 16 dB
python3 scripts/music_bed.py make --dur 397.5 --mood calme --lufs -32 out/bed.wav
# 2. mixage : la musique baisse quand la voix parle, l'image est copiée sans ré-encodage
python3 scripts/music_bed.py mix out/final.mp4 out/bed.wav out/final_musique.mp4 [--mute 28.0-34.5] [--abr 48k --ac 1]
```

| Ambiance | Pour | Niveau `--lufs` (programme −16 / −14) |
|---|---|---|
| `calme` | cours, explication longue | −32 / −30 : ≈ 21 dB sous la voix quand elle parle, ≈ 16 dB dans les pauses |
| `clair` | news, démo produit | −32 / −30 |
| `tension` | accroche, incident | −32 / −30 |
| plus présente (pub) | réseaux, sans paroles longues | programme − 12 |

- Le mixage se fait sur la vidéo finale déjà assemblée (voix et bruitages déjà mélangés) : pas de nouveau rendu d'image. Le faire aussi sur la version de livraison (`--abr 48k --ac 1` pour une version allégée).
- Couper la musique (`--mute début-fin`, en secondes) sur la phrase la plus importante d'une vidéo courte : le silence soudain marque.
- Même graine (`--seed`) = même musique : la série garde son identité sonore.
- Écoute humaine requise : envoyer un extrait de 60 à 100 s à l'utilisateur avant d'appliquer le niveau à toute une série.

## Bruitages

`scripts/sfx.py` : impacts, whoosh, riser, ticks, click, pop, synthétisés et placés sur des mots de la timeline (volume 0,25 à 0,5, sous la voix). 4 à 8 impacts par vidéo courte ; dans un cours, un bruitage discret à chaque apparition importante.

## Niveaux de sortie

| Destination | Loudness intégrée | Crête |
|---|---|---|
| Réseaux, e-mail | −14 LUFS | ≤ −1 dBTP |
| Cours (page, LMS) | −16 LUFS | ≤ −1,5 dBTP |

Mesure : `ffmpeg -i final.mp4 -af ebur128=peak=true -f null -`.
