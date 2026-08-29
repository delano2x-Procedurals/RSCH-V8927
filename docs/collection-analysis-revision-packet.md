# Collection-Plus-Analysis Revision Packet

Paste-ready replacements for the Project Plan nodes that are still Partial or Weak on the Alignment Map. Each block labeled **NEW** did not exist as a written step in the prior data-collection draft. Keep the study the same: GQI, critical-incident interviews, SME IT/network managers, stakeholder-salience as the guide when no finer step exists.

**Use with:** [alignment-assessment-data-collection.md](alignment-assessment-data-collection.md)

---

## Highlighted New Efforts

These are the new work products that close the Gap. Do not treat them as optional polish.

| # | **NEW** effort | Alignment Map marker it fills | Gap data it makes collectable |
| --- | --- | --- | --- |
| 1 | Timed interview protocol with ethics script, CIT opening, six salience-guided question sets, and a closing prompt | Measures/Artifacts; Data Collection | Competing claims; power, legitimacy, urgency; decision rights; escalation; proof |
| 2 | Interview decision rules (when to probe, when to skip, when to stop an abstract answer) | Procedures; Dependability | Stops generic “how we usually recover” talk that cannot close the Gap |
| 3 | Artifact pipeline with request script, three intake paths, field-note map, and MU-table entry rule | Measures/Artifacts; Data Collection | Formal intent vs. ad hoc action; recoverability-assurance evidence |
| 4 | Analysis bridge: Practice 2 four-step reduction + sensitizing start-list + theme-mapping rule | Data Analysis; Constructs | Findings that answer PQ1 and PQ2 without confirming Mitchell et al. in advance |
| 5 | Meaning-unit table template (talk + artifact rows) and required boundary case per construct | Dependability; Data Analysis | Contested authority and failed-proof incidents stay inside the finding |
| 6 | Citation repair table (what each source is now allowed to support) | Methodology; Dependability | Prevents CIT, saturation, and NIST from being used as the wrong method |
| 7 | Language-drift find/replace list (phenomenology and confirmatory wording out) | Methodology; Constructs | Keeps GQI on external events, decisions, and artifacts |
| 8 | Ethics-threat matrix tied to Gap data quality, plus member-check and storage SOP | Procedures; Dependability | Stops organizational risk from deleting the proof and authority talk PQ2 needs |
| 9 | Information-power sample justification and recruitment channel/length | Sample; Recruitment | Makes n = 10–15 defensible without claiming automatic saturation |
| 10 | Revised 3–4 paragraph Project Plan sections (Measures, Procedures, Analysis, Trustworthiness) | All collection nodes | Courseroom-ready prose, not only an appendix |

---

## 1. **NEW** Implied Questions (paste if official RQs are not yet locked)

- **PQ1.** How do U.S. SME IT and network managers describe stakeholder-claim management and salience shifts (power, legitimacy, urgency) during ITDRPaaS recovery or testing incidents?
- **PQ2.** How do those shifts get enacted as decision rights, escalation pathways, and evidentiary / recoverability-assurance standards that managers can defend to stakeholders?

Replace these two lines with official project-question wording when available. Do not change the unit of analysis (SME managers; one named incident; external platform recovery).

---

## 2. **NEW** Interview Protocol (concrete instrument)

**Length:** 60–75 minutes.  
**Modality:** One-to-one video session, English, audio- and video-recorded with a running notes backup.  
**Rule:** Theoretical words (salience, legitimacy, recoverability assurance) stay in the researcher codebook. Questions use manager language (Flanagan, 1954; Chell, 2004; Capella guiding-question rules).

### 2.1 Pre-session checklist (**NEW**)

1. Confirm signed electronic consent is on file.
2. Confirm inclusion: U.S. SME, 10–200 personnel; IT/network/systems/infrastructure/operations manager; direct role in external-platform or managed recovery; at least one disruption, failover, test, or operational recovery in 36 months; not vendor-only employed.
3. Assign participant code `P##` before the call. Do not speak the employer name into the recording if it can be avoided.
4. Start recorder. If recorder fails, stop and reschedule. Do not continue from memory.
5. Open a blank Artifact Map row set (Section 3.3) and a blank reflexive memo (Section 6.4).

### 2.2 Minute 0–3: Ethics script (read aloud) (**NEW**)

