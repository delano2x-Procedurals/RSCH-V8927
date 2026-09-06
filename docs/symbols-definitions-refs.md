# Symbols, Definitions, and Original vs Build-On References

**Companion to:** [gqi-semistructured-interview-guide.md](gqi-semistructured-interview-guide.md) (`ITDR-GQI-INT-v0.1.1`) and [chapter-iii-methodology.md](chapter-iii-methodology.md)  
**Audience:** researcher codebook, Delve descriptions, Alignment Map Constructs node  
**Not for:** spoken questions, Chapter IV theme titles, new theory claims

This register locks notation. It does not create a new theoretical symbol set. Original sources define the symbol. Build-on sources extend, test, or situate the construct for this Gap. The interview protocol remains a new unpublished instrument.

CSV mirror: [notion/templates/symbols.csv](notion/templates/symbols.csv). Reference register: [notion/templates/references.csv](notion/templates/references.csv) column `origin` = `original` | `build_on` | `new_instrument` | `software` | `audit_artifact`.

---

## 1. Symbol table (researcher only)

Mitchell et al. (1997) Venn types map onto the leverage-memo field `attribute_mix`. Type names stay in memos. They are not Delve theme titles.

| Symbol | `attribute_mix` | Mitchell type (memo only) | Instrument use | Delve `code_id` |
| --- | --- | --- | --- | --- |
| `P` | power-only | dormant | Set A | `power` |
| `L` | legitimacy-only | discretionary | Set B | `legitimacy` |
| `U` | urgency-only | demanding | Set C | `urgency` |
| `P+L` | power+legitimacy | dominant | leverage memo | dual-code; not a theme |
| `P+U` | power+urgency | dangerous | leverage memo | dual-code; not a theme |
| `L+U` | legitimacy+urgency | dependent | leverage memo | dual-code; not a theme |
| `P+L+U` | definitive (all three) | definitive | leverage memo | dual-code; not a theme |
| `Lev` | enacted combination | *not a Mitchell type* | Set L; phenomenon | `leverage_location` |
| `DR` | — | — | Set D; PQ2 | `decision_rights` |
| `ESC` | — | — | Set E; PQ2 | `escalation` |
| `EV` | — | — | Set F (F1–F2); PQ2 | `evidentiary_standards` |
| `RA` | — | — | Set F (F3 + artifact path); PQ2 | `recoverability_assurance` |
| — | unclear / none-observed | not a type | valid memo | `pull_unlocated` |

`Lev` is **not** a fourth salience attribute. It is the observed pull in the incident: who moved restore order, delayed an action, or redefined “done,” and what supplied that pull.

---

## 2. Definition cards

Each card has four clauses: original theoretical definition, this-study operational definition, spoken stand-in, and not-this.

### `P` — Power

| Clause | Text |
| --- | --- |
| Original theoretical def | A stakeholder’s capacity to influence the firm based on coercive, utilitarian, or normative means (Mitchell et al., 1997). |
| This-study operational def | In the named incident, a person or group could force, withhold, delay, override, or stop a recovery action. |
| Spoken stand-in | Request, pressure, delay, override, stop. |
| Not this | Asking “Did you experience a power problem?”; promoting Power to a theme title; treating snippet count as importance. |

### `L` — Legitimacy

| Clause | Text |
| --- | --- |
| Original theoretical def | A generalized perception that a claim or claimant is desirable, proper, or appropriate within some socially constructed system of norms, values, beliefs, and definitions (Mitchell et al., 1997). |
| This-study operational def | In the named incident, a claim to a service or restore order was treated as rightful (role, plan, contract, regulation) or treated as out of line / outside role. |
| Spoken stand-in | Right to ask; out of line; outside their role. |
| Not this | “Did you experience a legitimacy problem?”; scoring the plan against NIST/ISO/BCM; using legitimacy as a Chapter IV heading. |

### `U` — Urgency

