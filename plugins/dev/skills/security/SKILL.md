---
name: security
description: >
  Security-hardens and audits AI projects on FastAPI + Supabase + Vercel + LLM stacks,
  producing either a secure architecture plan for a new project or a prioritized
  remediation checklist for existing code — backed by a deterministic audit script and
  ready-to-use hardened code snippets. Use this skill whenever the user says "secure",
  "security audit", "harden", "OWASP", "prompt injection", "RGPD/GDPR", "RLS", "JWT auth",
  "CORS", "pentest", or starts/reviews a FastAPI backend or LLM agent — even without the
  word "security". Also trigger for reviewing the security of an API, a RAG pipeline, or
  a multi-tenant agent. Distinct from `infra-deploy`: this skill hardens/audits code and
  architecture; `infra-deploy` runs deploy checklists and live incidents. Déclencheurs
  français : "sécuriser", "audit sécurité", "cyber", "durcir", "faille", "injection",
  "RGPD", "conformité", "isolation tenant", "auth JWT", "CORS".
---

<!-- Original skill by the repo owner, migrated from a personal Claude skill into jt33120/claude-toolkit. -->

# Security

Sécurise les projets IA construits sur **FastAPI + Supabase + Vercel + LLM**. Deux
modes, un seul objectif : passer d'une intention vague ("c'est sécurisé ?") à des
décisions concrètes et vérifiables.

## 1. Choisir le mode

Lire la demande et le contexte :

- **NOUVEAU PROJET** — l'utilisateur démarre (pas encore de code, ou squelette
  vide). → Produire le **plan d'architecture sécurisé** (section 2).
- **AUDIT EXISTANT** — du code existe. → Lancer le **script d'audit déterministe**
  puis produire la **checklist de remédiation priorisée** (section 3).

En cas de doute, demander : « Tu pars de zéro, ou tu as déjà du code à auditer ? »
Ne pas produire les deux livrables à la fois — ils répondent à des besoins
différents.

Dans les deux modes, finir en proposant les **snippets durcis** (`assets/`) adaptés
au cas, et brancher la question auth selon `references/auth.md`.

---

## 2. Mode NOUVEAU PROJET — plan d'architecture sécurisé

Produire un plan structuré dans cet ordre exact. Garder chaque section concrète et
adaptée à la stack réelle de l'utilisateur (ne pas réciter des généralités).

### A. Architecture réseau
- Chemin : `Internet → WAF → API FastAPI → [zone privée] → DB + LLM`.
- Un seul port exposé : 443.
- La DB n'est jamais joignable directement depuis internet. Avec Supabase, garder
  les clés `service_role` côté serveur uniquement, jamais dans le front Vercel.
- Accès admin/dev distant via VPN ou tunnel (pas d'exposition publique d'un port
  de debug).

### B. Authentification & autorisation
**Décision structurante — lire `references/auth.md` avant de trancher.** Sur une
stack Supabase, l'auth native (GoTrue + RLS) est souvent le bon choix ; un JWT
custom côté FastAPI duplique ou entre en conflit avec elle. Ne pas imposer le JWT
custom par défaut.

Principes communs aux deux branches :
- Durée de vie d'un access token courte (≤ 1 h) + refresh token.
- Token jamais en `localStorage` (vol via XSS) → cookie `httpOnly` + `Secure` +
  `SameSite`, ou stockage géré par le SDK Supabase.
- RBAC défini dès le départ : lister les rôles et leurs droits.
- Isolation des tenants : chaque utilisateur ne voit que ses données — appliquée
  par RLS côté Supabase, pas seulement par filtrage applicatif.
- MFA sur les comptes admin ; révocation rapide prévue (départ collaborateur).

### C. Sécurité de l'API FastAPI
Pointer vers les snippets `assets/secure_main.py` et `assets/security.py` plutôt
que de réécrire la config de tête. Les points non négociables :
- CORS : liste explicite de domaines, jamais `["*"]` avec credentials.
- Rate limiting obligatoire sur les endpoints qui appellent le LLM (coût + abus).
- `/docs` et `/redoc` désactivés en prod (`docs_url=None`).
- `debug=False` en prod ; les erreurs ne fuient pas de stack trace au client.
- Validation Pydantic stricte de tous les inputs (longueurs bornées).
- Headers durcis : pas de `Server`/`X-Powered-By` révélant le framework.

### D. Sécurité LLM, RAG & agent
- Filtrer les inputs **avant** le LLM (pattern matching ; LLM de garde si budget).
- Séparer données et instructions — ne jamais concaténer naïvement un document
  externe dans le prompt système.
- Sorties structurées (JSON schema strict) pour borner les actions possibles.
- RAG multi-tenant : filtrer par `tenant_id` **avant** la recherche vectorielle,
  jamais après. Désactiver le cache LLM partagé en multi-tenant.
- Traçabilité : qui a uploadé quoi, quels chunks ont servi à quelle réponse.
- Human-in-the-loop : toute action irréversible (envoi de mail, suppression,
  paiement) est interceptée au niveau du tool et confirmée.

### E. MLSecOps — pipeline CI/CD
Automatiser avant chaque déploiement (voir `scripts/audit.py`, conçu pour tourner
en CI) :
- `pip-audit` — CVE sur les dépendances.
- `trufflehog` — secrets dans l'historique git.
- Vérifs de config : `/docs` off, `debug=False`, CORS sans `*`, `.env` ignoré.