> Thank you for meeting. This interview is part of a doctoral study of how IT and network managers in U.S. small and medium enterprises handle recovery decisions when they use an external recovery platform. Participation is voluntary. You may skip any question or stop at any time without penalty. I will record the session so I can transcribe it. I will remove your name, your employer’s name, vendor names, and product names from the transcript. You do not have to share any confidential disaster-recovery document. If you mention a plan, ticket, or test record, you may describe what it did in the event, or share a redacted excerpt if your organization allows it. Refusing to share a document does not end the interview. After transcription I will send you a de-identified transcript and ask you to correct anything I misheard. You will have seven calendar days to reply. Correcting a factual error is welcome. The analysis will still include de-identified accounts of contested recovery decisions. Do I have your permission to begin recording and to continue?

If no: stop, thank the participant, destroy any partial file.

### 2.3 Minutes 3–18: Critical-incident opening (PQ1)

**Q0 (required).**  
> Please walk me through one specific disruption, failover, recovery test, or operational recovery in the last 36 months where you used an external recovery platform or managed recovery service. Start wherever the event became your problem, and tell me what happened in as much detail as you can.

**Decision rules (**NEW**).**

| If the participant… | Researcher does this |
| --- | --- |
| Stays with “how we usually recover” | *If you can, stay with that one event rather than with how recovery usually works.* |
| Names several events | *Which one is the most vivid, or the one where the recovery decision was hardest? Let’s stay with that one.* |
| Cannot name any event in 36 months | Stop. The case fails inclusion. Thank and close. |
| Gives a thin timeline | *What happened first? What did you do next? Who else was in that conversation?* |
| Becomes distressed | Pause. Offer to skip or stop. Do not press for graphic incident detail. |

Do not introduce power, legitimacy, urgency, or proof in Q0. Let the story run.

### 2.4 Minutes 18–55: Topical guiding questions (only if the story did not already cover the construct)

Ask in this order. Skip a set if the incident narrative already answered it with a concrete example. After a skip, record “covered in Q0” on the construct checklist (Section 2.6).

#### Set A — Power (PQ1) **NEW**

- A1. *In that event, whose request or pressure most affected what got restored first?*
- A2. *Was there anyone who could delay, override, or stop a recovery action you thought was right?*
- A3. *If that pressure had not been there, what would you have done differently?*

#### Set B — Legitimacy (PQ1) **NEW**

- B1. *Whose claim to a service or a recovery order did people treat as legitimate — as “they have a right to ask for this”?*
- B2. *Was anyone’s request treated as out of line or outside their role? What happened then?*

Do not ask “Did you experience a legitimacy problem?” That hides an assumption.

#### Set C — Urgency (PQ1) **NEW**

- C1. *What made one service or one stakeholder more time-critical than another in that event?*
- C2. *Did that sense of urgency change while you were working the incident? What changed it?*

#### Set D — Decision rights (PQ2) **NEW**

- D1. *Who was supposed to make the call on that tradeoff, and who actually made it?*
- D2. *Was there a moment when you needed authority you did not have? What did you do?*

#### Set E — Escalation (PQ2) **NEW**

- E1. *What, if anything, triggered an escalation?*
- E2. *Did escalation speed the restoration, slow it, or change what “done” meant?*

If the participant says nothing was escalated, that is a **boundary case**, not a failed interview. Record it.

#### Set F — Evidentiary standards and recoverability assurance (PQ2) **NEW**

- F1. *When you told others the service was recovered, what did you treat as enough proof?*
- F2. *Did anyone ask for different proof mid-incident? What did you do?*
- F3. *Looking back, what would you point to — a log, a test, an approval, a ticket — if you had to defend that restoration?*

If F3 names an artifact, open the artifact pipeline immediately (Section 3.1). Do not wait until the end if the artifact is central to the story.

### 2.5 Minutes 55–70: Close and artifact request (**NEW**)

**Q-close.**  
> Is there anything about who had to be convinced, and with what, that I have not asked about?

Then run the artifact request (Section 3.1). Then:

> I will send the de-identified transcript within ten days. You will have seven calendar days to mark factual corrections. Thank you.

### 2.6 Flexible probes only (not new questions)

