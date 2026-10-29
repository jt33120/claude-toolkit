# Tableau de séquences : le message d'abord

Le tableau s'écrit avec le script, avant la voix et avant tout code. Il empêche la dérive constatée sur un prototype refusé : des images choisies parce qu'elles correspondent à un mot (« port » → photo de porte), quatre mèmes dans les 20 premières secondes, un schéma complet montré avant d'avoir servi. Résultat jugé « le bordel, clownesque ». La version refaite à partir de ce tableau : « beaucoup mieux ».

## Les cinq questions, pour chaque passage de 5 à 15 s

1. **Quel message** je fais passer ? Une phrase, du point de vue du spectateur.
2. **Est-il difficile** ? 1 (évident), 2 (demande un schéma), 3 (contre-intuitif : prévoir une démonstration ou une prédiction).
3. **Quelle est la meilleure façon de le montrer**, et pourquoi ? Par ordre de préférence :
   - la chose réelle (vraie page, vraie commande et sa sortie, vrai fichier de configuration) ;
   - un schéma qui se construit au moment où on en a besoin, à partir de ce qui est déjà à l'écran ;
   - une démonstration du cas qui marche puis du cas qui casse ;
   - une analogie seulement si le concept est abstrait, et alors une seule, tenue jusqu'au bout.
4. **Que fait le spectateur ?** Reconnaît, prédit, compare, repère une ligne, retient une procédure. « Regarde » ne suffit pas.
5. **Depuis quand rien de neuf ?** Au-delà du maximum de la fiche, ajouter une information, pas un effet.

## Gabarit

| Minutage | Message à faire passer | Diff. | Meilleure façon de le montrer | Ce que fait le spectateur |
|---|---|---|---|---|

## Les médias

- Un média réel entre seulement s'il montre la chose elle-même ou porte une émotion utile.
- Mème ou GIF : un par minute au plus, sur un moment d'émotion (frustration, danger, chute), jamais pendant une première explication.
- Sources sans clé, téléchargées depuis la machine de l'utilisateur quand le conteneur n'a pas accès au web : Mixkit (vidéos libres), Wikimedia Commons et Openverse (images libres et archives), GIPHY (GIF), imgflip (modèles de mèmes), xkcd. Pexels et Pixabay avec une clé gratuite (`video-remotion`). Usage personnel : tout est permis ; publication : licences à vérifier, mèmes recréés.
- Choix sur planche : télécharger des aperçus (GIF 200 px, vidéos 360p), faire une planche numérotée, choisir en regardant, puis télécharger la version finale. Noter chaque source dans `credits.json`.

## Exemple validé : début d'un cours réseau (84 s, voix existante)

| Minutage | Message à faire passer | Diff. | Meilleure façon de le montrer | Ce que fait le spectateur |
|---|---|---|---|---|
| 0:00–0:06 | Un client n'arrive pas sur DocuFact | 1 | Vraie fenêtre Chrome : l'adresse se tape, l'onglet tourne, puis la vraie page « Ce site est inaccessible » | Reconnaît une situation vécue |
| 0:06–0:09 | Pourtant, côté serveur, tout tourne | 1 | L'écran se partage : à droite le terminal du serveur, `systemctl status` actif, `curl /health` OK | Ressent le paradoxe |
| 0:09–0:15 | Le problème est entre les deux : 4 maillons, un seul suffit | 2 | Les deux fenêtres deviennent deux points ; la requête part et disparaît au milieu ; 4 cases « ? » apparaissent entre les deux ; l'une clignote en rouge | Se demande laquelle |
| 0:15–0:19 | Question ouverte : lequel regarder en premier ? | 1 | La question reste à l'écran, une loupe passe sur les cases | Garde la question en tête |
| 0:19–0:36 | Le trajet : DNS, pare-feu, reverse proxy, application + base | 2 | La requête avance case par case ; chaque case se remplit au mot : DNS traduit le nom en adresse, pare-feu laisse passer 443, cadenas HTTPS, application avec sa base | Suit le trajet, une étape à la fois |
| 0:36–0:39 | 5 étapes, en partant de ton code | 1 | La liste des 5 étapes s'affiche, l'étape 1 s'allume sur l'application ; la chaîne se range en haut et y restera (repère) | Sait où il en est |
| 0:39–0:43 | Une machine a une porte interne et une porte publique | 3 | Schéma du serveur : interface publique `eth0` côté Internet, interface interne `lo 127.0.0.1` à l'intérieur | Distingue les deux |
| 0:43–0:53 | Un port = le numéro d'entrée d'un programme | 2 | Les programmes apparaissent à leur numéro (sshd 22, caddy 80/443, postgres 5432), chacun relié à la porte où il écoute | Associe numéro et programme |
| 0:53–1:01 | L'app prend 3000 et, avec HOST=127.0.0.1, n'écoute que sa machine | 3 | `.env` qui se tape, l'app se branche sur la porte interne ; une requête d'Internet sur 3000 est refusée, celle du proxy passe | Voit pourquoi c'est protégé |
| 1:02–1:11 | La commande pour vérifier | 2 | Vrai terminal plein écran : `sudo ss -tlnp` et sa vraie sortie | Lit la sortie |
| 1:11–1:16 | Ce qu'il faut lire | 2 | La ligne `127.0.0.1:3000` s'allume en vert | Repère la bonne ligne |
| 1:16–1:21 | Le cas dangereux | 3 | La ligne devient `0.0.0.0:3000` en rouge (glitch) ; un seul mème : tout Internet a accès à ton app | Ressent le risque |
| 1:21–1:24 | Corriger, redémarrer, revérifier | 2 | Trois commandes à l'écran, la ligne redevient verte, la case application de la chaîne passe au ✓ (rappel) | Retient la procédure |