| Clause | Text |
| --- | --- |
| Original theoretical def | The degree to which a stakeholder claim calls for immediate attention, combining time sensitivity and criticality (Mitchell et al., 1997). Neville et al. (2011) treat urgency as amplifying salience rather than independently identifying stakeholders; that refinement is build-on, not a replacement definition. |
| This-study operational def | In the named incident, a time-critical demand reordered attention, or a claimed clock was not acted on (boundary). |
| Spoken stand-in | Time-critical; time pressure. Do not say “urgency” unless the participant uses it first. |
| Not this | Spoken codebook word “urgency” as a question stem; clock-as-theme-title; Guest et al. (2006) as the source of the construct. |

### `Lev` — Leverage

| Clause | Text |
| --- | --- |
| Original theoretical def | No original Mitchell type. Leverage is this study’s name for the enacted combination of P, L, and/or U. |
| This-study operational def | Who actually moved restore order, delayed an action, or redefined “done,” plus what supplied that pull, in one named ITDRPaaS event. |
| Spoken stand-in | Who moved / who could have stopped it; position, written rule, the clock, something else; pull. |
| Not this | A fourth salience attribute; the spoken word “leverage”; a finding that “confirms” a Mitchell type; `unclear` recoded as a type. |

### `DR` — Decision rights

| Clause | Text |
| --- | --- |
| Original theoretical def | Not a Mitchell attribute. Used here as the PQ2 enactment of whose claim counted: who was authorized to decide. |
| This-study operational def | Who was supposed to make the call on the restoration tradeoff versus who actually made it, including authority needed but absent. |
| Spoken stand-in | Who was supposed to make the call, and who actually made it. |
| Not this | An org-chart finding detached from the named incident; a theme titled “Decision Rights.” |

### `ESC` — Escalation

| Clause | Text |
| --- | --- |
| Original theoretical def | Not a Mitchell attribute. PQ2 enactment of how a stalled or contested claim was moved upward or outward. |
| This-study operational def | What triggered an escalation in the named incident, and whether it sped restoration, slowed it, or changed “done.” Nothing escalated is a boundary (`no_escalation`). |
| Spoken stand-in | What, if anything, triggered an escalation; did it speed, slow, or change “done.” |
| Not this | Failed interview if nothing was escalated; a theme titled “Escalation.” |

### `EV` — Evidentiary standards

| Clause | Text |
| --- | --- |
| Original theoretical def | Not a Mitchell attribute. PQ2 enactment of what counted as enough proof that a service was recovered. Assurance literature is build-on for the definition of reviewable, decision-relevant evidence (Lowry et al., 2025; Park et al., 2023; verify). |
| This-study operational def | What the manager treated as enough proof in the event, and whether anyone asked for different proof mid-incident. |
| Spoken stand-in | Enough proof; different proof mid-incident. |
| Not this | NIST/ISO/BCM scoring; a theme titled “Evidence.” |

### `RA` — Recoverability assurance

| Clause | Text |
| --- | --- |
| Original theoretical def | As used in the project plan: reviewable, decision-relevant evidence that prioritized services can be restored within tolerance (Lowry et al., 2025; Park et al., 2023; verify). |
| This-study operational def | What the manager would point to—log, test, approval, ticket, or verbal reconstruction—to defend that restoration. Path C (no artifact named) is `no_reviewable_proof`. |
| Spoken stand-in | What would you point to if you had to defend that restoration. |
| Not this | An audit of the artifact; treating Path C as invalid data. |

### Design symbols (not salience types)

| Symbol | Original theoretical def | This-study operational def | Spoken stand-in | Not this |
| --- | --- | --- | --- | --- |
| GQI | Patterned accounts of events, decisions, and conditions; theoretically informed items permitted (Caelli et al., 2003; Kahlke, 2014; Percy et al., 2015) | Managers’ accounts of one named ITDRPaaS incident and the objects used in it | Walk me through that event… | Lived experience; essence; voices |
| CIT | Focused account of a named incident (Flanagan, 1954; Chell, 2004; Butterfield et al., 2005) | Q0 opening; one disruption/failover/test/operational recovery in 36 months | Please walk me through one specific… | Guest et al. (2006) as the interview method |
| Hybrid TA | Deductive template plus inductive codes (Fereday & Muir-Cochrane, 2006) | STRUCTURAL + FRAMEWORK_DEDUCTIVE + BOUNDARY, then EMERGENT after MU lock | Not spoken | Reflexive TA mixed with kappa; “analyzed using Delve” |
| Information power | Sample size guided by aim, specificity, theory, dialogue, and analysis strategy (Malterud et al., 2016) | n = 12 locked; stopping is analytic | Not spoken | Automatic saturation at 12 |

