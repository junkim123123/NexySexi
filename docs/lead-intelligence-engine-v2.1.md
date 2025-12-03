# NexSupply AI Lead Intelligence Engine v2.1

## 1. Purpose

The NexSupply AI Lead Intelligence Engine v2.1 acts as an **AI Chief Intelligence Officer** that reads, scores, classifies, and assigns an SLA to every inbound lead before a human sees it.

**Goals:**
*   Enable the sales team to instantly know **"who to call first."**
*   Demote emotional inquiries, student research, and spam, while prioritizing leads discussing **strategy, margins, and risk**.
*   Serve as a **leverage tool** allowing the same team size to handle a larger pipeline.

---

## 2. Inputs & Data Flow

**Primary Input:** "Request Sourcing Audit / Sample Request" form on the website.
*   `name`
*   `email`
*   `company`
*   `use_case` (free text)
*   Optional fields: volume, category, region, etc.

**End-to-end Flow:**
1.  **API Entry:** `/api/sample-request` or `/api/sample-request/debug`
2.  **AI Analysis (`analyzeSampleRequest`):**
    *   Calls `gemini-2.5-pro`.
    *   Analyzes Intent, Fit, Authority, and Engagement based on a strict JSON schema.
3.  **Guardrails (`applyLeadGuardrails`):**
    *   Applies hard rules based on email domain, local part, and emotional vs. strategic language patterns.
4.  **Routing (`deriveLeadRouting`):**
    *   Determines Tier (A–D), Queue, and SLA.
5.  **Outputs:**
    *   **Admin Email:** Battlecard for RevOps/Sales.
    *   **User Email:** "Sourcing Audit Running" or "Reviewing" notification.
    *   **Inspector:** `/admin/lead-intel` for internal debugging and tuning.

---

## 3. Scoring Model

A single **`opportunity_score` (0–100)** is derived from four sub-scores:

*   **`intent_score` (35%)**
    *   Based on high/low intent language patterns (e.g., "landed cost, HTS, FCL, Section 301, EBITDA, inventory turns").
*   **`fit_score` (30%)**
    *   Alignment of industry, role, scale, and channel with NexSupply ICP.
*   **`authority_score` (20%)**
    *   Email domain (corporate vs. free vs. disposable) and job title/role.
*   **`engagement_score` (15%)**
    *   Completeness of form, specific volume/timeline mentions.

**Metadata:**
*   `intent_signals`: Tags like `"high_intent_fba"`, `"high_intent_logistics"`, `"low_intent_research"`.
*   `email_type`: `"business" | "prosumer" | "free" | "disposable"`.
*   `email_local_part_type`: `"person_name" | "role_based" | "suspicious"`.

---

## 4. Guardrails v2.1

We enforce hard rules to correct AI hallucinations or edge cases.

**Key Rules:**
*   **Corporate Override:** If `email_type === "business"`, ensure minimum score of **60** (e.g., protects academic research from being dropped too low).
*   **Prosumer Boost:** If `email_type === "prosumer"` with high-intent patterns, ensure minimum score of **50** (protects serious sellers using Gmail).
*   **Disposable Cap:** If `email_type === "disposable"`, cap score at **25** (forced Tier D).
*   **Emotional/Free Cap:** If free email + emotional/abstract language, cap score at **30** (Tier D).

---

## 5. Routing & SLA

**Tier Definitions:**
*   **Tier A (Strategic Enterprise):** High fit + high intent + authority (e.g., large retail buyer, 7-figure brand).
*   **Tier B (Serious Scaler):** Good fit and intent, but less urgent than Tier A.
*   **Tier C (Standard Operator):** Legitimate but exploratory/research phase (e.g., prosumer, student).
*   **Tier D (Nurture / Low Intent):** Spam, disposable, emotional venting, very early stage.

**SLA Benchmarks (v2.1):**
*   **Tier A:** **5–15 min** response (Priority Queue).
*   **Tier B:** **30 min – 2 hours** response.
*   **Tier C:** **4 hours** response.
*   **Tier D:** **24 hours** (Automated response only).

---

## 6. Emails & Inspector

**Admin Email (Battlecard):**
*   Tier / Score / SLA Badges.
*   **Traffic Light Snapshot:** Green (Strong), Yellow (Caution), Red (Risk).
*   Summary of key fields and recommended approach.

**User Email:**
*   **Tier A/B:** "Your Sourcing Audit is Running" – Personalized, micro-insights.
*   **Tier C/D:** "We’re Reviewing Your Request" – Educational focus.

**Lead Intelligence Inspector (`/admin/lead-intel`):**
*   Interactive console to test payloads and visualize routing/scoring logic.
*   Central tool for tuning and QA.

---

## 7. Roadmap (Next)

*   **v2.2:** Automated regression testing with standard fixture set. Industry-specific scenarios.
*   **v3.0:** Retraining based on real user data (false positives/negatives). Integration with CRM and behavioral signals.