- *What would be an example of that?*
- *Please say more about that moment.*
- *Who else was in that conversation?*
- *What did you do next?*
- Silence, or *Mmm*, after a thin answer.

Do not offer forced choices (yes/no, “power or legitimacy,” “NIST or BCM”).

### 2.7 **NEW** Construct coverage checklist (complete during or immediately after the session)

| Construct | Covered in Q0? | Set used | Concrete example captured? | Artifact named? | Boundary / negative case? |
| --- | --- | --- | --- | --- | --- |
| Power | | A / skip | Y/N | Y/N | |
| Legitimacy | | B / skip | Y/N | Y/N | |
| Urgency | | C / skip | Y/N | Y/N | |
| Decision rights | | D / skip | Y/N | Y/N | |
| Escalation | | E / skip | Y/N | Y/N | |
| Evidentiary standards | | F / skip | Y/N | Y/N | |
| Recoverability assurance | | F / skip | Y/N | Y/N | |

A session is complete for Alignment Tracking only when each row has a concrete example **or** a documented skip-plus-boundary (for example, “no escalation occurred”).

---

## 3. **NEW** Artifact Pipeline

This is the missing Measures/Artifacts process. Artifacts are situated contextual objects that show how written continuity intent was used, negotiated, or bypassed. They are not a NIST/BCM audit (same rule as holding Padilla & Chantler, 2011, out of confirming data in Data Analysis Practice 2).

### 3.1 Request script (read after F3 or after Q-close)

> You mentioned [plan / matrix / ticket / test / approval]. I do not need a confidential file. If you are allowed to share a redacted excerpt, that helps me see how the written process compared with what you actually did. If you cannot share it, please just describe what that document or record did in the event — who used it, who ignored it, and whether it counted as proof.

### 3.2 Three intake paths (**NEW**)

| Path | When | What the researcher captures | What the researcher does **not** do |
| --- | --- | --- | --- |
| **A. Redacted share** | Participant can send a screenshot, PDF excerpt, or ticket print after the call | File stored as `P##_ART##`; identifiers stripped on receipt | Do not score against NIST/ISO/BCM controls |
| **B. Verbal reconstruction** | Participant cannot share the file | Field-note reconstruction: type, who used it, who ignored it, whether it counted as proof | Do not invent contents the participant did not state |
| **C. No artifact** | Participant names none | Record “no reviewable artifact named” as a recoverability-assurance **boundary case** | Do not treat this as missing data that invalidates the interview |

Deadline for Path A: 14 calendar days after the interview. If nothing arrives, recode the row as Path B using the session notes.

### 3.3 **NEW** Artifact Map (one row per object)

| Field | Entry rule |
| --- | --- |
| Artifact ID | `P##_ART##` |
| Type | DR plan; escalation matrix; test report; ticket; authorization record; integrity check; other (name it) |
| How obtained | Path A / B / C |
| Role in the incident | Used as written / used then overridden / unused / unknown |
| Formal intent it stated (if known) | Risk tolerance, priority, downtime, approval path — only what the participant said or the redacted excerpt shows |
| Ad hoc action it was compared with | What was actually restored, delayed, or skipped |
| Counted as proof? | Yes / no / renegotiated / unknown |
| Linked constructs | Power; legitimacy; urgency; decision rights; escalation; evidentiary standards; recoverability assurance (check all that apply as *sensitizing links*, not theme names) |
| Confirming or boundary | Confirming = supports a later meaning unit; boundary = limits an over-broad claim |
| Identifiers stripped | Y/N date |

### 3.4 **NEW** De-identification SOP for artifacts

On receipt or on note-taking, replace:

- Person names → role only (`CFO`, `owner`, `help-desk lead`)
- Employer / client / city → `SME-A`, `site-1`
- Vendor / product / platform → `Platform-1`, `Vendor-1`
- IP addresses, account IDs, ticket numbers → `TICKET-##`
- Exact RTO/RPO numbers that could identify a firm → keep the *relationship* (missed, met, renegotiated), not the marketing figure, if the figure is unique

Do not store original Path A files outside the encrypted directory. Do not quote unique error strings that could identify a vendor incident write-up.

### 3.5 How an artifact enters analysis (**NEW**)

