---
name: hiring
description: "Builds the hiring packet (job post, interview guide, offer letter) and screens applicants for a French SASU, respecting French non-discrimination law, promesse d'embauche, and freelance-vs-CDI distinctions. Triggers (EN): help me hire, write a job post, screen these applications, draft an offer letter, interview questions, who should I interview. Triggers (FR): je recrute, offre d'emploi, ecrire une annonce, trier les candidatures, promesse d'embauche, questions d'entretien, redige une offre, qui interviewer."
model: claude-opus-5-5
effort: medium
---

<!--
Provenance: merged and adapted for France from Anthropic knowledge-work-plugins
(Apache-2.0, https://github.com/anthropics/knowledge-work-plugins):
- human-resources/skills/recruiting-pipeline
- human-resources/skills/interview-prep
- human-resources/skills/draft-offer
- small-business/skills/job-post-builder
- small-business/skills/hiring-screener
Adaptation: French labor law (non-discrimination, promesse d'embauche, periode d'essai,
freelance vs CDI). Not legal advice.
-->

# Hiring (France)

Construit le dossier de recrutement — annonce, grille d'entretien, offre — et trie les
candidatures pour une SASU qui recrute son premier salarie ou etoffe son equipe. **Ce skill ne
publie rien et n'envoie rien sans validation.**

## Quand l'utiliser
- "J'ai besoin de recruter" / "ecris une offre d'emploi".
- Un tri de CV ou une pile de candidatures a traiter.
- Preparer des entretiens structures ou rediger une offre (promesse d'embauche).

## Workflow

### 1. Cadrer le poste (`references/entretien-offre.md#brief`)
Titre, mission, competences requises (verifiables sur un CV — "sait faire X" pas "bon esprit
d'equipe"), fourchette de remuneration (donner un chiffre ou une fourchette, jamais
"competitif"), type de contrat envisage (CDI, CDD, freelance — voir section freelance vs CDI),
process d'entretien (nombre d'etapes, qui interviewe).

### 2. Rediger l'annonce
Langage inclusif, honnete sur les points difficiles du poste, exigences resserrees (chaque ligne
requise doit etre verifiable sur un CV). Mentionner la remuneration si connue — "competitif"
n'est pas une fourchette.

### 3. Grille d'entretien structuree (`references/droit-travail.md#entretiens`)
4-6 competences cles, questions comportementales par competence, grille de notation 1/3/5.
**Les questions d'entretien doivent rester liees au poste** — en droit francais, certaines
questions sont interdites ou risquees (situation familiale, grossesse, sante, opinions
politiques/religieuses, origine) meme formulees "innocemment". Voir `references/droit-travail.md`.

### 4. Trier les candidatures
Scorer uniquement sur la grille liee au poste — jamais sur l'age, le nom, la photo, l'adresse,
l'ecole, un trou dans le CV non explique. C'est a la fois une regle ethique/legale
(non-discrimination, art. 225-1 et suivants Code penal) et une meilleure methode de tri. Une
information manquante ("ne peut etre evaluee") justifie une question au candidat, pas un rejet
silencieux.

Repondre a tous les candidats — c'est aussi une question de reputation pour une petite
structure. Rediger les refus avec bienveillance, sans inventer de raison.

### 5. Offre et promesse d'embauche (`references/droit-travail.md#promesse`)
Distinguer une simple invitation a poursuivre les discussions d'une **promesse d'embauche
ferme et precise** (poste, remuneration, date de debut) qui engage presque comme un contrat en
droit francais — etre precis dans la formulation pour ne jamais engager sans le vouloir. Inclure
: poste, remuneration (brute annuelle), date de debut, periode d'essai, convention collective
applicable (souvent Syntec pour le conseil/IT — a verifier selon le code APE). **Rien n'est
envoye sans validation explicite de l'utilisateur.**

### 6. Freelance vs CDI (`references/droit-travail.md#freelance`)
Quand l'hesitation porte sur freelance vs salarie, signaler le risque de requalification en
salariat deguise si le freelance travaille en exclusivite et sous subordination. Orienter vers
un avocat en droit du travail ou l'expert-comptable en cas de doute reel — ne pas trancher a la
place de l'utilisateur.

## Garde-fous

- Ne jamais publier une annonce, envoyer un email, ou transmettre une offre sans validation
  explicite.
- Ne jamais scorer sur un critere hors grille du poste — c'est aussi une regle legale
  (non-discrimination).
- Ne jamais inventer une raison de refus — rester bienveillant et vague plutot que specifique et
  faux.
- Ne jamais formuler une "invitation a discuter" de facon a ce qu'elle ressemble a une promesse
  d'embauche ferme sans le vouloir.
- Ne jamais reproduire de donnees personnelles sensibles d'un candidat (date de naissance,
  adresse complete, numero de securite sociale) au-dela de ce qui est necessaire.
- Toujours rappeler que le droit du travail francais evolue et qu'un doute serieux merite un
  avocat ou l'expert-comptable — ceci n'est pas un avis juridique.
- Textes adresses aux candidats (annonce, offre, refus) passent par les skills coeur
  `writing-voice` et `language-strategy`.

## References

- `references/droit-travail.md` — non-discrimination, entretiens, promesse d'embauche, freelance vs CDI
- `references/entretien-offre.md` — brief de poste, structure de l'annonce, grille d'entretien, offre
