# RGPD et AI Act pour un consultant IA / editeur SaaS

Non exhaustif, non un avis juridique. Verifier contre cnil.fr et eur-lex.europa.eu (le texte
du reglement AI Act, UE 2024/1689) avant toute decision engageante.

## RGPD — les bases qui reviennent tout le temps

- **Base legale** : contrat (execution du service), interet legitime, consentement, obligation
  legale. Documenter laquelle s'applique a chaque traitement.
- **Registre des traitements** : obligatoire des qu'un traitement est regulier — une SASU
  consultant/SaaS en a un quasi systematiquement (clients, prospects, utilisateurs du produit).
  Pas besoin de DPO en dessous des seuils de traitement a grande echelle, mais le registre reste
  du.
- **Sous-traitants (art. 28)** : tout LLM/API tierce (OpenAI, Anthropic, etc.), tout hebergeur,
  tout outil CRM/emailing qui traite des donnees pour votre compte est un sous-traitant. Il faut
  un DPA (Data Processing Agreement) avec chacun. Verifier les clauses contractuelles types (SCC)
  si transfert hors UE (le cas de la plupart des fournisseurs US — verifier le mecanisme de
  transfert : Data Privacy Framework, SCC, etc.).
- **Duree de conservation** : definie et justifiee par finalite, pas "indefiniment".
- **Droits des personnes** : acces, rectification, effacement, portabilite, opposition. Delai
  de reponse : 1 mois, extensible de 2 mois si complexe.
- **Violation de donnees** : notification CNIL sous 72h si risque pour les personnes ; les
  personnes concernees informees si risque eleve.
- **Politique de confidentialite** : obligatoire, accessible, en francais, expliquant finalites,
  bases legales, destinataires, duree, droits et contact.
- **DPIA (analyse d'impact)** : requise si traitement a risque eleve (profilage a grande
  echelle, donnees sensibles a grande echelle, surveillance systematique). Rare pour un SaaS B2B
  standard mais a evaluer si le produit fait du profilage ou traite des categories particulieres
  de donnees.

### Points specifiques a l'IA generative/agentique
- Si le produit envoie des donnees clients a un LLM tiers pour traitement, c'est un transfert
  vers un sous-traitant — DPA + verification du mecanisme de transfert international requis.
- Informer les utilisateurs quand ils interagissent avec un systeme d'IA generative (transparence
  — recoupe aussi l'AI Act, voir ci-dessous).
- Eviter d'entrainer un modele sur des donnees clients sans base legale et sans le dire
  explicitement dans les CGU.

## AI Act (reglement UE 2024/1689) — classification rapide

Le reglement classe les systemes d'IA par niveau de risque. **Ne jamais presumer une
classification sans verifier l'annexe III (liste des cas a haut risque) pour le cas precis** —
la classification depend de l'usage, pas seulement de la technologie.

- **Risque inacceptable** — interdit (notation sociale, manipulation subliminale...). Peu
  probable pour un outil de conseil/SaaS B2B classique.
- **Risque eleve** — annexe III : RH/recrutement, credit scoring, evaluation d'eligibilite a des
  services essentiels, systemes utilises dans l'education, la justice, certains usages en sante.
  Si le SaaS touche a l'un de ces domaines (ex: un outil d'aide au recrutement, de scoring
  client), verifier serieusement — obligations lourdes (gestion des risques, qualite des
  donnees, documentation technique, supervision humaine, enregistrement).
- **Risque limite (transparence)** — chatbots, contenu genere par IA, systemes de recommandation
  utilisant l'IA generative : obligation d'informer l'utilisateur qu'il interagit avec une IA.
  C'est le cas le plus frequent pour un consultant/SaaS qui integre du LLM dans son produit.
- **Risque minimal** — la majorite des usages internes ou d'assistance (redaction, analyse de
  donnees non sensibles).

### A faire cote SASU
- Documenter, meme sommairement, la classification de risque de chaque fonctionnalite IA du
  produit, avec la justification.
- Ajouter une mention de transparence dans le produit/CGU si le systeme genere du contenu ou
  interagit directement avec l'utilisateur final.
- Suivre les echeances d'entree en application du reglement (elles sont echelonnees dans le
  temps par categorie d'obligation) — verifier la date en vigueur au moment de la question,
  le calendrier n'est pas figé dans cette fiche.

## Quand consulter un professionnel
- Le produit touche une categorie de l'annexe III (RH, credit, sante, education, justice).
- Volume de donnees important, donnees sensibles, ou profilage.
- Un client ou partenaire demande un DPA specifique, une certification, ou un audit RGPD.
- Doute sur le mecanisme de transfert international de donnees.

Sources a verifier : cnil.fr (guides RGPD, fiches pratiques IA), eur-lex.europa.eu (texte
consolide de l'AI Act), autorite competente pour l'AI Act en France (a confirmer).