Every Artifact Map row becomes one row in the meaning-unit table (Section 4.3), in the same format as a spoken excerpt. The speaker field is `P## + artifact type + path`. NIST, ISO, or BCM named by the participant is **context** in What We Know. It is not confirming data for a theme.

---

## 4. **NEW** Analysis Bridge (Practice 2 → ITDR Gap)

Do not start from the seven labels as theme titles. That would break Alignment Map alignment between Constructs and Data Analysis.

### 4.1 Order of work

1. **Constructs node (before analysis):** Power, Legitimacy, Urgency, Decision Rights, Escalation, Evidentiary Standards, Recoverability Assurance remain a sensitizing start-list and the interview topical sets.
2. **Data Collection:** Use the protocol and artifact pipeline above.
3. **Data Analysis Step 1:** After repeated reading of the transcript and Artifact Map, lock meaning units that state a *practice claim* before any theme name is written (Aronson, 1994; Taylor & Bogdan, 1998).
4. **Step 2:** Confirm each unit with a named excerpt **and** a negative or boundary case (Practice 2 rule).
5. **Step 3:** Group related units only when they describe the same **salience-to-assurance bargain** (who counted → who decided → what counted as proof), not merely the same recovery topic (Braun & Clarke, 2021).
6. **Step 4:** Synthesize two separate answers — PQ1 and PQ2 — so salience and proof do not collapse into one recovery story (Percy et al., 2015; Lester et al., 2020).
7. **Mapping pass (after themes exist):** Only now map emergent themes back onto the Gap mechanism. A theme may touch more than one construct. A construct with no supporting meaning unit is a finding of absence, not a license to force a theme.

### 4.2 Relatedness test (**NEW**)

Ask of every proposed grouping: *Do these units describe the same bargain?*

- Same bargain example: executive pressure reordered restore priority **and** the written RTO was ignored **and** “up” was declared without an integrity check.
- Same topic, not same bargain: “we used the cloud failover tool” and “we had a DR plan” — do not combine only because both are about recovery.

### 4.3 **NEW** Meaning-unit table template

Copy one table per study, add rows as units lock.