---

## 3. Mode AUDIT EXISTANT — remédiation priorisée

### Étape 1 — Lancer le script déterministe
Avant de raisonner, collecter des **preuves**. Résoudre le chemin du script fourni
avec le skill (depuis son dossier d'installation), puis exécuter :

```bash
python <dossier-du-skill>/scripts/audit.py <chemin_du_projet>
```

Le script scanne le code (stdlib only, pas de dépendance). Si `pip-audit` /
`trufflehog` sont installés, il cible les dépendances du projet et scanne séparément
les fichiers et l'historique Git. Une erreur d'outil laisse un résultat **inconnu**,
jamais un résultat « sans risque » (code de sortie 2 ; critique = 1). Les motifs regex
sont des indices à examiner, pas une certification de sécurité. Voir l'entête du script.

### Étape 2 — Compléter par une revue manuelle
Le script attrape les motifs mécaniques. Compléter par ce que seul un humain (ou le
modèle) peut juger, en lisant le code pertinent :
- Logique d'isolation tenant réellement appliquée (RLS active, pas juste un filtre
  applicatif contournable).
- Concaténation données/instructions dans les prompts LLM.
- Actions irréversibles sans human-in-the-loop.
- Cohérence RBAC (un rôle peut-il accéder aux données d'un autre ?).

### Étape 3 — Produire la checklist priorisée
Restituer sous forme de tableau, regroupé par criticité, **avec l'emplacement
précis** (fichier:ligne) et la remédiation concrète. Ne pas noyer : viser les vrais
risques d'abord.

Matrice de priorisation :

| Criticité | Critère | Délai |
|-----------|---------|-------|
| CRITIQUE | Fuite de données, accès non autorisé, clé/secret exposé, injection | Immédiat |
| IMPORTANT | Monitoring absent, config manquante, écart RGPD | Avant prod |
| NICE TO HAVE | Durcissement supplémentaire, certifications | Roadmap |

Pour le détail des règles d'audit (inputs/injection, auth, config, RAG,
monitoring, supply chain), voir l'entête de `scripts/audit.py`.

---

## 4. Snippets durcis (assets)

Proposer ces fichiers en fin d'intervention, adaptés au projet — ne pas les
régénérer de tête :

- `assets/secure_main.py` — initialisation FastAPI durcie (docs off en prod, CORS
  explicite, headers de sécurité, handler d'erreur qui ne fuit rien).
- `assets/security.py` — dépendance de vérification de token (branche Supabase JWKS
  **et** branche secret partagé), `get_current_user`, garde RBAC, rate limiting.
- `assets/env.example` — variables attendues, sans aucune valeur réelle.

Adapter (domaines CORS, rôles, issuer Supabase) au contexte avant de les livrer.

---

## 5. Conformité & références

Détail réglementaire dans `references/compliance.md` (à lire quand l'utilisateur
touche au RGPD, à l'AI Act, NIS2, DORA, ou héberge des données sensibles). En
résumé :
- **OWASP Top 10 Web & LLM 2025** — broken access control, injection,
  misconfiguration ; prompt injection, excessive agency, system prompt leakage.
- **AI Act** — classement/évaluation automatique de personnes (recrutement, etc.)
  = haut risque → documentation + supervision humaine obligatoires.
- **NIS2** — notification d'incident sous 24 h, sécurité de la supply chain.
- **RGPD** — minimisation, durée de conservation, droit à l'effacement, DPA client.

---

## 6. Où se situe cette skill

Cette skill durcit et audite le **code et l'architecture** (auth, RLS, CORS, LLM,
conformité) — avant ou indépendamment de tout déploiement. Pour la checklist de
mise en prod (CI, migrations, variables d'env, rollback) ou la gestion d'un
incident live, voir `infra-deploy` : les deux skills sont complémentaires, pas
redondantes. Une fois le code corrigé, faire vérifier le correctif par
`verification-before-completion` avant de le considérer résolu.

---

## 7. Répartition des rôles avec les autres outils sécurité

Plusieurs outils touchent à la sécurité dans cet écosystème — ne pas les confondre :

- **Plugin Anthropic `security-guidance`** — garde-fou en temps réel *pendant*
  l'écriture du code (suggestions inline au fil de l'eau). Continu, pas une
  revue déclenchée à la demande.
- **`/security-review` (intégré à Claude Code)** — revue du diff/de la PR en
  cours, ponctuelle, au moment de committer ou proposer une PR.
- **Cette skill (`security`)** — le niveau au-dessus : plan d'architecture
  sécurisé pour un *nouveau* projet, ou audit complet de la stack existante
  (FastAPI + RLS Supabase + Vercel + prompt injection LLM) via
  `scripts/audit.py`. Pas un linter continu, pas limité au diff courant —
  une revue de fond, déclenchée explicitement.
- **Skill vendor `supabase`** — référence pour le détail d'implémentation des
  policies RLS elles-mêmes (syntaxe, patterns, pièges). Cette skill vérifie
  *que* l'isolation tenant est appliquée par RLS, pas *comment* écrire chaque
  policy — déléguer ce dernier point au skill Supabase.

En résumé : `security-guidance` pendant que ça s'écrit, `/security-review`
avant de merger, cette skill pour l'architecture/l'audit complet, `supabase`
pour le détail RLS.

---

*Base : formation cyber + OWASP/AI Act/NIS2/RGPD — itéré 2026.*