---

## 3. Original versus build-on

### Theory

| Original (do not replace) | Build on (What We Know / why now / PQ2 definition only) |
| --- | --- |
| Mitchell, Agle, & Wood (1997) — power, legitimacy, urgency, salience, Venn types | Agle, Mitchell, & Sonnenfeld (1999) — empirical attribute–salience test |
| Donaldson & Preston (1995) — stakeholder-claim management (Gap / What We Know) | Parent & Deephouse (2007) — managerial level/role and attribute weighting |
| Freeman, Wicks, & Parmar (2004) — corporate objective / stakeholder theory context | Neville, Bell, & Whitwell (2011) — urgency as amplifier; legitimacy of the claim |
| | Dorobantu, Henisz, & Nartey (2024) — legitimacy judgments in informational environments (why now) |
| | Lowry, Petter, & Leimeister (2025)* and Park et al. (2023)* — recoverability-assurance definition only |

\* `citation_status=verify` until a 2023–2025 DOI is confirmed.

### Method

| Original | Build on |
| --- | --- |
| Caelli et al. (2003); Kahlke (2014); Percy et al. (2015) — GQI | Lester, Cho, & Lochmiller (2020) — write-up of qualitative analysis steps |
| Flanagan (1954); Chell (2004); Butterfield et al. (2005) — CIT | Guest, Bunce, & Johnson (2006) — **stopping discussion only** |
| Aronson (1994); Taylor & Bogdan (1998) — meaning units before theme names | Malterud, Siersma, & Guassora (2016) — information power |
| Fereday & Muir-Cochrane (2006) — hybrid codebook TA (this study’s analytic method) | Naeem, Ozuem, Howell, & Ranfagni (2024) — saturation as analytic decision guide |
| | Braun & Clarke (2019, 2021, 2022) — codes ≠ themes; patterned meaning; do not say themes “emerged”; frequency ≠ importance. **Not** the analytic method. **Not** mixed with ICR. |

### Trustworthiness and reporting

| Original | Build on |
| --- | --- |
| Lincoln & Guba (1985) — credibility, dependability, confirmability, transferability; audit trail; referential adequacy | Nowell et al. (2017) — TA trustworthiness tactics |
| | Korstjens & Moser (2018); Carcary (2020) — practical audit-trail guidance |
| | O’Brien et al. (2014) SRQR; Tong et al. (2007) COREQ — reporting checklists, not methods |
| | O’Connor & Joffe (2020) — ICR **only** if the committee requires a second coder |

### Software, instrument, audit artifacts

| Class | `origin` | What it is | Cite as |
| --- | --- | --- | --- |
| Delve | `software` | CAQDAS store for codebook, snippets, memos, URLs | Delve, Ho, & Limpaecher (n.d.) |
| `ITDR-GQI-INT-v0.1.1` | `new_instrument` | Spoken protocol, skip rules, coverage checklist, leverage memo | Walker (2026), unpublished instrument |
| Interval CSV nest | `audit_artifact` | Dated Codes/Snippets/items/references exports | Folder date; not literature |

---

## 4. Link keys

| From | To | Key |
| --- | --- | --- |
| Symbol | Spoken item | `question_id` (`L1` … `F3`) |
| Symbol | Delve | `code_id` |
| Symbol | Memo | `attribute_mix` |
| Symbol | Reference | `ref_id` in `references.csv` (`origin` column) |
| Chapter III matrix | This file | Question ID row |

Do not import Mitchell type names (`dormant`, `dangerous`, `definitive`, …) into Delve as codes or into Chapter IV as theme titles.
