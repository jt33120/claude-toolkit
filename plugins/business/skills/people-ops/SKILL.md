---
name: people-ops
description: "Runs onboarding, annual/professional review conversations, compensation checks, and basic org planning for a French SASU with employees, including mutuelle and reglement interieur thresholds. Triggers (EN): onboarding plan, performance review, entretien annuel, org chart, headcount plan, employee handbook, comp benchmarking. Triggers (FR): plan d'integration, entretien annuel, entretien professionnel, organigramme, plan d'effectifs, reglement interieur, mutuelle, remuneration equipe."
model: claude-opus-5-5
effort: medium
---

<!--
Provenance: merged and adapted for France from Anthropic knowledge-work-plugins
(Apache-2.0, https://github.com/anthropics/knowledge-work-plugins):
- human-resources/skills/onboarding
- human-resources/skills/performance-review
- human-resources/skills/comp-analysis
- human-resources/skills/org-planning
- human-resources/skills/policy-lookup
- human-resources/skills/people-report
Adaptation: French context (entretien annuel vs entretien professionnel, mutuelle obligatoire,
seuils du reglement interieur). Not legal advice.
-->

# People Ops (France)

Integration, entretiens, remuneration et organisation pour une SASU qui a (ou va avoir) des
salaries. Complement du skill `hiring` : celui-la recrute, celui-ci fait vivre l'equipe une fois
en poste.

## Quand l'utiliser
- Un nouveau salarie arrive — plan d'integration.
- Periode d'entretien annuel ou d'entretien professionnel.
- Question sur la remuneration d'un role, ou sur l'organisation de l'equipe.
- Question sur une politique interne (mutuelle, teletravail, notes de frais).

## Onboarding (`references/onboarding-entretiens.md#onboarding`)
Checklist avant J1 (comptes, materiel, contrat signe, DPAE faite — coordonner avec le skill
`payroll` sur les formalites), programme J1, semaine 1, objectifs 30/60/90 jours. Nommer un
"parrain/marraine" distinct du manager. Adapter au poste — l'integration d'un developpeur et
d'un commercial ne se ressemblent pas.

## Entretien annuel vs entretien professionnel
Deux exercices distincts en droit francais, a ne pas confondre :
- **Entretien annuel d'evaluation** : bilan de performance, objectifs, remuneration — usage
  d'entreprise, pas obligatoire legalement mais tres repandu.
- **Entretien professionnel** : obligatoire tous les 2 ans (Code du travail), porte sur les
  perspectives d'evolution professionnelle et les besoins de formation — jamais sur
  l'evaluation de la performance. Tous les 6 ans, un bilan recapitulatif verifie que le salarie
  a beneficie d'au moins une formation et d'un des autres criteres legaux.

Produire des trames separees pour les deux, en le disant clairement a l'utilisateur si la
question melange les deux usages.

## Remuneration (`references/onboarding-entretiens.md#remuneration`)
Aider a situer une remuneration par rapport au marche (recherche web, donnees fournies par
l'utilisateur) — toujours en brut annuel (usage francais), jamais en net presente comme
reference de marche sans le preciser. Signaler les ecarts a examiner (ex: deux postes
comparables avec un ecart injustifie) sans jamais presumer une cause.

## Organisation (`references/onboarding-entretiens.md#organisation`)
Pour une petite structure (SASU avec quelques salaries), l'organigramme et le plan d'effectifs
restent simples : qui rapporte a qui, quel est le prochain recrutement prioritaire. Pas de
benchmarks de grande entreprise a plaquer sur une equipe de 3-10 personnes.

## Politiques internes (`references/onboarding-entretiens.md#politiques`)
- **Mutuelle d'entreprise** : obligatoire des le premier salarie, participation employeur
  minimum 50% du cout.
- **Reglement interieur** : obligatoire des que l'effectif atteint le seuil legal (a verifier —
  actuellement 50 salaries, seuil et modalites a reconfirmer sur travail-emploi.gouv.fr) ;
  facultatif mais souvent utile avant, sous forme de note de service ou charte interne.
- Pour toute question de politique (teletravail, notes de frais, conges), repondre en clair,
  citer la source si un document interne existe, et dire explicitement si aucune politique
  ecrite n'existe — ne jamais inventer une regle.

## Garde-fous

- Ne jamais confondre entretien annuel (performance) et entretien professionnel (obligation
  legale, formation/evolution) — le dire si la demande les melange.
- Ne jamais presenter un seuil legal (reglement interieur, participation mutuelle) comme fige —
  signaler la verification a faire sur travail-emploi.gouv.fr ou service-public.fr.
- Ne jamais reproduire de donnees personnelles sensibles (sante, situation familiale) dans une
  synthese de remuneration ou de performance.
- Rappeler la limite : ceci prepare des trames et des reperes, ce n'est pas un avis juridique ni
  un audit RH formel.
- Textes adresses aux salaries (annonce, compte-rendu) passent par les skills coeur
  `writing-voice` et `language-strategy`.

## References

- `references/onboarding-entretiens.md` — checklist onboarding, trames d'entretien, remuneration, organisation, politiques
