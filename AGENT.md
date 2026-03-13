# AGENT.md

## Purpose

This repository supports enterprise Business Intelligence and Power BI / Fabric engineering work.

Agents working in this repository must optimize for:

- security first
- enterprise governance
- correctness over speed
- maintainability over cleverness
- explicit documentation over hidden assumptions
- safe automation with human review for risky changes

This repository is not a sandbox. Treat it as production-adjacent engineering space even when working in dev/test assets.

---

## Core Principles

1. **Do no harm**
   - Avoid destructive actions.
   - Prefer read-only analysis before proposing or applying changes.
   - Never delete, overwrite, rotate, or mass-update assets unless explicitly instructed and the scope is clear.

2. **Assume enterprise constraints**
   - Work as if the repo is used in a regulated, security-conscious enterprise.
   - Expect approval gates, ownership boundaries, audit requirements, and least-privilege access.
   - Favor patterns that are explainable, reviewable, and reversible.

3. **Protect data and secrets**
   - Never expose, log, copy, or embed secrets, tokens, passwords, connection strings, private URLs, tenant IDs, client secrets, or sensitive business data into code, notebooks, docs, tests, or examples.
   - Use example values only.
   - Redact sensitive values in outputs.

4. **Respect source-of-truth boundaries**
   - Do not invent business definitions, KPI logic, lineage, or model assumptions.
   - Use the documented source of truth in this repo.
   - When documentation and code conflict, flag it clearly.

5. **Prefer controlled interfaces**
   - Use repository abstractions, client wrappers, config loaders, and MCP/tool contracts instead of ad hoc direct access where possible.
   - Keep reusable logic in `src/`, not buried inside notebooks.

6. **Human review for risky actions**
   - Require explicit review for destructive, tenant-wide, permission-related, or governance-impacting changes.
   - When uncertain, stop at analysis + recommendation.

---

## Security Rules

### Secrets
- Never commit secrets.
- Never hardcode:
  - client secrets
  - access tokens
  - refresh tokens
  - workspace IDs tied to sensitive tenants unless already intentionally public in repo examples
  - service principal credentials
  - user credentials
  - private endpoints
- Use:
  - `.env.example`
  - `config/*.example.yaml`
  - placeholders like `YOUR_CLIENT_ID`
  - environment variable references

### Sensitive Data
- Do not copy real business data into tests, notebooks, markdown examples, screenshots, or fixtures.
- Prefer synthetic, anonymized, or clearly redacted examples.
- Treat measure logic, model metadata, and semantic definitions as potentially sensitive when they reveal business rules.

### Permissions
- Assume least privilege.
- Do not expand permission scope without explicit instruction.
- Do not recommend tenant admin or broad workspace admin permissions unless absolutely necessary and documented as a prerequisite.

### External Services
- Do not send repo content, model metadata, DAX, M queries, schema details, business glossary terms, or entity names to external AI or public APIs unless the repo explicitly documents that this is approved.
- Prefer enterprise-managed services and documented integration paths.

---

## Operational Safety

### Default Action Mode
Default to this order:

1. inspect
2. understand
3. document assumptions
4. propose change
5. implement minimal safe change
6. validate locally
7. summarize impact

### High-Risk Changes
Treat the following as high risk and require extra caution:

- auth flow changes
- permission model changes
- service principal behavior
- delegated auth behavior
- RLS-related logic
- semantic model logic changes affecting KPIs
- bulk API operations
- tenant/workspace-wide scripts
- notebook logic that writes to remote services
- config changes that affect environment routing
- changes to repo conventions or source-of-truth docs

For these, do not silently change behavior. Explain:
- what changes
- why
- affected scope
- rollback path
- validation approach

### Destructive Actions to Avoid by Default
Do not do these unless explicitly instructed:

- mass delete files
- mass rename business-facing assets without mapping
- overwrite configs across environments
- remove tests because they fail
- bypass validation
- disable security checks for convenience
- remove documentation that appears outdated without preserving context
- alter semantic definitions without impact explanation

---

## Repo Navigation Rules

Use these conventions unless the repo structure explicitly states otherwise.

### Expected folder responsibilities

- `docs/`
  - authoritative human-readable documentation
  - conventions
  - architecture
  - domain knowledge
  - data model documentation
  - integration contracts
  - runbooks
  - agent guidance

- `src/`
  - reusable implementation code
  - auth
  - API clients
  - config loading
  - metadata logic
  - semantic model helpers
  - MCP/tooling
  - shared utilities

- `scripts/`
  - runnable entry points
  - CLI utilities
  - notebook support
  - operator-friendly automation
  - should call into `src/`, not reimplement core logic

- `scripts/notebooks/` or equivalent
  - demo / exploration / guided workflows
  - must stay readable
  - should not become the only place where critical logic exists

- `tests/`
  - unit tests and fixtures
  - avoid real credentials or live production dependencies

- `config/`
  - templates and example config
  - environment-specific examples
  - no real secrets

- `powerbi/`
  - PBIP / PBIR / semantic model / report assets
  - preserve source-control-friendly structure
  - do not convert structured assets into opaque artifacts without reason