| MU | Meaning-claim (practice sentence, not a noun) | Inclusion bound | Confirming excerpt (P## + city/role band + incident type — no firm name) | Artifact row (if any) | Negative / boundary case | Later theme (filled in Step 3 only) |
| --- | --- | --- | --- | --- | --- | --- |
| MU1 | | | | | | — |
| MU2 | | | | | | — |

**Required:** at least one boundary case per sensitizing construct across the corpus (for example, a manager who never escalated; a restoration accepted with no reviewable proof; a low-power stakeholder whose claim still won).

### 4.4 **NEW** Worked analysis-bridge example (illustrative only)

Not findings. This shows how a future incident would travel the bridge.

- **Q0 excerpt (illustrative):** “The owner wanted email first. I wanted finance first because payroll was in two hours.”
- **Step 1 MU:** Competing restore claims were ranked by who could halt the work, not by the written critical-service list.
- **Set A follow-up:** Owner could stop the failover; finance manager could not.
- **Artifact Path B:** Verbal reconstruction of an escalation matrix that listed finance first; unused in the event.
- **Boundary case to seek later:** A participant whose written matrix *was* followed against owner pressure.
- **Step 3 bargain:** Power reordered priority; written legitimacy of the matrix lost; proof of “email is up” was a user ping, not an integrity check.
- **Step 4:** PQ1 paragraph on whose claim counted; PQ2 paragraph on who decided and what counted as enough proof.

### 4.5 Saturation / stopping rule (**NEW**)

Do not claim that 10–15 interviews saturate the Gap. Use information power (Malterud et al., 2016): narrow aim, specific sample, theoretically informed dialogue. Use Naeem et al. (2024) as a decision guide: stop adding interviews when new sessions no longer create new meaning units on the salience-to-assurance bargain, after at least one boundary case per construct. Guest et al. (2006) may be cited only in that stopping discussion, never as the interview method.

---

## 5. Citation Revisions

### 5.1 **NEW** Allowed-use table

| Source | Allowed use in this plan | Remove from |
| --- | --- | --- |
| Mitchell et al. (1997) | Constructs: power, legitimacy, urgency; topical sets A–C | Findings; theme titles |
| Donaldson & Preston (1995); Freeman et al. (2004) | What We Know / Gap (stakeholder-claim management) | CIT; interview procedures |
| Lowry et al. (2025); Park et al. (2023) | Recoverability assurance definition; PQ2 | Sampling screens |
| Dorobantu et al. (2024) | Why now (legitimacy judgments in fast information environments) | Methods |
| Flanagan (1954); Chell (2004); Butterfield et al. (2005) | **NEW** CIT method for Q0 | — |
| Caelli et al. (2003); Kahlke (2014); Percy et al. (2015) | GQI design justification | Inclusion-criteria screens (Caelli is not a sampling manual) |
| Aronson (1994); Taylor & Bogdan (1998); Braun & Clarke (2021) | Data Analysis Steps 1–4 | Collection as if they were interview protocols |
| Braun & Clarke (2019) | Reflexive memo; confirmability | — |
| Lester et al. (2020) | Write-up as continuation of analysis | — |
| Lincoln & Guba (1985); Korstjens & Moser (2018) | Trustworthiness / Dependability | Quantitative validity language |
| Malterud et al. (2016) | **NEW** n = 10–15 information power | — |
| Naeem et al. (2024) | Saturation as decision guide | Claim that n saturates |
| Guest et al. (2006) | Optional stopping discussion only | CIT; GQI execution; recruitment |
| NIST / BCM / ISO (as named by participants) | What We Know context; artifact *type* participants may mention | Analysis method; confirming excerpts |
| Padilla & Chantler (2011) analog rule from Practice 2 | Hold external frameworks out of confirming data | — |
| Walker (2026) Practice 2 | Analysis procedure already practiced | ITDR findings (it is a fashion-sample methods rehearsal) |

### 5.2 **NEW** In-text swaps (apply throughout the Project Plan)

| Current (incorrect or drifting) | Replace with |
| --- | --- |
| Critical-incident technique (Donaldson & Preston, 1995) | Critical-incident technique (Flanagan, 1954; Chell, 2004) |
| Critical-incident technique (Guest et al., 2006) | Critical-incident technique (Flanagan, 1954; Butterfield et al., 2005) |
| Screening criteria (Caelli et al., 2003) | Screening criteria (purposive/criterion sampling; Creswell & Poth, 2018, if a methods text is needed) |
| Artifact analysis (NIST, 2024) | Artifacts analyzed as situated contextual objects (Creswell & Poth, 2018); NIST/BCM remain context if participants name them |
| Saturation will be reached at 10–15 (Guest et al., 2006) | Sample size is justified by information power (Malterud et al., 2016); stopping follows analytic decision rules (Naeem et al., 2024) |

Add Flanagan (1954), Chell (2004) or Butterfield et al. (2005), and Malterud et al. (2016) to the reference list. Keep Mitchell, Donaldson & Preston, and Lowry where they belong (Gap and Constructs), not in Procedures.

---

## 6. Language-Drift Revisions

### 6.1 **NEW** Find/replace list (run on the whole Project Plan)

| Find (phenomenology, confirmation, or debris) | Replace (GQI / Alignment Map) |
| --- | --- |
| lived experiences | managers’ accounts of a named recovery or test event |
| lived experience | a named recovery or test event, in the manager’s own words |
| essence of the experience / essence of the phenomenon | patterned description of decisions and artifacts |
| socially constructed realities | organizational contexts in which recovery decisions were made |
| voices | de-identified accounts |
| absolute methodological alignment | sensitizing constructs that guide topical questions; themes remain emergent |
| mapped directly to the analytical codes | topical guiding questions linked to the Constructs node (Section 2.4) |
| such other auditing parameters BCM and NIST | internal DR plans, escalation matrices, recovery-test records, and, when managers name them, external references such as NIST or BCM frameworks |
| `;3)` | *(delete)* |
| `((Liu et al.,2020` | (Liu et al., 2020 |
| exploring participants’ lived experiences in their own terms | exploring how participants handled a named recovery or test event, in their own words |
| the researcher as weaver / tapestry | *(delete metaphor; state the analytic step)* |

### 6.2 **NEW** Sentence-level rewrites for the current draft

**Draft:** “The primary data collection instrument … explore how U.S. … managers perceive and operationalize disaster recovery governance challenges … Utilizing critical incident accounts … prompting open-ended dialogue that captures the nuanced, context-specific decision-making processes inherent in these scenarios.”

**Replace with:**  
The primary instrument is a semi-structured interview protocol that asks each manager to recount one named disruption, failover, recovery test, or operational recovery on an external platform (Flanagan, 1954; Chell, 2004). Follow-up questions, used only when the incident story does not already supply them, ask whose request carried power, whose claim was treated as legitimate, what made restoration urgent, who held the decision right, what triggered escalation, and what counted as enough proof that the service was recovered (Mitchell et al., 1997).

**Draft:** “By mapping the queries directly to the analytical codes of the study comprising Power, Legitimacy, Urgency, Decision Rights, Escalation, Evidentiary Standards, and Recoverability Assurance … the study maintains absolute methodological alignment.”

**Replace with:**  
Those seven labels sit on the Constructs node as a sensitizing start-list. They structure topical questions. They are not predetermined theme titles. Themes are locked only after meaning units are confirmed with excerpts and boundary cases (Aronson, 1994; Walker, 2026).

**Draft:** “The second phase … is modeled as a generic qualitative inquiry (GQI) utilizing a flexible protocol to explore participants’ lived experiences in their own terms.”

**Replace with:**  
The interview is a generic qualitative inquiry session (Caelli et al., 2003; Kahlke, 2014; Percy et al., 2015). It collects the manager’s account of an external recovery event, the decisions taken, and the artifacts used or bypassed, in the participant’s own words.

---

## 7. Ethics and Dependability Revisions

### 7.1 **NEW** Threat-to-Gap-data matrix (paste under Validity/Reliability/Credibility/Dependability)

| Ethical / quality threat | How it deletes Gap data | Concrete mitigation (**NEW**) |
| --- | --- | --- |
| Sharing DR plans, tickets, or vendor names | Manager withholds proof and escalation talk (PQ2) | Artifact Path B or C is a full interview; refusal never ends the session |
| Dual identifiability (person + firm + vendor) | Decision-rights talk is sanitized | `P##` codes; strip firm/vendor/product/city; encrypted directory |
| Supervisor-visible recruitment | Official plan is performed as “the truth” | Individual outreach; no participation list visible to a boss |
| Member checking as political edit | Contested proof is deleted | Seven-day factual-correction window only; script in 2.2 |
| Researcher loyalty to seven codes | Findings replay Mitchell et al. | Sensitizing list + MU table + post-interview reflexive memo |
| Recording failure | Lost incident narrative | No memory-only session; reschedule |
| Manager self-justification treated as proof | Assurance becomes rhetoric | Code “what I told stakeholders” separately from “what artifact existed” |
| Unique technical identifiers in artifacts | Re-identification | Section 3.4 SOP |

### 7.2 **NEW** Member-check SOP

1. Within 10 days, email the de-identified transcript to the address on the consent form.
2. Ask only: *Did I mishear any fact about the sequence of events, roles, or artifacts?*
3. Window: 7 calendar days. No reply = transcript stands as heard.
4. Accept corrections of names, sequence, and artifact type.
5. Do not accept deletion of a de-identified contested decision. If the participant objects, add a footnote: “Participant asked that this decision not be quoted; the analytic note that a contest occurred is retained without the wording.”
6. Store the marked transcript as `P##_MC` in the same encrypted directory.

### 7.3 **NEW** Storage SOP

- Location: encrypted, password-protected directory; researcher-only access.
- File set per participant: consent PDF, recording, verbatim transcript, de-identified transcript, Artifact Map, Path A files (if any), member-check file, reflexive memo.
- Retention: follow Capella IRB / university policy; destroy identifiers when the policy allows.
- Backup: one encrypted copy only; no cloud folder with employer-visible filenames.

### 7.4 **NEW** Reflexive memo (write within 24 hours of each interview)

Prompt, five lines maximum:

1. Where did I almost supply a salience word the participant had not used?
2. Which claim did I privately prefer (owner, auditor, platform, manager)?
3. Which artifact did I treat as “real proof” too quickly?
4. What boundary case did this session add or still lack?
5. What question did I skip that the coverage checklist still needs?

---

## 8. Sample and Recruitment Inserts (**NEW**)

**Information power (paste under Sample).**  
A sample of 10 to 15 managers is justified by information power, not by a promise of saturation at a fixed n (Malterud et al., 2016). The aim is narrow (enactment of stakeholder-claim management in SME ITDRPaaS incidents), the sample is specific (U.S. SME IT/network managers with a recent external-platform recovery event), and the dialogue is theoretically informed by stakeholder-salience without being a closed questionnaire. Stopping follows the analysis-bridge rule in Section 4.5 (Naeem et al., 2024).

**Recruitment (paste under Recruitment).**  
Candidates are approached individually through professional networks, practitioner associations, and professional social platforms. The researcher does not recruit through a supervisor. Screening uses the inclusion criteria already in the draft. After eligibility is confirmed, the consent form is emailed. After signed consent is returned, a 60–75 minute virtual interview is scheduled in English.

---

## 9. Paste-Ready Project Plan Paragraphs

These replace the current Measures, Procedures, Analysis, and Trustworthiness blocks. They incorporate every **NEW** effort above. Suggested length matches the courseroom prompt (3–4 paragraphs for measures and procedures; 1–2 for trustworthiness).

### 9.1 Measures or Artifacts to Be Reviewed — **NEW** replacement

The primary instrument is a semi-structured interview protocol that asks each participating U.S. SME IT or network manager to recount one named disruption, failover, recovery test, or operational recovery in the preceding 36 months in which an external recovery platform or managed recovery service was used (Flanagan, 1954; Chell, 2004). The opening question is a single critical-incident prompt. It does not introduce theory terms. If the account stays abstract, the researcher asks the participant to remain with that one event. This design fits generic qualitative inquiry because it collects an account of an external event, the decisions taken, and the objects used, in the participant’s own words (Caelli et al., 2003; Kahlke, 2014; Percy et al., 2015).

When the incident story does not already supply the needed practice detail, the researcher uses topical guiding questions organized by stakeholder-salience and its enactment (Mitchell et al., 1997). Sets A–C ask whose request carried power, whose claim was treated as legitimate, and what made restoration time-critical. Sets D–E ask who was supposed to decide, who actually decided, and what triggered escalation. Set F asks what counted as enough proof that a service was recovered, whether that threshold was renegotiated mid-incident, and what log, test, approval, or ticket the manager would point to if the restoration had to be defended. These seven labels are sensitizing constructs. They are not predetermined theme titles.

The secondary instrument is a review of organizational artifacts the manager names while telling that incident. Eligible objects include an internal disaster-recovery plan, an escalation matrix, a recovery-test record, a ticket, an integrity check, or an authorization action. External frameworks such as NIST or BCM are recorded only when the manager names them, and only as context. They are not scored as a compliance checklist (Creswell & Poth, 2018). Recoverability assurance is operationalized as decision-relevant, reviewable evidence that prioritized services could be restored within tolerance — for example a documented restoration outcome, an integrity check, or a recorded authorization (Lowry et al., 2025).

If a file can be shared in redacted form, it is stored under an alphanumeric code after identifiers are stripped. If it cannot be shared, the researcher writes a field-note reconstruction of what the artifact did in the event. If no artifact is named, that absence is retained as a boundary case for recoverability assurance. Every artifact row later enters the same meaning-unit table as spoken excerpts. This keeps Measures/Artifacts accountable to the Gap: a comparison of formal continuity intent with the ad hoc decisions managers executed under pressure.

### 9.2 Detailed Procedures — **NEW** replacement

Recruitment is individual and purposive. The researcher approaches candidates through professional networks, practitioner associations, and professional social platforms, not through a supervisor. Eligibility requires an active IT, network, systems, infrastructure, or operations management role in a U.S. enterprise of 10 to 200 personnel; direct responsibility for, or participation in, IT disaster-recovery coordination that uses an external platform or managed recovery service; and at least one disruption, failover, recovery test, or operational recovery in the preceding 36 months. People employed only by a vendor, or without that platform experience, are excluded. A sample of 10 to 15 managers is justified by information power (Malterud et al., 2016). After eligibility is confirmed, the researcher emails an informed-consent form. When signed electronic consent is returned, a 60- to 75-minute virtual interview in English is scheduled and recorded.

The session follows a written protocol. The researcher reads a short ethics script, then deploys the critical-incident opening (Flanagan, 1954; Chell, 2004). Flexible probes stay with that event. Topical questions on power, legitimacy, urgency, decision rights, escalation, and proof are asked only if the story did not already answer them. The researcher completes a construct-coverage checklist before closing so that a skipped set is either covered in the opening narrative or documented as a boundary case (for example, no escalation occurred). After the incident account, the researcher runs the artifact request. Sharing a document is optional and does not end the interview.

After the session the recording is transcribed verbatim. The transcript, field notes, and artifact map are stripped of person, firm, vendor, and product names and stored under an alphanumeric code in an encrypted, password-protected directory. The de-identified transcript is sent to the participant for a seven-day factual check. Participants may correct sequence, roles, and artifact type. They may not delete a de-identified contested recovery decision from the analytic file. The researcher writes a short reflexive memo within 24 hours so that stakeholder-salience terms used as probes are not mistaken for findings (Braun & Clarke, 2019; Lincoln & Guba, 1985).

### 9.3 Proposed Data Analysis — **NEW** section (the plan draft did not include this node)

Analysis reuses the four-step generic thematic reduction already practiced in Data Analysis Practice 2 (Aronson, 1994; Taylor & Bogdan, 1998; Braun & Clarke, 2021; Walker, 2026). After repeated reading of each de-identified transcript and artifact map, the researcher (1) locks meaning units that state a practice claim before any theme name is written, (2) confirms each unit with a named excerpt and a negative or boundary case, (3) groups related units only when they describe the same salience-to-assurance bargain rather than the same recovery topic, and (4) synthesizes two separate answers, one for stakeholder-claim and salience enactment and one for decision rights, escalation, and recoverability assurance (Percy et al., 2015; Lester et al., 2020). Stakeholder-salience and governance labels remain a sensitizing start-list. They become a mapping pass after themes exist; they are not Step 3 titles. Saturation is treated as an analytic decision guide (Naeem et al., 2024), not as a claim that 10 to 15 interviews close the Gap.

### 9.4 Validity / Reliability / Credibility / Dependability — **NEW** replacement

This project uses the qualitative trustworthiness criteria of credibility, dependability, confirmability, and transferability (Lincoln & Guba, 1985; Korstjens & Moser, 2018). Credibility is supported by staying with one critical-incident narrative long enough to show whether salience moved, by a construct-coverage checklist, and by a limited member check that corrects factual mishearing without erasing contested proof. Dependability is supported by the written protocol, the artifact map, and the meaning-unit table that another reader can follow from excerpt to theme to PQ1 and PQ2. Confirmability is supported by a post-interview reflexive memo and by the rule that power, legitimacy, and urgency guide questions rather than pre-write themes. Transferability is supported by rich description of role, firm-size band, platform type, and incident type without naming organizations.

The main threats to those claims are organizational disclosure risk, dual identifiability, supervisor-visible recruitment, political sanitizing during member check, and researcher allegiance to the sensitizing list. Mitigations are optional artifact sharing with a verbal-reconstruction fallback, identifier stripping, individual recruitment, a seven-day factual-only member check, encrypted storage, and the requirement of at least one boundary case per construct across the corpus. These tactics are included because they protect the exact data the Gap requires: how managers enacted whose claim counted, who decided, and what counted as enough proof.

---

## 10. Close-the-Gap Checklist

Collection-plus-analysis can be said to address the Gap only when all of the following **NEW** efforts are in the Project Plan, not merely intended:

1. PQ1 and PQ2 (or official wording) sit on the Questions marker.
2. The seven labels sit on Constructs as sensitizing terms, not as analytic conclusions.
3. The Section 2 protocol is attached as the interview instrument.
4. The Section 3 artifact pipeline is attached, including Path B/C.
5. The Section 4 analysis bridge and MU table are the Data Analysis node.
6. Citation swaps in Section 5 are applied in the prose.
7. Language swaps in Section 6 are applied in the prose.
8. Ethics/member-check/storage SOPs in Section 7 are in Procedures and Dependability.
9. Information power and recruitment channel/length in Section 8 are in Sample/Recruitment.
10. Section 9 paragraphs replace the current Measures, Procedures, and Trustworthiness text.

Until those ten items are in the document, the Alignment Map’s Data Collection marker remains Partial, and the Gap is aimed at rather than instrumented.
