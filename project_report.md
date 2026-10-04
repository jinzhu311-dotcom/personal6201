# PitchCraft: Individual Project Report (Revised)

## 1. Title and problem

**PitchCraft: generating platform-native promotional copy for student startup teams.** A student team often has one project brief but needs three versions for Xiaohongshu, WeChat Official Accounts and WeChat Video Account. Technical students understand the product but may not know the conventions of each platform. Rewriting takes time and can produce copy that is grammatically correct but does not sound native to the platform. PitchCraft turns one brief into three editable drafts for human review.

## 2. User and context

The primary user is a student startup team’s technical lead working close to a competition deadline. At present, the user moves between three editors and repeatedly rewrites the same material. When the system works, the user pastes a brief, selects a platform and makes only a small number of final edits. The output separates the hook, body, hashtags and call to action so that it can be reviewed and copied easily.

## 3. Why AI

The non-AI baseline is one fixed template per platform, filled with the project name, problem, user and advantage. It is cheap, explainable and suitable for a controlled comparison. An LLM is useful for expressing platform-specific tone and structure, but it should not make factual decisions. The intended design is hybrid: LLM/rule-based generation plus deterministic validation. Input validation, output schema validation, high-risk term detection and human publication remain rule-based. The current MVP uses an offline rule generator so that the product remains runnable; a course-approved rented LLM can later replace this function without changing the database or evaluation protocol.

## 4. Data and method

The revised scope is **120 Chinese reference copies**: 40 Chinese student project briefs, each paired with one manually authored reference copy for Xiaohongshu, WeChat Official Account and WeChat Video Account. The reference copies must be locked before any model run. The database separates `briefs`, `references_copy`, `generation_runs`, `ratings` and `banned_terms`. Restricted source data is not copied into the repository; only authorised, de-identified briefs and copy should be imported.

The evaluation set must not appear in the few-shot reference set. Each record retains a `brief_key` so that programmatic leakage checks can be performed. The repository contains three demo rows only to verify the interface; they are not the formal 120-item dataset.

## 5. Evaluation

The primary metric is blind human rating of platform-native tone on a 1–5 scale by two independent raters. The author must not act as a rater. The target is an average of at least 4.0 across the three platforms. A secondary metric measures whether the project purpose, target user, key advantage and call to action are present. The fixed-template baseline and PitchCraft must use the same briefs and rating form. If the baseline wins, that is reported as a finding. Ratings are stored under `rater_a` and `rater_b`.

## 6. Risks and boundaries

The system may overstate a claim, so it flags terms such as “number one”, “the best” and “guaranteed” for human review. It never auto-publishes. User input is not persisted by the web interface. Formal source data must be de-identified before processing and used only within its authorised scope. The interface states that the copy is AI-assisted and the user remains responsible for publication. The project does not add RAG, an agent, auto-posting or a Singapore A/B experiment: these would add cost and variables without being necessary for this problem.

## 7. Smallest first version and deliverables

The MVP is one end-to-end path: paste a project brief → select a platform → generate a structured draft → run deterministic checks → copy and review manually. The repository includes a Flask interface, SQLite schema, CSV importer, reference-copy template, tests and startup instructions. The next steps are to import the locked 120 Chinese reference copies, connect a pinned LLM version, conduct the two-rater blind evaluation, and report the mean scores, inter-rater agreement, completeness and abstention/failure cases.