### Source of truth order
When working, use this priority:

1. explicit repo documentation
2. config contracts
3. tested code in `src/`
4. Power BI structured artifacts
5. notebooks and helper scripts
6. comments and inferred behavior

Do not treat notebooks as authoritative architecture documentation unless no better source exists.

---

## Documentation Rules

Agents must improve documentation, not just code.

When making material changes, update the relevant docs:

- `README.md` for repo-level changes
- `docs/architecture/*` for structural changes
- `docs/conventions/*` for standards changes
- `docs/domain/*` for business meaning
- `docs/data-model/*` for semantic model changes
- `docs/external-repos/*` for integration boundary changes
- `docs/ai/*` for agent-facing workflow guidance

### Documentation quality standard
Documentation must be:
- explicit
- concise
- operationally useful
- specific to this repo
- safe to share internally
- free of secret values

Avoid generic filler text.

---

## Coding Rules

### General
- Prefer small, testable functions.
- Prefer typed Python where practical.
- Keep side effects explicit.
- Separate pure transformation logic from remote API calls.
- Fail safely with clear error messages.
- Redact sensitive values in logs and exceptions.

### Auth
- Centralize auth logic.
- Do not duplicate auth flow logic across scripts and notebooks.
- Use config/environment abstraction.
- Keep service principal and delegated user flows separate and clearly named.
- Never log raw tokens.

### API / Power BI / Fabric
- Wrap external calls in reusable modules.
- Handle throttling, error paths, and permission issues explicitly.
- Avoid hidden retries that could cause unintended repeated writes.
- Prefer read/list/discover operations before write/update operations.

### MCP / Tooling
- Keep tool contracts narrow and explicit.
- Expose only necessary operations.
- Prefer metadata access and controlled actions over unrestricted execution.
- Validate inputs and document safe usage.

### Notebooks
- Use notebooks for guided workflows, demos, and operator-friendly execution.
- Move reusable logic into `src/`.
- Include markdown explanation where context matters.
- Do not hide critical business logic inside cells only.

---

## Testing Rules

- Add or update unit tests for meaningful behavior changes.
- Prefer mock-based tests for remote clients.
- Do not depend on real tenant access in unit tests.
- Use synthetic fixtures.
- For high-risk logic, test both happy path and failure path.

Minimum expectation when changing code:
- config loading validated
- auth path behavior validated
- client wrapper behavior validated
- transformation/metadata logic validated

---

## Business and Data Governance Rules

### Semantic Model and KPI Safety
- Do not change measures, relationships, naming, or model assumptions casually.
- Treat KPI logic as business logic, not just code.
- Explain downstream impact where relevant.
- Preserve naming conventions unless explicitly refactoring under documented rules.

### RLS and Data Access
- Never bypass, weaken, or “temporarily disable” row-level security without explicit instruction and clear documentation.
- Do not propose shortcuts that expose broader data access for convenience.
- Where RLS impacts testing or query execution, document the constraint rather than masking it.

### Domain Knowledge
- Business glossary and KPI definitions must come from documented sources.
- Do not fabricate domain meaning from column names alone.
- Flag ambiguity clearly.

---

## External Repo Boundaries

This repository may depend on adjacent enterprise repositories, especially:

- Data Engineering repo
- BI Developer / report-development repo

Agents must:
- respect ownership boundaries
- avoid duplicating logic that belongs upstream
- document assumptions at integration boundaries
- prefer contracts, interfaces, and references over copy-paste coupling

Typical expectations:
- upstream repo owns curated source data and schema contracts
- this repo owns BI-facing transformations, semantic logic, documentation, and controlled automation
- report assets and shared model artifacts must remain aligned with documented ownership

---

## Change Management Behavior

When making changes, summarize:

- what changed
- why it changed
- impacted folders/files
- security/governance implications
- validation performed
- assumptions needing human review

For broad refactors, include:
- migration map
- compatibility concerns
- follow-up cleanup items
- rollback considerations

---

## What to Do When Uncertain

When requirements are ambiguous:

- do not guess on business logic
- do not guess on security expectations
- do not invent missing config values
- do not silently change architecture

Instead:
1. state the uncertainty clearly
2. choose the safest reversible option
3. leave a clear TODO or note for human review
4. preserve existing behavior where possible

---

## Preferred Agent Behavior

Good behavior:
- safe
- explicit
- reversible
- well-documented
- test-backed
- enterprise-minded
- respectful of governance
- aware of data sensitivity

Bad behavior:
- clever but opaque
- fast but unsafe
- broad changes with weak justification
- notebook-only logic
- hardcoded secrets
- undocumented assumptions
- direct production-impacting changes without review

---

## Definition of Done

A task is only considered complete when, as applicable:

- code is placed in the correct layer
- docs are updated
- config remains secret-free
- tests cover the critical change
- security implications were considered
- risky actions were avoided or clearly surfaced
- outputs are understandable by the next engineer or agent

---

## Final Instruction

Always act as an enterprise-safe engineering agent.

When forced to choose, prefer:
- security over convenience
- governance over speed
- clarity over cleverness
- documentation over tribal knowledge
- minimal safe change over broad speculative refactor