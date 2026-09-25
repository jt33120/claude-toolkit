---
name: payroll
description: "Explains salary structure, president compensation vs dividends, social charges, and payroll prep for a French SASU that may hire. Triggers (EN): run payroll, how much should I pay myself, president salary vs dividends, social charges, URSSAF, DSN, payslip, hire an employee salary. Triggers (FR): fiche de paie, combien me verser, remuneration du president, dividendes ou salaire, charges sociales, URSSAF, DSN, bulletin de salaire, salaire brut net, convention collective."
---

<!--
Provenance: adapted for France from Anthropic knowledge-work-plugins (Apache-2.0,
https://github.com/anthropics/knowledge-work-plugins):
- small-business/skills/payroll-prep
- small-business/skills/plan-payroll
Rewritten for French payroll: brut/net, URSSAF, DSN, president SASU vs employee, convention
collective. Not a substitute for an expert-comptable / payroll provider (silae, PayFit...).
-->

# Payroll (France)

Aide a comprendre et preparer la paie d'une SASU : remuneration du president (assimile-salarie),
et, si l'activite embauche, la paie des salaries. **Ce skill ne genere jamais un bulletin de
paie officiel et ne declare rien a l'URSSAF.** Il explique, calcule des ordres de grandeur, et
prepare ce qu'il faut transmettre a l'expert-comptable ou au logiciel de paie (PayFit, Silae...).

## Quand l'utiliser
- "Combien dois-je me verser" / arbitrage salaire president vs dividendes.
- Preparer une embauche : ordre de grandeur du cout charge, choix du statut.
- Comprendre un bulletin de paie, une charge URSSAF, ou une echeance DSN.
- Verifier avant l'expert-comptable que rien n'est oublie.

## President de SASU : salaire vs dividendes (`references/remuneration-president.md`)

Le president de SASU (non associe unique obligatoirement, mais frequemment) est en principe
**assimile-salarie** : affilie au regime general de la Securite sociale, avec des charges
sociales sur son salaire proches (pas identiques) de celles d'un salarie classique, mais **sans
cotisation chomage**. C'est different d'un gerant majoritaire de SARL (TNS).

- **Salaire** : charge deductible du resultat de la SASU (economie d'IS), couvre le president
  (maladie, retraite, prevoyance si mise en place), mais charges sociales elevees (souvent
  60-80% du net en charges patronales + salariales cumulees, ordre de grandeur a verifier).
- **Dividendes** : pas de charges sociales URSSAF sur les dividendes du president de SASU (a la
  difference du gerant majoritaire de SARL), mais soumis aux prelevements sociaux (CSG/CRDS,
  18,6 % depuis le 1er janvier 2026) et au PFU de 31,4 % au total, ou au bareme de l'IR ;
  verifier les taux officiels applicables a la date du versement avant tout calcul ; pas de droits sociaux generes (pas de retraite,
  pas de couverture maladie liee) ; imposition de la SASU a l'IS en amont.
- **Arbitrage typique** : un minimum de salaire pour ouvrir des droits sociaux (couverture
  maladie, trimestres de retraite) + le reste en dividendes une fois les resultats connus, mais
  l'equilibre depend du chiffre d'affaires, du besoin de tresorerie personnelle regulier, et de
  la situation globale (autres revenus, age, projets de retraite). **Toujours faire trancher
  par l'expert-comptable** — les taux de charges et l'IS changent regulierement.

## Embaucher un salarie (`references/urssaf-dsn.md`)

Si l'activite grandit et qu'une embauche est envisagee :
- Determiner la convention collective applicable (souvent Syntec pour le conseil/IT en France —
  a verifier selon le code APE/NAF exact de la SASU).
- Estimer le cout charge total : salaire brut x ~1,4-1,45 en ordre de grandeur pour les charges
  patronales (variable selon le niveau de salaire et les exonerations, ex: reduction generale
  de cotisations sur les bas salaires) — donner une fourchette, jamais un chiffre unique
  presente comme exact.
- Formalites : DPAE (declaration prealable a l'embauche) avant le premier jour, contrat de
  travail ecrit (CDI ou CDD selon le besoin), periode d'essai, visite medicale, affiliation a la
  mutuelle d'entreprise (obligatoire, participation employeur minimum 50%).
- DSN (declaration sociale nominative) : declaration mensuelle obligatoire, generalement geree
  par le logiciel de paie — ce skill prepare les elements (heures, absences, variables) mais ne
  la soumet pas.

## Freelance vs CDI

Pour un consultant qui hesite entre recruter un salarie ou faire appel a un freelance/sous-
traitant : rappeler le risque de requalification en salariat deguise si le freelance travaille
en exclusivite, sous subordination (horaires imposes, outils imposes, pas de clientele propre).
Ne pas trancher a la place de l'utilisateur — signaler le risque et orienter vers un avocat en
droit du travail ou l'expert-comptable si le doute est reel.

## Workflow

1. Comprendre la question (arbitrage remuneration, preparation d'embauche, ou lecture d'un
   bulletin) et le contexte (SASU seule, ou deja des salaries).
2. Donner des ordres de grandeur clairement etiquetes comme tels, jamais des chiffres presentes
   comme exacts sans verification.
3. Preparer ce qui doit remonter au professionnel (montants souhaites, dates, variables de paie)
   plutot que de produire un document officiel.
4. Toujours conclure par : "a confirmer avec votre expert-comptable ou logiciel de paie" pour
   tout chiffre engageant une declaration.

## Garde-fous

- Ne jamais generer un bulletin de paie officiel ni le presenter comme valant declaration.
- Ne jamais transmettre ou "soumettre" une DSN — preparer seulement les elements.
- Toujours signaler que les taux de charges, seuils d'exoneration et plafonds (PASS) evoluent
  chaque annee — verifier sur urssaf.fr avant tout calcul engageant.
- Ne jamais reproduire de donnees personnelles sensibles (numero de securite sociale, RIB) dans
  une sortie.
- Rappeler systematiquement la limite : "je ne suis pas expert-comptable, ceci est indicatif."

## References

- `references/remuneration-president.md` — detail salaire vs dividendes, charges, arbitrage
- `references/urssaf-dsn.md` — embauche, cout charge, DSN, convention collective, freelance vs CDI
