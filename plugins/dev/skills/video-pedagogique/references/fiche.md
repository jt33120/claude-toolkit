# Fiche de paramètres

La partie variable d'une vidéo. Copier le gabarit dans le projet (`video.md` ou en tête du brief), le remplir à partir de la colonne du type, puis ne changer une valeur que sur demande de l'utilisateur ou après une leçon consignée.

## Gabarit

```markdown
# Fiche vidéo : <titre>
- Type : news-reel | cours | demo-produit | pub
- Public : <qui regarde, ce qu'il sait déjà>
- Objectif : <ce qu'il doit savoir faire ou penser après>
- Canal et format : <réseau / Notion / e-mail / site> · <ratio, taille> · 30 i/s
- Durée cible : <…> · mots : <…> · scènes : <…>
- Structure : <gabarit du type, adapté>
- Rythme : micro-changement toutes les <…> s · nouvelle scène toutes les <…> s · relance toutes les <…> min
- Références : <3 à 5 liens ou fichiers> · charte : <palette, polices, symboles> · texture : <aucune / CRT discret / CRT marqué>
- Tableau de séquences : <chemin du fichier> · maquette : <oui / non>
- Voix : <voix, modèle, vitesse, ton> · génération : <une seule / par scène> · crédits estimés : <…> (solde : <…>)
- Sous-titres : <oui mot à mot / non, mots-clés seulement>
- Son : bruitages <oui/non> · musique <ambiance calme/clair/tension, niveau, coupée où ?> · sortie <LUFS>
- Livraison : <fichiers, poids maximum, destination>
- Validation avant la voix : <oui / mode autonome>
```

## Valeurs par type

| Paramètre | news-reel | cours | demo-produit | pub |
|---|---|---|---|---|
| Fichier | [types/news-reel.md](types/news-reel.md) | [types/cours.md](types/cours.md) | [types/demo-produit.md](types/demo-produit.md) | [types/pub.md](types/pub.md) |
| Statut | validé | validé | non produit | non produit |
| Format | 4:5 1080×1350 (9:16 si réseau vertical) | 16:9 1920×1080 | 16:9, ou 1:1 pour les réseaux | 9:16 et 1:1 |
| Durée | 45–60 s (+5–6 s de carton muet) | 6–8 min ; au-delà, chapitres | 45–90 s | 15–30 s |
| Mots | 130–150 | 1 050–1 350 (≈ 175 mots/min) | 110–220 | 35–75 |
| Scènes | 7–9 | 18–24, de 40 à 65 mots | 6–10 | 4–7 |
| Micro-changement | 1,5–2,5 s | ≤ 3 s | 2–3 s | 1–1,5 s |
| Nouvelle scène | 6–10 s | 20–25 s | 6–10 s | 3–5 s |
| Relance de l'attention | — | toutes les 1,5 à 3 min | — | — |
| Structure | accroche choc → qui/quoi → échelle → « mais… » → leçon → réflexe → question | accroche à question ouverte → étapes avec barre de progression → relances → « À toi » | problème → produit → 3 fonctionnalités montrées en vrai → résultat → appel | accroche → promesse → preuve → appel |
| Visuels | capture de la source, typographie cinétique | schémas qui se construisent, terminaux, commandes exactes | captures et parcours réels de l'interface | références de style, produit, logo |
| Sous-titres | mot à mot (vu sans le son) | non : mots-clés au moment où ils sont dits | mots-clés | mot à mot |
| Voix | une génération, stabilité 0,35, vitesse 1,08, 3–4 balises | une génération par scène, question et réponse séparées par un silence de 2,7 s | une génération, ton posé | une génération, énergique |
| Musique | ambiance `clair` ou `tension`, coupée sur la leçon | ambiance `calme`, ≈ 21 dB sous la voix | `clair` | `clair` ou `tension`, plus présente (≈ 16 dB sous la voix) |
| Sortie son | −14 LUFS, crête ≤ −1 dBTP | −16 LUFS | −14 LUFS | −14 LUFS |
| Livraison | pleine qualité + version e-mail ≤ 15 Mo | pleine qualité + version ≤ 19 Mo (page Notion) | pleine qualité + version web | une version par ratio |
| Validation avant la voix | script | script + plan + carte des relances | script + parcours montré | 2 ou 3 pistes d'accroche |

Le seuil de 19 Mo vient de l'envoi de fichiers dans Notion par l'API, limité à 20 Mio.
